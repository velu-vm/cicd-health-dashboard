#!/usr/bin/env python3
"""
Test script for CI/CD Health Dashboard API endpoints
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🔍 Testing: {description}")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Success!")
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
            except:
                print(f"   Response: {response.text}")
        else:
            print("   ❌ Failed!")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error - Is the server running?")
    except requests.exceptions.Timeout:
        print("   ❌ Timeout Error")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def main():
    print("🚀 Testing CI/CD Health Dashboard API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    test_endpoint("/health", description="Health Check")
    
    # Test metrics endpoint
    test_endpoint("/api/metrics/summary", description="Metrics Summary")
    
    # Test builds endpoint
    test_endpoint("/api/builds", description="List Builds")
    
    # Test builds with parameters
    test_endpoint("/api/builds?limit=5", description="List Builds (limit=5)")
    
    # Test seed endpoint
    test_endpoint("/api/seed", method="POST", data={}, description="Seed Database")
    
    # Test metrics again after seeding
    time.sleep(2)
    test_endpoint("/api/metrics/summary", description="Metrics Summary (after seeding)")
    
    # Test builds again after seeding
    test_endpoint("/api/builds", description="List Builds (after seeding)")
    
    # Test alert endpoint
    alert_data = {
        "message": "Test alert from API testing",
        "severity": "info",
        "alert_type": "email"
    }
    test_endpoint("/api/alert/test", method="POST", data=alert_data, description="Test Alert")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print(f"📅 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
