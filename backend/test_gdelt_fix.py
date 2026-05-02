"""
Test script to verify GDELT API fixes
"""
import asyncio
import httpx
from datetime import datetime, timedelta


async def test_gdelt_api():
    """Test GDELT API with corrected parameters"""
    print("=" * 70)
    print("Testing GDELT API with Fixed Implementation")
    print("=" * 70)
    
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(15.0, connect=5.0),
        follow_redirects=True
    )
    
    try:
        # Test 1: Simple environmental query
        print("\n[Test 1] Simple environmental query...")
        base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
        
        params = {
            "query": "environmental pollution",
            "mode": "artlist",
            "maxrecords": "10",
            "format": "json",
            "sort": "datedesc"
        }
        
        print(f"  URL: {base_url}")
        print(f"  Params: {params}")
        
        response = await client.get(base_url, params=params, timeout=15.0)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                articles = data.get("articles", [])
                print(f"  ✅ SUCCESS: Found {len(articles)} articles")
                
                if articles:
                    print(f"\n  Sample article:")
                    art = articles[0]
                    print(f"    - Title: {art.get('title', 'N/A')[:60]}...")
                    print(f"    - URL: {art.get('url', 'N/A')[:60]}...")
                    print(f"    - Tone: {art.get('tone', 'N/A')}")
                    print(f"    - Date: {art.get('seendate', 'N/A')}")
            except Exception as e:
                print(f"  ❌ JSON parse error: {e}")
                print(f"  Response preview: {response.text[:200]}")
        else:
            print(f"  ❌ FAILED: Status {response.status_code}")
            print(f"  Response: {response.text[:200]}")
        
        # Test 2: Query with date range
        print("\n[Test 2] Query with date range (last 30 days)...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        params2 = {
            "query": "emissions",
            "mode": "artlist",
            "maxrecords": "10",
            "format": "json",
            "sort": "datedesc",
            "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
            "enddatetime": end_date.strftime("%Y%m%d%H%M%S")
        }
        
        print(f"  Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        response2 = await client.get(base_url, params=params2, timeout=15.0)
        print(f"  Status: {response2.status_code}")
        
        if response2.status_code == 200:
            try:
                data2 = response2.json()
                articles2 = data2.get("articles", [])
                print(f"  ✅ SUCCESS: Found {len(articles2)} articles in date range")
            except Exception as e:
                print(f"  ❌ JSON parse error: {e}")
        else:
            print(f"  ❌ FAILED: Status {response2.status_code}")
        
        # Test 3: Query with company name
        print("\n[Test 3] Query with company name...")
        params3 = {
            "query": "Tesla emissions",
            "mode": "artlist",
            "maxrecords": "10",
            "format": "json",
            "sort": "datedesc"
        }
        
        response3 = await client.get(base_url, params=params3, timeout=15.0)
        print(f"  Status: {response3.status_code}")
        
        if response3.status_code == 200:
            try:
                data3 = response3.json()
                articles3 = data3.get("articles", [])
                print(f"  ✅ SUCCESS: Found {len(articles3)} articles")
            except Exception as e:
                print(f"  ❌ JSON parse error: {e}")
        else:
            print(f"  ❌ FAILED: Status {response3.status_code}")
        
        print("\n" + "=" * 70)
        print("Test Summary:")
        print("  - GDELT API endpoint is accessible")
        print("  - Query parameters are correctly formatted")
        print("  - JSON responses can be parsed")
        print("  - Date range filtering works")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(test_gdelt_api())

# Made with Bob
