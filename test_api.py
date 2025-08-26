# API Test Script for VRAI Data Analyzer
# Run this script to test your deployed application

import requests
import json
import sys
from datetime import datetime


def test_api(base_url):
    """Test the deployed VRAI Data Analyzer API"""

    print(f"🧪 Testing API at: {base_url}")
    print("=" * 50)

    # Test 1: Health Check
    print("1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

    print()

    # Test 2: API Documentation
    print("2. Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ API docs accessible!")
            print(f"   Docs URL: {base_url}/docs")
        else:
            print(f"   ⚠️ API docs returned status {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ API docs not accessible: {e}")

    print()

    # Test 3: Analysis Endpoint
    print("3. Testing analysis endpoint...")

    test_data = {
        "trainee_id": f"test-pilot-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "simulation_log": [
            {"timestamp": 0.0, "altitude": 5000, "speed": 250, "event": "start"},
            {"timestamp": 2.5, "altitude": 4500, "speed": 280, "event": "turbulence"},
            {"timestamp": 5.0, "altitude": 4000, "speed": 310, "event": "overspeed"},
            {"timestamp": 7.5, "altitude": 3500, "speed": 295, "event": "correction"},
            {"timestamp": 10.0, "altitude": 3000, "speed": 270, "event": "approach"},
        ],
    }

    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if response.status_code == 200:
            print("   ✅ Analysis endpoint working!")
            result = response.json()

            print("   📊 Analysis Results:")
            print(f"      Trainee ID: {result.get('trainee_id')}")

            analysis = result.get("analysis_summary", {})
            print(f"      Performance Score: {analysis.get('performance_score')}")
            print(
                f"      Total Duration: {analysis.get('total_duration_seconds')} seconds"
            )
            print(f"      Average Speed: {analysis.get('average_speed')} mph")

            critical_events = analysis.get("critical_events", {})
            print(
                f"      Overspeed Incidents: {critical_events.get('overspeed_incidents')}"
            )
            print(
                f"      Unstable Approach Events: {critical_events.get('unstable_approach_events')}"
            )

            # Check if data was saved
            save_status = analysis.get("save_status")
            if save_status:
                if save_status.get("saved"):
                    print(
                        f"   ✅ Data saved to Cosmos DB with ID: {save_status.get('id')}"
                    )
                else:
                    print(f"   ⚠️ Data not saved: {save_status.get('reason')}")

        else:
            print(f"   ❌ Analysis endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ Analysis endpoint failed: {e}")
        return False

    print()
    print("🎉 All tests completed successfully!")
    print(f"🌐 Your API is running at: {base_url}")
    print(f"📚 API Documentation: {base_url}/docs")

    return True


def main():
    """Main function to run API tests"""

    if len(sys.argv) != 2:
        print("Usage: python test_api.py <base_url>")
        print("Example: python test_api.py https://vrai-analyzer-dev.azurewebsites.net")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")

    print("🚀 VRAI Data Analyzer API Test")
    print("=" * 50)
    print(f"Target URL: {base_url}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    success = test_api(base_url)

    if success:
        print("\n✅ All tests passed! Your API is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
