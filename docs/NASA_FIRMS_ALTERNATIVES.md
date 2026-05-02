# NASA FIRMS Alternatives Research

## Overview
This document provides a comprehensive analysis of free and open alternatives to NASA FIRMS (Fire Information for Resource Management System) for fire and environmental monitoring.

## Current Implementation: NASA FIRMS
- **API**: VIIRS (Visible Infrared Imaging Radiometer Suite) Near Real-Time data
- **Coverage**: Global thermal anomaly detection
- **Update Frequency**: Near real-time (within 3 hours)
- **Cost**: Free with API key registration
- **Data Retention**: 90 days of historical data
- **Limitations**: Requires API key, rate limits apply

---

## Alternative Solutions

### 1. Copernicus Emergency Management Service (EMS)
**Provider**: European Space Agency (ESA) / European Commission

**Description**: Comprehensive emergency monitoring service providing rapid mapping and early warning for natural disasters including fires.

**Pros**:
- ✅ Free and open access
- ✅ High-resolution satellite imagery (Sentinel satellites)
- ✅ Multiple data products (fire detection, burned area mapping)
- ✅ European coverage with global capabilities
- ✅ Well-documented REST API
- ✅ Integration with Copernicus Data Space Ecosystem
- ✅ No API key required for basic access

**Cons**:
- ❌ More complex API structure than FIRMS
- ❌ May have slower update frequency for some products
- ❌ Better coverage in Europe than other regions
- ❌ Requires understanding of Sentinel data products

**API Endpoint**: `https://emergency.copernicus.eu/mapping/`

**Implementation Complexity**: Medium-High

**Recommendation Score**: 8/10

---

### 2. Sentinel Hub (Sentinel-2 & Sentinel-3)
**Provider**: Sinergise / European Space Agency

**Description**: Cloud-based platform for accessing and processing Sentinel satellite data, including thermal anomaly detection.

**Pros**:
- ✅ Free tier available (limited requests)
- ✅ High-resolution multispectral imagery
- ✅ Custom processing capabilities
- ✅ Good documentation and Python SDK
- ✅ Can detect fires using SWIR (Short-Wave Infrared) bands
- ✅ Historical data archive available

**Cons**:
- ❌ Free tier has strict rate limits (2,500 processing units/month)
- ❌ Requires OAuth authentication
- ❌ More complex setup than FIRMS
- ❌ Need to process raw satellite data for fire detection
- ❌ Not specifically designed for fire monitoring

**API Endpoint**: `https://services.sentinel-hub.com/`

**Implementation Complexity**: High

**Recommendation Score**: 6/10

---

### 3. MODIS Active Fire Data (Direct from NASA)
**Provider**: NASA Earth Observing System Data and Information System (EOSDIS)

**Description**: Direct access to MODIS (Moderate Resolution Imaging Spectroradiometer) active fire data without going through FIRMS.

**Pros**:
- ✅ Completely free, no API key required
- ✅ Global coverage
- ✅ Long historical archive (2000-present)
- ✅ Multiple satellites (Terra and Aqua)
- ✅ CSV and shapefile formats available
- ✅ Well-established and reliable

**Cons**:
- ❌ Lower spatial resolution than VIIRS (1km vs 375m)
- ❌ Less frequent updates than VIIRS
- ❌ No REST API - requires FTP or direct file downloads
- ❌ More manual data processing required
- ❌ Older technology compared to VIIRS

**Data Access**: FTP: `ftp://nrt1.modaps.eosdis.nasa.gov/`

**Implementation Complexity**: Medium

**Recommendation Score**: 7/10

---

### 4. VIIRS Active Fire Data (Direct from NOAA)
**Provider**: NOAA (National Oceanic and Atmospheric Administration)

**Description**: Direct access to VIIRS active fire data from NOAA's CLASS (Comprehensive Large Array-data Stewardship System).

