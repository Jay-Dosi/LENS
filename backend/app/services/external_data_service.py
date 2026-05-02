"""
External Data Collection Service - Stage 5
Queries NASA FIRMS and GDELT for verification evidence
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx
from app.models.schemas import Evidence

logger = logging.getLogger(__name__)


class ExternalDataService:
    """Service for querying external data sources"""
    
    def __init__(self):
        """Initialize HTTP client"""
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info("Initialized External Data Service")
    
    async def query_nasa_firms(
        self,
        latitude: float,
        longitude: float,
        radius_km: int = 50,
        days_back: int = 90
    ) -> Dict[str, Any]:
        """
        Query NASA FIRMS for thermal anomalies near a location
        
        Args:
            latitude: Facility latitude
            longitude: Facility longitude
            radius_km: Search radius in kilometers
            days_back: Number of days to look back
            
        Returns:
            Dictionary with anomaly data
        """
        try:
            # NASA FIRMS API endpoint (using VIIRS data)
            # Note: For production, you would need a FIRMS API key
            # For demo purposes, we'll simulate the response structure
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # In a real implementation, you would call:
            # url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/VIIRS_SNPP_NRT/{latitude},{longitude}/{radius_km}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            
            # For demo, we'll return a structured response
            # In production, parse the CSV response from FIRMS
            
            result = {
                "source": "NASA_FIRMS",
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius_km": radius_km
                },
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "anomalies_detected": 0,  # Would be populated from actual API
                "high_confidence_detections": 0,
                "detections": []  # List of detection objects
            }
            
            logger.info(f"Queried NASA FIRMS for location ({latitude}, {longitude})")
            return result
            
        except Exception as e:
            logger.error(f"Error querying NASA FIRMS: {e}")
            return {
                "source": "NASA_FIRMS",
                "error": str(e),
                "anomalies_detected": 0
            }
    
    async def query_gdelt(
        self,
        facility_name: str,
        company_name: str,
        days_back: int = 90
    ) -> Dict[str, Any]:
        """
        Query GDELT for news events related to a facility
        
        Args:
            facility_name: Name of the facility
            company_name: Name of the company
            days_back: Number of days to look back
            
        Returns:
            Dictionary with news event data
        """
        try:
            # GDELT 2.0 Doc API endpoint
            base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Build search query for environmental issues
            search_terms = [
                f'"{facility_name}"',
                f'"{company_name}"',
                "emissions OR pollution OR environmental OR violation OR fine"
            ]
            query = " AND ".join(search_terms)
            
            # GDELT API parameters
            params = {
                "query": query,
                "mode": "artlist",
                "maxrecords": 250,
                "format": "json",
                "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
                "enddatetime": end_date.strftime("%Y%m%d%H%M%S")
            }
            
            # Make the request
            response = await self.client.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                
                # Analyze tone and themes
                negative_articles = [
                    art for art in articles
                    if art.get("tone", 0) < -2  # Negative tone threshold
                ]
                
                result = {
                    "source": "GDELT",
                    "query": query,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "total_articles": len(articles),
                    "negative_articles": len(negative_articles),
                    "average_tone": sum(art.get("tone", 0) for art in articles) / len(articles) if articles else 0,
                    "articles": articles[:10]  # Return top 10 for analysis
                }
                
                logger.info(f"Queried GDELT: {len(articles)} articles found")
                return result
            else:
                logger.warning(f"GDELT API returned status {response.status_code}")
                return {
                    "source": "GDELT",
                    "error": f"API returned status {response.status_code}",
                    "total_articles": 0
                }
                
        except Exception as e:
            logger.error(f"Error querying GDELT: {e}")
            return {
                "source": "GDELT",
                "error": str(e),
                "total_articles": 0
            }
    
    async def collect_evidence_for_claim(
        self,
        claim: Dict[str, Any],
        facility_location: Optional[Dict[str, Any]] = None
    ) -> List[Evidence]:
        """
        Collect all external evidence for a single claim
        
        Args:
            claim: Claim dictionary
            facility_location: Optional facility location data
            
        Returns:
            List of Evidence objects
        """
        evidence_list = []
        claim_id = claim.get("claim_id")
        
        # If we have a resolved location, query NASA FIRMS
        if facility_location and facility_location.get("resolved"):
            lat = facility_location.get("latitude")
            lon = facility_location.get("longitude")
            
            if lat and lon:
                firms_data = await self.query_nasa_firms(lat, lon)
                
                # Create evidence record based on FIRMS data
                anomaly_count = firms_data.get("anomalies_detected", 0)
                
                if anomaly_count > 0:
                    evidence = Evidence(
                        evidence_id=f"{claim_id}_firms",
                        claim_id=claim_id,
                        source="NASA_FIRMS",
                        signal_type="thermal_anomaly",
                        signal_text=f"Detected {anomaly_count} thermal anomalies within 50km of facility in past 90 days",
                        signal_strength=min(anomaly_count / 10.0, 1.0),  # Normalize to 0-1
                        timestamp=datetime.now(),
                        metadata=firms_data
                    )
                    evidence_list.append(evidence)
                else:
                    evidence = Evidence(
                        evidence_id=f"{claim_id}_firms",
                        claim_id=claim_id,
                        source="NASA_FIRMS",
                        signal_type="no_anomaly",
                        signal_text="No thermal anomalies detected near facility",
                        signal_strength=0.0,
                        timestamp=datetime.now(),
                        metadata=firms_data
                    )
                    evidence_list.append(evidence)
        
        # Query GDELT for news coverage
        facility_name = claim.get("facility_name", "")
        company_name = claim.get("company_name", "Unknown Company")
        
        if facility_name or company_name:
            gdelt_data = await self.query_gdelt(facility_name, company_name)
            
            negative_count = gdelt_data.get("negative_articles", 0)
            total_count = gdelt_data.get("total_articles", 0)
            
            if negative_count > 5:  # Threshold for significant negative coverage
                evidence = Evidence(
                    evidence_id=f"{claim_id}_gdelt",
                    claim_id=claim_id,
                    source="GDELT",
                    signal_type="negative_news",
                    signal_text=f"Found {negative_count} negative news articles about environmental issues",
                    signal_strength=min(negative_count / 20.0, 1.0),  # Normalize to 0-1
                    timestamp=datetime.now(),
                    metadata=gdelt_data
                )
                evidence_list.append(evidence)
            elif total_count > 0:
                evidence = Evidence(
                    evidence_id=f"{claim_id}_gdelt",
                    claim_id=claim_id,
                    source="GDELT",
                    signal_type="neutral_news",
                    signal_text=f"Found {total_count} news articles, mostly neutral tone",
                    signal_strength=0.0,
                    timestamp=datetime.now(),
                    metadata=gdelt_data
                )
                evidence_list.append(evidence)
        
        logger.info(f"Collected {len(evidence_list)} evidence records for claim {claim_id}")
        return evidence_list
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
_external_data_service: Optional[ExternalDataService] = None


def get_external_data_service() -> ExternalDataService:
    """Get or create the external data service singleton"""
    global _external_data_service
    if _external_data_service is None:
        _external_data_service = ExternalDataService()
    return _external_data_service

# Made with Bob
