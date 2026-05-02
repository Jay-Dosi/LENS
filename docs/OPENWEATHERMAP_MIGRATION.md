# Migration from NASA FIRMS to OpenWeatherMap Air Pollution API

## Overview

This document describes the migration from NASA FIRMS (Fire Information for Resource Management System) to OpenWeatherMap Air Pollution API for environmental monitoring in the ESG Claim Verification Assistant.

## Why the Change?

### NASA FIRMS Limitations
- **Requires API key**: Not freely available without registration
- **Limited scope**: Only detects thermal anomalies (fires, flares)
- **Delayed data**: Satellite data can be 3-24 hours old
- **Geographic limitations**: May miss pollution events without thermal signatures

### OpenWeatherMap Advantages
- **Free tier available**: 1,000 API calls/day (more than sufficient)
- **Comprehensive data**: Measures actual air quality (AQI, CO, NO₂, O₃, SO₂, PM2.5, PM10)
- **Real-time data**: Current air quality measurements
- **Historical data**: Access to past 90 days of air quality data
- **Better for ESG**: Direct measurement of air pollution vs. indirect thermal detection

## What Changed?

### 1. API Endpoint
**Before (NASA FIRMS):**
```
https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/VIIRS_SNPP_NRT/{lat},{lon}/{radius}/{start_date}/{end_date}
```

**After (OpenWeatherMap):**
```
Current: http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}
Historical: http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}
```

### 2. Data Structure

**Before (NASA FIRMS):**
- Thermal anomaly detections
- Brightness temperature
- Confidence levels (high/nominal/low)
- Detection count

**After (OpenWeatherMap):**
- Air Quality Index (AQI): 1-5 scale
  - 1 = Good
  - 2 = Fair
  - 3 = Moderate
  - 4 = Poor
  - 5 = Very Poor
- Pollutant concentrations (μg/m³):
  - CO (Carbon Monoxide)
  - NO₂ (Nitrogen Dioxide)
  - O₃ (Ozone)
  - SO₂ (Sulphur Dioxide)
  - PM2.5 (Fine Particles)
  - PM10 (Coarse Particles)

### 3. Evidence Generation

**Before:**
```python
signal_type: "thermal_anomaly" | "no_anomaly"
signal_text: "Detected X thermal anomalies within 50km"
signal_strength: Based on anomaly count (0-1)
```

**After:**
```python
signal_type: "poor_air_quality" | "moderate_air_quality" | "good_air_quality"
signal_text: "Current air quality: {label} (AQI: {value}/5)"
signal_strength: Based on AQI level (0-1)
```

### 4. Configuration

**Before (.env):**
```bash
NASA_FIRMS_API_KEY=your_nasa_firms_api_key_here
NASA_FIRMS_API_URL=https://firms.modaps.eosdis.nasa.gov/api/area/csv
```

**After (.env):**
```bash
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
```

## Getting Started

### 1. Get a Free API Key

1. Visit: https://openweathermap.org/api
2. Click "Sign Up" or go to: https://home.openweathermap.org/users/sign_up
3. Create a free account
4. Navigate to "API keys" section
5. Copy your API key (it may take a few minutes to activate)

### 2. Configure the Application

Add your API key to `backend/.env`:
```bash
OPENWEATHERMAP_API_KEY=your_actual_api_key_here
```

### 3. Test the Integration

Run the test script:
```bash
cd backend
python test_openweathermap.py
```

Expected output:
```
✅ OpenWeatherMap API key found - will use real API
✅ Query successful!
Current AQI: 3 - Moderate
Average AQI: 2.85
High Pollution Days (90d): 12
```

## Demo Mode

If no API key is configured, the system automatically falls back to demo mode:
- Generates realistic air quality data based on location
- Ensures the application works for demonstrations
- Shows clear indication that demo data is being used

## API Rate Limits

### Free Tier
- **Calls per day**: 1,000
- **Calls per minute**: 60
- **Cost**: $0

### Usage in Application
- **Per claim verification**: 2 API calls (current + historical)
- **With rate limiting**: 2-second delay between requests
- **Daily capacity**: ~500 claim verifications

## Migration Checklist

- [x] Replace `query_nasa_firms()` with `query_openweathermap()`
- [x] Update evidence generation logic
- [x] Update `.env.example` with new API key
- [x] Update `config.py` to remove NASA FIRMS references
- [x] Create test script for OpenWeatherMap
- [x] Update documentation
- [x] Implement retry logic with exponential backoff
- [x] Add proper error handling for API failures
- [x] Maintain demo mode for testing without API key

## Backward Compatibility

**Breaking Changes:**
- NASA FIRMS API key is no longer used
- Evidence records now use different signal types
- Metadata structure has changed

**Migration Path:**
1. Update `.env` file with OpenWeatherMap API key
2. Remove NASA FIRMS API key (optional)
3. Restart the application
4. Test with `test_openweathermap.py`

## Troubleshooting

### "Invalid API key" Error
- Verify your API key is correct
- Wait 10-15 minutes after creating the key (activation time)
- Check that the key is active in your OpenWeatherMap dashboard

### "Rate limit exceeded" Error
- Free tier allows 60 calls/minute
- Application implements 2-second delays between requests
- If you hit the limit, wait 1 minute and try again

### No Data Returned
- Check your internet connection
- Verify the API endpoint is accessible
- Review logs for detailed error messages
- System will fall back to demo mode automatically

## Benefits for ESG Verification

1. **Direct Pollution Measurement**: Actual air quality data vs. thermal anomalies
2. **Multiple Pollutants**: Track CO, NO₂, O₃, SO₂, PM2.5, PM10
3. **Historical Trends**: 90 days of data to identify patterns
4. **Standardized Scale**: AQI provides universal air quality metric
5. **Better Evidence**: More relevant for ESG compliance verification

## Resources

- **OpenWeatherMap API Docs**: https://openweathermap.org/api/air-pollution
- **Air Quality Index Guide**: https://openweathermap.org/api/air-pollution#concept
- **Free API Signup**: https://home.openweathermap.org/users/sign_up
- **Pricing**: https://openweathermap.org/price

## Support

For issues or questions:
1. Check the test script output: `python test_openweathermap.py`
2. Review application logs for detailed error messages
3. Verify API key configuration in `.env`
4. Consult OpenWeatherMap API documentation

---

**Migration Date**: May 2026  
**Status**: ✅ Complete  
**Tested**: ✅ Yes