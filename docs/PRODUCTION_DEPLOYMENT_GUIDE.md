# Production Deployment Guide

**Complete guide for deploying the ESG Claim Verification Assistant from local development to production**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Configuration](#production-configuration)
4. [Deployment Options](#deployment-options)
5. [Free Hosting Platforms](#free-hosting-platforms)
6. [Production Checklist](#production-checklist)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Required Software

#### 1. Python 3.11+
**Windows:**
```powershell
# Download from python.org
# Or use winget
winget install Python.Python.3.11

# Verify installation
python --version
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

#### 2. Node.js 18+ and npm
**Windows:**
```powershell
# Download from nodejs.org
# Or use winget
winget install OpenJS.NodeJS.LTS

# Verify installation
node --version
npm --version
```

**macOS:**
```bash
# Using Homebrew
brew install node

# Verify installation
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version
```

#### 3. Git
**Windows:**
```powershell
winget install Git.Git
```

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

### Required Services

#### IBM watsonx.ai (REQUIRED - Only IBM Service Needed)

1. **Create IBM Cloud Account**
   - Visit: https://cloud.ibm.com/registration
   - Sign up (free tier available)
   - No credit card required for free tier

2. **Create watsonx.ai Project**
   - Navigate to: https://dataplatform.cloud.ibm.com/wx/home
   - Click "Create a project"
   - Select "Create an empty project"
   - Name your project (e.g., "ESG-Lens-Project")
   - **Save your Project ID** (found in project settings → General)

3. **Get API Key**
   - Go to: https://cloud.ibm.com/iam/apikeys
   - Click "Create an IBM Cloud API key"
   - Name it (e.g., "esg-lens-api-key")
   - **Copy and save the API key** (you won't see it again!)

4. **Free Tier Limits**
   - 10 Compute Unit Hours (CUH) per month
   - Approximately 100 pages of text processing
   - Perfect for demos and proof-of-concepts

#### Optional: NASA FIRMS API Key (Free)

For satellite thermal anomaly detection:
1. Visit: https://firms.modaps.eosdis.nasa.gov/api/area/
2. Request a MAP_KEY (free, instant approval)
3. Save the key for later configuration

---

## Local Development Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd LENS

# Verify structure
ls -la
# Should see: backend/, frontend/, docs/, config/, README.md
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

**Windows:**
```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

**macOS/Linux:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

#### 2.2 Install Dependencies

```bash
# Ensure virtual environment is activated
# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import fastapi; import spacy; print('✓ Dependencies installed successfully')"
```

#### 2.3 Configure Environment Variables

```bash
# Copy example environment file
# Windows:
copy .env.example .env

# macOS/Linux:
cp .env.example .env

# Edit .env file with your credentials
# Use your preferred text editor (notepad, nano, vim, VS Code, etc.)
```

**Edit `backend/.env`:**
```env
# ============================================
# IBM watsonx.ai (REQUIRED)
# ============================================
IBM_CLOUD_API_KEY=your_actual_api_key_here
IBM_WATSONX_PROJECT_ID=your_actual_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct

# ============================================
# Storage Configuration
# ============================================
# For local development, use memory mode
STORAGE_MODE=memory
SESSION_TIMEOUT_MINUTES=60

# ============================================
# NLU Configuration
# ============================================
SPACY_MODEL=en_core_web_sm

# ============================================
# External APIs (Optional)
# ============================================
NASA_FIRMS_MAP_KEY=your_nasa_firms_key_here
GDELT_API_URL=https://api.gdeltproject.org/api/v2/doc/doc

# ============================================
# Application Settings
# ============================================
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### 2.4 Test Backend

```bash
# Ensure you're in backend directory with venv activated
python -m app.main

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test in browser:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

**Expected health check response:**
```json
{
  "status": "healthy",
  "service": "ESG Claim Verification Assistant"
}
```

### Step 3: Frontend Setup

Open a **new terminal** (keep backend running):

#### 3.1 Install Dependencies

```bash
cd frontend

# Install npm packages
npm install

# Verify installation
npm list --depth=0
```

#### 3.2 Configure Environment

```bash
# Copy example environment file
# Windows:
copy .env.example .env

# macOS/Linux:
cp .env.example .env
```

**Edit `frontend/.env`:**
```env
# API Base URL (for local development)
VITE_API_URL=http://localhost:8000/api/v1
```

#### 3.3 Start Development Server

```bash
# Start Vite dev server
npm run dev

# You should see:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:5173/
```

**Open in browser:** http://localhost:5173/

### Step 4: Verify Local Setup

#### Test Complete Workflow

1. **Upload a PDF**
   - Use a sample sustainability report
   - Should see upload progress and success message

2. **Extract Claims**
   - Click "Extract Claims" button
   - Should see 3-5 claims extracted with confidence scores

3. **Verify Claims**
   - Select a claim
   - Click "Verify" button
   - Should see evidence from NASA FIRMS and GDELT

4. **View Risk Score**
   - Should see overall risk score
   - Click claim for detailed breakdown
   - Read AI-generated explanation

**If all steps work, your local setup is complete! ✅**

---

## Production Configuration

### Environment Variables for Production

#### Backend Production `.env`

```env
# ============================================
# IBM watsonx.ai (REQUIRED)
# ============================================
IBM_CLOUD_API_KEY=your_production_api_key
IBM_WATSONX_PROJECT_ID=your_production_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct

# ============================================
# Storage Configuration (Production)
# ============================================
# Use memory mode for stateless deployment (recommended for free hosting)
STORAGE_MODE=memory
SESSION_TIMEOUT_MINUTES=60

# OR use persistent mode if you have disk storage
# STORAGE_MODE=persistent
# STORAGE_PERSIST_DIRECTORY=/app/chroma_storage

# ============================================
# NLU Configuration
# ============================================
# Use larger model for better accuracy in production
SPACY_MODEL=en_core_web_lg

# ============================================
# External APIs
# ============================================
NASA_FIRMS_MAP_KEY=your_production_nasa_key
GDELT_API_URL=https://api.gdeltproject.org/api/v2/doc/doc

# ============================================
# Application Settings (Production)
# ============================================
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO

# CORS - Update with your production frontend URL
CORS_ORIGINS=https://your-frontend-domain.com

# ============================================
# Security (Production)
# ============================================
# Add admin token for protected endpoints
ADMIN_TOKEN=your_secure_random_token_here
```

#### Frontend Production `.env`

```env
# API Base URL - Update with your production backend URL
VITE_API_URL=https://your-backend-domain.com/api/v1
```

### Building for Production

#### Backend Production Build

```bash
cd backend

# Install production dependencies only
pip install -r requirements.txt --no-dev

# Download production spaCy model
python -m spacy download en_core_web_lg

# Test production configuration
python -c "from app.config import settings; print(f'Storage: {settings.storage_mode}'); print(f'CORS: {settings.cors_origins}')"
```

#### Frontend Production Build

```bash
cd frontend

# Install dependencies
npm ci --production

# Build for production
npm run build

# Output will be in frontend/dist/
# Verify build
ls -la dist/
```

**Production build creates:**
- Minified JavaScript
- Optimized CSS
- Compressed assets
- Ready for static hosting

---

## Deployment Options

### Option 1: Docker Deployment

#### Backend Dockerfile

The project includes `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Run with Docker

```bash
# Build backend image
cd backend
docker build -t esg-lens-backend:latest .

# Run backend container
docker run -d \
  --name esg-lens-backend \
  -p 8000:8000 \
  --env-file .env \
  esg-lens-backend:latest

# Check logs
docker logs -f esg-lens-backend

# Test
curl http://localhost:8000/api/v1/health
```

#### Docker Compose (Full Stack)

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - STORAGE_MODE=memory
      - SESSION_TIMEOUT_MINUTES=60
    env_file:
      - backend/.env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

networks:
  default:
    name: esg-lens-network
```

**Frontend Dockerfile** (create `frontend/Dockerfile`):

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Nginx config** (create `frontend/nginx.conf`):

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Deploy with Docker Compose:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Traditional Server Deployment

#### Ubuntu/Debian Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip nginx git

# Create application user
sudo useradd -m -s /bin/bash esgapp
sudo su - esgapp

# Clone repository
git clone <your-repo-url> /home/esgapp/LENS
cd /home/esgapp/LENS

# Setup backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Setup frontend
cd ../frontend
npm install
npm run build
```

#### Systemd Service (Backend)

Create `/etc/systemd/system/esg-lens-backend.service`:

```ini
[Unit]
Description=ESG Lens Backend API
After=network.target

[Service]
Type=simple
User=esgapp
Group=esgapp
WorkingDirectory=/home/esgapp/LENS/backend
Environment="PATH=/home/esgapp/LENS/backend/venv/bin"
EnvironmentFile=/home/esgapp/LENS/backend/.env
ExecStart=/home/esgapp/LENS/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable esg-lens-backend
sudo systemctl start esg-lens-backend
sudo systemctl status esg-lens-backend
```

#### Nginx Configuration (Frontend + Reverse Proxy)

Create `/etc/nginx/sites-available/esg-lens`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    root /home/esgapp/LENS/frontend/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # File upload size limit
    client_max_body_size 50M;
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/esg-lens /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

---

## Free Hosting Platforms

### Option 1: Render.com (Recommended - NO Credit Card)

**✅ Completely FREE, NO credit card required**

#### Deploy Backend

1. **Sign up at [render.com](https://render.com)**
   - Use GitHub account (free)

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: esg-lens-backend
   Environment: Python 3
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   
   Build Command:
   pip install -r requirements.txt && python -m spacy download en_core_web_lg
   
   Start Command:
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   
   Instance Type: Free
   ```

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add all variables from your `.env` file:
   ```
   IBM_CLOUD_API_KEY=your_key
   IBM_WATSONX_PROJECT_ID=your_project_id
   STORAGE_MODE=memory
   SESSION_TIMEOUT_MINUTES=60
   SPACY_MODEL=en_core_web_lg
   CORS_ORIGINS=https://your-frontend-url.onrender.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://esg-lens-backend.onrender.com`

#### Deploy Frontend

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository

2. **Configure Site**
   ```
   Name: esg-lens-frontend
   Branch: main
   Root Directory: frontend
   
   Build Command:
   npm install && npm run build
   
   Publish Directory: dist
   ```

3. **Add Environment Variable**
   ```
   VITE_API_URL=https://esg-lens-backend.onrender.com/api/v1
   ```

4. **Deploy**
   - Click "Create Static Site"
   - Wait for deployment (3-5 minutes)
   - Access at: `https://esg-lens-frontend.onrender.com`

**✅ Done! Your app is live!**

**Free Tier Limits:**
- 512MB RAM
- Shared CPU
- 100GB bandwidth/month
- Sleeps after 15 minutes of inactivity
- Wakes up automatically on request (cold start ~30 seconds)

### Option 2: Railway.app

**✅ FREE tier with GitHub, NO credit card initially**

#### Deploy

1. **Sign up at [railway.app](https://railway.app)**
   - Use GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Backend**
   - Railway auto-detects Python
   - Add environment variables in dashboard
   - Set custom start command:
   ```bash
   cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_lg && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Configure Frontend**
   - Add new service from same repo
   - Set build command:
   ```bash
   cd frontend && npm install && npm run build
   ```
   - Set start command:
   ```bash
   cd frontend && npx serve -s dist -l $PORT
   ```

5. **Get URLs**
   - Railway provides URLs for both services
   - Update CORS and API URL accordingly

**Free Tier Limits:**
- $5 credit per month
- 512MB RAM
- Shared CPU
- No sleep policy

### Option 3: Vercel (Frontend) + Render (Backend)

**Best for production-like performance**

#### Deploy Frontend to Vercel

1. **Sign up at [vercel.com](https://vercel.com)**
   - Use GitHub account

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   
   Environment Variables:
   VITE_API_URL=https://your-backend.onrender.com/api/v1
   ```

4. **Deploy**
   - Click "Deploy"
   - Get URL: `https://your-app.vercel.app`

#### Deploy Backend to Render

Follow Render.com instructions above.

**Benefits:**
- Vercel: Global CDN, instant deployments, no cold starts
- Render: Free backend hosting
- Best performance for end users

### Option 4: Fly.io

**✅ FREE tier available**

#### Install Fly CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### Deploy Backend

```bash
cd backend

# Login (creates free account)
fly auth signup

# Launch app
fly launch --name esg-lens-backend --region ord

# Set secrets
fly secrets set IBM_CLOUD_API_KEY=your_key
fly secrets set IBM_WATSONX_PROJECT_ID=your_project_id
fly secrets set STORAGE_MODE=memory

# Deploy
fly deploy

# Get URL
fly status
```

#### Deploy Frontend

```bash
cd frontend

# Launch app
fly launch --name esg-lens-frontend --region ord

# Set environment
fly secrets set VITE_API_URL=https://esg-lens-backend.fly.dev/api/v1

# Deploy
fly deploy
```

**Free Tier Limits:**
- 3 shared-cpu-1x VMs
- 256MB RAM each
- 160GB bandwidth/month
- No sleep policy

---

## Production Checklist

### Pre-Deployment

- [ ] **Code Review**
  - [ ] All sensitive data removed from code
  - [ ] No hardcoded credentials
  - [ ] Error handling implemented
  - [ ] Logging configured

- [ ] **Environment Configuration**
  - [ ] Production `.env` files created
  - [ ] All API keys obtained and tested
  - [ ] CORS origins updated
  - [ ] Storage mode configured

- [ ] **Dependencies**
  - [ ] All dependencies in requirements.txt
  - [ ] All dependencies in package.json
  - [ ] spaCy model specified
  - [ ] No dev dependencies in production

- [ ] **Testing**
  - [ ] Local testing completed
  - [ ] All API endpoints tested
  - [ ] File upload tested
  - [ ] Error scenarios tested

### Deployment

- [ ] **Backend Deployment**
  - [ ] Backend deployed successfully
  - [ ] Health check endpoint responding
  - [ ] API documentation accessible
  - [ ] Logs showing no errors

- [ ] **Frontend Deployment**
  - [ ] Frontend built successfully
  - [ ] Static files served correctly
  - [ ] API connection working
  - [ ] All routes accessible

- [ ] **Integration**
  - [ ] Frontend can reach backend
  - [ ] CORS configured correctly
  - [ ] File uploads working
  - [ ] All features functional

### Post-Deployment

- [ ] **Security**
  - [ ] HTTPS enabled (if applicable)
  - [ ] API keys secured
  - [ ] Admin endpoints protected
  - [ ] Rate limiting considered

- [ ] **Monitoring**
  - [ ] Health checks configured
  - [ ] Logging enabled
  - [ ] Error tracking setup
  - [ ] Usage monitoring active

- [ ] **Documentation**
  - [ ] Deployment documented
  - [ ] URLs documented
  - [ ] Access credentials secured
  - [ ] Rollback plan documented

- [ ] **Performance**
  - [ ] Load testing performed
  - [ ] Response times acceptable
  - [ ] Memory usage monitored
  - [ ] Cold start times acceptable

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Backend Won't Start

**Symptom:** Server crashes on startup

**Solutions:**

```bash
# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip list | grep fastapi
pip list | grep spacy

# Check environment variables
python -c "from app.config import settings; print(settings.dict())"

# View detailed error
python -m app.main --log-level debug

# Check spaCy model
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ Model loaded')"
```

#### 2. Frontend Build Fails

**Symptom:** `npm run build` fails

**Solutions:**

```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 18+

# Build with verbose output
npm run build --verbose

# Check environment variables
cat .env
```

#### 3. CORS Errors

**Symptom:** "Access-Control-Allow-Origin" errors in browser console

**Solutions:**

```env
# Backend .env - Add frontend URL to CORS_ORIGINS
CORS_ORIGINS=http://localhost:5173,https://your-frontend-domain.com

# Restart backend after changing
```

#### 4. API Connection Failed

**Symptom:** Frontend can't reach backend

**Solutions:**

```javascript
// Check frontend .env
console.log(import.meta.env.VITE_API_URL);

// Test backend directly
curl https://your-backend-url.com/api/v1/health

// Check network tab in browser DevTools
// Verify URL is correct
```

#### 5. watsonx.ai Authentication Failed

**Symptom:** "401 Unauthorized" or "Invalid API key"

**Solutions:**

```bash
# Verify API key
echo $IBM_CLOUD_API_KEY

# Test API key
curl -X POST "https://iam.cloud.ibm.com/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=YOUR_API_KEY"

# Regenerate API key if needed
# Go to: https://cloud.ibm.com/iam/apikeys

# Verify project ID
# Go to: https://dataplatform.cloud.ibm.com/wx/home
# Click your project → Settings → General
```

#### 6. Out of Memory (Free Hosting)

**Symptom:** App crashes with memory errors

**Solutions:**

```env
# Reduce session timeout
SESSION_TIMEOUT_MINUTES=30

# Use smaller spaCy model
SPACY_MODEL=en_core_web_sm

# Limit file size
MAX_FILE_SIZE_MB=20
```

```bash
# Manual cleanup endpoint
curl -X POST https://your-app.com/admin/cleanup-expired

# Monitor memory usage
# Check hosting platform dashboard
```

#### 7. Cold Start Issues (Render/Railway)

**Symptom:** First request takes 30+ seconds

**Solutions:**

```bash
# Use a ping service (cron-job.org)
# Ping every 10 minutes: GET https://your-app.com/api/v1/health

# Or upgrade to paid tier for always-on
```

#### 8. File Upload Fails

**Symptom:** "File too large" or upload timeout

**Solutions:**

```env
# Backend .env
MAX_FILE_SIZE_MB=50

# Check hosting platform limits
# Render: 100MB max
# Railway: 100MB max
# Vercel: 4.5MB max (use backend for uploads)
```

```nginx
# Nginx configuration
client_max_body_size 50M;
```

#### 9. spaCy Model Not Found

**Symptom:** "Can't find model 'en_core_web_sm'"

**Solutions:**

```bash
# Download model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; spacy.load('en_core_web_sm')"

# For Docker, ensure Dockerfile includes:
RUN python -m spacy download en_core_web_sm
```

#### 10. Session Expired Errors

**Symptom:** "Session not found or expired"

**Solutions:**

```javascript
// Frontend: Implement session refresh
const createSession = async () => {
  const response = await fetch('/session/create', { method: 'POST' });
  const { session_id } = await response.json();
  localStorage.setItem('session_id', session_id);
  return session_id;
};

// Check session before each request
const getSessionId = async () => {
  let sessionId = localStorage.getItem('session_id');
  if (!sessionId) {
    sessionId = await createSession();
  }
  return sessionId;
};
```

### Debug Mode

Enable detailed logging:

```env
# Backend .env
LOG_LEVEL=DEBUG
```

```bash
# View logs
# Render: Dashboard → Logs
# Railway: Dashboard → Deployments → Logs
# Fly.io: fly logs
# Docker: docker logs -f container_name
```

---

## Monitoring & Maintenance

### Health Checks

#### Automated Health Monitoring

**Using UptimeRobot (Free):**

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.com/api/v1/health`
   - Interval: 5 minutes
3. Set up alerts (email/SMS)

**Using Cron-Job.org (Free):**

1. Sign up at [cron-job.org](https://cron-job.org)
2. Create job:
   - URL: `https://your-app.com/api/v1/health`
   - Schedule: Every 10 minutes
3. Enable notifications

#### Manual Health Check

```bash
# Check backend health
curl https://your-backend-url.com/api/v1/health

# Expected response:
# {"status":"healthy","service":"ESG Claim Verification Assistant"}

# Check frontend
curl -I https://your-frontend-url.com

# Expected: HTTP 200 OK
```

### Log Monitoring

#### Application Logs

**Render.com:**
- Dashboard → Your Service → Logs
- Real-time log streaming
- Search and filter

**Railway.app:**
- Dashboard → Deployments → Logs
- Download logs
- Real-time viewing

**Fly.io:**
```bash
fly logs
fly logs --app esg-lens-backend
```

**Docker:**
```bash
docker logs -f esg-lens-backend
docker logs --tail 100 esg-lens-backend
```

#### Log Analysis

Look for:
- Error patterns
- Slow requests (>5 seconds)
- Memory warnings
- API quota warnings
- Failed authentication attempts

### Performance Monitoring

#### Key Metrics

1. **Response Time**
   - Target: <2 seconds for API calls
   - Target: <5 seconds for claim extraction

2. **Memory Usage**
   - Monitor: Stay under 80% of limit
   - Alert: If consistently above 90%

3. **API Usage**
   - watsonx.ai CUH consumption
   - Track daily usage
   - Alert at 80% of monthly quota

4. **Error Rate**
   - Target: <1% error rate
   - Alert: If >5% errors

#### Monitoring Tools

**Free Options:**
- **Render/Railway Dashboard:** Built-in metrics
- **Google Analytics:** Frontend usage
- **Sentry (Free tier):** Error tracking
- **LogRocket (Free tier):** Session replay

### Maintenance Tasks

#### Daily

- [ ] Check health status
- [ ] Review error logs
- [ ] Monitor API usage

#### Weekly

- [ ] Review performance metrics
- [ ] Check disk usage (if persistent storage)
- [ ] Clean up expired sessions
- [ ] Review security logs

#### Monthly

- [ ] Update dependencies
- [ ] Review and rotate API keys
- [ ] Backup configuration
- [ ] Review and optimize costs
- [ ] Test disaster recovery

#### Quarterly

- [ ] Security audit
- [ ] Performance optimization
- [ ] Update documentation
- [ ] Review and update monitoring

### Backup and Recovery

#### Configuration Backup

```bash
# Backup environment files (without sensitive data)
cp backend/.env backend/.env.backup
cp frontend/.env frontend/.env.backup

# Backup to secure location
# Use password manager or secret management service
```

#### Data Backup (if using persistent storage)

```bash
# Backup ChromaDB data
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz backend/chroma_storage/

# Upload to cloud storage
# aws s3 cp chroma_backup_*.tar.gz s3://your-backup-bucket/
```

#### Disaster Recovery Plan

1. **Service Outage**
   - Check hosting platform status
   - Review recent deployments
   - Rollback if needed

2. **Data Loss**
   - Restore from backup
   - Verify data integrity
   - Test application

3. **Security Breach**
   - Rotate all API keys immediately
   - Review access logs
   - Update security measures

### Scaling Considerations

#### When to Scale

Consider upgrading when:
- Consistent >80% memory usage
- Response times >5 seconds
- >10 concurrent users
- Cold starts affecting UX
- Need 24/7 uptime

#### Scaling Options

**Vertical Scaling (Upgrade Instance):**
- Render: Upgrade to Starter ($7/month)
- Railway: Add more credits
- Fly.io: Increase VM size

**Horizontal Scaling (Multiple Instances):**
- Use load balancer
- Stateless architecture (already implemented!)
- Session management across instances

**Optimization Before Scaling:**
1. Enable caching
2. Optimize database queries
3. Compress responses
4. Use CDN for static assets
5. Implement rate limiting

---

## Additional Resources

### Documentation

- [IBM watsonx.ai Docs](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [spaCy Production](https://spacy.io/usage/production)

### Hosting Platforms

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Fly.io Documentation](https://fly.io/docs/)

### Tools

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [UptimeRobot](https://uptimerobot.com/)

### Community

- [FastAPI Discord](https://discord.gg/fastapi)
- [React Community](https://react.dev/community)
- [Stack Overflow](https://stackoverflow.com/)

---

## Support

### Getting Help

1. **Check Documentation**
   - Review this guide
   - Check README.md
   - Review API documentation

2. **Search Issues**
   - GitHub Issues
   - Stack Overflow
   - Platform-specific forums

3. **Debug Locally**
   - Enable debug logging
   - Test with curl/Postman
   - Check browser console

4. **Create Issue**
   - Include error messages
   - Provide configuration (no secrets!)
   - Describe steps to reproduce

### Reporting Issues

When reporting issues, include:

```
**Environment:**
- Platform: (Render/Railway/Local/etc.)
- Python version: 
- Node version:
- Browser: (if frontend issue)

**Configuration:**
- Storage mode: (memory/persistent)
- spaCy model: 
- CORS origins: 

**Error:**
[Paste error message]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Logs:**
[Relevant log entries]
```

---

## Conclusion

You now have a complete guide for deploying the ESG Claim Verification Assistant from local development to production!

### Quick Reference

**Local Development:**
```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && python -m spacy download en_core_web_sm
python -m app.main

# Frontend
cd frontend && npm install && npm run dev
```

**Production Deployment (Render):**
1. Push code to GitHub
2. Create Web Service (backend)
3. Create Static Site (frontend)
4. Configure environment variables
5. Deploy!

**Health Check:**
```bash
curl https://your-app.com/api/v1/health
```

### Next Steps

1. ✅ Complete local setup
2. ✅ Test all features locally
3. ✅ Choose hosting platform
4. ✅ Deploy to production
5. ✅ Configure monitoring
6. ✅ Share with users!

---

**🎉 Congratulations! You're ready to deploy a production-grade ESG Claim Verification Assistant!**

For questions or issues, refer to the [Troubleshooting](#troubleshooting) section or create an issue on GitHub.

---

*Last Updated: 2026-05-02*
*Version: 1.0.0*