# Production Setup Guide

This guide explains how to deploy the ESG Claim Verification Assistant in production using only **watsonx.ai** from IBM Cloud, with open-source alternatives for other services.

## 🎯 Architecture Overview

### Services Used

**IBM Cloud (Required):**
- ✅ **watsonx.ai** - AI-powered claim extraction and explanation generation
  - Granite 13B Instruct v2 for claim extraction
  - Granite 3.0 8B Instruct for explanation generation

**Open-Source/Free Alternatives:**
- ✅ **spaCy** - Entity extraction and NER (replaces IBM Watson NLU)
- ✅ **Local Storage or AWS S3** - Document and data storage (replaces IBM Cloud Object Storage)
- ✅ **NASA FIRMS** - Satellite thermal anomaly data (free, no auth)
- ✅ **GDELT** - News sentiment analysis (free, no auth)

---

## 📋 Prerequisites

### 1. IBM watsonx.ai Setup

1. **Create IBM Cloud Account**
   - Sign up at [cloud.ibm.com](https://cloud.ibm.com/registration)
   - Free tier available (10 CUH/month)

2. **Create watsonx.ai Project**
   - Navigate to [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
   - Create a new project
   - Note your **Project ID** (found in project settings)

3. **Get API Key**
   - Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
   - Create a new API key
   - Save it securely (you won't be able to see it again)

### 2. Storage Setup (Choose One)

#### Option A: Local Storage (Development/Testing)
- No additional setup required
- Files stored in `./storage` directory
- **Pros:** Simple, no external dependencies
- **Cons:** Not suitable for distributed deployments

#### Option B: AWS S3 (Production)
1. Create an S3 bucket in AWS
2. Create IAM user with S3 access
3. Generate access key and secret key
4. **Free tier:** 5GB storage, 20,000 GET requests/month

#### Option C: MinIO (Self-Hosted S3-Compatible)
1. Install MinIO server: [min.io/download](https://min.io/download)
2. Start MinIO: `minio server /data`
3. Create bucket via MinIO console
4. Use MinIO access key and secret key
5. **Pros:** Full control, no cloud costs
6. **Cons:** Requires server management

#### Option D: Azure Blob Storage (S3-Compatible)
1. Create Azure Storage Account
2. Enable S3-compatible endpoint
3. Use Azure credentials
4. **Free tier:** 5GB storage

### 3. Python Environment

```bash
# Python 3.11+ required
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

---

## ⚙️ Configuration

### 1. Environment Variables

Copy `.env.example` to `.env`:

```bash
cp backend/.env.example backend/.env
```

### 2. Required Configuration

Edit `backend/.env`:

```env
# IBM watsonx.ai (REQUIRED)
IBM_CLOUD_API_KEY=your_actual_api_key_here
IBM_WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Storage Backend
STORAGE_BACKEND=local  # or "s3" for production
```

### 3. Production Storage Configuration

For **AWS S3**:
```env
STORAGE_BACKEND=s3
STORAGE_S3_BUCKET=your-bucket-name
STORAGE_S3_REGION=us-east-1
STORAGE_S3_ACCESS_KEY=your_access_key
STORAGE_S3_SECRET_KEY=your_secret_key
```

For **MinIO**:
```env
STORAGE_BACKEND=s3
STORAGE_S3_BUCKET=esg-lens
STORAGE_S3_REGION=us-east-1
STORAGE_S3_ACCESS_KEY=minioadmin
STORAGE_S3_SECRET_KEY=minioadmin
STORAGE_S3_ENDPOINT=http://localhost:9000
```

For **Azure Blob Storage**:
```env
STORAGE_BACKEND=s3
STORAGE_S3_BUCKET=your-container-name
STORAGE_S3_REGION=eastus
STORAGE_S3_ACCESS_KEY=your_azure_account_name
STORAGE_S3_SECRET_KEY=your_azure_account_key
STORAGE_S3_ENDPOINT=https://your-account.blob.core.windows.net
```

### 4. Optional: Enhanced NER Accuracy

For better entity extraction in production:

```bash
# Download larger spaCy model (requires ~500MB)
python -m spacy download en_core_web_lg
```

Update `.env`:
```env
SPACY_MODEL=en_core_web_lg
```

---

## 🚀 Deployment Options

### Option 1: Local Development

```bash
cd backend
python -m app.main
```

Access at: `http://localhost:8000`

### Option 2: Docker Deployment

```bash
# Build image
cd backend
docker build -t esg-lens-backend .

# Run container
docker run -p 8000:8000 --env-file .env esg-lens-backend
```

### Option 3: Docker Compose (with MinIO)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - STORAGE_BACKEND=s3
      - STORAGE_S3_ENDPOINT=http://minio:9000
      - STORAGE_S3_BUCKET=esg-lens
      - STORAGE_S3_ACCESS_KEY=minioadmin
      - STORAGE_S3_SECRET_KEY=minioadmin
    env_file:
      - backend/.env
    depends_on:
      - minio

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```

Run:
```bash
docker-compose up -d
```

### Option 4: Cloud Deployment

#### AWS EC2 / Azure VM / Google Compute Engine

1. **Provision VM**
   - Ubuntu 22.04 LTS
   - 2 vCPU, 4GB RAM minimum
   - Open ports: 80, 443, 8000

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip nginx
   ```

3. **Deploy Application**
   ```bash
   git clone <your-repo>
   cd LENS/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Configure Systemd Service**
   
   Create `/etc/systemd/system/esg-lens.service`:
   ```ini
   [Unit]
   Description=ESG Lens Backend
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/LENS/backend
   Environment="PATH=/home/ubuntu/LENS/backend/venv/bin"
   ExecStart=/home/ubuntu/LENS/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable esg-lens
   sudo systemctl start esg-lens
   ```

5. **Configure Nginx Reverse Proxy**
   
   Create `/etc/nginx/sites-available/esg-lens`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/esg-lens /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

#### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create esg-lens-app
heroku config:set IBM_CLOUD_API_KEY=your_key
heroku config:set IBM_WATSONX_PROJECT_ID=your_project_id
git push heroku main
```

#### Railway / Render

1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push

---

## 🔒 Security Best Practices

### 1. API Key Management

- ✅ Never commit `.env` files to version control
- ✅ Use environment variables or secret managers
- ✅ Rotate API keys regularly (every 90 days)
- ✅ Use separate keys for dev/staging/production

### 2. Storage Security

**For S3:**
- Enable bucket encryption
- Use IAM roles instead of access keys when possible
- Enable versioning for data recovery
- Configure bucket policies to restrict access

**For Local Storage:**
- Set proper file permissions (chmod 600)
- Use encrypted volumes in production
- Regular backups

### 3. Application Security

- ✅ Enable HTTPS in production (use Let's Encrypt)
- ✅ Configure CORS properly
- ✅ Implement rate limiting
- ✅ Validate all file uploads
- ✅ Keep dependencies updated

---

## 📊 Monitoring & Logging

### Application Logs

Logs are written to stdout. Configure log aggregation:

**CloudWatch (AWS):**
```bash
pip install watchtower
```

**Datadog:**
```bash
pip install ddtrace
```

**ELK Stack:**
```bash
# Configure logstash to read from stdout
```

### Health Checks

Endpoint: `GET /api/v1/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "ESG Claim Verification Assistant"
}
```

### Metrics to Monitor

- API response times
- watsonx.ai API usage (CUH consumption)
- Storage usage
- Error rates
- Memory usage

---

## 💰 Cost Optimization

### watsonx.ai (Primary Cost)

**Free Tier:**
- 10 CUH/month
- ~100 pages of processing

**Optimization Strategies:**
1. Process only ESG-relevant chunks
2. Cache results during development
3. Limit claims per document (5-10)
4. Use smaller models for testing

**Paid Tier:**
- $0.50 per CUH
- Upgrade when needed

### Storage Costs

**AWS S3:**
- Free tier: 5GB, 20K GET requests
- Beyond: $0.023/GB/month

**MinIO (Self-Hosted):**
- Free (server costs only)
- Recommended for high-volume deployments

### Compute Costs

**Development:**
- Local machine: Free

**Production:**
- AWS t3.medium: ~$30/month
- Heroku Hobby: $7/month
- Railway: $5/month (with free tier)

---

## 🧪 Testing Production Setup

### 1. Verify Configuration

```bash
cd backend
python -c "from app.config import settings; print(f'Storage: {settings.storage_backend}'); print(f'spaCy: {settings.spacy_model}')"
```

### 2. Test Storage

```bash
python -c "from app.services import get_storage_service; s = get_storage_service(); print('Storage initialized successfully')"
```

### 3. Test NLU

```bash
python -c "from app.services import get_nlu_service; n = get_nlu_service(); print('NLU initialized successfully')"
```

### 4. Test watsonx.ai

```bash
python -c "from app.services import get_watsonx_service; w = get_watsonx_service(); print('watsonx.ai initialized successfully')"
```

### 5. Full Integration Test

```bash
# Start server
python -m app.main

# In another terminal, test upload
curl -X POST http://localhost:8000/api/v1/health
```

---

## 🔧 Troubleshooting

### Issue: "spaCy model not found"

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### Issue: "boto3 not installed" (when using S3)

**Solution:**
```bash
pip install boto3
```

### Issue: "watsonx.ai authentication failed"

**Solutions:**
1. Verify API key is correct
2. Check project ID is correct
3. Ensure API key has watsonx.ai access
4. Try regenerating API key

### Issue: "Storage bucket not found"

**Solutions:**
1. Create bucket manually
2. Verify bucket name in config
3. Check credentials have bucket access

### Issue: "Out of CUH quota"

**Solutions:**
1. Wait for monthly reset
2. Upgrade to paid tier
3. Use cached results for testing
4. Reduce number of claims processed

---

## 📚 Additional Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [spaCy Documentation](https://spacy.io/usage)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎯 Production Checklist

- [ ] IBM watsonx.ai API key configured
- [ ] Storage backend configured and tested
- [ ] spaCy model downloaded
- [ ] Environment variables set
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Health checks working
- [ ] Logging configured
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] Security review completed
- [ ] Load testing performed

---

**Ready for production! 🚀**

For questions or issues, refer to the main [README.md](../README.md) or create an issue in the repository.