"""
IBM watsonx.ai Service - Stages 3 & 7
Handles claim extraction and explanation generation using Granite models
"""
import json
import logging
import uuid
from typing import List, Dict, Any, Optional
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from app.config import settings
from app.models.schemas import Claim

logger = logging.getLogger(__name__)


class WatsonxService:
    """IBM watsonx.ai client for LLM inference"""
    
    # Extraction prompt template for Granite 13B Instruct v2
    EXTRACTION_PROMPT = """You are an ESG analyst extracting carbon and emissions claims from corporate sustainability reports.

Extract ONLY claims related to:
- Carbon emissions (Scope 1, 2, or 3)
- Greenhouse gas emissions
- Energy consumption
- Renewable electricity
- Carbon offsets
- Net-zero commitments
- Factory or facility operations

For each claim found, return a JSON object with these exact fields:
- claim_text: The full sentence or paragraph containing the claim
- claim_type: One of [emissions_reduction, net_zero_target, renewable_energy, scope_1, scope_2, scope_3, energy_efficiency, carbon_offset]
- value: The numeric value (if present, otherwise null)
- unit: The unit of measurement (percent, tonnes CO2e, MWh, etc., or null)
- year: The reporting or target year (integer, or null)
- target_or_achieved: One of [target, achieved, unknown]
- confidence: Your confidence in this extraction (0.0 to 1.0)

Return ONLY a valid JSON array of claim objects. If no claims are found, return an empty array [].

TEXT TO ANALYZE:
{text}

JSON OUTPUT:"""

    # Explanation prompt template for Granite 3.0 8B Instruct
    EXPLANATION_PROMPT = """You are an ESG verification analyst. Based on the claims and evidence below, write a concise 4-bullet summary.

You must deeply analyze all provided evidence. Do NOT just look at keywords. Read the full text and descriptions of the news articles, and carefully evaluate the map and air quality (AQI) reports.

For the first 3 bullets:
- Cite the specific claim and the specific external signal (e.g., news article details, map/location data, AQI levels)
- Do NOT accuse the company of fraud
- Use neutral, factual language
- Focus on what was verified, what was not verified, and what appears inconsistent

For the 4th bullet:
- Provide a "Final Verdict" that states clearly what is true and what is not based on the news articles and map results.

CLAIMS:
{claims}

EVIDENCE:
{evidence}

Write exactly 4 bullet points:"""

    def __init__(self):
        """Initialize watsonx.ai client"""
        credentials = {
            "url": settings.watsonx_url,
            "apikey": settings.ibm_cloud_api_key
        }
        
        self.client = APIClient(credentials)
        self.project_id = settings.ibm_watsonx_project_id
        
        # Initialize model instances
        self.extraction_model = ModelInference(
            model_id=settings.watsonx_extraction_model,
            api_client=self.client,
            project_id=self.project_id,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 1500,
                "temperature": 0.1,
                "repetition_penalty": 1.1
            }
        )
        
        self.explanation_model = ModelInference(
            model_id=settings.watsonx_explanation_model,
            api_client=self.client,
            project_id=self.project_id,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 500,
                "temperature": 0.3,
                "repetition_penalty": 1.1
            }
        )
        
        logger.info("Initialized watsonx.ai service")
    
    def extract_claims_from_chunk(
        self,
        chunk_text: str,
        page_number: int,
        document_id: str
    ) -> List[Claim]:
        """
        Extract ESG claims from a text chunk using Granite 13B Instruct v2
        
        Args:
            chunk_text: Text to analyze
            page_number: Source page number
            document_id: Parent document ID
            
        Returns:
            List of extracted Claim objects
        """
        try:
            # Format the prompt
            prompt = self.EXTRACTION_PROMPT.format(text=chunk_text)
            
            # Call the model
            response = self.extraction_model.generate_text(prompt=prompt)
            
            # Parse JSON response
            claims_data = self._parse_json_response(response)
            
            # Convert to Claim objects
            claims = []
            for idx, claim_dict in enumerate(claims_data):
                try:
                    claim = Claim(
                        claim_id=f"{document_id}_claim_{str(uuid.uuid4())[:8]}",
                        document_id=document_id,
                        claim_text=claim_dict.get("claim_text", ""),
                        claim_type=claim_dict.get("claim_type", "unknown"),
                        value=claim_dict.get("value"),
                        unit=claim_dict.get("unit"),
                        year=claim_dict.get("year"),
                        target_or_achieved=claim_dict.get("target_or_achieved", "unknown"),
                        page_number=page_number,
                        confidence=float(claim_dict.get("confidence", 0.5))
                    )
                    
                    # Only include claims with confidence >= 0.6
                    if claim.confidence >= 0.6:
                        claims.append(claim)
                    else:
                        logger.warning(f"Filtered low-confidence claim: {claim.confidence}")
                        
                except Exception as e:
                    logger.error(f"Error creating Claim object: {e}")
                    continue
            
            logger.info(f"Extracted {len(claims)} claims from chunk")
            return claims
            
        except Exception as e:
            logger.error(f"Error extracting claims: {e}")
            return []
    
    def generate_explanation(
        self,
        claims: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> str:
        """
        Generate natural language explanation using Granite 3.0 8B Instruct
        
        Args:
            claims: List of claim dictionaries
            evidence: List of evidence dictionaries
            
        Returns:
            3-bullet explanation text
        """
        try:
            # Format claims and evidence for the prompt
            claims_text = json.dumps(claims, indent=2)
            evidence_text = json.dumps(evidence, indent=2)
            
            # Format the prompt
            prompt = self.EXPLANATION_PROMPT.format(
                claims=claims_text,
                evidence=evidence_text
            )
            
            # Call the model
            response = self.explanation_model.generate_text(prompt=prompt)
            
            # Clean up the response
            explanation = response.strip()
            
            logger.info("Generated explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return "Unable to generate explanation due to an error."
    
    def _parse_json_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse JSON from model response, handling common formatting issues
        
        Args:
            response: Raw model output
            
        Returns:
            Parsed JSON array
        """
        try:
            # Try direct parsing first
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
                return json.loads(json_str)
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
                return json.loads(json_str)
            else:
                # Try to find JSON array in the response
                start_idx = response.find("[")
                end_idx = response.rfind("]") + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    logger.warning("Could not parse JSON from response")
                    return []


# Singleton instance
_watsonx_service: Optional[WatsonxService] = None


def get_watsonx_service() -> WatsonxService:
    """Get or create the watsonx service singleton"""
    global _watsonx_service
    if _watsonx_service is None:
        _watsonx_service = WatsonxService()
    return _watsonx_service

# Made with Bob
