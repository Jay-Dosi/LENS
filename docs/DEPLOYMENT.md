# Deployment Guide - IBM Cloud Code Engine

This guide walks through deploying the ESG Claim Verification Assistant to IBM Cloud Code Engine.

---

## Prerequisites

1. IBM Cloud account with billing enabled (free tier is sufficient)
2. IBM Cloud CLI installed
3. Docker installed locally
4. All IBM Cloud services provisioned (watsonx.ai, COS, NLU)

---

## Step 1: Install IBM Cloud CLI

### Windows
```powershell
# Download and run installer from:
# https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases/
```

### macOS
```bash
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh
```

### Linux
```bash
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
```

### Verify Installation
```bash
ibmcloud --version
```

---

## Step 2: Install Code Engine Plugin

```bash
ibmcloud plugin install code-engine
```

---

## Step 3: Login to IBM Cloud

```bash
# Login
ibmcloud login

# Or with SSO
ibmcloud login --sso

# Target your resource group
ibmcloud target -g Default

# Select region (e.g., us-south)
ibmcloud target -r us-south
```

---

## Step 4: Create Code Engine Project

```bash
# Create project
ibmcloud ce project create --name esg-lens-project

# Select the project
ibmcloud ce project select --name esg-lens-project
```

---

## Step 5: Create Container Registry Namespace

```bash
# Create namespace in IBM Container Registry
ibmcloud cr namespace-add esg-lens

# Login to registry
ibmcloud cr login
```

---

## Step 6: Build and Push Docker Image

```bash
# Navigate to backend directory
cd backend

# Build image
docker build -t us.icr.io/esg-lens/esg-lens-backend:v1 .

# Push to IBM Container Registry
docker push us.icr.io/esg-lens/esg-lens-backend:v1
```

---

## Step 7: Create ConfigMap for Environment Variables

```bash
# Create configmap from .env file
ibmcloud ce configmap create --name esg-lens-config \
  --from-env-file .env
```

**Alternative: Create secrets for sensitive data**

```bash
# Create secret for API keys
ibmcloud ce secret create --name esg-lens-secrets \
  --from-literal IBM_CLOUD_API_KEY=your_key_here \
  --from-literal IBM_COS_API_KEY=your_key_here \
  --from-literal IBM_NLU_API_KEY=your_key_here
```

---

## Step 8: Deploy Application

```bash
# Deploy from container registry
ibmcloud ce application create \
  --name esg-lens-api \
  --image us.icr.io/esg-lens/esg-lens-backend:v1 \
  --registry-secret icr-secret \
  --port 8000 \
  --env-from-configmap esg-lens-config \
  --env-from-secret esg-lens-secrets \
  --min-scale 0 \
  --max-scale 2 \
  --cpu 1 \
  --memory 2G \
  --concurrency 10
```

**Parameters Explained:**
- `--min-scale 0`: Scales to zero when idle (saves costs)
- `--max-scale 2`: Maximum 2 instances
- `--cpu 1`: 1 vCPU per instance
- `--memory 2G`: 2GB RAM per instance
- `--concurrency 10`: Max 10 concurrent requests per instance

---

## Step 9: Get Application URL

```bash
# Get application details
ibmcloud ce application get --name esg-lens-api

# The URL will be in the format:
# https://esg-lens-api.xxxxxx.us-south.codeengine.appdomain.cloud
```

---

## Step 10: Test Deployment

```bash
# Health check
curl https://your-app-url.codeengine.appdomain.cloud/health

# API docs
# Open in browser:
# https://your-app-url.codeengine.appdomain.cloud/docs
```

---

## Step 11: Update Application

When you make changes:

```bash
# Rebuild image with new tag
docker build -t us.icr.io/esg-lens/esg-lens-backend:v2 .
docker push us.icr.io/esg-lens/esg-lens-backend:v2

# Update application
ibmcloud ce application update \
  --name esg-lens-api \
  --image us.icr.io/esg-lens/esg-lens-backend:v2
```

---

## Step 12: Monitor Application

```bash
# View logs
ibmcloud ce application logs --name esg-lens-api

# Follow logs in real-time
ibmcloud ce application logs --name esg-lens-api --follow

# View application events
ibmcloud ce application events --name esg-lens-api
```

---

## Cost Optimization

### Free Tier Limits
- Code Engine: Free tier includes compute time
- Scales to zero when idle = no cost when not in use
- Only pay for actual request processing time

### Tips
1. Set `--min-scale 0` to scale to zero
2. Use appropriate `--cpu` and `--memory` (don't over-provision)
3. Set reasonable `--concurrency` limits
4. Monitor usage in IBM Cloud dashboard

---

## Troubleshooting

### Application Won't Start

```bash
# Check application status
ibmcloud ce application get --name esg-lens-api

# View logs for errors
ibmcloud ce application logs --name esg-lens-api --tail 100
```

### Environment Variables Not Loading

```bash
# Verify configmap
ibmcloud ce configmap get --name esg-lens-config

# Verify secret
ibmcloud ce secret get --name esg-lens-secrets
```

### Image Pull Errors

```bash
# Verify registry secret
ibmcloud ce registry get --name icr-secret

# Recreate if needed
ibmcloud ce registry create --name icr-secret \
  --server us.icr.io \
  --username iamapikey \
  --password YOUR_IBM_CLOUD_API_KEY
```

---

## Cleanup

To remove all resources:

```bash
# Delete application
ibmcloud ce application delete --name esg-lens-api

# Delete configmap
ibmcloud ce configmap delete --name esg-lens-config

# Delete secret
ibmcloud ce secret delete --name esg-lens-secrets

# Delete project
ibmcloud ce project delete --name esg-lens-project

# Delete container registry namespace
ibmcloud cr namespace-rm esg-lens
```

---

## Production Considerations

For a production deployment, consider:

1. **Custom Domain**: Map a custom domain to your Code Engine app
2. **HTTPS**: Code Engine provides HTTPS by default
3. **Rate Limiting**: Implement rate limiting in the API
4. **Monitoring**: Set up IBM Cloud Monitoring
5. **Logging**: Configure IBM Log Analysis
6. **Secrets Management**: Use IBM Secrets Manager
7. **CI/CD**: Set up automated deployments with IBM Toolchain
8. **Backup**: Regular backups of Object Storage data

---

## Additional Resources

- [IBM Code Engine Documentation](https://cloud.ibm.com/docs/codeengine)
- [IBM Container Registry Documentation](https://cloud.ibm.com/docs/Registry)
- [Code Engine Pricing](https://cloud.ibm.com/docs/codeengine?topic=codeengine-pricing)

---

**Deployment complete! Your ESG Claim Verification Assistant is now running on IBM Cloud. 🚀**