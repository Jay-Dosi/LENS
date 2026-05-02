# Free Deployment Guide - NO Credit Card Required

This guide shows you how to deploy the ESG Claim Verification Assistant on **completely free platforms** that require **NO credit card**.

## 🎯 Architecture Overview

The application uses a **stateless, session-based architecture**:

- ✅ **ChromaDB** - In-memory vector database (FREE, no external service)
- ✅ **Session Management** - Automatic cleanup after timeout
- ✅ **No External Storage** - Everything runs in-memory or local disk
- ✅ **No Database Service** - No PostgreSQL, MongoDB, or cloud databases needed
- ✅ **No Object Storage** - No S3, Azure Blob, or cloud storage needed

**Perfect for demos, hackathons, and proof-of-concepts!**

---

## 🚀 Quick Start - Choose Your Platform

### Option 1: Render.com (Recommended)

**✅ Completely FREE, NO credit card required**

#### Step 1: Prepare Your Repository

1. Push your code to GitHub
2. Ensure `.env.example` is in your repository
3. Make sure `requirements.txt` includes `chromadb==0.4.22`

#### Step 2: Deploy Backend

1. Go to [render.com](https://render.com) and sign up (free, no credit card)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `esg-lens-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

5. Add Environment Variables:
   ```
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   STORAGE_MODE=memory
   SESSION_TIMEOUT_MINUTES=60
   CORS_ORIGINS=https://your-frontend-url.onrender.com
   ```

6. Click **"Create Web Service"**

#### Step 3: Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `esg-lens-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

4. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

5. Click **"Create Static Site"**

**Done! Your app is live! 🎉**

---

### Option 2: Railway.app

**✅ FREE tier with GitHub, NO credit card initially**

#### Step 1: Deploy

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (free)
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository

#### Step 2: Configure Backend

1. Railway will auto-detect Python
2. Add environment variables in the Railway dashboard:
   ```
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   STORAGE_MODE=memory
   SESSION_TIMEOUT_MINUTES=60
   PORT=8000
   ```

3. Set custom start command:
   ```bash
   cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

#### Step 3: Configure Frontend

1. Add a new service for frontend
2. Set build command:
   ```bash
   cd frontend && npm install && npm run build
   ```
3. Set start command:
   ```bash
   cd frontend && npm run preview -- --host 0.0.0.0 --port $PORT
   ```

**Done! Railway provides URLs for both services! 🎉**

---

### Option 3: Fly.io

**✅ FREE tier available**

#### Step 1: Install Fly CLI

```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### Step 2: Deploy Backend

```bash
cd backend

# Login (free signup)
fly auth signup

# Create app
fly launch --name esg-lens-backend --no-deploy

# Set secrets
fly secrets set IBM_CLOUD_API_KEY=your_api_key_here
fly secrets set IBM_WATSONX_PROJECT_ID=your_project_id_here
fly secrets set STORAGE_MODE=memory

# Deploy
fly deploy
```

#### Step 3: Deploy Frontend

```bash
cd frontend

# Create app
fly launch --name esg-lens-frontend --no-deploy

# Set environment
fly secrets set VITE_API_URL=https://esg-lens-backend.fly.dev

# Deploy
fly deploy
```

**Done! Access at https://esg-lens-frontend.fly.dev 🎉**

---

### Option 4: Replit

**✅ Completely FREE, browser-based**

#### Step 1: Import Project

1. Go to [replit.com](https://replit.com)
2. Click **"Create Repl"** → **"Import from GitHub"**
3. Paste your repository URL

#### Step 2: Configure

1. Replit will auto-detect the project
2. Add secrets in the "Secrets" tab (lock icon):
   ```
   IBM_CLOUD_API_KEY=your_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   STORAGE_MODE=memory
   ```

3. Create `.replit` file:
   ```toml
   run = "cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm && uvicorn app.main:app --host 0.0.0.0 --port 8000"
   ```

4. Click **"Run"**

**Done! Replit provides a URL automatically! 🎉**

---

## 🔧 Configuration for Stateless Mode

### Environment Variables

**Required:**
```bash
IBM_CLOUD_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
```

**Storage Configuration:**
```bash
# Use in-memory storage (stateless, perfect for free hosting)
STORAGE_MODE=memory

# Session timeout (data auto-deleted after this time)
SESSION_TIMEOUT_MINUTES=60
```

**Optional:**
```bash
# For persistent storage (uses local disk)
STORAGE_MODE=persistent
STORAGE_PERSIST_DIRECTORY=./chroma_storage
```

---

## 📊 Session Management

### How It Works

1. **Session Creation**: Each user gets a unique session ID
2. **Data Storage**: All data stored in-memory with session ID
3. **Auto Cleanup**: Sessions expire after `SESSION_TIMEOUT_MINUTES`
4. **Manual Reset**: Use admin endpoints to clear data

### API Endpoints

#### Create Session
```bash
POST /session/create
Response: { "session_id": "uuid", "timeout_minutes": 60 }
```

#### Get Session Info
```bash
GET /session/{session_id}
Response: { "session_id": "uuid", "created_at": "...", "active": true }
```

#### Cleanup Session
```bash
DELETE /session/{session_id}
Response: { "message": "Session cleaned up successfully" }
```

#### Cleanup Expired Sessions (Admin)
```bash
POST /admin/cleanup-expired
Response: { "message": "Cleaned up N expired sessions", "count": N }
```

#### Reset All Data (Admin)
```bash
POST /admin/reset
Response: { "message": "All data reset successfully" }
```

### Using Sessions in Frontend

```javascript
// Create session on app load
const response = await fetch('/session/create', { method: 'POST' });
const { session_id } = await response.json();

// Store session ID
localStorage.setItem('session_id', session_id);

// Include in all requests
fetch('/upload', {
  method: 'POST',
  headers: {
    'X-Session-ID': session_id
  },
  body: formData
});

// Cleanup on logout
await fetch(`/session/${session_id}`, { method: 'DELETE' });
localStorage.removeItem('session_id');
```

---

## 🎯 Demo Mode

Perfect for hackathons and presentations!

### Quick Reset Between Demos

```bash
# Reset all data
curl -X POST https://your-app.com/admin/reset

# Or use the frontend
// Add a reset button in your UI
const resetDemo = async () => {
  await fetch('/admin/reset', { method: 'POST' });
  alert('Demo reset! Ready for next presentation.');
};
```

### Multiple Demo Sessions

```bash
# Each demo gets its own session
# Sessions auto-expire after 60 minutes
# No manual cleanup needed!

# Demo 1
POST /session/create → session_1

# Demo 2 (parallel)
POST /session/create → session_2

# Both sessions isolated, auto-cleanup after timeout
```

---

## 💾 Storage Modes Comparison

| Feature | Memory Mode | Persistent Mode |
|---------|-------------|-----------------|
| **Cost** | FREE | FREE |
| **External Services** | None | None |
| **Data Persistence** | Session only | Survives restarts |
| **Best For** | Demos, hackathons | Development |
| **Cleanup** | Automatic | Manual |
| **Deployment** | Any platform | Needs disk access |

---

## 🔒 Security Considerations

### For Free Hosting

1. **API Keys**: Always use environment variables, never commit
2. **Session Timeout**: Keep it reasonable (30-60 minutes)
3. **Rate Limiting**: Consider adding rate limits for public demos
4. **Admin Endpoints**: Protect with authentication in production

### Example: Protect Admin Endpoints

```python
from fastapi import Header, HTTPException

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "change-me-in-production")

@router.post("/admin/reset")
async def reset_all_data(
    authorization: str = Header(None)
):
    if authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    storage = get_storage_service()
    storage.reset_all_data()
    return {"message": "Reset successful"}
```

---

## 📈 Scaling Considerations

### Free Tier Limits

| Platform | Memory | CPU | Bandwidth | Sleep Policy |
|----------|--------|-----|-----------|--------------|
| **Render** | 512MB | Shared | 100GB/mo | After 15min inactive |
| **Railway** | 512MB | Shared | 100GB/mo | No sleep |
| **Fly.io** | 256MB | Shared | 160GB/mo | No sleep |
| **Replit** | 512MB | Shared | Unlimited | After 1hr inactive |

### Optimization Tips

1. **Session Timeout**: Lower timeout = less memory usage
2. **Cleanup**: Run `/admin/cleanup-expired` periodically
3. **File Size**: Limit PDF uploads to 10-20MB
4. **Concurrent Users**: Free tiers handle 5-10 concurrent users

### When to Upgrade

Consider paid hosting when:
- More than 10 concurrent users
- Need 24/7 uptime
- Require data persistence
- Need more than 512MB RAM

---

## 🐛 Troubleshooting

### App Sleeps on Free Tier

**Problem**: App goes to sleep after inactivity

**Solution**: Use a ping service
```bash
# Use cron-job.org (free) to ping your app every 10 minutes
GET https://your-app.com/health
```

### Out of Memory

**Problem**: App crashes with memory errors

**Solution**:
1. Lower `SESSION_TIMEOUT_MINUTES` to 30
2. Run cleanup more frequently
3. Limit concurrent sessions
4. Reduce PDF file size limit

### ChromaDB Errors

**Problem**: ChromaDB initialization fails

**Solution**:
```bash
# Ensure ChromaDB is installed
pip install chromadb==0.4.22

# Check Python version (3.8+ required)
python --version

# Clear any existing data
rm -rf ./chroma_storage
```

### Session Not Found

**Problem**: "Session not found or expired" errors

**Solution**:
1. Check session timeout setting
2. Ensure session ID is passed in headers
3. Create new session if expired
4. Check server logs for cleanup events

---

## 🎓 Best Practices

### For Demos

1. **Pre-create Sessions**: Create sessions before demo starts
2. **Quick Reset**: Have reset button ready
3. **Sample Data**: Prepare sample PDFs in advance
4. **Monitoring**: Watch memory usage during demo

### For Development

1. **Use Persistent Mode**: Set `STORAGE_MODE=persistent`
2. **Local Testing**: Test with in-memory mode first
3. **Session Management**: Implement proper session handling in frontend
4. **Error Handling**: Handle session expiration gracefully

### For Production

1. **Upgrade Hosting**: Use paid tier for reliability
2. **Add Authentication**: Protect admin endpoints
3. **Monitoring**: Set up logging and alerts
4. **Backups**: If using persistent mode, backup data regularly

---

## 📚 Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Render.com Docs](https://render.com/docs)
- [Railway.app Docs](https://docs.railway.app/)
- [Fly.io Docs](https://fly.io/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review server logs on your hosting platform
3. Test locally with `STORAGE_MODE=memory`
4. Open an issue on GitHub with:
   - Platform used
   - Error messages
   - Configuration (without API keys!)

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables configured
- [ ] ChromaDB in requirements.txt
- [ ] STORAGE_MODE set to "memory"
- [ ] Session timeout configured
- [ ] CORS origins updated
- [ ] Frontend API URL configured
- [ ] Tested locally first
- [ ] Admin endpoints protected (if public)
- [ ] Monitoring/logging enabled

---

**🎉 Congratulations! You now have a fully functional, stateless ESG Claim Verification Assistant running on FREE infrastructure with NO credit card required!**

---

*Made with ❤️ for hackathons, demos, and proof-of-concepts*