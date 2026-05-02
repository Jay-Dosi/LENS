"""
Test script for OpenWeatherMap Air Pollution API integration
Tests both with and without API key (demo mode)
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.external_data_service import ExternalDataService


async def test_openweathermap():
    """Test OpenWeatherMap Air Pollution API"""
    print("=" * 80)
    print("Testing OpenWeatherMap Air Pollution API Integration")
    print("=" * 80)
    
    # Initialize service
    service = ExternalDataService()
    
    # Test location: Houston, TX (near petrochemical facilities)
    test_lat = 29.7604
    test_lon = -95.3698
    
    print(f"\n📍 Test Location: Houston, TX ({test_lat}, {test_lon})")
    print("-" * 80)
    
    # Check if API key is configured
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if api_key and api_key != "your_openweathermap_api_key_here":
        print("✅ OpenWeatherMap API key found - will use real API")
    else:
        print("⚠️  No OpenWeatherMap API key - will use demo data")
        print("   Get a free API key at: https://openweathermap.org/api")
    
    print("\n🔍 Querying OpenWeatherMap Air Pollution API...")
    print("-" * 80)
    
    try:
        # Query OpenWeatherMap
        result = await service.query_openweathermap(test_lat, test_lon)
        
        print("\n✅ Query successful!")
        print(f"Source: {result.get('source')}")
        print(f"Current AQI: {result.get('current_aqi')} - {result.get('current_aqi_label')}")
        print(f"Average AQI: {result.get('average_aqi')}")
        print(f"High Pollution Days (90d): {result.get('high_pollution_days')}")
        
        print("\n🌫️  Air Quality Components (μg/m³):")
        components = result.get('components', {})
        print(f"  • CO (Carbon Monoxide): {components.get('co', 0):.2f}")
        print(f"  • NO₂ (Nitrogen Dioxide): {components.get('no2', 0):.2f}")
        print(f"  • O₃ (Ozone): {components.get('o3', 0):.2f}")
        print(f"  • SO₂ (Sulphur Dioxide): {components.get('so2', 0):.2f}")
        print(f"  • PM2.5 (Fine Particles): {components.get('pm2_5', 0):.2f}")
        print(f"  • PM10 (Coarse Particles): {components.get('pm10', 0):.2f}")
        
        if result.get('note'):
            print(f"\n📝 Note: {result.get('note')}")
        
        print("\n" + "=" * 80)
        print("✅ OpenWeatherMap integration test PASSED")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n" + "=" * 80)
        print("❌ OpenWeatherMap integration test FAILED")
        print("=" * 80)
        raise
    
    finally:
        await service.close()


async def test_evidence_collection():
    """Test evidence collection with OpenWeatherMap"""
    print("\n" + "=" * 80)
    print("Testing Evidence Collection with OpenWeatherMap")
    print("=" * 80)
    
    service = ExternalDataService()
    
    # Mock claim data
    claim = {
        "claim_id": "test_claim_001",
        "facility_name": "Test Petrochemical Plant",
        "company_name": "Test Energy Corp"
    }
    
    # Mock facility location
    facility_location = {
        "resolved": True,
        "latitude": 29.7604,
        "longitude": -95.3698
    }
    
    print("\n🔍 Collecting evidence for test claim...")
    print("-" * 80)
    
    try:
        evidence_list = await service.collect_evidence_for_claim(claim, facility_location)
        
        print(f"\n✅ Collected {len(evidence_list)} evidence records:")
        print("-" * 80)
        
        for i, evidence in enumerate(evidence_list, 1):
            print(f"\n{i}. Evidence ID: {evidence.evidence_id}")
            print(f"   Source: {evidence.source}")
            print(f"   Signal Type: {evidence.signal_type}")
            print(f"   Signal Text: {evidence.signal_text}")
            print(f"   Signal Strength: {evidence.signal_strength:.2f}")
        
        print("\n" + "=" * 80)
        print("✅ Evidence collection test PASSED")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n" + "=" * 80)
        print("❌ Evidence collection test FAILED")
        print("=" * 80)
        raise
    
    finally:
        await service.close()


async def main():
    """Run all tests"""
    print("\n🚀 Starting OpenWeatherMap Integration Tests\n")
    
    try:
        # Test 1: Direct API query
        await test_openweathermap()
        
        # Test 2: Evidence collection
        await test_evidence_collection()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 80)
        print("\n📋 Next Steps:")
        print("1. Get a free OpenWeatherMap API key: https://openweathermap.org/api")
        print("2. Add it to your .env file: OPENWEATHERMAP_API_KEY=your_key_here")
        print("3. Run this test again to verify real API integration")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n💥 Test suite failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
