"""
Test script for Google News RSS implementation
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.external_data_service import ExternalDataService


async def test_google_news():
    """Test Google News RSS query"""
    print("=" * 60)
    print("Testing Google News RSS Implementation")
    print("=" * 60)
    
    service = ExternalDataService()
    
    try:
        # Test 1: Query with facility name
        print("\n[Test 1] Querying Google News for 'Tesla Gigafactory'...")
        result1 = await service.query_google_news(
            facility_name="Tesla Gigafactory",
            company_name="Tesla",
            days_back=30
        )
        
        print(f"✓ Query successful!")
        print(f"  - Source: {result1.get('source')}")
        print(f"  - Total articles: {result1.get('total_articles', 0)}")
        print(f"  - Negative articles: {result1.get('negative_articles', 0)}")
        print(f"  - Query: {result1.get('query')}")
        
        if result1.get('articles'):
            print(f"\n  Sample articles:")
            for i, article in enumerate(result1['articles'][:3], 1):
                print(f"    {i}. {article.get('title', 'N/A')[:80]}...")
                print(f"       Source: {article.get('source', 'Unknown')}")
                print(f"       Published: {article.get('published', 'N/A')}")
        
        # Test 2: Query with environmental keywords
        print("\n[Test 2] Querying Google News for 'BP oil spill'...")
        result2 = await service.query_google_news(
            facility_name="BP",
            company_name="British Petroleum",
            days_back=90
        )
        
        print(f"✓ Query successful!")
        print(f"  - Total articles: {result2.get('total_articles', 0)}")
        print(f"  - Negative articles: {result2.get('negative_articles', 0)}")
        
        # Test 3: Test evidence generation
        print("\n[Test 3] Testing evidence generation...")
        evidence_list = await service._query_google_news_with_evidence(
            claim_id="test_claim_001",
            facility_name="ExxonMobil Refinery",
            company_name="ExxonMobil"
        )
        
        print(f"✓ Evidence generation successful!")
        print(f"  - Evidence records: {len(evidence_list)}")
        for evidence in evidence_list:
            print(f"    - {evidence.source}: {evidence.signal_type}")
            print(f"      Signal: {evidence.signal_text[:80]}...")
            print(f"      Strength: {evidence.signal_strength}")
        
        # Test 4: Test parallel execution
        print("\n[Test 4] Testing parallel execution with NASA FIRMS...")
        test_claim = {
            "claim_id": "test_parallel_001",
            "facility_name": "Chevron Richmond Refinery",
            "company_name": "Chevron"
        }
        test_location = {
            "resolved": True,
            "latitude": 37.9297,
            "longitude": -122.3542
        }
        
        all_evidence = await service.collect_evidence_for_claim(
            claim=test_claim,
            facility_location=test_location
        )
        
        print(f"✓ Parallel execution successful!")
        print(f"  - Total evidence records: {len(all_evidence)}")
        for evidence in all_evidence:
            print(f"    - {evidence.source}: {evidence.signal_type}")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(test_google_news())

# Made with Bob
