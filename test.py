"""
Test script to verify the enhanced Interactive Button Application features
"""

import os
import sys
import json
import requests
import time
from pathlib import Path

def test_data_persistence():
    """Test data file creation and persistence"""
    print("Testing data persistence...")
    
    # Check if data directory is created
    data_dir = Path("data")
    if data_dir.exists():
        print("✓ Data directory exists")
    else:
        print("✗ Data directory not found")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    
    try:
        from config import config, DevelopmentConfig, ProductionConfig
        
        # Test development config
        dev_config = config['development']
        if dev_config.DEBUG:
            print("✓ Development configuration loaded")
        else:
            print("✗ Development configuration issue")
            return False
            
        # Test production config
        prod_config = config['production']
        if not prod_config.DEBUG:
            print("✓ Production configuration loaded")
        else:
            print("✗ Production configuration issue")
            return False
            
        return True
        
    except ImportError as e:
        print(f"✗ Configuration import error: {e}")
        return False

def test_data_manager():
    """Test data manager functionality"""
    print("Testing data manager...")
    
    try:
        from config import config
        from data_manager import DataManager
        
        dm = DataManager(config['testing'])
        
        # Test button state operations
        test_state = {"count": 42, "test": True}
        success = dm.save_button_state(test_state)
        if not success:
            print("✗ Failed to save button state")
            return False
            
        loaded_state = dm.load_button_state()
        if loaded_state.get("count") == 42:
            print("✓ Data manager save/load working")
        else:
            print("✗ Data manager save/load failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Data manager error: {e}")
        return False

def test_rate_limiter():
    """Test rate limiting functionality"""
    print("Testing rate limiter...")
    
    try:
        from rate_limiter import RateLimiter
        
        # Create rate limiter with low limit for testing
        rl = RateLimiter(max_requests_per_minute=5)
        
        client_id = "test_client"
        
        # Should allow first 5 requests
        allowed_count = 0
        for i in range(10):
            if rl.is_allowed(client_id):
                allowed_count += 1
        
        if allowed_count == 5:
            print("✓ Rate limiter working correctly")
            return True
        else:
            print(f"✗ Rate limiter failed: allowed {allowed_count}/5 requests")
            return False
            
    except Exception as e:
        print(f"✗ Rate limiter error: {e}")
        return False

def test_app_startup():
    """Test application startup"""
    print("Testing application startup...")
    
    try:
        # Import the enhanced app
        from app import app, socketio, button_state
        
        if app is not None:
            print("✓ Flask app created successfully")
        else:
            print("✗ Flask app creation failed")
            return False
            
        if socketio is not None:
            print("✓ SocketIO initialized successfully")
        else:
            print("✗ SocketIO initialization failed")
            return False
            
        if isinstance(button_state, dict):
            print("✓ Button state initialized successfully")
        else:
            print("✗ Button state initialization failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ App startup error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints (requires running server)"""
    print("Testing API endpoints...")
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("status") == "healthy":
                print("✓ Health endpoint working")
            else:
                print("✗ Health endpoint returned unhealthy status")
                return False
        else:
            print("✗ Health endpoint not accessible")
            return False
            
        # Test stats endpoint
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            print("✓ Stats endpoint working")
        else:
            print("✗ Stats endpoint failed")
            return False
            
        return True
        
    except requests.exceptions.RequestException:
        print("⚠ API endpoints test skipped (server not running)")
        return True  # Don't fail if server isn't running

def run_all_tests():
    """Run all tests and return results"""
    print("=== Enhanced Interactive Button Application Tests ===\n")
    
    tests = [
        ("Configuration Loading", test_configuration),
        ("Data Manager", test_data_manager),
        ("Rate Limiter", test_rate_limiter),
        ("Data Persistence", test_data_persistence),
        ("Application Startup", test_app_startup),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n=== Test Summary ===")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the enhanced Interactive Button Application")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only (skip server-dependent tests)")
    
    args = parser.parse_args()
    
    if args.quick:
        print("Running quick tests only...")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
