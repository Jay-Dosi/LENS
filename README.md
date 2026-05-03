# ESG Claim Verification Assistant

**Production-Grade Greenwashing Detection Tool**

An AI-powered greenwashing risk detection tool that verifies corporate sustainability claims against publicly available satellite and news data. Built with **watsonx.ai** and open-source technologies for production deployment.

---

## 🎯 Overview

The ESG Claim Verification Assistant ingests corporate sustainability reports (PDFs), extracts carbon and emissions-related claims using IBM watsonx.ai, cross-references those claims against OpenWeatherMap air quality data and Google News data, and produces an explainable, transparent risk score.

**Key Features:**
- 📄 PDF text extraction with intelligent chunking
- 🤖 AI-powered claim extraction using IBM Granite models (watsonx.ai)
- 🔍 Entity extraction for preliminary facility identification using IBM Watson NLU
- 🗺️ Interactive facility mapping with precision manual location pinning
- 🌡️ Historical air quality analysis via OpenWeatherMap API
- 📰 News sentiment analysis via Google News RSS
- 📊 Transparent risk scoring with explainable results
- 💾 Flexible storage: In-memory ChromaDB or persistent local storage
- 🎨 Modern React frontend with interactive visualizations

---

## 🏗️ Architecture

### Technology Stack

**Backend (Python)**
- **FastAPI** - Async REST API framework
- **IBM watsonx.ai** - Granite 3.0 8B Instruct model for claim extraction and explanation
- **IBM Watson NLU** - Cloud-based entity extraction and NER
- **ChromaDB** - In-memory or persistent vector storage
  - Memory mode for stateless deployment
  - Persistent mode for local development
- **PyMuPDF** - PDF text extraction
- **httpx** - Async HTTP client for external APIs
- **OpenWeatherMap API** - Air quality data

**Frontend (React)**
- **React 18** + **Vite** - Fast build tooling and modern UI
- **Tailwind CSS** - Utility-first styling
- **react-pdf** - PDF viewer component
- **react-leaflet** - Interactive maps with facility markers
- **Axios** - HTTP client for API communication

**Deployment**
- **IBM Code Engine** - Serverless container deployment (recommended for hackathon)
- **Local Development** - Quick setup with Python + Node.js
- **Cloud Foundry** - Alternative IBM Cloud deployment
- Multiple deployment options: AWS, Azure, GCP, or self-hosted

---

## 📋 Prerequisites

### Required Services

