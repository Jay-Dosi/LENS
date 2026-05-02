"""
NLU Service - IBM Watson Natural Language Understanding
Uses IBM Watson NLU API for entity extraction
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
        """Initialize IBM Watson NLU client"""
        try:
            # Create authenticator
            authenticator = IAMAuthenticator(settings.watson_nlu_api_key)
            
            # Initialize NLU service
            self.nlu = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            
            # Set service URL
            self.nlu.set_service_url(settings.watson_nlu_url)
            
            logger.info("Initialized IBM Watson NLU service successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Watson NLU: {e}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text using Watson NLU
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with entity types as keys and lists of entity mentions as values
        """
        try:
            # Call Watson NLU API
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(
                        sentiment=False,
                        emotion=False,
                        limit=50
                    ),
                    keywords=KeywordsOptions(
                        sentiment=False,
                        emotion=False,
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
            
            # Extract entities from response
            for entity in response.get('entities', []):
                entity_text = entity.get('text', '').strip()
                entity_type = entity.get('type', '')
                
                # Map Watson NLU entity types to our categories
                if entity_type in ['Location', 'GeographicFeature', 'City', 'Country', 'StateOrCounty']:
                    entities['locations'].append(entity_text)
                    
                elif entity_type in ['Organization', 'Company', 'Facility']:
                    entities['organizations'].append(entity_text)
                    if entity_type == 'Facility':
                        entities['facilities'].append(entity_text)
            
            # Extract keywords
            for keyword in response.get('keywords', []):
                keyword_text = keyword.get('text', '').strip()
                entities['keywords'].append(keyword_text)
                
                # Check if keyword is facility-related
                facility_keywords = [
                    'plant', 'facility', 'factory', 'site', 'center', 'centre',
                    'manufacturing', 'production', 'warehouse', 'office', 'campus',
                    'refinery', 'mill', 'works'
                ]
                if any(kw in keyword_text.lower() for kw in facility_keywords):
                    entities['facilities'].append(keyword_text)
            
            # Remove duplicates while preserving order
            for key in entities:
                entities[key] = list(dict.fromkeys(entities[key]))
            
            logger.info(f"Extracted entities: {len(entities['locations'])} locations, "
                       f"{len(entities['organizations'])} organizations, "
                       f"{len(entities['facilities'])} facilities")
            
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities with Watson NLU: {e}")
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
        # Process in chunks to handle large documents
        if full_document_text:
            # Limit to first 10000 characters for efficiency
            sample_text = full_document_text[:10000]
            entities = self.extract_entities(sample_text)
            facility_names.update(entities['facilities'])
            facility_names.update(entities['keywords'])
        
        # Filter out generic terms and keep only specific facility names
        filtered_facilities = []
        generic_terms = {'facility', 'plant', 'factory', 'site', 'center', 'centre'}
        
        for facility in facility_names:
            # Keep if it's not just a generic term
            if facility.lower() not in generic_terms:
                # Keep if it contains a proper noun or specific identifier
                if any(char.isupper() for char in facility) or any(char.isdigit() for char in facility):
                    filtered_facilities.append(facility)
        
        facility_list = list(set(filtered_facilities))
        logger.info(f"Identified {len(facility_list)} unique facility names")
        return facility_list
    
    def extract_locations_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extract location entities with additional context
        
        Args:
            text: Text to analyze
            
        Returns:
            List of location dictionaries with text and type
        """
        try:
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(
                        sentiment=False,
                        emotion=False,
                        limit=50
                    )
                ),
                language='en'
            ).get_result()
            
            locations = []
            
            for entity in response.get('entities', []):
                entity_type = entity.get('type', '')
                if entity_type in ['Location', 'GeographicFeature', 'City', 'Country', 'StateOrCounty']:
                    locations.append({
                        'text': entity.get('text', ''),
                        'type': entity_type,
                        'relevance': entity.get('relevance', 0)
                    })
            
            return locations
            
        except Exception as e:
            logger.error(f"Error extracting locations: {e}")
            return []
    
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
            mapped_normalized = mapped_name.lower().strip()
            
            # Exact match or substring match
            if (normalized_name == mapped_normalized or 
                normalized_name in mapped_normalized or 
                mapped_normalized in normalized_name):
                
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
    
    def extract_numerical_values(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract numerical values and their units from text
        Useful for extracting emissions values, percentages, etc.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of dictionaries with value, unit, and context
        """
        try:
            # Use Watson NLU to extract entities and keywords
            response = self.nlu.analyze(
                text=text,
                features=Features(
                    entities=EntitiesOptions(limit=50),
                    keywords=KeywordsOptions(limit=50)
                ),
                language='en'
            ).get_result()
            
            values = []
            
            # Look for quantity-related entities
            for entity in response.get('entities', []):
                if entity.get('type') == 'Quantity':
                    values.append({
                        'value': entity.get('text', ''),
                        'unit': None,  # Watson NLU doesn't always provide units
                        'context': entity.get('text', ''),
                        'relevance': entity.get('relevance', 0)
                    })
            
            return values
            
        except Exception as e:
            logger.error(f"Error extracting numerical values: {e}")
            return []


# Singleton instance
_nlu_service: Optional[NLUService] = None


def get_nlu_service() -> NLUService:
    """Get or create the NLU service singleton"""
    global _nlu_service
    if _nlu_service is None:
        _nlu_service = NLUService()
    return _nlu_service

# Made with Bob
