# ESG Claim Verification Assistant

**Production-Grade Greenwashing Detection Tool**

An AI-powered greenwashing risk detection tool that verifies corporate sustainability claims against publicly available satellite and news data. Built with **watsonx.ai** and open-source technologies for production deployment.

---

## 🎯 Overview

The ESG Claim Verification Assistant ingests corporate sustainability reports (PDFs), extracts carbon and emissions-related claims using IBM watsonx.ai, cross-references those claims against NASA FIRMS satellite data and GDELT news data, and produces an explainable, transparent risk score.

**Key Features:**
- 📄 PDF text extraction with intelligent chunking
- 🤖 AI-powered claim extraction using IBM Granite models (watsonx.ai)
- 🔍 Production-grade entity extraction using IBM Watson NLU
- 🛰️ Satellite thermal anomaly detection via NASA FIRMS
- 📰 News sentiment analysis via GDELT
- 📊 Transparent risk scoring with explainable results
- 🗺️ Interactive facility mapping and evidence visualization
- 💾 Flexible storage: Local filesystem, AWS S3, Azure Blob, or MinIO

---

## 🏗️ Architecture

### Technology Stack

**Backend (Python)**
- **FastAPI** - Async REST API framework
- **IBM watsonx.ai** - Granite 13B & 8B models for claim extraction and explanation
- **IBM Watson NLU** - Cloud-based entity extraction and NER
- **Local/S3 Storage** - Flexible storage backend
  - Local filesystem for development
  - AWS S3, Azure Blob Storage, or MinIO for production
- **PyMuPDF** - PDF text extraction
- **httpx** - Async HTTP client for external APIs

**Frontend (React)**
- React + Vite - Fast build tooling
- Tailwind CSS - Utility-first styling
- react-pdf - PDF viewer component
- react-leaflet - Interactive maps

**Deployment**
- Docker - Containerization
- Multiple deployment options: AWS, Azure, GCP, Heroku, Railway, or self-hosted

---

## 📋 Prerequisites

### Required Services

1. **IBM Cloud Account** - [Sign up here](https://cloud.ibm.com/registration)

2. **IBM watsonx.ai** (Lite Plan - 10 CUH/month)
   - Create a watsonx.ai project at [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
   - Note your Project ID and API Key
   - Free tier: 10 CUH/month (~100 pages of processing)

3. **IBM Watson NLU** (Lite Plan - 30,000 items/month)
   - Create a Watson NLU service in IBM Cloud
   - Get your API Key and Service URL
   - Free tier: 30,000 NLU items/month
   - See [Watson NLU Setup Guide](docs/WATSON_NLU_SETUP.md) for detailed instructions

### Optional Services (Choose One for Production)

3. **Storage Backend** (Choose one):
   - **Local Filesystem** (Development) - No setup required
   - **AWS S3** (Production) - Free tier: 5GB storage
   - **Azure Blob Storage** (Production) - Free tier: 5GB storage
   - **MinIO** (Self-hosted) - Free, S3-compatible

### Local Development

- Python 3.11+
- Node.js 18+ (for frontend)
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

# Download spaCy model for NER
python -m spacy download en_core_web_sm

# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env with your IBM watsonx.ai credentials
```

**Required Environment Variables:**

```env
# IBM watsonx.ai (REQUIRED - Only IBM service needed)
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
IBM_WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct

# Storage Backend (local for development, s3 for production)
STORAGE_BACKEND=local
STORAGE_LOCAL_PATH=./storage

# NLU Configuration (spaCy - open source)
SPACY_MODEL=en_core_web_sm

# Optional: For production with S3
# STORAGE_BACKEND=s3
# STORAGE_S3_BUCKET=your-bucket-name
# STORAGE_S3_REGION=us-east-1
# STORAGE_S3_ACCESS_KEY=your_access_key
# STORAGE_S3_SECRET_KEY=your_secret_key
```

**For detailed production setup, see [PRODUCTION_SETUP.md](docs/PRODUCTION_SETUP.md)**

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

**spaCy (Open Source):**
- No quota limits
- Runs locally
- Fast and efficient
- Production-grade accuracy

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
1. Document Ingest → Upload PDF to local/S3 storage
2. Text Parsing → Extract and chunk text locally (PyMuPDF)
3. Claim Extraction → watsonx.ai Granite 13B extracts claims
4. Facility Resolution → spaCy NER identifies locations and entities
5. Evidence Collection → Query NASA FIRMS + GDELT (free APIs)
6. Risk Scoring → Transparent heuristic calculation
7. Explanation → watsonx.ai Granite 8B generates summary
```

**Key Improvements:**
- ✅ Only watsonx.ai requires IBM Cloud
- ✅ spaCy provides production-grade NER without API limits
- ✅ Flexible storage supports multiple backends
- ✅ All external data sources are free
- ✅ Easy to deploy anywhere

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

### Documentation
- [Production Setup Guide](docs/PRODUCTION_SETUP.md) - Detailed deployment instructions
- [API Setup Guide](docs/API_SETUP_GUIDE.md) - API configuration details
- [Quick Start Guide](docs/QUICK_START.md) - Get started quickly

### External Services
- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [spaCy Documentation](https://spacy.io/usage) - NER and NLP
- [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/) - Satellite data
- [GDELT Project](https://www.gdeltproject.org/) - News data

### Storage Options
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Azure Blob Storage](https://docs.microsoft.com/azure/storage/blobs/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html) - Self-hosted S3

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
✅ **Only watsonx.ai from IBM Cloud required**
✅ **Production-grade with open-source alternatives**
✅ **Easy deployment to any cloud or on-premises**

---

## 🚀 What's New in This Version

### Production-Ready Architecture
- ✅ **Simplified IBM Cloud dependency** - Only watsonx.ai required
- ✅ **Open-source NER** - spaCy replaces IBM Watson NLU
- ✅ **Flexible storage** - Local, AWS S3, Azure Blob, or MinIO
- ✅ **No vendor lock-in** - Deploy anywhere
- ✅ **Cost-effective** - Minimal cloud costs
- ✅ **Production-grade** - Battle-tested open-source components

### Key Benefits
1. **Lower Costs** - Only pay for watsonx.ai usage
2. **Better Performance** - spaCy runs locally, no API latency
3. **More Flexible** - Choose your storage backend
4. **Easier Deployment** - Fewer dependencies to configure
5. **Production Ready** - Proven technologies at scale

---

**Ready to detect greenwashing in production? Let's go! 🚀**

For detailed setup instructions, see [PRODUCTION_SETUP.md](docs/PRODUCTION_SETUP.md)