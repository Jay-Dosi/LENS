# API Keys and Configuration Guide

## 🔑 Required API Keys

This document provides detailed information about all API keys needed for the ESG Claim Verification Assistant, including where to obtain them and their free tier limits.

---

## IBM Cloud Services (All Free Tier Available)

### 1. IBM Cloud API Key
**Purpose:** Primary authentication for IBM Cloud services (watsonx.ai, Cloud Object Storage, Watson NLU)

**How to Get:**
1. Sign up for IBM Cloud: https://cloud.ibm.com/registration
2. Navigate to: https://cloud.ibm.com/iam/apikeys
3. Click "Create an IBM Cloud API key"
4. Give it a name (e.g., "ESG-LENS-API-Key")
5. Copy and save the API key securely

**Free Tier:** Yes, IBM Cloud account is free to create

**Environment Variable:** `IBM_CLOUD_API_KEY`

---

### 2. IBM watsonx.ai Project ID
**Purpose:** Access IBM watsonx.ai Granite models for claim extraction and explanation generation

**How to Get:**
1. Go to: https://dataplatform.cloud.ibm.com/wx/home
2. Create a new watsonx.ai project or select existing one
3. Click on "Manage" tab in your project
4. Copy the "Project ID" from the project details

**Free Tier:** 
- Lite Plan: 10 Compute Unit Hours (CUH) per month
- Sufficient for ~100 pages of text processing
- No credit card required

**Models Used:**
- `ibm/granite-13b-instruct-v2` - Claim extraction
- `ibm/granite-3-8b-instruct` - Explanation generation

**Environment Variables:**
- `IBM_WATSONX_PROJECT_ID`
- `WATSONX_URL=https://us-south.ml.cloud.ibm.com`
- `WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2`
- `WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct`

**Documentation:** https://www.ibm.com/docs/en/watsonx-as-a-service

---

### 3. IBM Cloud Object Storage (COS)
**Purpose:** Store uploaded PDFs, extracted text, claims, evidence, and final reports

**How to Get:**
1. Go to: https://cloud.ibm.com/catalog/services/cloud-object-storage
2. Select "Lite" plan (free)
3. Create the service
4. Create a bucket named `esg-lens-hackathon`
5. Go to "Service credentials" → "New credential"
6. Copy the following from credentials JSON:
   - `apikey` → `IBM_COS_API_KEY`
   - `iam_serviceid_crn` → `IBM_COS_INSTANCE_CRN`
7. Get endpoint from "Endpoints" tab (e.g., `https://s3.us-south.cloud-object-storage.appdomain.cloud`)

**Free Tier:**
- Lite Plan: 25 GB storage
- 2,000 Class A requests/month
- 20,000 Class B requests/month
- No credit card required

**Environment Variables:**
- `IBM_COS_API_KEY`
- `IBM_COS_INSTANCE_CRN`
- `IBM_COS_ENDPOINT`
- `IBM_COS_BUCKET_NAME=esg-lens-hackathon`

**Documentation:** https://cloud.ibm.com/docs/cloud-object-storage

---

### 4. IBM Watson Natural Language Understanding (NLU)
**Purpose:** Extract entities (facilities, locations, organizations) from sustainability reports

**How to Get:**
1. Go to: https://cloud.ibm.com/catalog/services/natural-language-understanding
2. Select "Lite" plan (free)
3. Create the service
4. Go to "Manage" → Copy the API key and URL
5. Use the URL as-is (e.g., `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com`)

**Free Tier:**
- Lite Plan: 30,000 NLU items per month
- Sufficient for processing hundreds of documents
- No credit card required

**Environment Variables:**
- `IBM_NLU_API_KEY`
- `IBM_NLU_URL`

**Documentation:** https://cloud.ibm.com/docs/natural-language-understanding

---

## External Data Sources (No API Keys Required)

### 5. OpenWeatherMap Air Pollution API
**Purpose:** Historical and current air quality monitoring near facilities

