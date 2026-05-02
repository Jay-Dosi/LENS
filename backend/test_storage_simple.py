"""
Simple standalone test for ChromaDB storage
Tests core functionality without requiring all dependencies
"""
import sys
import os
import json
import tempfile
import uuid
from datetime import datetime, timedelta

print("\n" + "="*60)
print("CHROMADB STORAGE - SIMPLE TEST")
print("="*60)

# Test 1: Import ChromaDB
print("\n[1/6] Testing ChromaDB import...")
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    print("✓ ChromaDB imported successfully")
except ImportError as e:
    print(f"✗ ChromaDB import failed: {e}")
    print("\nPlease install ChromaDB:")
    print("  pip install chromadb==0.4.22")
    sys.exit(1)

# Test 2: Initialize in-memory ChromaDB
print("\n[2/6] Testing in-memory ChromaDB initialization...")
try:
    client = chromadb.Client(ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    ))
    print("✓ In-memory ChromaDB initialized")
except Exception as e:
    print(f"✗ Initialization failed: {e}")
    sys.exit(1)

# Test 3: Create collection
print("\n[3/6] Testing collection creation...")
try:
    collection = client.get_or_create_collection("test_collection")
    print(f"✓ Collection created: {collection.name}")
except Exception as e:
    print(f"✗ Collection creation failed: {e}")
    sys.exit(1)

# Test 4: Store and retrieve data
print("\n[4/6] Testing data storage and retrieval...")
try:
    # Store data
    test_data = {
        "session_id": str(uuid.uuid4()),
        "document_id": "test-123",
        "timestamp": datetime.now().isoformat()
    }
    
    collection.add(
        ids=["test-doc-1"],
        documents=[json.dumps(test_data)],
        metadatas=[{"session_id": test_data["session_id"]}]
    )
    print("✓ Data stored successfully")
    
    # Retrieve data
    result = collection.get(ids=["test-doc-1"])
    retrieved_data = json.loads(result["documents"][0])
    
    assert retrieved_data["document_id"] == "test-123", "Data mismatch"
    print("✓ Data retrieved successfully")
    print(f"  Retrieved: {retrieved_data['document_id']}")
    
except Exception as e:
    print(f"✗ Data operations failed: {e}")
    sys.exit(1)

# Test 5: Session-based filtering
print("\n[5/6] Testing session-based data isolation...")
try:
    session1 = str(uuid.uuid4())
    session2 = str(uuid.uuid4())
    
    # Add data for session 1
    collection.add(
        ids=["session1-doc1"],
        documents=[json.dumps({"data": "session1"})],
        metadatas=[{"session_id": session1}]
    )
    
    # Add data for session 2
    collection.add(
        ids=["session2-doc1"],
        documents=[json.dumps({"data": "session2"})],
        metadatas=[{"session_id": session2}]
    )
    
    # Query session 1 data
    session1_data = collection.get(where={"session_id": session1})
    assert len(session1_data["ids"]) == 1, "Should have 1 document for session 1"
    print(f"✓ Session isolation working")
    print(f"  Session 1: {len(session1_data['ids'])} documents")
    
    # Delete session 1 data
    collection.delete(ids=session1_data["ids"])
    
    # Verify session 2 data still exists
    session2_data = collection.get(where={"session_id": session2})
    assert len(session2_data["ids"]) == 1, "Session 2 data should still exist"
    print("✓ Session cleanup working")
    
except Exception as e:
    print(f"✗ Session operations failed: {e}")
    sys.exit(1)

# Test 6: Reset functionality
print("\n[6/6] Testing reset functionality...")
try:
    # Add some data
    collection.add(
        ids=["reset-test-1"],
        documents=[json.dumps({"test": "reset"})],
        metadatas=[{"type": "test"}]
    )
    
    # Reset client
    client.reset()
    print("✓ ChromaDB reset successful")
    
    # Verify data is gone
    new_client = chromadb.Client(ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    ))
    new_collection = new_client.get_or_create_collection("test_collection")
    result = new_collection.get()
    
    assert len(result["ids"]) == 0, "Collection should be empty after reset"
    print("✓ Data cleared after reset")
    
except Exception as e:
    print(f"✗ Reset failed: {e}")
    sys.exit(1)

# Success!
print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nChromaDB is working correctly for stateless storage!")
print("\nKey Features Verified:")
print("  ✓ In-memory storage (no external services)")
print("  ✓ Session-based data isolation")
print("  ✓ Automatic cleanup capability")
print("  ✓ Reset functionality for demos")
print("\nReady for deployment on FREE platforms:")
print("  • Render.com")
print("  • Railway.app")
print("  • Fly.io")
print("  • Replit")
print("\nSee docs/FREE_DEPLOYMENT.md for deployment instructions.")
print("="*60 + "\n")

# Made with Bob
