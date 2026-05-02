"""
Quick test to verify external data service fixes
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.external_data_service import ExternalDataService


async def test_external_data_service():
    """Test that external data service handles errors gracefully"""
    print("Testing External Data Service...")
    
    service = ExternalDataService()
    
    # Test 1: Query GDELT (may fail but should return structured response)
    print("\n1. Testing GDELT query...")
    gdelt_result = await service.query_gdelt("Test Facility", "Test Company")
    print(f"   - Source: {gdelt_result.get('source')}")
    print(f"   - Total articles: {gdelt_result.get('total_articles', 0)}")
    print(f"   - Has error: {'error' in gdelt_result}")
    if 'error' in gdelt_result:
        print(f"   - Error: {gdelt_result['error'][:100]}")
    
    # Test 2: Query NASA FIRMS (simulated)
    print("\n2. Testing NASA FIRMS query...")
    firms_result = await service.query_nasa_firms(40.7128, -74.0060)
    print(f"   - Source: {firms_result.get('source')}")
    print(f"   - Anomalies detected: {firms_result.get('anomalies_detected', 0)}")
    print(f"   - Has error: {'error' in firms_result}")
    
    # Test 3: Collect evidence for a claim (should always return evidence)
    print("\n3. Testing evidence collection...")
    test_claim = {
        "claim_id": "test_claim_001",
        "facility_name": "Test Facility",
        "company_name": "Test Company"
    }
    
    evidence_list = await service.collect_evidence_for_claim(test_claim, None)
    print(f"   - Evidence records collected: {len(evidence_list)}")
    
    for i, evidence in enumerate(evidence_list, 1):
        print(f"   - Evidence {i}:")
        print(f"     * Source: {evidence.source}")
        print(f"     * Signal type: {evidence.signal_type}")
        print(f"     * Signal text: {evidence.signal_text[:80]}...")
        print(f"     * Signal strength: {evidence.signal_strength}")
    
    # Verify we always get evidence
    assert len(evidence_list) > 0, "Should always return at least one evidence record"
    
    await service.close()
    
    print("\n✅ All tests passed! External data service handles errors gracefully.")
    print("   - Frontend will no longer be stuck in 'Loading...' state")
    print("   - Evidence is always returned, even when external APIs fail")
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_external_data_service())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