**Pros**:
- ✅ Same data source as FIRMS but different access method
- ✅ Free access
- ✅ High spatial resolution (375m)
- ✅ Near real-time data
- ✅ Multiple satellites (SNPP and NOAA-20)
- ✅ No API key required for some products

**Cons**:
- ❌ Complex data format (HDF5/NetCDF)
- ❌ Requires significant processing to extract fire locations
- ❌ Large file sizes
- ❌ No simple REST API
- ❌ Steep learning curve

**Data Access**: `https://www.class.noaa.gov/`

**Implementation Complexity**: High

**Recommendation Score**: 5/10

---

### 5. OpenWeatherMap Air Pollution API
**Provider**: OpenWeatherMap

**Description**: Air quality and pollution data API that can indicate environmental issues including fires through air quality degradation.

**Pros**:
- ✅ Free tier available (1,000 calls/day)
- ✅ Simple REST API
- ✅ Real-time and forecast data
- ✅ Global coverage
- ✅ Easy to integrate
- ✅ Provides AQI, CO, NO2, SO2, PM2.5, PM10, O3
- ✅ Good documentation

**Cons**:
- ❌ Indirect fire detection (through air quality)
- ❌ Requires API key
- ❌ Limited free tier
- ❌ Not specifically for fire monitoring
- ❌ May miss fires that don't significantly affect air quality
- ❌ Paid plans required for higher usage

**API Endpoint**: `http://api.openweathermap.org/data/2.5/air_pollution`

**Implementation Complexity**: Low

**Recommendation Score**: 6/10

---

### 6. EPA Air Quality System (AQS) API
**Provider**: U.S. Environmental Protection Agency

**Description**: Comprehensive air quality monitoring data from EPA's network of monitoring stations across the United States.

**Pros**:
- ✅ Completely free, no API key required
- ✅ High-quality ground-based measurements
- ✅ Historical data available
- ✅ Well-documented REST API
- ✅ Multiple pollutants tracked
- ✅ Reliable and authoritative source

**Cons**:
- ❌ U.S. only coverage
- ❌ Station-based (not satellite), limited spatial coverage
- ❌ Indirect fire detection
- ❌ Not real-time (typically 1-hour delay)
- ❌ Requires knowledge of monitoring station locations
- ❌ Not suitable for remote/rural areas

**API Endpoint**: `https://aqs.epa.gov/data/api/`

**Implementation Complexity**: Low-Medium

**Recommendation Score**: 7/10 (for U.S. facilities only)

---

## Comparison Table

| Alternative | Cost | API Complexity | Coverage | Real-time | Fire-Specific | Overall Score |
|-------------|------|----------------|----------|-----------|---------------|---------------|
| **NASA FIRMS (Current)** | Free (API key) | Low | Global | Yes | Yes | 9/10 |
| Copernicus EMS | Free | Medium-High | Global (EU focus) | Yes | Yes | 8/10 |
| Sentinel Hub | Free tier | High | Global | Yes | No | 6/10 |
| MODIS Direct | Free | Medium | Global | Yes | Yes | 7/10 |
| VIIRS Direct | Free | High | Global | Yes | Yes | 5/10 |
| OpenWeatherMap | Free tier | Low | Global | Yes | No | 6/10 |
| EPA AQS | Free | Low-Medium | U.S. only | Near | No | 7/10 |

---

## Recommendations

### Best Overall Alternative: **Copernicus Emergency Management Service (EMS)**

**Rationale**:
1. **Free and Open**: No API key required, truly open access
2. **Fire-Specific**: Designed for emergency monitoring including fires
3. **High Quality**: Uses Sentinel satellites with excellent resolution
4. **Well-Maintained**: Backed by ESA and European Commission
5. **Good Documentation**: Clear API documentation and examples

