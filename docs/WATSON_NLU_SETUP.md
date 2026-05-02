# IBM Watson NLU Setup Guide

## Overview

This application now uses **IBM Watson Natural Language Understanding (NLU)** for entity extraction. Watson NLU is a cloud-based service that provides advanced natural language processing capabilities.

---

## 🎯 What Watson NLU Does

Watson NLU extracts:
- **Organizations**: Companies, agencies, institutions
- **Locations**: Cities, countries, geographic features
- **Facilities**: Buildings, plants, factories
- **Keywords**: Important terms and concepts
- **Entities**: People, dates, quantities, and more

---

## 📋 Prerequisites

1. **IBM Cloud Account** (Free tier available)
2. **Watson NLU Service Instance**
3. **API Key**

---

## 🚀 Step-by-Step Setup

### Step 1: Create IBM Cloud Account

1. Go to [IBM Cloud](https://cloud.ibm.com/registration)
2. Sign up for a free account
3. Verify your email address

### Step 2: Create Watson NLU Service

1. Log in to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **"Create resource"** (top right)
3. Search for **"Natural Language Understanding"**
4. Select the **Watson Natural Language Understanding** service
5. Choose your plan:
   - **Lite Plan** (FREE): 30,000 NLU items/month
   - **Standard Plan**: Pay-as-you-go pricing
6. Select a region (e.g., **Dallas** or **London**)
7. Click **"Create"**

### Step 3: Get Your API Key

1. After creating the service, you'll be redirected to the service page
2. Click on **"Service credentials"** in the left sidebar
3. Click **"New credential"** if no credentials exist
4. Click **"View credentials"** to see your API key
5. Copy the following values:
   - **apikey**: Your Watson NLU API key
   - **url**: Your service endpoint URL

Example credentials:
```json
{
  "apikey": "your-watson-nlu-api-key-here",
  "url": "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/xxxxx"
}
```

### Step 4: Configure Your Application

1. Open `backend/.env` file
2. Add your Watson NLU credentials:

```bash
# IBM Watson NLU Configuration
WATSON_NLU_API_KEY=your-watson-nlu-api-key-here
WATSON_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
```

**Important**: Replace the URL with your actual service URL from Step 3.

### Step 5: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `ibm-watson==8.0.0` - Watson SDK
- All other required dependencies

### Step 6: Test the Setup

Run this test to verify Watson NLU is working:

```bash
cd backend
python -c "
from app.services.nlu_service import get_nlu_service
nlu = get_nlu_service()
result = nlu.extract_entities('Apple Inc. is located in Cupertino, California.')
print('✓ Watson NLU is working!')
print(f'Organizations: {result[\"organizations\"]}')
print(f'Locations: {result[\"locations\"]}')
"
```

Expected output:
```
✓ Watson NLU is working!
Organizations: ['Apple Inc.']
Locations: ['Cupertino', 'California']
```

---

## 💰 Pricing

### Lite Plan (FREE)
- **30,000 NLU items per month**
- 1 NLU item = 1 text unit analyzed
- Perfect for development and testing
- No credit card required

### Standard Plan
- **$0.003 per NLU item** (first 250,000 items)
- Volume discounts available
- Pay only for what you use

**Example Usage**:
- Analyzing 100 ESG reports/month with 50 claims each = ~5,000 items
- Cost: **$15/month** (well within free tier)

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WATSON_NLU_API_KEY` | Yes | - | Your Watson NLU API key |
| `WATSON_NLU_URL` | Yes | - | Your service endpoint URL |

### Service Regions

Watson NLU is available in multiple regions:

| Region | URL |
|--------|-----|
| Dallas | `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com` |
| Washington DC | `https://api.us-east.natural-language-understanding.watson.cloud.ibm.com` |
| Frankfurt | `https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com` |
| London | `https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com` |
| Tokyo | `https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com` |
| Sydney | `https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com` |

Choose the region closest to your users for best performance.

---

## 🎯 Features Used

Our application uses these Watson NLU features:

### 1. Entity Extraction
Identifies and categorizes entities in text:
- Organizations (companies, agencies)
- Locations (cities, countries)
- Facilities (buildings, plants)
- People, dates, quantities

### 2. Keyword Extraction
Extracts important keywords and phrases from text.

### 3. Language Support
- Primary: English (`en`)
- Watson NLU supports 13+ languages

---

## 🔍 How It Works

### Entity Extraction Flow

```
1. User uploads ESG report (PDF)
   ↓
2. PDF text is extracted
   ↓
3. Text is sent to Watson NLU API
   ↓
4. Watson NLU analyzes and returns entities
   ↓
5. Entities are categorized and stored
   ↓
6. Used for claim verification and scoring
```

### API Call Example

```python
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

# Analyze text
response = nlu.analyze(
    text="Tesla operates a Gigafactory in Austin, Texas.",
    features=Features(
        entities=EntitiesOptions(limit=50)
    ),
    language='en'
).get_result()

# Results:
# Entities: [
#   {"text": "Tesla", "type": "Organization"},
#   {"text": "Gigafactory", "type": "Facility"},
#   {"text": "Austin", "type": "Location"},
#   {"text": "Texas", "type": "Location"}
# ]
```

---

## 🐛 Troubleshooting

### Error: "Unauthorized" or "Invalid API Key"

**Solution**:
1. Verify your API key is correct in `.env`
2. Check that you copied the entire key (no spaces)
3. Ensure the service is active in IBM Cloud Console

### Error: "Service URL not found"

**Solution**:
1. Verify the `WATSON_NLU_URL` in `.env`
2. Make sure it matches your service credentials
3. Include the full URL with `/instances/xxxxx` if provided

### Error: "Rate limit exceeded"

**Solution**:
1. You've exceeded the free tier limit (30,000 items/month)
2. Wait until next month or upgrade to Standard plan
3. Optimize your code to reduce API calls

### Error: "Import 'ibm_watson' could not be resolved"

**Solution**:
```bash
pip install ibm-watson==8.0.0
```

---

## 📊 Monitoring Usage

### Check Your Usage

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Navigate to **Resource list**
3. Click on your Watson NLU service
4. View **Usage** tab to see:
   - Items used this month
   - Remaining free tier items
   - Cost (if on paid plan)

### Best Practices

1. **Cache Results**: Store entity extraction results to avoid re-analyzing
2. **Batch Processing**: Analyze multiple claims together when possible
3. **Text Limits**: Watson NLU has a 50KB text limit per request
4. **Error Handling**: Always handle API errors gracefully

---

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for credentials
3. **Rotate API keys** regularly
4. **Use IAM policies** to restrict access
5. **Monitor usage** for unusual activity

---

## 📚 Additional Resources

- [Watson NLU Documentation](https://cloud.ibm.com/docs/natural-language-understanding)
- [Watson NLU API Reference](https://cloud.ibm.com/apidocs/natural-language-understanding)
- [Python SDK Documentation](https://github.com/watson-developer-cloud/python-sdk)
- [IBM Cloud Support](https://cloud.ibm.com/unifiedsupport/supportcenter)

---

## 🆘 Getting Help

### IBM Cloud Support
- Free tier: Community support
- Paid plans: Ticket-based support
- [Support Center](https://cloud.ibm.com/unifiedsupport/supportcenter)

### Community Resources
- [IBM Developer Community](https://community.ibm.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/ibm-watson)
- [GitHub Issues](https://github.com/watson-developer-cloud/python-sdk/issues)

---

## ✅ Checklist

Before running the application:

- [ ] IBM Cloud account created
- [ ] Watson NLU service instance created
- [ ] API key obtained
- [ ] Service URL copied
- [ ] `.env` file configured with credentials
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test script run successfully
- [ ] Usage monitoring set up

---

## 🎉 You're Ready!

Your application is now configured to use IBM Watson NLU for entity extraction. Start the backend server and begin analyzing ESG reports!

```bash
cd backend
uvicorn app.main:app --reload
```

---

*Made with Bob*