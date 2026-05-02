# OpenWeatherMap Air Pollution API Setup Guide

## Quick Start

### 1. Get Your Free API Key

1. **Sign up for OpenWeatherMap**
   - Visit: https://home.openweathermap.org/users/sign_up
   - Create a free account (no credit card required)
   - Verify your email address

2. **Get Your API Key**
   - Log in to your OpenWeatherMap account
   - Navigate to: https://home.openweathermap.org/api_keys
   - Copy your default API key (or create a new one)
   - **Note**: New API keys may take 10-15 minutes to activate

3. **Add to Your Environment**
   - Open `backend/.env`
   - Add your API key:
     ```bash
     OPENWEATHERMAP_API_KEY=your_actual_api_key_here
     ```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Test the Integration

```bash
cd backend
python test_openweathermap.py
```

Expected output:
```
================================================================================
Testing OpenWeatherMap Air Pollution API Integration
================================================================================

📍 Test Location: Houston, TX (29.7604, -95.3698)
--------------------------------------------------------------------------------
✅ OpenWeatherMap API key found - will use real API

🔍 Querying OpenWeatherMap Air Pollution API...
--------------------------------------------------------------------------------

✅ Query successful!
Source: OPENWEATHERMAP
Current AQI: 3 - Moderate
Average AQI: 2.85
High Pollution Days (90d): 12

🌫️  Air Quality Components (μg/m³):
  • CO (Carbon Monoxide): 456.78
  • NO₂ (Nitrogen Dioxide): 23.45
  • O₃ (Ozone): 67.89
  • SO₂ (Sulphur Dioxide): 12.34
  • PM2.5 (Fine Particles): 18.90
  • PM10 (Coarse Particles): 34.56

================================================================================
✅ OpenWeatherMap integration test PASSED
================================================================================
```

## API Details

### Free Tier Limits
- **Calls per day**: 1,000
- **Calls per minute**: 60
- **Cost**: $0 (completely free)
- **No credit card required**

### What We Query
1. **Current Air Pollution**: Real-time air quality at facility location
2. **Historical Data**: Past 90 days of air quality measurements

### Data Provided
- **AQI (Air Quality Index)**: 1-5 scale
  - 1 = Good
  - 2 = Fair
  - 3 = Moderate
  - 4 = Poor
  - 5 = Very Poor

- **Pollutant Concentrations** (μg/m³):
  - CO (Carbon Monoxide)
  - NO₂ (Nitrogen Dioxide)
  - O₃ (Ozone)
  - SO₂ (Sulphur Dioxide)
  - PM2.5 (Fine Particles)
  - PM10 (Coarse Particles)

## Demo Mode

If you don't configure an API key, the system automatically uses **demo mode**:
- ✅ Application works without API key
- ✅ Generates realistic air quality data
- ✅ Perfect for testing and demonstrations
- ⚠️ Shows "Demo data" indicator in results

## Integration with ESG Verification

### How It Works

1. **Claim Extraction**: System extracts facility location from ESG report
2. **Parallel Queries**: Simultaneously queries:
   - OpenWeatherMap Air Pollution API (air quality data)
   - Google News RSS (news articles)
3. **Evidence Generation**: Creates evidence records based on:
   - Current AQI level
   - Historical pollution trends
   - Pollutant concentrations
4. **Scoring**: Contributes to overall claim credibility score

### Evidence Types

**Poor Air Quality** (AQI 4-5):
```
Signal Type: poor_air_quality
Signal Text: "Current air quality: Poor (AQI: 4/5). 15 high pollution days in past 90 days"
Signal Strength: 0.75 (high concern)
```

**Moderate Air Quality** (AQI 3):
```
Signal Type: moderate_air_quality
Signal Text: "Current air quality: Moderate (AQI: 3/5). 8 high pollution days in past 90 days"
Signal Strength: 0.50 (medium concern)
```

**Good Air Quality** (AQI 1-2):
```
Signal Type: good_air_quality
Signal Text: "Current air quality: Good (AQI: 2/5)"
Signal Strength: 0.00 (no concern)
```

## Troubleshooting

### "Invalid API key" Error
**Cause**: API key is incorrect or not activated yet

**Solution**:
1. Verify the API key in your `.env` file
2. Wait 10-15 minutes after creating the key
3. Check key status at: https://home.openweathermap.org/api_keys
4. Ensure no extra spaces or quotes around the key

### "Rate limit exceeded" Error
**Cause**: Too many API calls in a short time

**Solution**:
- Free tier allows 60 calls/minute
- Application implements 2-second delays
- Wait 1 minute and try again
- Consider upgrading if you need more calls

### No Data Returned
**Cause**: Network issues or API unavailable

**Solution**:
1. Check your internet connection
2. Verify API endpoint is accessible
3. Review logs for detailed error messages
4. System will automatically fall back to demo mode

### Module Import Errors
**Cause**: Dependencies not installed

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

## API Endpoints Used

### Current Air Pollution
```
GET http://api.openweathermap.org/data/2.5/air_pollution
Parameters:
  - lat: Facility latitude
  - lon: Facility longitude
  - appid: Your API key
```

### Historical Air Pollution
```
GET http://api.openweathermap.org/data/2.5/air_pollution/history
Parameters:
  - lat: Facility latitude
  - lon: Facility longitude
  - start: Unix timestamp (90 days ago)
  - end: Unix timestamp (now)
  - appid: Your API key
```

## Production Deployment

### Environment Variables
Ensure these are set in your production environment:
```bash
OPENWEATHERMAP_API_KEY=your_production_api_key
```

### Rate Limiting
The application implements:
- ✅ 2-second delay between requests
- ✅ 3 retry attempts with exponential backoff
- ✅ Graceful fallback to demo mode on failure

### Monitoring
Monitor your API usage at:
- https://home.openweathermap.org/statistics

### Scaling
If you need more than 1,000 calls/day:
1. Visit: https://openweathermap.org/price
2. Upgrade to a paid plan (starts at $40/month for 100,000 calls)
3. Update your API key in `.env`

## Comparison with NASA FIRMS

| Feature | NASA FIRMS | OpenWeatherMap |
|---------|-----------|----------------|
| **Data Type** | Thermal anomalies | Air quality |
| **API Key** | Required (registration) | Free tier available |
| **Free Tier** | Limited | 1,000 calls/day |
| **Real-time** | 3-24 hour delay | Real-time |
| **Historical** | Yes | 90 days |
| **ESG Relevance** | Indirect (fires) | Direct (pollution) |
| **Pollutants** | None | CO, NO₂, O₃, SO₂, PM2.5, PM10 |

## Resources

- **API Documentation**: https://openweathermap.org/api/air-pollution
- **Sign Up**: https://home.openweathermap.org/users/sign_up
- **API Keys**: https://home.openweathermap.org/api_keys
- **Pricing**: https://openweathermap.org/price
- **Support**: https://openweathermap.org/faq

## Next Steps

1. ✅ Get your free API key
2. ✅ Add it to `backend/.env`
3. ✅ Run `python test_openweathermap.py`
4. ✅ Start verifying ESG claims with real air quality data!

---

**Last Updated**: May 2026  
**Status**: Production Ready ✅