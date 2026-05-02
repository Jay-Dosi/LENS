# ESG Claim Verification Assistant

**IBM Dev Day Hackathon Submission**

An AI-powered greenwashing risk detection tool that verifies corporate sustainability claims against publicly available satellite and news data.

---

## 🎯 Overview

The ESG Claim Verification Assistant ingests corporate sustainability reports (PDFs), extracts carbon and emissions-related claims using IBM watsonx.ai, cross-references those claims against NASA FIRMS satellite data and GDELT news data, and produces an explainable, transparent risk score.

**Key Features:**
- 📄 PDF text extraction with intelligent chunking
- 🤖 AI-powered claim extraction using IBM Granite models
- 🛰️ Satellite thermal anomaly detection via NASA FIRMS
- 📰 News sentiment analysis via GDELT
- 📊 Transparent risk scoring with explainable results
- 🗺️ Interactive facility mapping and evidence visualization

---

## 🏗️ Architecture

### Technology Stack

**Backend (Python)**
- FastAPI - Async REST API framework
- IBM watsonx.ai - Granite 13B & 8B models for claim extraction and explanation
- IBM Cloud Object Storage - Document and data storage
- IBM Watson NLU - Entity extraction for facility resolution
- PyMuPDF - PDF text extraction
- httpx - Async HTTP client for external APIs

**Frontend (React)**
- React + Vite - Fast build tooling
- Tailwind CSS - Utility-first styling
- react-pdf - PDF viewer component
- react-leaflet - Interactive maps

**Deployment**
- Docker - Containerization
- IBM Cloud Code Engine - Serverless deployment

---

## 📋 Prerequisites

### IBM Cloud Services (All Free Tier)

