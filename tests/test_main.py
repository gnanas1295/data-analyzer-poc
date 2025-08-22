from fastapi.testclient import TestClient
from src.main import app, get_container
from unittest.mock import MagicMock

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "VRAI Simulation Data Analyzer"}

def test_analyze_data():
    mock_container = MagicMock()
    app.dependency_overrides[get_container] = lambda: mock_container

    request_data = {
        "trainee_id": "test-pilot",
        "simulation_log": [
            {"timestamp": 0.0, "altitude": 5000, "speed": 250, "event": "start"},
            {"timestamp": 2.5, "altitude": 4500, "speed": 280, "event": "turbulence"},
            {"timestamp": 5.0, "altitude": 4000, "speed": 310, "event": "overspeed"}
        ]
    }
    response = client.post("/analyze", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["trainee_id"] == "test-pilot"
    assert "id" in response_data
    assert response_data["analysis_summary"]["performance_score"] == 80
    assert response_data["analysis_summary"]["total_duration_seconds"] == 5.0
    assert response_data["analysis_summary"]["average_speed"] == 280.0
    assert response_data["analysis_summary"]["critical_events"]["overspeed_incidents"] == 1
    mock_container.create_item.assert_called_once()

    app.dependency_overrides = {}
