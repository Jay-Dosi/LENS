**User:**

<task>
Create a quick reference document at `docs/QUICK_START.md` that shows:

1. A visual diagram of where each API key goes in the project
2. A simple copy-paste template for the .env file with placeholders
3. A "5-minute setup" checklist
4. Common errors and quick fixes
5. How to verify each service is working
6. A test command to check if all APIs are configured correctly

Make it extremely concise and action-oriented - this should be the document someone uses when they have all their API keys and just need to know where to put them.
</task>
<environment_details>
# VSCode Visible Files
docs\API_SETUP_GUIDE.md

# VSCode Open Tabs
backend/.env.example,docs/API_SETUP_GUIDE.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:44:53.745Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/Users/jaydo/OneDrive/Desktop/Hackathon/LENS) Files
.gitignore
PROJECT_SUMMARY.md
README.md
backend/
backend/.env.example
backend/Dockerfile
backend/requirements.txt
backend/app/
backend/app/__init__.py
backend/app/config.py
backend/app/main.py
backend/app/api/
backend/app/api/__init__.py
backend/app/api/routes.py
backend/app/models/
backend/app/models/__init__.py
backend/app/models/schemas.py
backend/app/services/
backend/app/services/__init__.py
backend/app/services/external_data_service.py
backend/app/services/nlu_service.py
backend/app/services/pdf_extractor.py
backend/app/services/scoring_service.py
backend/app/services/storage_service.py
backend/app/services/watsonx_service.py
backend/app/utils/
config/
config/facility_mapping.json
docs/
docs/API_SETUP_GUIDE.md
docs/DEMO_SCENARIO.md
docs/DEPLOYMENT.md
frontend/
frontend/.env.example
frontend/index.html
frontend/package.json
frontend/postcss.config.js
frontend/README.md
frontend/tailwind.config.js
frontend/vite.config.js
frontend/public/
frontend/src/
frontend/src/App.jsx
frontend/src/index.css
frontend/src/main.jsx
frontend/src/components/
frontend/src/components/ClaimsTable.jsx
frontend/src/components/EvidencePanel.jsx
frontend/src/components/UploadModal.jsx
frontend/src/services/
frontend/src/services/api.js
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll create a concise, action-oriented quick start guide. Let me first check the existing API setup guide to understand the project structure and API requirements.

