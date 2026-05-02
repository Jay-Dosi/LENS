"""
FastAPI Routes - API Endpoints
"""
import os
import uuid
import logging
from typing import List
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    UploadResponse,
    ClaimExtractionResponse,
    VerificationResponse,
    ScoringResponse,
    Claim,
    Evidence
)
from app.services import (
    PDFExtractor,
    get_storage_service,
    get_watsonx_service,
    get_nlu_service,
    get_external_data_service,
    get_scoring_service
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    company_name: str = "Unknown Company"
) -> UploadResponse:
    """
    Stage 1: Upload a sustainability report PDF
    
    Args:
        file: PDF file upload
        company_name: Name of the reporting company
        
    Returns:
        UploadResponse with document ID and status
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Validate file size
        file_content = await file.read()
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.max_file_size_mb}MB limit"
            )
        
        # Generate document ID
        document_id = str(uuid.uuid4())
        
        # Save file locally
        os.makedirs(settings.upload_dir, exist_ok=True)
        local_path = os.path.join(settings.upload_dir, f"{document_id}.pdf")
        
        with open(local_path, 'wb') as f:
            f.write(file_content)
        
        # Upload to IBM Cloud Object Storage
        storage = get_storage_service()
        object_key = f"uploads/{document_id}.pdf"
        file_url = storage.upload_file(local_path, object_key)
        
        # Store document metadata
        document_metadata = {
            "document_id": document_id,
            "filename": file.filename,
            "company_name": company_name,
            "uploaded_at": datetime.now().isoformat(),
            "file_url": file_url,
            "status": "uploaded"
        }
        
        storage.upload_json(
            document_metadata,
            f"metadata/{document_id}.json"
        )
        
        logger.info(f"Document uploaded: {document_id}")
        
        return UploadResponse(
            document_id=document_id,
            filename=file.filename,
            file_url=file_url,
            status="uploaded",
            message="Document uploaded successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-claims", response_model=ClaimExtractionResponse)
async def extract_claims(document_id: str) -> ClaimExtractionResponse:
    """
    Stages 2 & 3: Extract text and claims from uploaded document
    
    Args:
        document_id: Document identifier
        
    Returns:
        ClaimExtractionResponse with extracted claims
    """
    try:
        storage = get_storage_service()
        
        # Download PDF from storage
        local_path = os.path.join(settings.upload_dir, f"{document_id}.pdf")
        storage.download_file(f"uploads/{document_id}.pdf", local_path)
        
        # Stage 2: Extract and chunk text
        pdf_extractor = PDFExtractor()
        pages, candidate_chunks = pdf_extractor.process_pdf(local_path)
        
        # Store extracted text
        storage.upload_json(
            {"pages": pages, "chunks": candidate_chunks},
            f"text/{document_id}.json"
        )
        
        logger.info(f"Extracted {len(candidate_chunks)} candidate chunks")
        
        # Stage 3: Extract claims using watsonx.ai
        watsonx = get_watsonx_service()
        all_claims = []
        
        # Process up to 5 chunks to stay within quota
        for chunk in candidate_chunks[:5]:
            claims = watsonx.extract_claims_from_chunk(
                chunk_text=chunk["text"],
                page_number=chunk["page_number"],
                document_id=document_id
            )
            all_claims.extend(claims)
        
        # Store claims
        claims_data = [claim.dict() for claim in all_claims]
        storage.upload_json(
            {"claims": claims_data},
            f"claims/{document_id}.json"
        )
        
        logger.info(f"Extracted {len(all_claims)} claims")
        
        return ClaimExtractionResponse(
            document_id=document_id,
            claims=all_claims,
            total_claims=len(all_claims),
            status="claims_extracted"
        )
        
    except Exception as e:
        logger.error(f"Error extracting claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=VerificationResponse)
async def verify_claims(document_id: str) -> VerificationResponse:
    """
    Stages 4 & 5: Resolve facilities and collect external evidence
    
    Args:
        document_id: Document identifier
        
    Returns:
        VerificationResponse with evidence
    """
    try:
        storage = get_storage_service()
        
        # Load claims
        claims_data = storage.download_json(f"claims/{document_id}.json")
        claims = claims_data.get("claims", [])
        
        # Load document metadata
        metadata = storage.download_json(f"metadata/{document_id}.json")
        company_name = metadata.get("company_name", "Unknown Company")
        
        # Stage 4: Resolve facility locations
        nlu = get_nlu_service()
        
        # Load facility mapping (for demo, use a simple mapping)
        # In production, this would be a comprehensive database
        facility_mapping = {}  # Empty for now, would be loaded from config
        
        # Extract full document text for context
        text_data = storage.download_json(f"text/{document_id}.json")
        full_text = " ".join([page["text"] for page in text_data.get("pages", [])])
        
        # Identify facilities
        facility_names = nlu.identify_facilities_in_claims(claims, full_text[:5000])
        
        # Resolve locations
        resolved_facilities = {}
        for facility_name in facility_names[:2]:  # Limit to 2 facilities for demo
            location = nlu.resolve_facility_location(facility_name, facility_mapping)
            resolved_facilities[facility_name] = location.dict()
        
        # Stage 5: Collect external evidence
        external_data = get_external_data_service()
        all_evidence = []
        
        for claim in claims[:5]:  # Limit to 5 claims for demo
            # Add company name and facility info to claim
            claim["company_name"] = company_name
            if facility_names:
                claim["facility_name"] = facility_names[0]
            
            # Get facility location if available
            facility_location = None
            if facility_names and facility_names[0] in resolved_facilities:
                facility_location = resolved_facilities[facility_names[0]]
            
            # Collect evidence
            evidence_list = await external_data.collect_evidence_for_claim(
                claim,
                facility_location
            )
            all_evidence.extend(evidence_list)
        
        # Store evidence
        evidence_data = [ev.dict() for ev in all_evidence]
        storage.upload_json(
            {
                "evidence": evidence_data,
                "facilities": resolved_facilities
            },
            f"evidence/{document_id}.json"
        )
        
        logger.info(f"Collected {len(all_evidence)} evidence records")
        
        return VerificationResponse(
            document_id=document_id,
            evidence=all_evidence,
            total_evidence=len(all_evidence),
            status="verification_complete"
        )
        
    except Exception as e:
        logger.error(f"Error verifying claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/score", response_model=ScoringResponse)
async def score_claims(document_id: str) -> ScoringResponse:
    """
    Stages 6 & 7: Calculate risk score and generate explanation
    
    Args:
        document_id: Document identifier
        
    Returns:
        ScoringResponse with risk score and explanation
    """
    try:
        storage = get_storage_service()
        
        # Load claims and evidence
        claims_data = storage.download_json(f"claims/{document_id}.json")
        claims = claims_data.get("claims", [])
        
        evidence_data = storage.download_json(f"evidence/{document_id}.json")
        evidence = evidence_data.get("evidence", [])
        
        # Stage 6: Calculate risk score
        scoring = get_scoring_service()
        risk_score = scoring.calculate_risk_score(document_id, claims, evidence)
        
        # Stage 7: Generate explanation
        watsonx = get_watsonx_service()
        explanation = watsonx.generate_explanation(claims[:5], evidence[:10])
        
        # Update risk score with AI-generated explanation
        risk_score.reasoning = explanation
        
        # Store final report
        storage.upload_json(
            risk_score.dict(),
            f"reports/{document_id}.json"
        )
        
        logger.info(f"Generated risk score: {risk_score.truth_score}")
        
        return ScoringResponse(
            document_id=document_id,
            risk_score=risk_score,
            status="scoring_complete"
        )
        
    except Exception as e:
        logger.error(f"Error scoring claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ESG Claim Verification Assistant"}

# Made with Bob