**API Access:** 
- **API:** https://openweathermap.org/api/air-pollution
- **API key required**
- Sign up at: https://home.openweathermap.org/users/sign_up

**Free Tier:** 
- 1,000 API calls/day
- Current and historical air pollution data
- CO, NO2, O3, SO2, PM2.5, PM10 metrics

**Environment Variable:** `OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here`

**Documentation:** https://openweathermap.org/api/air-pollution

---

### 6. Google News RSS
**Purpose:** News sentiment analysis and environmental coverage tracking

**API Access:**
- **Public RSS:** https://news.google.com/rss/search
- **No API key required**
- Open to use with standard feed parsing

**Free Tier:**
- Unlimited access (but rate limiting of 2 seconds between requests recommended)
- Real-time global news monitoring

**Documentation:** https://news.google.com/rss

---

## Application Settings (No API Keys)

These are configuration settings for the application itself:

```env
UPLOAD_DIR=./uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=pdf
LOG_LEVEL=INFO
```

---

## Summary Table

| Service | API Key Required | Free Tier | Credit Card Required | Monthly Limit |
|---------|------------------|-----------|---------------------|---------------|
| IBM Cloud API | ✅ Yes | ✅ Yes | ❌ No | N/A |
| IBM watsonx.ai | ✅ Yes (Project ID) | ✅ Yes | ❌ No | 10 CUH |
| IBM Cloud Object Storage | ✅ Yes | ✅ Yes | ❌ No | 25 GB |
| IBM Watson NLU | ✅ Yes | ✅ Yes | ❌ No | 30,000 items |
| OpenWeatherMap | ✅ Yes | ✅ Yes | ❌ No | 1,000 calls/day |
| Google News | ❌ No | ✅ Yes | ❌ No | Unlimited |

---

## Quick Setup Checklist

- [ ] Create IBM Cloud account
- [ ] Generate IBM Cloud API key
- [ ] Create watsonx.ai project and get Project ID
- [ ] Create Cloud Object Storage instance and bucket
- [ ] Create Watson NLU instance
- [ ] Copy all credentials to `.env` file
- [ ] Sign up for OpenWeatherMap and get API key

---

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Rotate API keys regularly** (every 90 days recommended)
3. **Use separate keys** for development and production
4. **Limit API key permissions** to only required services
5. **Monitor usage** through IBM Cloud dashboard
6. **Set up billing alerts** if upgrading from free tier

---

## Troubleshooting

### "Invalid API Key" Error
- Verify the API key is copied correctly (no extra spaces)
- Check if the key has been revoked in IBM Cloud console
- Ensure the key has access to the required services

### "Quota Exceeded" Error
- Check usage in IBM Cloud dashboard
- Wait until next month for quota reset
- Consider upgrading to paid tier for production

### "Service Not Found" Error
- Verify the service instance is created in IBM Cloud
- Check the service URL/endpoint is correct
- Ensure the API key has access to the service

---

## Cost Optimization Tips

1. **Process only candidate chunks** - Filter PDF content before sending to watsonx.ai
2. **Limit claims per demo** - Process max 5 claims to conserve CUH
3. **Cache results** - Store processed documents to avoid reprocessing
4. **Use local PDF extraction** - Don't send raw PDFs to watsonx.ai
5. **Batch NLU requests** - Combine multiple text segments when possible

---

## Additional Resources

- **IBM Cloud Console:** https://cloud.ibm.com/
- **watsonx.ai Documentation:** https://www.ibm.com/docs/en/watsonx-as-a-service
- **IBM Cloud Object Storage Docs:** https://cloud.ibm.com/docs/cloud-object-storage
- **Watson NLU Docs:** https://cloud.ibm.com/docs/natural-language-understanding
- **OpenWeatherMap API:** https://openweathermap.org/api
- **Google News RSS:** https://news.google.com/rss

---

*Last Updated: 2026-05-02*