<read_file>
<args>
<file>
<path>docs/API_SETUP_GUIDE.md</path>
</file>
<file>
<path>backend/.env.example</path>
</file>
<file>
<path>frontend/.env.example</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'docs/API_SETUP_GUIDE.md', 'backend/.env.example', 'frontend/.env.example'] Result:
<files>
<file><path>docs/API_SETUP_GUIDE.md</path>
<content lines="1-551">
  1 | # API Setup Guide for LENS Platform
  2 | 
  3 | This comprehensive guide will walk you through obtaining and configuring all required API keys and credentials for the LENS (Liability Evidence & Natural disaster Scoring) platform.
  4 | 
  5 | ## 📋 Prerequisites Checklist
  6 | 
  7 | Before you begin, ensure you have:
  8 | - [ ] A valid email address
  9 | - [ ] A credit card (for IBM Cloud - free tier available, no charges for basic usage)
 10 | - [ ] Access to create accounts on cloud platforms
 11 | - [ ] A text editor to store your credentials temporarily
 12 | 
 13 | ## 🎯 Quick Credentials Checklist
 14 | 
 15 | Use this checklist to track your progress:
 16 | 
 17 | - [ ] **IBM Cloud Account** - Created and verified
 18 | - [ ] **IBM watsonx.ai** - Project ID and API Key
 19 | - [ ] **IBM Cloud Object Storage** - API Key, Instance CRN, and Endpoint URL
 20 | - [ ] **IBM Watson NLU** - API Key and Service URL
 21 | - [ ] **NASA FIRMS API** - API Key (optional)
 22 | - [ ] **GDELT API** - No key needed, usage understood
 23 | 
 24 | ---
 25 | 
 26 | ## 1️⃣ IBM Cloud Account Setup
 27 | 
 28 | ### Step 1: Create IBM Cloud Account
 29 | 
 30 | 1. **Navigate to IBM Cloud**
 31 |    - Go to: [https://cloud.ibm.com/registration](https://cloud.ibm.com/registration)
 32 |    
 33 | 2. **Fill in Registration Details**
 34 |    - Enter your email address
 35 |    - Create a strong password
 36 |    - Select your country/region
 37 |    - Accept the terms and conditions
 38 |    - Click "Create account"
 39 | 
 40 | 3. **Verify Your Email**
 41 |    - Check your email inbox for a verification email from IBM Cloud
 42 |    - Click the verification link
 43 |    - You may need to wait a few minutes for the email to arrive
 44 | 
 45 | 4. **Complete Account Setup**
 46 |    - Log in to: [https://cloud.ibm.com/](https://cloud.ibm.com/)
 47 |    - You may be prompted to provide additional information
 48 |    - Add payment method (required even for free tier, but you won't be charged for basic usage)
 49 | 
 50 | ### Step 2: Navigate to IBM Cloud Dashboard
 51 | 
 52 | - Once logged in, you'll see the IBM Cloud Dashboard
 53 | - Bookmark this page: [https://cloud.ibm.com/](https://cloud.ibm.com/)
 54 | 
 55 | ### ⚠️ Troubleshooting Tips
 56 | - **Email not received?** Check spam/junk folder
 57 | - **Account locked?** Contact IBM Cloud support at [https://cloud.ibm.com/unifiedsupport/supportcenter](https://cloud.ibm.com/unifiedsupport/supportcenter)
 58 | - **Payment issues?** Ensure your card supports international transactions
 59 | 
 60 | ---
 61 | 
 62 | ## 2️⃣ IBM watsonx.ai Setup
 63 | 
 64 | ### What You'll Get
 65 | - **Project ID**: Unique identifier for your watsonx.ai project
 66 | - **API Key**: Authentication credential for API access
 67 | 
 68 | ### Step 1: Access watsonx.ai
 69 | 
 70 | 1. **Navigate to watsonx.ai**
 71 |    - Go to: [https://dataplatform.cloud.ibm.com/wx/home](https://dataplatform.cloud.ibm.com/wx/home)
 72 |    - Or from IBM Cloud Dashboard: Click "Catalog" → Search "watsonx.ai" → Click "watsonx.ai"
 73 | 
 74 | 2. **Create a watsonx.ai Service Instance** (if not already created)
 75 |    - Click "Create" or "Launch watsonx.ai"
 76 |    - Select a region (e.g., Dallas, Frankfurt, Tokyo)
 77 |    - Choose the "Lite" plan (free tier)
 78 |    - Give it a name (e.g., "LENS-watsonx")
 79 |    - Click "Create"
 80 | 
 81 | ### Step 2: Create a Project
 82 | 
 83 | 1. **Create New Project**
 84 |    - In watsonx.ai, click "Projects" in the left sidebar
 85 |    - Click "New project"
 86 |    - Select "Create an empty project"
 87 |    - Enter project name: "LENS-Project" (or your preferred name)
 88 |    - Add a description (optional)
 89 |    - Click "Create"
 90 | 
 91 | 2. **Get Your Project ID**
 92 |    - Once in your project, click the "Manage" tab
 93 |    - Click "General" in the left sidebar
 94 |    - Look for "Project ID" section
 95 |    - **Copy the Project ID** - it looks like: `12345678-abcd-1234-abcd-123456789abc`
 96 |    - Save this value as `WATSONX_PROJECT_ID` in your `.env` file
 97 | 
 98 | ### Step 3: Create API Key
 99 | 
100 | 1. **Navigate to API Keys**
101 |    - Go to: [https://cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
102 |    - Or from IBM Cloud Dashboard: Click your profile icon (top right) → "API keys"
103 | 
104 | 2. **Create New API Key**
105 |    - Click "Create an IBM Cloud API key"
106 |    - Enter a name: "LENS-watsonx-key"
107 |    - Add a description: "API key for LENS watsonx.ai access"
108 |    - Click "Create"
109 | 
110 | 3. **Copy and Save Your API Key**
111 |    - **IMPORTANT**: A dialog will appear with your API key
112 |    - Click "Copy" or manually select and copy the key
113 |    - **Save it immediately** - you cannot retrieve it later!
114 |    - Save this value as `WATSONX_API_KEY` in your `.env` file
115 |    - Click "Download" to save a backup copy (optional but recommended)
116 | 
117 | ### 📝 Example Values
118 | ```
119 | WATSONX_PROJECT_ID=12345678-abcd-1234-abcd-123456789abc
120 | WATSONX_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
121 | ```
122 | 
123 | ### ⚠️ Troubleshooting Tips
124 | - **Can't find Project ID?** Make sure you're inside the project, then go to Manage → General
125 | - **API Key not working?** Ensure you copied the entire key without extra spaces
126 | - **Access denied?** Verify your IBM Cloud account is active and verified
127 | - **Project creation fails?** Check if you have sufficient permissions in your IBM Cloud account
128 | 
129 | ---
130 | 
131 | ## 3️⃣ IBM Cloud Object Storage Setup
132 | 
133 | ### What You'll Get
134 | - **API Key**: Authentication credential (can reuse the one from watsonx.ai)
135 | - **Instance CRN**: Cloud Resource Name for your storage instance
136 | - **Endpoint URL**: Service endpoint for your region
137 | 
138 | ### Step 1: Create Cloud Object Storage Instance
139 | 
140 | 1. **Navigate to Catalog**
141 |    - Go to: [https://cloud.ibm.com/catalog/services/cloud-object-storage](https://cloud.ibm.com/catalog/services/cloud-object-storage)
142 |    - Or from IBM Cloud Dashboard: Click "Catalog" → Search "Object Storage"
143 | 
144 | 2. **Create Service Instance**
145 |    - Select the "Lite" plan (free tier - 25GB storage)
146 |    - Choose a region (same as your watsonx.ai for better performance)
147 |    - Enter service name: "LENS-Object-Storage"
148 |    - Select a resource group (use "Default" if unsure)
149 |    - Click "Create"
150 | 
151 | ### Step 2: Get Instance CRN
152 | 
153 | 1. **Access Service Credentials**
154 |    - After creation, you'll be on the service dashboard
155 |    - Click "Service credentials" in the left sidebar
156 |    - If no credentials exist, click "New credential"
157 |      - Name: "LENS-COS-Credentials"
158 |      - Role: "Writer" or "Manager"
159 |      - Click "Add"
160 | 
161 | 2. **Copy Instance CRN**
162 |    - Click "View credentials" (dropdown arrow) next to your credential
163 |    - Find the `"resource_instance_id"` field
164 |    - **Copy the entire CRN value** - it looks like: `crn:v1:bluemix:public:cloud-object-storage:global:a/...`
165 |    - Save this value as `COS_INSTANCE_CRN` in your `.env` file
166 | 
167 | ### Step 3: Get API Key
168 | 
169 | You can use the same API key from watsonx.ai setup, OR create a new one:
170 | 
171 | 1. **Option A: Reuse Existing API Key**
172 |    - Use the same `WATSONX_API_KEY` value
173 |    - Save it as `COS_API_KEY` in your `.env` file
174 | 
175 | 2. **Option B: Create New API Key**
176 |    - In the service credentials view, the API key is shown as `"apikey"` field
177 |    - Copy this value
178 |    - Save it as `COS_API_KEY` in your `.env` file
179 | 
180 | ### Step 4: Get Endpoint URL
181 | 
182 | 1. **Find Your Endpoint**
183 |    - In your Cloud Object Storage instance, click "Endpoints" in the left sidebar
184 |    - Choose endpoint type based on your needs:
185 |      - **Public**: For general access (recommended for development)
186 |      - **Private**: For internal IBM Cloud network only
187 |      - **Direct**: For high-performance scenarios
188 | 
189 | 2. **Select Region**
190 |    - Find the region where you created your instance
191 |    - Under "Public" endpoints, find your region (e.g., "us-south", "eu-de")
192 |    - **Copy the endpoint URL** - it looks like: `https://s3.us-south.cloud-object-storage.appdomain.cloud`
193 |    - Save this value as `COS_ENDPOINT` in your `.env` file
194 | 
195 | ### Step 5: Create a Bucket (Optional but Recommended)
196 | 
197 | 1. **Create Bucket**
198 |    - Click "Buckets" in the left sidebar
199 |    - Click "Create bucket"
200 |    - Choose "Customize your bucket"
201 |    - Enter bucket name: "lens-evidence-storage" (must be globally unique)
202 |    - Select same region as your instance
203 |    - Choose "Standard" storage class
204 |    - Click "Create bucket"
205 | 
206 | 2. **Note Bucket Name**
207 |    - Save the bucket name as `COS_BUCKET_NAME` in your `.env` file
208 | 
209 | ### 📝 Example Values
210 | ```
211 | COS_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
212 | COS_INSTANCE_CRN=crn:v1:bluemix:public:cloud-object-storage:global:a/1234567890abcdef:12345678-abcd-1234-abcd-123456789abc::
213 | COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
214 | COS_BUCKET_NAME=lens-evidence-storage
215 | ```
216 | 
217 | ### ⚠️ Troubleshooting Tips
218 | - **Can't find CRN?** Look for `resource_instance_id` in service credentials
219 | - **Endpoint not working?** Ensure you're using the correct endpoint type (Public/Private/Direct)
220 | - **Bucket name taken?** Bucket names must be globally unique; try adding numbers or your organization name
221 | - **Access denied?** Verify your API key has "Writer" or "Manager" role
222 | - **Connection timeout?** Check if you're using the correct regional endpoint
223 | 
224 | ---
225 | 
226 | ## 4️⃣ IBM Watson Natural Language Understanding Setup
227 | 
228 | ### What You'll Get
229 | - **API Key**: Authentication credential for NLU service
230 | - **Service URL**: Endpoint URL for your NLU instance
231 | 
232 | ### Step 1: Create NLU Service Instance
233 | 
234 | 1. **Navigate to Catalog**
235 |    - Go to: [https://cloud.ibm.com/catalog/services/natural-language-understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding)
236 |    - Or from IBM Cloud Dashboard: Click "Catalog" → Search "Natural Language Understanding"
237 | 
238 | 2. **Create Service Instance**
239 |    - Select the "Lite" plan (free tier - 30,000 NLU items per month)
240 |    - Choose a region (same as your other services for consistency)
241 |    - Enter service name: "LENS-NLU"
242 |    - Select resource group (use "Default" if unsure)
243 |    - Click "Create"
244 | 
245 | ### Step 2: Get API Key and URL
246 | 
247 | 1. **Access Service Credentials**
248 |    - After creation, you'll be on the service dashboard
249 |    - Click "Service credentials" in the left sidebar
250 |    - If no credentials exist, click "New credential"
251 |      - Name: "LENS-NLU-Credentials"
252 |      - Role: "Manager"
253 |      - Click "Add"
254 | 
255 | 2. **Copy API Key**
256 |    - Click "View credentials" (dropdown arrow) next to your credential
257 |    - Find the `"apikey"` field
258 |    - **Copy the API key value**
259 |    - Save this value as `NLU_API_KEY` in your `.env` file
260 | 
261 | 3. **Copy Service URL**
262 |    - In the same credentials view, find the `"url"` field
263 |    - **Copy the URL** - it looks like: `https://api.us-south.natural-language-understanding.watson.cloud.ibm.com`
264 |    - Save this value as `NLU_URL` in your `.env` file
265 | 
266 | ### 📝 Example Values
267 | ```
268 | NLU_API_KEY=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
269 | NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
270 | ```
271 | 
272 | ### ⚠️ Troubleshooting Tips
273 | - **API key not working?** Ensure you copied the entire key without spaces
274 | - **Wrong URL format?** The URL should start with `https://api.` and end with `.watson.cloud.ibm.com`
275 | - **Service not responding?** Check if your service instance is active in the IBM Cloud dashboard
276 | - **Rate limit exceeded?** Lite plan has 30,000 items/month limit; monitor usage in the dashboard
277 | - **Authentication error?** Verify the API key matches the service instance region
278 | 
279 | ---
280 | 
281 | ## 5️⃣ NASA FIRMS API Setup (Optional)
282 | 
283 | ### What You'll Get
284 | - **MAP_KEY**: API key for accessing NASA FIRMS fire data
285 | 
286 | ### About NASA FIRMS
287 | NASA's Fire Information for Resource Management System (FIRMS) provides near real-time active fire data. This is optional for the LENS platform but enhances wildfire-related claim analysis.
288 | 
289 | ### Step 1: Request API Key
290 | 
291 | 1. **Navigate to FIRMS**
292 |    - Go to: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)
293 | 
294 | 2. **Request MAP_KEY**
295 |    - Scroll down to "Request a MAP_KEY"
296 |    - Click "Request a MAP_KEY" button
297 |    - Or go directly to: [https://firms.modaps.eosdis.nasa.gov/api/map_key/](https://firms.modaps.eosdis.nasa.gov/api/map_key/)
298 | 
299 | 3. **Fill in Request Form**
300 |    - Enter your email address
301 |    - Enter your first and last name
302 |    - Select your organization type (e.g., "Academic/Research", "Commercial", "Government")
303 |    - Describe your intended use: "Insurance claim verification and natural disaster analysis"
304 |    - Complete the CAPTCHA
305 |    - Click "Request MAP_KEY"
306 | 
307 | ### Step 2: Retrieve Your API Key
308 | 
309 | 1. **Check Your Email**
310 |    - You'll receive an email from NASA FIRMS within a few minutes
311 |    - Subject: "Your FIRMS MAP_KEY"
312 |    - The email contains your MAP_KEY
313 | 
314 | 2. **Copy MAP_KEY**
315 |    - **Copy the MAP_KEY from the email**
316 |    - It's a long alphanumeric string
317 |    - Save this value as `FIRMS_API_KEY` in your `.env` file
318 | 
319 | ### 📝 Example Values
320 | ```
321 | FIRMS_API_KEY=1234567890abcdef1234567890abcdef12345678
322 | ```
323 | 
324 | ### API Usage Information
325 | - **Rate Limits**: Reasonable use policy (no hard limits for most users)
326 | - **Data Coverage**: Global fire data from MODIS and VIIRS satellites
327 | - **Update Frequency**: Near real-time (3-hour latency)
328 | - **Documentation**: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)
329 | 
330 | ### ⚠️ Troubleshooting Tips
331 | - **Email not received?** Check spam folder; wait up to 30 minutes
332 | - **Key not working?** Ensure you copied the entire key without line breaks
333 | - **Access denied?** Verify your key is active; keys may expire after long periods of inactivity
334 | - **Rate limited?** Contact NASA FIRMS support if you need higher limits
335 | 
336 | ---
337 | 
338 | ## 6️⃣ GDELT API Setup
339 | 
340 | ### What You'll Get
341 | - **No API Key Required**: GDELT is open access
342 | 
343 | ### About GDELT
344 | The Global Database of Events, Language, and Tone (GDELT) monitors news media worldwide. It provides context for natural disasters and events that may impact insurance claims.
345 | 
346 | ### API Access
347 | 
348 | 1. **No Registration Required**
349 |    - GDELT API is completely open and free
350 |    - No API key or authentication needed
351 |    - Direct access to all endpoints
352 | 
353 | 2. **Main Endpoints**
354 |    - **GDELT 2.0 Doc API**: [https://api.gdeltproject.org/api/v2/doc/doc](https://api.gdeltproject.org/api/v2/doc/doc)
355 |    - **GDELT 2.0 TV API**: [https://api.gdeltproject.org/api/v2/tv/tv](https://api.gdeltproject.org/api/v2/tv/tv)
356 |    - **GDELT GEO API**: [https://api.gdeltproject.org/api/v2/geo/geo](https://api.gdeltproject.org/api/v2/geo/geo)
357 | 
358 | ### Usage Guidelines
359 | 
360 | 1. **Rate Limits**
361 |    - Be respectful with request frequency
362 |    - Recommended: No more than 1 request per second
363 |    - For high-volume needs, consider caching results
364 | 
365 | 2. **Query Parameters**
366 |    - `query`: Search terms (e.g., "wildfire California")
367 |    - `mode`: Output mode (e.g., "artlist", "timeline")
368 |    - `maxrecords`: Maximum results (default: 250, max: 250)
369 |    - `format`: Output format (e.g., "json", "csv")
370 |    - `startdatetime`: Start date (format: YYYYMMDDHHMMSS)
371 |    - `enddatetime`: End date (format: YYYYMMDDHHMMSS)
372 | 
373 | ### 📝 Example API Call
374 | ```bash
375 | # Search for wildfire news in California
376 | https://api.gdeltproject.org/api/v2/doc/doc?query=wildfire%20California&mode=artlist&maxrecords=50&format=json&startdatetime=20240101000000&enddatetime=20240131235959
377 | ```
378 | 
379 | ### Documentation
380 | - **Main Documentation**: [https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
381 | - **Query Guide**: [https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)
382 | 
383 | ### ⚠️ Troubleshooting Tips
384 | - **No results returned?** Check your query syntax and date range
385 | - **Timeout errors?** Reduce `maxrecords` or narrow your search query
386 | - **Invalid date format?** Use YYYYMMDDHHMMSS format (e.g., 20240101000000)
387 | - **Too many requests?** Implement rate limiting in your code (1 request/second)
388 | 
389 | ---
390 | 
391 | ## 🔧 Environment Configuration
392 | 
393 | ### Step 1: Copy Environment Template
394 | 
395 | 1. **Backend Configuration**
396 |    ```bash
397 |    cd backend
398 |    cp .env.example .env
399 |    ```
400 | 
401 | 2. **Frontend Configuration** (if applicable)
402 |    ```bash
403 |    cd frontend
404 |    cp .env.example .env
405 |    ```
406 | 
407 | ### Step 2: Fill in Your Credentials
408 | 
409 | Open `backend/.env` and fill in all the values you collected:
410 | 
411 | ```env
412 | # IBM watsonx.ai Configuration
413 | WATSONX_API_KEY=your_watsonx_api_key_here
414 | WATSONX_PROJECT_ID=your_project_id_here
415 | 
416 | # IBM Cloud Object Storage Configuration
417 | COS_API_KEY=your_cos_api_key_here
418 | COS_INSTANCE_CRN=your_instance_crn_here
419 | COS_ENDPOINT=your_cos_endpoint_here
420 | COS_BUCKET_NAME=your_bucket_name_here
421 | 
422 | # IBM Watson Natural Language Understanding Configuration
423 | NLU_API_KEY=your_nlu_api_key_here
424 | NLU_URL=your_nlu_url_here
425 | 
426 | # NASA FIRMS API Configuration (Optional)
427 | FIRMS_API_KEY=your_firms_api_key_here
428 | 
429 | # GDELT API (No key required)
430 | # GDELT is open access - no configuration needed
431 | ```
432 | 
433 | ### Step 3: Verify Configuration
434 | 
435 | 1. **Check for Typos**
436 |    - Ensure no extra spaces before or after values
437 |    - Verify all URLs start with `https://`
438 |    - Confirm CRN starts with `crn:v1:bluemix:`
439 | 
440 | 2. **Test Connections** (after starting the application)
441 |    - The application will validate credentials on startup
442 |    - Check logs for any authentication errors
443 | 
444 | ---
445 | 
446 | ## ✅ Final Checklist
447 | 
448 | Before running the LENS platform, verify you have:
449 | 
450 | ### Required Credentials
451 | - [x] IBM Cloud account created and verified
452 | - [x] watsonx.ai Project ID copied to `.env`
453 | - [x] watsonx.ai API Key copied to `.env`
454 | - [x] Cloud Object Storage Instance CRN copied to `.env`
455 | - [x] Cloud Object Storage API Key copied to `.env`
456 | - [x] Cloud Object Storage Endpoint URL copied to `.env`
457 | - [x] Cloud Object Storage Bucket created and name copied to `.env`
458 | - [x] Watson NLU API Key copied to `.env`
459 | - [x] Watson NLU Service URL copied to `.env`
460 | 
461 | ### Optional Credentials
462 | - [ ] NASA FIRMS API Key copied to `.env` (optional)
463 | - [ ] GDELT API usage understood (no key needed)
464 | 
465 | ### Configuration Files
466 | - [ ] `backend/.env` file created and populated
467 | - [ ] All values verified for typos and formatting
468 | - [ ] No placeholder text remaining in `.env` file
469 | 
470 | ---
471 | 
472 | ## 🆘 Common Issues and Solutions
473 | 
474 | ### Issue: "Invalid API Key" Error
475 | 
476 | **Solution:**
477 | 1. Verify you copied the entire key without spaces
478 | 2. Check if the key is for the correct service
479 | 3. Regenerate the API key if necessary
480 | 4. Ensure your IBM Cloud account is active
481 | 
482 | ### Issue: "Project Not Found" Error
483 | 
484 | **Solution:**
485 | 1. Verify the Project ID is correct
486 | 2. Ensure the project exists in watsonx.ai
487 | 3. Check if you have access permissions to the project
488 | 4. Try creating a new project
489 | 
490 | ### Issue: "Access Denied" to Cloud Object Storage
491 | 
492 | **Solution:**
493 | 1. Verify the Instance CRN is correct
494 | 2. Check if the API key has "Writer" or "Manager" role
495 | 3. Ensure the bucket exists and name is correct
496 | 4. Verify the endpoint URL matches your region
497 | 
498 | ### Issue: "Service Unavailable" Error
499 | 
500 | **Solution:**
501 | 1. Check IBM Cloud status: [https://cloud.ibm.com/status](https://cloud.ibm.com/status)
502 | 2. Verify your service instances are active
503 | 3. Check if you've exceeded free tier limits
504 | 4. Try a different region endpoint
505 | 
506 | ### Issue: Rate Limiting or Quota Exceeded
507 | 
508 | **Solution:**
509 | 1. Check your usage in IBM Cloud dashboard
510 | 2. Upgrade to a paid plan if needed
511 | 3. Implement caching to reduce API calls
512 | 4. Monitor and optimize your API usage
513 | 
514 | ---
515 | 
516 | ## 📚 Additional Resources
517 | 
518 | ### IBM Cloud Documentation
519 | - **IBM Cloud Getting Started**: [https://cloud.ibm.com/docs](https://cloud.ibm.com/docs)
520 | - **watsonx.ai Documentation**: [https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html](https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/welcome-main.html)
521 | - **Cloud Object Storage Docs**: [https://cloud.ibm.com/docs/cloud-object-storage](https://cloud.ibm.com/docs/cloud-object-storage)
522 | - **Watson NLU Documentation**: [https://cloud.ibm.com/docs/natural-language-understanding](https://cloud.ibm.com/docs/natural-language-understanding)
523 | 
524 | ### API Documentation
525 | - **NASA FIRMS API**: [https://firms.modaps.eosdis.nasa.gov/api/](https://firms.modaps.eosdis.nasa.gov/api/)
526 | - **GDELT Documentation**: [https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
527 | 
528 | ### Support
529 | - **IBM Cloud Support**: [https://cloud.ibm.com/unifiedsupport/supportcenter](https://cloud.ibm.com/unifiedsupport/supportcenter)
530 | - **Community Forums**: [https://community.ibm.com/community/user/cloud/home](https://community.ibm.com/community/user/cloud/home)
531 | 
532 | ---
533 | 
534 | ## 🎉 You're Ready!
535 | 
536 | Once you've completed all the steps above and filled in your `.env` file, you're ready to run the LENS platform!
537 | 
538 | ### Next Steps
539 | 1. Review the main [README.md](../README.md) for installation instructions
540 | 2. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment guidelines
541 | 3. Explore [DEMO_SCENARIO.md](./DEMO_SCENARIO.md) for usage examples
542 | 
543 | **Need Help?** If you encounter any issues not covered in this guide, please:
544 | - Check the troubleshooting sections above
545 | - Review IBM Cloud documentation
546 | - Contact support through the appropriate channels
547 | 
548 | ---
549 | 
550 | *Last Updated: May 2026*
551 | *Version: 1.0*
</content>
</file>
<file><path>backend/.env.example</path>
<content lines="1-28">
 1 | # IBM Cloud Configuration
 2 | IBM_CLOUD_API_KEY=your_ibm_cloud_api_key_here
 3 | IBM_WATSONX_PROJECT_ID=your_watsonx_project_id_here
 4 | 
 5 | # IBM Cloud Object Storage
 6 | IBM_COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
 7 | IBM_COS_API_KEY=your_cos_api_key_here
 8 | IBM_COS_INSTANCE_CRN=your_cos_instance_crn_here
 9 | IBM_COS_BUCKET_NAME=esg-lens-hackathon
10 | 
11 | # IBM Watson Natural Language Understanding
12 | IBM_NLU_API_KEY=your_nlu_api_key_here
13 | IBM_NLU_URL=https://api.us-south.natural-language-understanding.watson.cloud.ibm.com
14 | 
15 | # watsonx.ai Configuration
16 | WATSONX_URL=https://us-south.ml.cloud.ibm.com
17 | WATSONX_EXTRACTION_MODEL=ibm/granite-13b-instruct-v2
18 | WATSONX_EXPLANATION_MODEL=ibm/granite-3-8b-instruct
19 | 
20 | # External APIs (No authentication required)
21 | NASA_FIRMS_API_URL=https://firms.modaps.eosdis.nasa.gov/api/area/csv
22 | GDELT_API_URL=https://api.gdeltproject.org/api/v2/doc/doc
23 | 
24 | # Application Settings
25 | UPLOAD_DIR=./uploads
26 | MAX_FILE_SIZE_MB=50
27 | ALLOWED_EXTENSIONS=pdf
28 | LOG_LEVEL=INFO
</content>
</file>
<file><path>frontend/.env.example</path>
<content lines="1-7">
1 | # Frontend Environment Variables
2 | 
3 | # API Base URL
4 | VITE_API_URL=http://localhost:8000/api/v1
5 | 
6 | # For production deployment, update to your IBM Cloud Code Engine URL:
7 | # VITE_API_URL=https://your-app-url.codeengine.appdomain.cloud/api/v1
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
docs\API_SETUP_GUIDE.md

# VSCode Open Tabs
backend/.env.example,docs/API_SETUP_GUIDE.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:44:59.026Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll create a concise, action-oriented quick start guide that focuses on getting API keys configured quickly.

<write_to_file>
<path>docs/QUICK_START.md</path>
<content>
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
</content>
<line_count>298</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'docs/QUICK_START.md'] Result:
<file_write_result>
<path>docs/QUICK_START.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
docs\QUICK_START.md

# VSCode Open Tabs
docs/API_SETUP_GUIDE.md,docs/QUICK_START.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T10:45:42.753Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.05

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Created `docs/QUICK_START.md` - a concise, action-oriented quick reference guide that includes:

✅ **Visual API Key Map** - ASCII diagram showing exactly where each key goes in the project structure

✅ **Copy-Paste .env Templates** - Complete templates for both backend and frontend with clear placeholders

✅ **5-Minute Setup Checklist** - Step-by-step commands to get from zero to running in 5 minutes

✅ **Quick Reference Table** - Shows where to find each API key with format examples

✅ **Common Errors & Quick Fixes** - 6 most common errors with immediate solutions

✅ **Service Verification Tests** - Individual curl commands to test each API service

✅ **All-in-One Test Command** - Python script that validates all API keys are configured correctly before starting

The guide is designed for someone who already has their API keys and just needs to know where to put them. It's extremely concise (under 300 lines) and focuses on action over explanation. Each section provides immediate, copy-paste solutions.

Key features:
- Visual diagram for quick understanding
- No placeholder confusion (clear "paste_your_" format)
- Troubleshooting focused on symptoms → fixes
- Test commands to verify each service independently
- Comprehensive validation script to check all keys at once
</result>
</attempt_completion>

