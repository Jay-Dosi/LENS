# 🚀 LENS Quick Start Guide

**Got your API keys? Let's get you running in 5 minutes.**

---

## 📍 Visual API Key Map

```
LENS Platform
│
├── Backend (.env)
│   ├── IBM watsonx.ai
│   │   ├── IBM_CLOUD_API_KEY ──────────► IBM Cloud API Key
│   │   └── IBM_WATSONX_PROJECT_ID ─────► watsonx Project ID
│   │
│   ├── IBM Cloud Object Storage
│   │   ├── IBM_COS_API_KEY ────────────► Same as IBM_CLOUD_API_KEY (or separate)
│   │   ├── IBM_COS_INSTANCE_CRN ───────► COS Instance CRN
│   │   ├── IBM_COS_ENDPOINT ───────────► Regional endpoint URL
│   │   └── IBM_COS_BUCKET_NAME ────────► Your bucket name
│   │
│   └── IBM Watson NLU
│       ├── IBM_NLU_API_KEY ────────────► NLU API Key
│       └── IBM_NLU_URL ────────────────► NLU Service URL
│
└── Frontend (.env)
    └── VITE_API_URL ───────────────────► Backend URL (default: http://localhost:8000/api/v1)
```

---

## 📋 Copy-Paste .env Template

### Backend: `backend/.env`

```env
# IBM Cloud Configuration
IBM_CLOUD_API_KEY=paste_your_ibm_cloud_api_key_here
IBM_WATSONX_PROJECT_ID=paste_your_watsonx_project_id_here

# IBM Cloud Object Storage
IBM_COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
IBM_COS_API_KEY=paste_your_cos_api_key_here
IBM_COS_INSTANCE_CRN=crn:v1:bluemix:public:cloud-object-storage:global:a/...
IBM_COS_BUCKET_NAME=your-bucket-name

# IBM Watson Natural Language Understanding
IBM_NLU_API_KEY=paste_your_nlu_api_key_here
IBM_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com

# watsonx.ai Configuration (pre-configured)
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct

# External APIs (No authentication required)
NASA_FIRMS_API_URL=https://firms.modaps.eosdis.nasa.gov/api/area/csv
GDELT_API_URL=https://api.gdeltproject.org/api/v2/doc/doc

# Application Settings (pre-configured)
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf
LOG_LEVEL=INFO
```

### Frontend: `frontend/.env`

```env
# API Base URL
VITE_API_URL=http://localhost:8000/api/v1
```

---

## ⚡ 5-Minute Setup Checklist

### Prerequisites
- [ ] IBM Cloud account created
- [ ] All API keys obtained (see [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md) if needed)

### Setup Steps
```bash
# 1. Clone/navigate to project
cd LENS

# 2. Backend setup
cd backend
cp .env.example .env
# Edit .env with your API keys (use template above)

# 3. Frontend setup
cd ../frontend
cp .env.example .env
# Edit .env (default values work for local development)

# 4. Install dependencies
cd ../backend
pip install -r requirements.txt

cd ../frontend
npm install

# 5. Start services
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**✅ Done!** Open http://localhost:5173 in your browser.

---

## 🔍 Where to Find Each API Key

| Key | Where to Get It | Format Example |
|-----|----------------|----------------|
| `IBM_CLOUD_API_KEY` | IBM Cloud → Manage → API Keys → Create | `AbCdEf123...` (44 chars) |
| `IBM_WATSONX_PROJECT_ID` | watsonx.ai → Project → Manage → General | `12345678-abcd-1234-abcd-123456789abc` |
| `IBM_COS_INSTANCE_CRN` | COS → Service Credentials → resource_instance_id | `crn:v1:bluemix:public:cloud-object-storage:...` |
| `IBM_COS_API_KEY` | COS → Service Credentials → apikey (or reuse IBM_CLOUD_API_KEY) | `AbCdEf123...` |
| `IBM_COS_ENDPOINT` | COS → Endpoints → Public → Your Region | `https://s3.us-south.cloud-object-storage.appdomain.cloud` |
| `IBM_COS_BUCKET_NAME` | COS → Buckets → Your bucket name | `lens-evidence-storage` |
| `IBM_NLU_API_KEY` | NLU → Service Credentials → apikey | `AbCdEf123...` |
| `IBM_NLU_URL` | NLU → Service Credentials → url | `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com` |

---

## ❌ Common Errors & Quick Fixes

### Error: "Invalid API Key"
```
✗ Symptom: 401 Unauthorized or authentication failed
✓ Fix: Copy the ENTIRE key without spaces. Regenerate if needed.
✓ Check: Key matches the service (watsonx key for watsonx, NLU key for NLU)
```

### Error: "Project Not Found"
```
✗ Symptom: watsonx.ai returns 404 or project error
✓ Fix: Verify IBM_WATSONX_PROJECT_ID is correct (from Project → Manage → General)
✓ Check: You have access to the project in watsonx.ai
```

