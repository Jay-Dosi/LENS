# API Setup Guide for LENS Platform

This comprehensive guide will walk you through obtaining and configuring all required API keys and credentials for the LENS (Liability Evidence & Natural disaster Scoring) platform.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:
- [ ] A valid email address
- [ ] A credit card (for IBM Cloud - free tier available, no charges for basic usage)
- [ ] Access to create accounts on cloud platforms
- [ ] A text editor to store your credentials temporarily

## 🎯 Quick Credentials Checklist

Use this checklist to track your progress:

- [ ] **IBM Cloud Account** - Created and verified
- [ ] **IBM watsonx.ai** - Project ID and API Key
- [ ] **IBM Cloud Object Storage** - API Key, Instance CRN, and Endpoint URL
- [ ] **IBM Watson NLU** - API Key and Service URL
- [ ] **NASA FIRMS API** - API Key (optional)
- [ ] **GDELT API** - No key needed, usage understood

---

## 1️⃣ IBM Cloud Account Setup

### Step 1: Create IBM Cloud Account

1. **Navigate to IBM Cloud**
   - Go to: [https://cloud.ibm.com/registration](https://cloud.ibm.com/registration)
   
2. **Fill in Registration Details**
   - Enter your email address
   - Create a strong password
   - Select your country/region
   - Accept the terms and conditions
   - Click "Create account"

3. **Verify Your Email**
   - Check your email inbox for a verification email from IBM Cloud
   - Click the verification link
   - You may need to wait a few minutes for the email to arrive

4. **Complete Account Setup**
   - Log in to: [https://cloud.ibm.com/](https://cloud.ibm.com/)
   - You may be prompted to provide additional information
   - Add payment method (required even for free tier, but you won't be charged for basic usage)

### Step 2: Navigate to IBM Cloud Dashboard

- Once logged in, you'll see the IBM Cloud Dashboard
- Bookmark this page: [https://cloud.ibm.com/](https://cloud.ibm.com/)

### ⚠️ Troubleshooting Tips
- **Email not received?** Check spam/junk folder
- **Account locked?** Contact IBM Cloud support at [https://cloud.ibm.com/unifiedsupport/supportcenter](https://cloud.ibm.com/unifiedsupport/supportcenter)
- **Payment issues?** Ensure your card supports international transactions

---

## 2️⃣ IBM watsonx.ai Setup

### What You'll Get
- **Project ID**: Unique identifier for your watsonx.ai project
- **API Key**: Authentication credential for API access

### Step 1: Access watsonx.ai

1. **Navigate to watsonx.ai**
   - Go to: [https://dataplatform.cloud.ibm.com/wx/home](https://dataplatform.cloud.ibm.com/wx/home)
   - Or from IBM Cloud Dashboard: Click "Catalog" → Search "watsonx.ai" → Click "watsonx.ai"

2. **Create a watsonx.ai Service Instance** (if not already created)
   - Click "Create" or "Launch watsonx.ai"
   - Select a region (e.g., Dallas, Frankfurt, Tokyo)
   - Choose the "Lite" plan (free tier)
   - Give it a name (e.g., "LENS-watsonx")
   - Click "Create"

### Step 2: Create a Project

1. **Create New Project**
   - In watsonx.ai, click "Projects" in the left sidebar
   - Click "New project"
   - Select "Create an empty project"
   - Enter project name: "LENS-Project" (or your preferred name)
   - Add a description (optional)
   - Click "Create"

2. **Get Your Project ID**
   - Once in your project, click the "Manage" tab
   - Click "General" in the left sidebar
   - Look for "Project ID" section
   - **Copy the Project ID** - it looks like: `12345678-abcd-1234-abcd-123456789abc`
   - Save this value as `WATSONX_PROJECT_ID` in your `.env` file

### Step 3: Create API Key

1. **Navigate to API Keys**
   - Go to: [https://cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
   - Or from IBM Cloud Dashboard: Click your profile icon (top right) → "API keys"

2. **Create New API Key**
   - Click "Create an IBM Cloud API key"
   - Enter a name: "LENS-watsonx-key"
   - Add a description: "API key for LENS watsonx.ai access"
   - Click "Create"

3. **Copy and Save Your API Key**
   - **IMPORTANT**: A dialog will appear with your API key
   - Click "Copy" or manually select and copy the key
   - **Save it immediately** - you cannot retrieve it later!
   - Save this value as `WATSONX_API_KEY` in your `.env` file
   - Click "Download" to save a backup copy (optional but recommended)

### 📝 Example Values
```
WATSONX_PROJECT_ID=12345678-abcd-1234-abcd-123456789abc
WATSONX_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
```

### ⚠️ Troubleshooting Tips
- **Can't find Project ID?** Make sure you're inside the project, then go to Manage → General
- **API Key not working?** Ensure you copied the entire key without extra spaces
- **Access denied?** Verify your IBM Cloud account is active and verified
- **Project creation fails?** Check if you have sufficient permissions in your IBM Cloud account

---

## 3️⃣ IBM Cloud Object Storage Setup

### What You'll Get
- **API Key**: Authentication credential (can reuse the one from watsonx.ai)
- **Instance CRN**: Cloud Resource Name for your storage instance
- **Endpoint URL**: Service endpoint for your region

### Step 1: Create Cloud Object Storage Instance

1. **Navigate to Catalog**
   - Go to: [https://cloud.ibm.com/catalog/services/cloud-object-storage](https://cloud.ibm.com/catalog/services/cloud-object-storage)
   - Or from IBM Cloud Dashboard: Click "Catalog" → Search "Object Storage"

2. **Create Service Instance**
   - Select the "Lite" plan (free tier - 25GB storage)
   - Choose a region (same as your watsonx.ai for better performance)
   - Enter service name: "LENS-Object-Storage"
   - Select a resource group (use "Default" if unsure)
   - Click "Create"

### Step 2: Get Instance CRN

1. **Access Service Credentials**
   - After creation, you'll be on the service dashboard
   - Click "Service credentials" in the left sidebar
   - If no credentials exist, click "New credential"
     - Name: "LENS-COS-Credentials"
     - Role: "Writer" or "Manager"
     - Click "Add"

2. **Copy Instance CRN**
   - Click "View credentials" (dropdown arrow) next to your credential
   - Find the `"resource_instance_id"` field
   - **Copy the entire CRN value** - it looks like: `crn:v1:bluemix:public:cloud-object-storage:global:a/...`
   - Save this value as `COS_INSTANCE_CRN` in your `.env` file

### Step 3: Get API Key

You can use the same API key from watsonx.ai setup, OR create a new one:

1. **Option A: Reuse Existing API Key**
   - Use the same `WATSONX_API_KEY` value
   - Save it as `COS_API_KEY` in your `.env` file

2. **Option B: Create New API Key**
   - In the service credentials view, the API key is shown as `"apikey"` field
   - Copy this value
   - Save it as `COS_API_KEY` in your `.env` file

### Step 4: Get Endpoint URL

1. **Find Your Endpoint**
   - In your Cloud Object Storage instance, click "Endpoints" in the left sidebar
   - Choose endpoint type based on your needs:
     - **Public**: For general access (recommended for development)
     - **Private**: For internal IBM Cloud network only
     - **Direct**: For high-performance scenarios

2. **Select Region**
   - Find the region where you created your instance
   - Under "Public" endpoints, find your region (e.g., "us-south", "eu-de")
   - **Copy the endpoint URL** - it looks like: `https://s3.us-south.cloud-object-storage.appdomain.cloud`
   - Save this value as `COS_ENDPOINT` in your `.env` file

### Step 5: Create a Bucket (Optional but Recommended)

1. **Create Bucket**
   - Click "Buckets" in the left sidebar
   - Click "Create bucket"
   - Choose "Customize your bucket"
   - Enter bucket name: "lens-evidence-storage" (must be globally unique)
   - Select same region as your instance
   - Choose "Standard" storage class
   - Click "Create bucket"

2. **Note Bucket Name**
   - Save the bucket name as `COS_BUCKET_NAME` in your `.env` file

### 📝 Example Values
```
COS_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
COS_INSTANCE_CRN=crn:v1:bluemix:public:cloud-object-storage:global:a/1234567890abcdef:12345678-abcd-1234-abcd-123456789abc::
COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET_NAME=lens-evidence-storage
```

### ⚠️ Troubleshooting Tips
- **Can't find CRN?** Look for `resource_instance_id` in service credentials
- **Endpoint not working?** Ensure you're using the correct endpoint type (Public/Private/Direct)
- **Bucket name taken?** Bucket names must be globally unique; try adding numbers or your organization name
- **Access denied?** Verify your API key has "Writer" or "Manager" role
- **Connection timeout?** Check if you're using the correct regional endpoint

---

## 4️⃣ IBM Watson Natural Language Understanding Setup

### What You'll Get
- **API Key**: Authentication credential for NLU service
- **Service URL**: Endpoint URL for your NLU instance

### Step 1: Create NLU Service Instance

1. **Navigate to Catalog**
   - Go to: [https://cloud.ibm.com/catalog/services/natural-language-understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding)
   - Or from IBM Cloud Dashboard: Click "Catalog" → Search "Natural Language Understanding"

2. **Create Service Instance**
   - Select the "Lite" plan (free tier - 30,000 NLU items per month)
   - Choose a region (same as your other services for consistency)
   - Enter service name: "LENS-NLU"
   - Select resource group (use "Default" if unsure)
   - Click "Create"

### Step 2: Get API Key and URL

1. **Access Service Credentials**
   - After creation, you'll be on the service dashboard
   - Click "Service credentials" in the left sidebar
   - If no credentials exist, click "New credential"
     - Name: "LENS-NLU-Credentials"
     - Role: "Manager"
     - Click "Add"

2. **Copy API Key**
   - Click "View credentials" (dropdown arrow) next to your credential
   - Find the `"apikey"` field
   - **Copy the API key value**
   - Save this value as `NLU_API_KEY` in your `.env` file

3. **Copy Service URL**
   - In the same credentials view, find the `"url"` field
   - **Copy the URL** - it looks like: `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com`
   - Save this value as `NLU_URL` in your `.env` file

### 📝 Example Values
```
NLU_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

### ⚠️ Troubleshooting Tips
- **API key not working?** Ensure you copied the entire key without spaces
- **Wrong URL format?** The URL should start with `https://api.` and end with `.watson.cloud.ibm.com`
- **Service not responding?** Check if your service instance is active in the IBM Cloud dashboard
- **Rate limit exceeded?** Lite plan has 30,000 items/month limit; monitor usage in the dashboard
- **Authentication error?** Verify the API key matches the service instance region

---

## 5️⃣ NASA FIRMS API Setup (Optional)

### What You'll Get
- **MAP_KEY**: API key for accessing NASA FIRMS fire data

### About NASA FIRMS
NASA's Fire Information for Resource Management System (FIRMS) provides near real-time active fire data. This is optional for the LENS platform but enhances wildfire-related claim analysis.

### Step 1: Request API Key

1. **Navigate to FIRMS**
   - Go to: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)

2. **Request MAP_KEY**
   - Scroll down to "Request a MAP_KEY"
   - Click "Request a MAP_KEY" button
   - Or go directly to: [https://firms.modaps.eosdis.nasa.gov/api/map_key/](https://firms.modaps.eosdis.nasa.gov/api/map_key/)

3. **Fill in Request Form**
   - Enter your email address
   - Enter your first and last name
   - Select your organization type (e.g., "Academic/Research", "Commercial", "Government")
   - Describe your intended use: "Insurance claim verification and natural disaster analysis"
   - Complete the CAPTCHA
   - Click "Request MAP_KEY"

### Step 2: Retrieve Your API Key

1. **Check Your Email**
   - You'll receive an email from NASA FIRMS within a few minutes
   - Subject: "Your FIRMS MAP_KEY"
   - The email contains your MAP_KEY

2. **Copy MAP_KEY**
   - **Copy the MAP_KEY from the email**
   - It's a long alphanumeric string
   - Save this value as `FIRMS_API_KEY` in your `.env` file

### 📝 Example Values
```
FIRMS_API_KEY=1234567890abcdef1234567890abcdef12345678
```

### API Usage Information
- **Rate Limits**: Reasonable use policy (no hard limits for most users)
- **Data Coverage**: Global fire data from MODIS and VIIRS satellites
- **Update Frequency**: Near real-time (3-hour latency)
- **Documentation**: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)

### ⚠️ Troubleshooting Tips
- **Email not received?** Check spam folder; wait up to 30 minutes
- **Key not working?** Ensure you copied the entire key without line breaks
- **Access denied?** Verify your key is active; keys may expire after long periods of inactivity
- **Rate limited?** Contact NASA FIRMS support if you need higher limits

---

## 6️⃣ GDELT API Setup

### What You'll Get
- **No API Key Required**: GDELT is open access

### About GDELT
The Global Database of Events, Language, and Tone (GDELT) monitors news media worldwide. It provides context for natural disasters and events that may impact insurance claims.

### API Access

1. **No Registration Required**
   - GDELT API is completely open and free
   - No API key or authentication needed
   - Direct access to all endpoints

2. **Main Endpoints**
   - **GDELT 2.0 Doc API**: [https://api.gdeltproject.org/api/v2/doc/doc](https://api.gdeltproject.org/api/v2/doc/doc)
   - **GDELT 2.0 TV API**: [https://api.gdeltproject.org/api/v2/tv/tv](https://api.gdeltproject.org/api/v2/tv/tv)
   - **GDELT GEO API**: [https://api.gdeltproject.org/api/v2/geo/geo](https://api.gdeltproject.org/api/v2/geo/geo)

### Usage Guidelines

1. **Rate Limits**
   - Be respectful with request frequency
   - Recommended: No more than 1 request per second
   - For high-volume needs, consider caching results

2. **Query Parameters**
   - `query`: Search terms (e.g., "wildfire California")
   - `mode`: Output mode (e.g., "artlist", "timeline")
   - `maxrecords`: Maximum results (default: 250, max: 250)
   - `format`: Output format (e.g., "json", "csv")
   - `startdatetime`: Start date (format: YYYYMMDDHHMMSS)
   - `enddatetime`: End date (format: YYYYMMDDHHMMSS)

### 📝 Example API Call
```bash
# Search for wildfire news in California
https://api.gdeltproject.org/api/v2/doc/doc?query=wildfire%20California&mode=artlist&maxrecords=50&format=json&startdatetime=20240101000000&enddatetime=20240131235959
```

### Documentation
- **Main Documentation**: [https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
- **Query Guide**: [https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)

### ⚠️ Troubleshooting Tips
- **No results returned?** Check your query syntax and date range
- **Timeout errors?** Reduce `maxrecords` or narrow your search query
- **Invalid date format?** Use YYYYMMDDHHMMSS format (e.g., 20240101000000)
- **Too many requests?** Implement rate limiting in your code (1 request/second)

---

## 🔧 Environment Configuration

### Step 1: Copy Environment Template

1. **Backend Configuration**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Frontend Configuration** (if applicable)
   ```bash
   cd frontend
   cp .env.example .env
   ```

### Step 2: Fill in Your Credentials

Open `backend/.env` and fill in all the values you collected:

```env
# IBM watsonx.ai Configuration
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_PROJECT_ID=your_project_id_here

# IBM Cloud Object Storage Configuration
COS_API_KEY=your_cos_api_key_here
COS_INSTANCE_CRN=your_instance_crn_here
COS_ENDPOINT=your_cos_endpoint_here
COS_BUCKET_NAME=your_bucket_name_here

# IBM Watson Natural Language Understanding Configuration
NLU_API_KEY=your_nlu_api_key_here
NLU_URL=your_nlu_url_here

# NASA FIRMS API Configuration (Optional)
FIRMS_API_KEY=your_firms_api_key_here

# GDELT API (No key required)
# GDELT is open access - no configuration needed
```

### Step 3: Verify Configuration

1. **Check for Typos**
   - Ensure no extra spaces before or after values
   - Verify all URLs start with `https://`
   - Confirm CRN starts with `crn:v1:bluemix:`

2. **Test Connections** (after starting the application)
   - The application will validate credentials on startup
   - Check logs for any authentication errors

---

## ✅ Final Checklist

Before running the LENS platform, verify you have:

### Required Credentials
- [x] IBM Cloud account created and verified
- [x] watsonx.ai Project ID copied to `.env`
- [x] watsonx.ai API Key copied to `.env`
- [x] Cloud Object Storage Instance CRN copied to `.env`
- [x] Cloud Object Storage API Key copied to `.env`
- [x] Cloud Object Storage Endpoint URL copied to `.env`
- [x] Cloud Object Storage Bucket created and name copied to `.env`
- [x] Watson NLU API Key copied to `.env`
- [x] Watson NLU Service URL copied to `.env`

### Optional Credentials
- [ ] NASA FIRMS API Key copied to `.env` (optional)
- [ ] GDELT API usage understood (no key needed)

### Configuration Files
- [ ] `backend/.env` file created and populated
- [ ] All values verified for typos and formatting
- [ ] No placeholder text remaining in `.env` file

---

## 🆘 Common Issues and Solutions

### Issue: "Invalid API Key" Error

**Solution:**
1. Verify you copied the entire key without spaces
2. Check if the key is for the correct service
3. Regenerate the API key if necessary
4. Ensure your IBM Cloud account is active

### Issue: "Project Not Found" Error

**Solution:**
1. Verify the Project ID is correct
2. Ensure the project exists in watsonx.ai
3. Check if you have access permissions to the project
4. Try creating a new project

### Issue: "Access Denied" to Cloud Object Storage

**Solution:**
1. Verify the Instance CRN is correct
2. Check if the API key has "Writer" or "Manager" role
3. Ensure the bucket exists and name is correct
4. Verify the endpoint URL matches your region

### Issue: "Service Unavailable" Error

**Solution:**
1. Check IBM Cloud status: [https://cloud.ibm.com/status](https://cloud.ibm.com/status)
2. Verify your service instances are active
3. Check if you've exceeded free tier limits
4. Try a different region endpoint

### Issue: Rate Limiting or Quota Exceeded

**Solution:**
1. Check your usage in IBM Cloud dashboard
2. Upgrade to a paid plan if needed
3. Implement caching to reduce API calls
4. Monitor and optimize your API usage

---

## 📚 Additional Resources

### IBM Cloud Documentation
- **IBM Cloud Getting Started**: [https://cloud.ibm.com/docs](https://cloud.ibm.com/docs)
- **watsonx.ai Documentation**: [https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html](https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html)
- **Cloud Object Storage Docs**: [https://cloud.ibm.com/docs/cloud-object-storage](https://cloud.ibm.com/docs/cloud-object-storage)
- **Watson NLU Documentation**: [https://cloud.ibm.com/docs/natural-language-understanding](https://cloud.ibm.com/docs/natural-language-understanding)

### API Documentation
- **NASA FIRMS API**: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)
- **GDELT Documentation**: [https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)

### Support
- **IBM Cloud Support**: [https://cloud.ibm.com/unifiedsupport/supportcenter](https://cloud.ibm.com/unifiedsupport/supportcenter)
- **Community Forums**: [https://community.ibm.com/community/user/cloud/home](https://community.ibm.com/community/user/cloud/home)

---

## 🎉 You're Ready!

Once you've completed all the steps above and filled in your `.env` file, you're ready to run the LENS platform!

### Next Steps
1. Review the main [README.md](../README.md) for installation instructions
2. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment guidelines
3. Explore [DEMO_SCENARIO.md](./DEMO_SCENARIO.md) for usage examples

**Need Help?** If you encounter any issues not covered in this guide, please:
- Check the troubleshooting sections above
- Review IBM Cloud documentation
- Contact support through the appropriate channels

---

*Last Updated: May 2026*
*Version: 1.0*