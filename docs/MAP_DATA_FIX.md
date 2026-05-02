# Map Data Display Fix

## Problem Summary
The frontend was showing "Location data pending" for facility locations even though the backend was successfully returning map data through the `/map-data/{document_id}` endpoint.

## Root Cause Analysis

### What Was Working ✅
1. **Backend API**: The `/map-data/{document_id}` endpoint was correctly implemented and returning location data
2. **Frontend API Call**: `App.jsx` was calling `getMapData()` after verification completed
3. **State Management**: Map data was being stored in the `mapData` state variable
4. **Props Passing**: `mapData` was being passed to the `EvidencePanel` component

### What Was Broken ❌
The `EvidencePanel` component was checking for coordinates in the wrong place:
- It was looking for `claim.latitude` and `claim.longitude` on the claim object
- But the coordinates were actually in `mapData.locations[]` array
- This caused the component to always show "Coordinates being resolved..." message

## The Fix

### Changes Made

#### 1. EvidencePanel.jsx - Added Location Matching Logic
```javascript
// Find location data for the current claim from mapData
const claimLocation = useMemo(() => {
  if (!claim || !mapData || !mapData.locations) return null;
  
  // Try to match by facility name first
  const location = mapData.locations.find(loc => 
    loc.facility_name === claim.facility_name
  );
  
  // If no match and only one location, use it
  if (!location && mapData.locations.length === 1) {
    return mapData.locations[0];
  }
  
  return location;
}, [claim, mapData]);
```

#### 2. EvidencePanel.jsx - Updated Display Logic
Changed from checking `claim.latitude && claim.longitude` to checking `claimLocation`:
- Now displays coordinates from `claimLocation.latitude` and `claimLocation.longitude`
- Shows facility name from `claimLocation.facility_name`
- Displays address from `claimLocation.address`
- Shows claim count if multiple claims share the same location
- Provides better feedback when map data is loading vs. when coordinates are unavailable

#### 3. App.jsx - Enhanced Logging
Added detailed console logging to track map data loading:
```javascript
console.log('✅ Map data loaded successfully:', {
  total_locations: mapResponse.total_locations,
  locations: mapResponse.locations,
  facilities: Object.keys(mapResponse.facilities || {}).length
})
```

## Data Flow

### Backend Response Structure
```json
{
  "document_id": "uuid",
  "locations": [
    {
      "facility_name": "Manufacturing Plant A",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "address": "New York, NY",
      "claim_count": 2
    }
  ],
  "facilities": {},
  "total_locations": 1
}
```

### Frontend Data Flow
1. User uploads document → `handleUpload()` triggered
2. Document uploaded → `uploadDocument()` returns document_id
3. Claims extracted → `extractClaims()` returns claims array
4. Claims verified → `verifyClaims()` returns evidence array
5. **Map data fetched** → `getMapData()` returns location data
6. Map data stored in state → `setMapData(mapResponse)`
7. Map data passed to EvidencePanel → `<EvidencePanel mapData={mapData} />`
8. EvidencePanel matches claim to location → `claimLocation` computed
9. Coordinates displayed → Shows lat/lon from `claimLocation`

## Testing Checklist

- [x] Frontend builds successfully without errors
- [ ] Map data API is called after verification completes
- [ ] Console shows "✅ Map data loaded successfully" message
- [ ] Facility coordinates are displayed in the Evidence Panel
- [ ] "Location data pending" message is replaced with actual coordinates
- [ ] Multiple locations are handled correctly
- [ ] Error handling works when map data fails to load

## Expected Behavior After Fix

### When Map Data Loads Successfully
- Shows facility name (e.g., "Manufacturing Plant A")
- Shows address if available
- Displays latitude and longitude with 4 decimal precision
- Shows total number of locations identified
- Indicates if multiple claims share the same location

### When Map Data Is Loading
- Shows "Loading location data..." message
- Displays facility name from claim if available

### When Map Data Fails or No Coordinates
- Shows "No coordinates available for this facility" message
- Gracefully continues without breaking the UI

## Future Enhancements

1. **Interactive Map Integration**: Add Leaflet or Mapbox to show actual map visualization
2. **Geocoding Fallback**: If coordinates missing, attempt to geocode from facility name/address
3. **Map Clustering**: Group nearby facilities when multiple locations exist
4. **Satellite Imagery**: Show satellite view of facility locations
5. **Heat Map**: Visualize risk scores across geographic regions

## Related Files

- `frontend/src/App.jsx` - Main application component, handles data fetching
- `frontend/src/components/EvidencePanel.jsx` - Displays evidence and location data
- `frontend/src/services/api.js` - API service layer with `getMapData()` function
- `backend/app/api/routes.py` - Backend endpoint `/map-data/{document_id}`

## Deployment Notes

No backend changes required - this is purely a frontend fix. Simply rebuild and redeploy the frontend:

```bash
cd frontend
npm run build
# Deploy dist/ folder to your hosting service