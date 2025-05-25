import pytest
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_limiter():
    app.state.limiter.reset()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_regions():
    response = client.get("/api/v1/regions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "regions" in data
    assert isinstance(data["regions"], list)

def test_predict_invalid_mode():
    body = {"area_geometry": {"coordinates": [[[-74, 39], [-74, 39]]]}, "date": "2025-01-01"}
    response = client.post("/api/v1/predict?analysis_mode=invalid", json=body)
    assert response.status_code == 400
    assert "Invalid analysis mode" in response.json().get("detail", "")

def test_predict_basic():
    body = {"area_geometry": {"coordinates": [[[-74, 39], [-74, 39]]]}, "date": "2025-01-01"}
    response = client.post("/api/v1/predict?analysis_mode=basic", json=body)
    assert response.status_code == 200
    data = response.json()
    for key in ["risk_score", "confidence", "risk_factors", "environmental_factors", "historical_data", "infrastructure_risk", "mitigation_recommendations", "timestamp"]:
        assert key in data

def test_predict_professional():
    coords = [[[-74.5, 39.8], [-74.5, 39.8]]]
    body = {"area_geometry": {"coordinates": coords}, "date": "2025-01-01"}
    response = client.post("/api/v1/predict?analysis_mode=professional", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data.get("historical_data")
    assert data.get("environmental_factors").get("precipitation") is not None

def test_log_frontend_error():
    payload = {"message": "err", "details": "det", "stack": "st"}
    response = client.post("/api/v1/log-error", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "logged"}

def test_get_camping_site_risk():
    response = client.get("/api/v1/camping-sites/XYZ/risk")
    assert response.status_code == 200
    data = response.json()
    for key in ["site_risk", "max_capacity", "evacuation_time"]:
        assert key in data

def test_analyze_structures():
    payload = {"foo": "bar"}
    response = client.post("/api/v1/structures/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("buildings"), list)

def test_analyze_traffic():
    response = client.get("/api/v1/traffic/analysis?area=test")
    assert response.status_code == 200
    data = response.json()
    for key in ["current_flow", "evacuation_capacity", "recommended_routes"]:
        assert key in data

def test_get_current_weather():
    response = client.get("/api/v1/weather/current")
    assert response.status_code == 200
    data = response.json()
    for key in ["temperature", "humidity", "wind_speed", "conditions", "timestamp", "location"]:
        assert key in data