**Implementation Strategy**:
```python
# Example Copernicus EMS integration
async def query_copernicus_ems(latitude, longitude, radius_km=50):
    """Query Copernicus EMS for fire events"""
    base_url = "https://emergency.copernicus.eu/mapping/list-of-components/EMSR"
    # Use Sentinel-3 SLSTR for fire detection
    # Or Sentinel-2 for burned area mapping
    pass
```

### Best for U.S. Facilities: **EPA AQS API + MODIS Direct**

**Rationale**:
- Combine ground-based air quality data (EPA) with satellite fire detection (MODIS)
- Both are completely free with no API keys
- Provides complementary data sources
- EPA data is highly reliable for U.S. locations

### Best for Simplicity: **MODIS Active Fire Data (Direct)**

**Rationale**:
- No API key required
- Simpler than VIIRS direct access
- Proven technology with long track record
- CSV format is easy to parse
- Good enough resolution for most use cases

---

## Implementation Priority

### Phase 1: Keep NASA FIRMS (Current)
- Already implemented and working
- Best balance of features and ease of use
- Free with simple API key registration

### Phase 2: Add Copernicus EMS as Secondary Source
- Provides redundancy if FIRMS is unavailable
- European facilities get better coverage
- No API key dependency

### Phase 3: Consider EPA AQS for U.S. Facilities
- Add as supplementary data source
- Provides ground-truth validation
- Completely free and reliable

---

## Code Examples

### Copernicus EMS Integration (Recommended)

```python
async def query_copernicus_fires(latitude, longitude, radius_km=50, days_back=90):
    """
    Query Copernicus for fire events using Sentinel-3 SLSTR
    """
    # Copernicus Data Space Ecosystem API
    base_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    
    # Calculate bounding box
    lat_offset = radius_km / 111.0
    lon_offset = radius_km / (111.0 * abs(math.cos(math.radians(latitude))))
    
    bbox = f"{longitude - lon_offset},{latitude - lat_offset},{longitude + lon_offset},{latitude + lat_offset}"
    
    # Query for Sentinel-3 SLSTR fire products
    params = {
        "$filter": f"Collection/Name eq 'SENTINEL-3' and OData.CSC.Intersects(area=geography'SRID=4326;POLYGON(({bbox}))')",
        "$orderby": "ContentDate/Start desc",
        "$top": 100
    }
    
    response = await client.get(base_url, params=params)
    # Process fire detection data
    return response.json()
```

### MODIS Direct Access (Simplest Alternative)

```python
async def query_modis_direct(latitude, longitude, radius_km=50, days_back=90):
    """
    Query MODIS active fire data directly from NASA EOSDIS
    """
    # MODIS NRT fire data URL
    base_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/"
    
    # Download recent fire CSV
    file_url = f"{base_url}MODIS_C6_1_Global_24h.csv"
    
    response = await client.get(file_url)
    
    # Parse CSV and filter by location
    fires = []
    for line in response.text.split('\n')[1:]:  # Skip header
        parts = line.split(',')
        if len(parts) >= 10:
            fire_lat = float(parts[0])
            fire_lon = float(parts[1])
            
            # Calculate distance
            distance = haversine_distance(latitude, longitude, fire_lat, fire_lon)
            
            if distance <= radius_km:
                fires.append({
                    'latitude': fire_lat,
                    'longitude': fire_lon,
                    'brightness': float(parts[2]),
                    'confidence': parts[9],
                    'date': parts[5]
                })
    
    return fires
```

---

## Conclusion

**Recommended Approach**:
1. **Keep NASA FIRMS** as primary source (already implemented, works well)
2. **Add Copernicus EMS** as secondary/backup source for redundancy
3. **Consider EPA AQS** for U.S. facilities as supplementary validation

This multi-source approach provides:
- Redundancy if one service is down
- Cross-validation of fire events
- Better coverage across different regions
- No single point of failure

**Next Steps**:
1. Test current NASA FIRMS implementation
2. Prototype Copernicus EMS integration
3. Evaluate performance and coverage
4. Implement fallback logic between sources