1. **IBM Cloud Account** - [Sign up here](https://cloud.ibm.com/registration)

2. **IBM watsonx.ai** (Lite Plan - 10 CUH/month)
   - Create a watsonx.ai project at [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
   - Note your Project ID and API Key
   - Free tier: 10 CUH/month (~100 pages of processing)
   - Model used: `ibm/granite-3-8b-instruct`

3. **IBM Watson NLU** (Lite Plan - 30,000 items/month)
   - Create a Watson NLU service in IBM Cloud
   - Get your API Key and Service URL
   - Free tier: 30,000 NLU items/month

4. **OpenWeatherMap API** (Free Tier - 1,000 calls/day)
   - Sign up at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
   - Get your free API key for air quality data
   - Free tier: 1,000 API calls/day

### Optional Services

5. **Google News RSS** (No API Key Required)
   - Public RSS feeds for news sentiment analysis
   - No setup required

### Local Development

- Python 3.11+
- Node.js 18+ (for frontend)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Jay-Dosi/LENS
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

# Edit .env with your IBM watsonx.ai credentials
```

**Required Environment Variables:**

```env
# IBM watsonx.ai
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
IBM_WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-3-8b-instruct
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct

# IBM Watson NLU
WATSON_NLU_API_KEY=your_watson_nlu_api_key_here
WATSON_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com

# OpenWeatherMap API (for air quality data)
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here

# Storage Configuration - ChromaDB
STORAGE_MODE=memory  # or "persistent" for local disk storage
STORAGE_PERSIST_DIRECTORY=./chroma_storage  # only used if STORAGE_MODE=persistent
SESSION_TIMEOUT_MINUTES=60

# Application Settings
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Disable ChromaDB Telemetry
ANONYMIZED_TELEMETRY=False
```

**For detailed API setup, see [`API_KEYS_GUIDE.md`](API_KEYS_GUIDE.md)**

### 3. Run the Backend

```bash
# From backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📡 API Endpoints

### POST /api/v1/session/create
Create a new stateless session
**Returns:** `{"session_id": "uuid", "timeout_minutes": 60}`

### POST /api/v1/upload
Upload a sustainability report PDF

**Headers:**
- `X-Session-ID`: Session identifier (optional, creates new if omitted)

**Request:**
- `file`: PDF file (multipart/form-data)
- `company_name`: Company name (form field)
- `latitude`: Optional manual facility latitude (form field)
- `longitude`: Optional manual facility longitude (form field)
- `location_name`: Optional manual location name (form field)

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

**Headers:**
- `X-Session-ID`: Session identifier (required)

**Request:**
```
?document_id=uuid
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

**Headers:**
- `X-Session-ID`: Session identifier (required)

**Request:**
```
?document_id=uuid
```

**Response:**
```json
{
  "document_id": "uuid",
  "evidence": [
    {
      "evidence_id": "uuid_claim_0_firms",
      "claim_id": "uuid_claim_0",
      "source": "OPENWEATHERMAP",
      "signal_type": "poor_air_quality",
      "signal_text": "Current air quality: Poor (AQI: 4/5). 15 high pollution days in past 1095 days",
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

**Headers:**
- `X-Session-ID`: Session identifier (required)

**Request:**
```
?document_id=uuid
```

**Response:**
```json
{
  "document_id": "uuid",
  "risk_score": {
    "truth_score": 65,
    "risk_band": "Medium Risk",
    "claim_breakdown": [...],
    "reasoning": "• Claim about 25% emissions reduction contradicted by poor air quality near facility\n• Facility location verified\n• Moderate negative news coverage detected",
    "generated_at": "2024-01-15T10:35:00Z"
  },
  "status": "scoring_complete"
}
```

### GET /api/v1/map-data/{document_id}
Get facility location data for map visualization

**Headers:**
- `X-Session-ID`: Session identifier (required)

### GET /api/v1/health
Health check endpoint

### Admin Endpoints
- `POST /api/v1/admin/cleanup-expired`: Clean up expired sessions
- `POST /api/v1/admin/reset`: Reset all data (for testing)

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
   - System queries OpenWeatherMap and Google News
   - Evidence appears in right pane with map

4. **View Risk Score**
   - Overall score displayed in top bar
   - Click claim to see detailed breakdown
   - Read AI-generated explanation

### Best Demo Moment

Show a **visible contradiction** between:
- A reported emissions reduction claim
- Detected poor air quality or negative news spike near the facility

**Script:** "This is what an analyst used to spend days doing. The system does it in under a minute."

---



---

## 📊 System Workflow

```
1. Document Ingest → Upload PDF to ChromaDB storage
2. Text Parsing → Extract and chunk text locally (PyMuPDF)
3. Claim Extraction → watsonx.ai Granite 3.0 8B extracts claims
4. Entity Analysis → IBM Watson NLU identifies facility names from claims
5. Evidence Collection → Query OpenWeatherMap + Google News using facility coordinates
6. Risk Scoring → Transparent heuristic calculation
7. Explanation → watsonx.ai Granite 3.0 8B generates summary
```

**Key Features:**
- ✅ In-memory or persistent storage with ChromaDB
- ✅ IBM watsonx.ai Granite 3.0 8B for AI processing
- ✅ Watson NLU for entity extraction
- ✅ OpenWeatherMap for air quality data
- ✅ Google News RSS for sentiment analysis
- ✅ Fully implemented React frontend
- ✅ Easy deployment to IBM Code Engine

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
- [`HACKATHON_DEPLOYMENT_GUIDE.md`](HACKATHON_DEPLOYMENT_GUIDE.md) - IBM Code Engine deployment for hackathon
- [`WORKFLOW_AND_IMPLEMENTATION.md`](WORKFLOW_AND_IMPLEMENTATION.md) - Detailed system architecture and workflow
- [`API_KEYS_GUIDE.md`](API_KEYS_GUIDE.md) - Complete API setup instructions

### External Services
- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Watson NLU Documentation](https://cloud.ibm.com/docs/natural-language-understanding)
- [OpenWeatherMap API](https://openweathermap.org/api) - Air quality data
- [Google News RSS](https://news.google.com/rss) - News feeds
- [ChromaDB Documentation](https://docs.trychroma.com/) - Vector database

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
✅ **IBM watsonx.ai and Watson NLU integration**
✅ **In-memory storage for stateless deployment**
✅ **Easy deployment to IBM Code Engine**

---

## 🚀 What's New in This Version

### Hackathon-Ready Architecture
- ✅ **ChromaDB Storage** - In-memory or persistent vector storage
- ✅ **Granite 3.0 8B Model** - Latest IBM instruction-tuned model
- ✅ **OpenWeatherMap Integration** - Real air quality data
- ✅ **Fully Implemented Frontend** - React + Vite + Tailwind CSS
- ✅ **IBM Code Engine Ready** - Optimized for serverless deployment
- ✅ **Comprehensive Documentation** - Deployment and workflow guides

### Key Benefits
1. **Stateless Deployment** - In-memory ChromaDB for serverless environments
2. **Latest AI Models** - Granite 3.0 8B for both extraction and explanation
3. **Real Data Sources** - OpenWeatherMap air quality + Google News
4. **Modern Frontend** - Interactive visualizations with maps and charts
5. **Hackathon Optimized** - Credit-efficient deployment strategies

---

**Ready to detect greenwashing? Let's go! 🚀**

For detailed setup instructions, see:
- [`HACKATHON_DEPLOYMENT_GUIDE.md`](HACKATHON_DEPLOYMENT_GUIDE.md) - IBM Code Engine deployment
- [`API_KEYS_GUIDE.md`](API_KEYS_GUIDE.md) - API configuration
- [`WORKFLOW_AND_IMPLEMENTATION.md`](WORKFLOW_AND_IMPLEMENTATION.md) - System architecture
