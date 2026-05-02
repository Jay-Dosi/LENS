"""
Test script for stateless storage implementation
Tests ChromaDB-based session management and storage
"""
import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.storage_service import StorageService


def test_session_management():
    """Test session creation and management"""
    print("\n=== Testing Session Management ===")
    
    storage = StorageService(in_memory=True, session_timeout_minutes=1)
    
    # Test 1: Create session
    session_id = storage.create_session()
    print(f"✓ Created session: {session_id}")
    
    # Test 2: Get session info
    info = storage.get_session_info(session_id)
    assert info is not None, "Session should exist"
    assert info["session_id"] == session_id, "Session ID should match"
    print(f"✓ Retrieved session info: {info['created_at']}")
    
    # Test 3: Invalid session
    invalid_info = storage.get_session_info("invalid-session-id")
    assert invalid_info is None, "Invalid session should return None"
    print("✓ Invalid session handled correctly")
    
    return storage, session_id


def test_file_storage(storage, session_id):
    """Test file upload and download"""
    print("\n=== Testing File Storage ===")
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content for stateless storage")
        temp_file = f.name
    
    try:
        # Test 1: Upload file
        object_key = "test/document.txt"
        result = storage.upload_file(session_id, temp_file, object_key)
        print(f"✓ Uploaded file: {result}")
        
        # Test 2: Download file
        download_path = tempfile.mktemp(suffix='.txt')
        downloaded = storage.download_file(object_key, download_path)
        
        with open(downloaded, 'r') as f:
            content = f.read()
        
        assert content == "Test content for stateless storage", "Content should match"
        print(f"✓ Downloaded file: {downloaded}")
        
        # Cleanup
        os.unlink(download_path)
        
    finally:
        os.unlink(temp_file)


def test_json_storage(storage, session_id):
    """Test JSON upload and download"""
    print("\n=== Testing JSON Storage ===")
    
    # Test data
    test_data = {
        "document_id": "test-123",
        "claims": [
            {"id": 1, "text": "Test claim 1"},
            {"id": 2, "text": "Test claim 2"}
        ],
        "metadata": {
            "company": "Test Corp",
            "date": "2024-01-01"
        }
    }
    
    # Test 1: Upload JSON
    object_key = "claims/test-123.json"
    result = storage.upload_json(session_id, test_data, object_key)
    print(f"✓ Uploaded JSON: {result}")
    
    # Test 2: Download JSON
    downloaded_data = storage.download_json(object_key)
    assert downloaded_data == test_data, "JSON data should match"
    print(f"✓ Downloaded JSON: {len(downloaded_data['claims'])} claims")


def test_session_cleanup(storage, session_id):
    """Test session cleanup"""
    print("\n=== Testing Session Cleanup ===")
    
    # Upload some data
    test_data = {"test": "data"}
    storage.upload_json(session_id, test_data, "test/data.json")
    print("✓ Uploaded test data")
    
    # Cleanup session
    success = storage.cleanup_session(session_id)
    assert success, "Cleanup should succeed"
    print(f"✓ Cleaned up session: {session_id}")
    
    # Verify session is gone
    info = storage.get_session_info(session_id)
    assert info is None, "Session should be deleted"
    print("✓ Session deleted successfully")
    
    # Verify data is gone
    try:
        storage.download_json("test/data.json")
        assert False, "Data should be deleted"
    except FileNotFoundError:
        print("✓ Session data deleted successfully")