1. **IBM Cloud Account** - [Sign up here](https://cloud.ibm.com/registration)

2. **IBM watsonx.ai** (Lite Plan - 10 CUH/month)
   - Create a watsonx.ai project
   - Note your Project ID and API Key

3. **IBM Cloud Object Storage** (Lite Plan - 5GB)
   - Create a bucket named `esg-lens-hackathon`
   - Note your API Key, Instance CRN, and Endpoint

4. **IBM Watson Natural Language Understanding** (Lite Plan - 30K items/month)
   - Create an NLU instance
   - Note your API Key and URL

### Local Development

- Python 3.11+
- Node.js 18+
- Docker (optional, for containerized deployment)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LENS
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env with your IBM Cloud credentials
```

**Required Environment Variables:**

```env
# IBM Cloud Configuration
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
IBM_WATSONX_PROJECT_ID=your_watsonx_project_id_here

# IBM Cloud Object Storage
IBM_COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
IBM_COS_API_KEY=your_cos_api_key_here
IBM_COS_INSTANCE_CRN=your_cos_instance_crn_here
IBM_COS_BUCKET_NAME=esg-lens-hackathon

# IBM Watson Natural Language Understanding
IBM_NLU_API_KEY=your_nlu_api_key_here
IBM_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com

# watsonx.ai Configuration
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct
```

### 3. Run the Backend

```bash
# From backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup (Coming Soon)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📡 API Endpoints

### POST /api/v1/upload
Upload a sustainability report PDF

**Request:**
- `file`: PDF file (multipart/form-data)
- `company_name`: Company name (form field)

**Response:**
```json
{
  "document_id": "uuid",
  "filename": "report.pdf",
  "file_url": "https://...",
  "status": "uploaded",
  "message": "Document uploaded successfully"
}
```

### POST /api/v1/extract-claims
Extract ESG claims from uploaded document

**Request:**
```json
{
  "document_id": "uuid"
}
```

**Response:**
```json
{
  "document_id": "uuid",
  "claims": [
    {
      "claim_id": "uuid_claim_0",
      "claim_text": "Reduced Scope 1 emissions by 25% in 2023",
      "claim_type": "emissions_reduction",
      "value": 25.0,
      "unit": "percent",
      "year": 2023,
      "target_or_achieved": "achieved",
      "page_number": 12,
      "confidence": 0.92
    }
  ],
  "total_claims": 5,
  "status": "claims_extracted"
}
```

### POST /api/v1/verify
Collect external evidence for claims

**Request:**
```json
{
  "document_id": "uuid"
}
```

**Response:**
```json
{
  "document_id": "uuid",
  "evidence": [
    {
      "evidence_id": "uuid_claim_0_firms",
      "claim_id": "uuid_claim_0",
      "source": "NASA_FIRMS",
      "signal_type": "thermal_anomaly",
      "signal_text": "Detected 3 thermal anomalies within 50km",
      "signal_strength": 0.3,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "total_evidence": 8,
  "status": "verification_complete"
}
```

### POST /api/v1/score
Calculate risk score and generate explanation

**Request:**
```json
{
  "document_id": "uuid"
}
```

**Response:**
```json
{
  "document_id": "uuid",
  "risk_score": {
    "truth_score": 65,
    "risk_band": "Medium Risk",
    "claim_breakdown": [...],
    "reasoning": "• Claim about 25% emissions reduction contradicted by thermal anomalies\n• Facility location verified\n• Moderate negative news coverage detected",
    "generated_at": "2024-01-15T10:35:00Z"
  },
  "status": "scoring_complete"
}
```

---

## 🔧 Configuration

### Facility Mapping

Edit `config/facility_mapping.json` to add known facility locations for your demo company:

```json
{
  "facility_mapping": {
    "Company XYZ Manufacturing Plant": {
      "latitude": 37.7749,
      "longitude": -122.4194,
      "address": "San Francisco, CA, USA",
      "facility_type": "manufacturing",
      "description": "Primary manufacturing facility"
    }
  }
}
```

### Quota Management

**IBM watsonx.ai Lite Plan Limits:**
- 10 Compute Unit Hours (CUH) per month
- ~100 pages of text processing

**Mitigation Strategies:**
1. Process only candidate chunks (ESG-related content)
2. Limit to 5 claims per demo
3. Use local PDF extraction to save CUH
4. Cache results during rehearsal

**IBM Watson NLU Lite Plan Limits:**
- 30,000 NLU items per month

**Mitigation:**
- Use NLU only for short text segments
- Limit facility extraction to first 5000 characters

---

## 🎬 Demo Scenario

### Recommended Flow

1. **Upload Report**
   - Select a publicly available sustainability report PDF
   - Enter company name
   - Click "Upload"

2. **Extract Claims**
   - System processes PDF and extracts 3-5 claims
   - Claims appear in center pane with confidence scores

3. **Verify Claims**
   - Select a claim asserting emissions reduction
   - System queries NASA FIRMS and GDELT
   - Evidence appears in right pane with map

4. **View Risk Score**
   - Overall score displayed in top bar
   - Click claim to see detailed breakdown
   - Read AI-generated explanation

### Best Demo Moment

Show a **visible contradiction** between:
- A reported emissions reduction claim
- A detected thermal anomaly or negative news spike near the facility

**Script:** "This is what an analyst used to spend days doing. The system does it in under a minute."

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build backend image
cd backend
docker build -t esg-lens-backend .

# Run container
docker run -p 8000:8000 --env-file .env esg-lens-backend
```

### Deploy to IBM Cloud Code Engine

```bash
# Login to IBM Cloud
ibmcloud login

# Target Code Engine
ibmcloud ce project select --name esg-lens-project

# Build and deploy
ibmcloud ce application create \
  --name esg-lens-api \
  --image esg-lens-backend \
  --port 8000 \
  --env-from-configmap esg-lens-config \
  --min-scale 0 \
  --max-scale 1
```

---

## 📊 System Workflow

```
1. Document Ingest → Upload PDF to IBM COS
2. Text Parsing → Extract and chunk text locally
3. Claim Extraction → watsonx.ai Granite 13B extracts claims
4. Facility Resolution → Watson NLU identifies locations
5. Evidence Collection → Query NASA FIRMS + GDELT
6. Risk Scoring → Transparent heuristic calculation
7. Explanation → watsonx.ai Granite 8B generates summary
```

---

## 🔒 Security Notes

- Never commit `.env` files to version control
- Use IBM Cloud IAM for production authentication
- Rotate API keys regularly
- Limit CORS origins in production
- Validate all file uploads

---

## 🐛 Troubleshooting

### Common Issues

**"Import errors" in IDE**
- These are expected before installing dependencies
- Run `pip install -r requirements.txt`

**"CUH quota exceeded"**
- Wait until next month or upgrade to paid tier
- Use cached results for rehearsal

**"PDF extraction fails"**
- Ensure PDF is text-based, not scanned images
- Check file size is under 50MB

**"No claims extracted"**
- Verify PDF contains ESG-related content
- Check watsonx.ai API key and project ID

---

## 📚 Additional Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Cloud Object Storage Docs](https://cloud.ibm.com/docs/cloud-object-storage)
- [IBM Watson NLU Docs](https://cloud.ibm.com/docs/natural-language-understanding)
- [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/)
- [GDELT Project](https://www.gdeltproject.org/)

---

## 📄 License

This project is created for the IBM Dev Day Hackathon.

---

## 👥 Team

Built with ❤️ for IBM Dev Day Hackathon

---

## 🎯 Success Criteria

✅ PDF upload and claim extraction in <60 seconds  
✅ At least one claim linked to a mappable facility  
✅ At least one external signal retrieved and displayed  
✅ Risk score with visible breakdown  
✅ Natural language explanation citing specific evidence  
✅ All services on IBM Cloud free tier  

---

**Ready to detect greenwashing? Let's go! 🚀**