"""
IBM Watson Natural Language Understanding Service - Stage 4
Handles entity extraction for facility and location resolution
"""
import logging
from typing import List, Dict, Any, Optional
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from app.config import settings
from app.models.schemas import FacilityLocation

logger = logging.getLogger(__name__)


class NLUService:
    """IBM Watson NLU client for entity extraction"""
    
    def __init__(self):
        """Initialize Watson NLU client"""
        authenticator = IAMAuthenticator(settings.ibm_nlu_api_key)
        
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        
        self.nlu.set_service_url(settings.ibm_nlu_url)
        logger.info("Initialized Watson NLU service")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text using Watson NLU
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with entity types as keys and lists of entity mentions as values
        """
        try:
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(
                        sentiment=False,
                        limit=50
                    ),
                    keywords=KeywordsOptions(
                        sentiment=False,
                        limit=50
                    )
                ),
                language='en'
            ).get_result()
            
            # Organize entities by type
            entities = {
                'locations': [],
                'organizations': [],
                'facilities': [],
                'keywords': []
            }
            
            # Extract location and organization entities
            for entity in response.get('entities', []):
                entity_type = entity.get('type', '').lower()
                entity_text = entity.get('text', '')
                
                if entity_type == 'location':
                    entities['locations'].append(entity_text)
                elif entity_type == 'organization':
                    entities['organizations'].append(entity_text)
                elif entity_type in ['facility', 'geographicfeature']:
                    entities['facilities'].append(entity_text)
            
            # Extract keywords that might be facility names
            for keyword in response.get('keywords', []):
                keyword_text = keyword.get('text', '')
                # Look for keywords that contain facility-related terms
                if any(term in keyword_text.lower() for term in ['plant', 'facility', 'factory', 'site', 'center']):
                    entities['keywords'].append(keyword_text)
            
            logger.info(f"Extracted entities: {len(entities['locations'])} locations, "
                       f"{len(entities['organizations'])} organizations, "
                       f"{len(entities['facilities'])} facilities")
            
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities with NLU: {e}")
            return {'locations': [], 'organizations': [], 'facilities': [], 'keywords': []}
    
    def identify_facilities_in_claims(
        self,
        claims: List[Dict[str, Any]],
        full_document_text: str
    ) -> List[str]:
        """
        Identify facility names mentioned in claims
        
        Args:
            claims: List of claim dictionaries
            full_document_text: Complete document text for context
            
        Returns:
            List of unique facility names
        """
        facility_names = set()
        
        # Extract entities from each claim
        for claim in claims:
            claim_text = claim.get('claim_text', '')
            if claim_text:
                entities = self.extract_entities(claim_text)
                facility_names.update(entities['facilities'])
                facility_names.update(entities['keywords'])
        
        # Also scan the full document for facility mentions
        # (limited to first 5000 chars to stay within NLU quota)
        if full_document_text:
            sample_text = full_document_text[:5000]
            entities = self.extract_entities(sample_text)
            facility_names.update(entities['facilities'])
            facility_names.update(entities['keywords'])
        
        facility_list = list(facility_names)
        logger.info(f"Identified {len(facility_list)} unique facility names")
        return facility_list
    
    def resolve_facility_location(
        self,
        facility_name: str,
        location_mapping: Dict[str, Dict[str, Any]]
    ) -> FacilityLocation:
        """
        Resolve a facility name to geographic coordinates
        
        Args:
            facility_name: Name of the facility
            location_mapping: Pre-loaded mapping of facility names to coordinates
            
        Returns:
            FacilityLocation object
        """
        # Normalize facility name for matching
        normalized_name = facility_name.lower().strip()
        
        # Check if facility exists in mapping
        for mapped_name, location_data in location_mapping.items():
            if normalized_name in mapped_name.lower() or mapped_name.lower() in normalized_name:
                return FacilityLocation(
                    facility_name=facility_name,
                    latitude=location_data.get('latitude'),
                    longitude=location_data.get('longitude'),
                    address=location_data.get('address'),
                    resolved=True
                )
        
        # If not found, return unresolved
        logger.warning(f"Could not resolve location for facility: {facility_name}")
        return FacilityLocation(
            facility_name=facility_name,
            resolved=False
        )


# Singleton instance
_nlu_service: Optional[NLUService] = None


def get_nlu_service() -> NLUService:
    """Get or create the NLU service singleton"""
    global _nlu_service
    if _nlu_service is None:
        _nlu_service = NLUService()
    return _nlu_service

# Made with Bob