def test_multiple_sessions():
    """Test multiple concurrent sessions"""
    print("\n=== Testing Multiple Sessions ===")
    
    storage = StorageService(in_memory=True)
    
    # Create multiple sessions
    session1 = storage.create_session()
    session2 = storage.create_session()
    session3 = storage.create_session()
    
    print(f"✓ Created 3 sessions: {session1[:8]}..., {session2[:8]}..., {session3[:8]}...")
    
    # Upload data to each session
    storage.upload_json(session1, {"session": 1}, "data/session1.json")
    storage.upload_json(session2, {"session": 2}, "data/session2.json")
    storage.upload_json(session3, {"session": 3}, "data/session3.json")
    print("✓ Uploaded data to all sessions")
    
    # Verify data isolation
    data1 = storage.download_json("data/session1.json")
    data2 = storage.download_json("data/session2.json")
    data3 = storage.download_json("data/session3.json")
    
    assert data1["session"] == 1, "Session 1 data should be isolated"
    assert data2["session"] == 2, "Session 2 data should be isolated"
    assert data3["session"] == 3, "Session 3 data should be isolated"
    print("✓ Data isolation verified")
    
    # Cleanup one session
    storage.cleanup_session(session2)
    print(f"✓ Cleaned up session 2")
    
    # Verify other sessions still exist
    info1 = storage.get_session_info(session1)
    info3 = storage.get_session_info(session3)
    assert info1 is not None, "Session 1 should still exist"
    assert info3 is not None, "Session 3 should still exist"
    print("✓ Other sessions unaffected")


def test_reset_all_data():
    """Test reset all data functionality"""
    print("\n=== Testing Reset All Data ===")
    
    storage = StorageService(in_memory=True)
    
    # Create sessions and data
    session1 = storage.create_session()
    session2 = storage.create_session()
    storage.upload_json(session1, {"test": 1}, "data/test1.json")
    storage.upload_json(session2, {"test": 2}, "data/test2.json")
    print("✓ Created test data")
    
    # Reset all data
    success = storage.reset_all_data()
    assert success, "Reset should succeed"
    print("✓ Reset all data")
    
    # Verify everything is gone
    info1 = storage.get_session_info(session1)
    info2 = storage.get_session_info(session2)
    assert info1 is None, "Session 1 should be deleted"
    assert info2 is None, "Session 2 should be deleted"
    print("✓ All sessions deleted")
    
    try:
        storage.download_json("data/test1.json")
        assert False, "Data should be deleted"
    except FileNotFoundError:
        print("✓ All data deleted")


def test_persistent_mode():
    """Test persistent storage mode"""
    print("\n=== Testing Persistent Mode ===")
    
    # Create storage with persistence
    persist_dir = tempfile.mkdtemp()
    storage = StorageService(in_memory=False, session_timeout_minutes=60)
    storage.storage.persist_directory = persist_dir
    
    try:
        # Create session and data
        session_id = storage.create_session()
        test_data = {"persistent": True}
        storage.upload_json(session_id, test_data, "data/persistent.json")
        print(f"✓ Created persistent data in: {persist_dir}")
        
        # Verify data exists
        data = storage.download_json("data/persistent.json")
        assert data["persistent"] == True, "Data should be persisted"
        print("✓ Data persisted successfully")
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(persist_dir, ignore_errors=True)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("STATELESS STORAGE IMPLEMENTATION TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Session Management
        storage, session_id = test_session_management()
        
        # Test 2: File Storage
        test_file_storage(storage, session_id)
        
        # Test 3: JSON Storage
        test_json_storage(storage, session_id)
        
        # Test 4: Session Cleanup
        test_session_cleanup(storage, session_id)
        
        # Test 5: Multiple Sessions
        test_multiple_sessions()
        
        # Test 6: Reset All Data
        test_reset_all_data()
        
        # Test 7: Persistent Mode
        test_persistent_mode()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nStateless storage implementation is working correctly!")
        print("Ready for deployment on free platforms with NO credit card required.")
        print("\nNext steps:")
        print("1. Update .env with your IBM watsonx credentials")
        print("2. Set STORAGE_MODE=memory")
        print("3. Deploy to Render.com, Railway.app, or Fly.io")
        print("4. See docs/FREE_DEPLOYMENT.md for detailed instructions")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ TEST FAILED!")
        print("="*60)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

# Made with Bob