### Error: "Access Denied" (COS)
```
✗ Symptom: Cannot access Cloud Object Storage
✓ Fix: Verify IBM_COS_INSTANCE_CRN is complete (starts with crn:v1:bluemix:)
✓ Check: Bucket exists and name is correct
✓ Check: API key has "Writer" or "Manager" role
```

### Error: "Connection Timeout"
```
✗ Symptom: Services not responding
✓ Fix: Check IBM_COS_ENDPOINT matches your region
✓ Fix: Verify IBM_NLU_URL is correct for your service instance
✓ Check: IBM Cloud services are active (https://cloud.ibm.com/status)
```

### Error: "Module Not Found" (Python)
```
✗ Symptom: ImportError when starting backend
✓ Fix: Run `pip install -r requirements.txt` in backend directory
✓ Check: Using correct Python environment (3.8+)
```

### Error: "Port Already in Use"
```
✗ Symptom: Backend won't start on port 8000
✓ Fix: Kill existing process or use different port:
       uvicorn app.main:app --reload --port 8001
✓ Update: frontend/.env VITE_API_URL to match new port
```

---

## ✅ Verify Each Service

### 1. Test Backend API
```bash
# Backend should be running on http://localhost:8000
curl http://localhost:8000/health

# Expected: {"status": "healthy"}
```

### 2. Test watsonx.ai Connection
```bash
curl -X POST http://localhost:8000/api/v1/test/watsonx \
  -H "Content-Type: application/json"

# Expected: {"status": "success", "message": "watsonx.ai connection successful"}
```

### 3. Test Cloud Object Storage
```bash
curl -X POST http://localhost:8000/api/v1/test/cos \
  -H "Content-Type: application/json"

# Expected: {"status": "success", "message": "COS connection successful"}
```

### 4. Test Watson NLU
```bash
curl -X POST http://localhost:8000/api/v1/test/nlu \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test"}'

# Expected: {"status": "success", "sentiment": {...}}
```

### 5. Test Frontend
```
Open browser: http://localhost:5173
Expected: LENS dashboard loads without errors
```

---

## 🧪 All-in-One Test Command

Run this to verify all APIs are configured correctly:

```bash
# From project root
cd backend

# Run comprehensive API test
python -c "
import os
from dotenv import load_dotenv

load_dotenv()

required_keys = [
    'IBM_CLOUD_API_KEY',
    'IBM_WATSONX_PROJECT_ID',
    'IBM_COS_API_KEY',
    'IBM_COS_INSTANCE_CRN',
    'IBM_COS_ENDPOINT',
    'IBM_COS_BUCKET_NAME',
    'IBM_NLU_API_KEY',
    'IBM_NLU_URL'
]

print('🔍 Checking API Configuration...\n')
missing = []
for key in required_keys:
    value = os.getenv(key)
    if not value or 'your_' in value or 'paste_' in value:
        print(f'❌ {key}: MISSING or PLACEHOLDER')
        missing.append(key)
    else:
        print(f'✅ {key}: Configured ({len(value)} chars)')

if missing:
    print(f'\n❌ {len(missing)} key(s) need configuration')
    exit(1)
else:
    print('\n✅ All API keys configured!')
    print('Run: uvicorn app.main:app --reload')
"
```

**Expected Output:**
```
🔍 Checking API Configuration...

✅ IBM_CLOUD_API_KEY: Configured (44 chars)
✅ IBM_WATSONX_PROJECT_ID: Configured (36 chars)
✅ IBM_COS_API_KEY: Configured (44 chars)
✅ IBM_COS_INSTANCE_CRN: Configured (120 chars)
✅ IBM_COS_ENDPOINT: Configured (62 chars)
✅ IBM_COS_BUCKET_NAME: Configured (22 chars)
✅ IBM_NLU_API_KEY: Configured (44 chars)
✅ IBM_NLU_URL: Configured (78 chars)

✅ All API keys configured!
Run: uvicorn app.main:app --reload
```

---

## 🆘 Still Stuck?

1. **Check detailed guide**: [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md)
2. **Verify IBM Cloud status**: https://cloud.ibm.com/status
3. **Check logs**: Backend terminal shows detailed error messages
4. **Common issue**: Using placeholder values instead of actual API keys

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start backend | `cd backend && uvicorn app.main:app --reload` |
| Start frontend | `cd frontend && npm run dev` |
| Check backend health | `curl http://localhost:8000/health` |
| View backend logs | Check terminal running uvicorn |
| View frontend | http://localhost:5173 |
| Backend API docs | http://localhost:8000/docs |

---

**⏱️ Total Setup Time: ~5 minutes** (assuming you have all API keys)

**Need API keys?** See [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md) for detailed instructions.