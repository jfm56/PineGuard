import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_risk_prediction(client):
    test_area = {
        "area_geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-74.5, 39.8],
                [-74.5, 39.9],
                [-74.4, 39.9],
                [-74.4, 39.8],
                [-74.5, 39.8]
            ]]
        },
        "date": "2025-04-08"
    }
   
    response = client.post("/api/v1/predict", json=test_area)
    assert response.status_code == 200
   
    data = response.json()
    assert "risk_score" in data
    assert 0 <= data["risk_score"] <= 1
    assert "confidence" in data
    assert "risk_factors" in data

def test_camping_site_analysis(client):
    site_id = "TEST001"
    response = client.get(f"/api/v1/camping-sites/{site_id}/risk")
    assert response.status_code == 200
   
    data = response.json()
    assert "site_risk" in data
    assert "max_capacity" in data
    assert "evacuation_time" in data

def test_structure_analysis(client):
    test_buildings = {
        "buildings": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-74.5, 39.8],
                        [-74.5, 39.81],
                        [-74.49, 39.81],
                        [-74.49, 39.8],
                        [-74.5, 39.8]
                    ]]
                },
                "properties": {
                    "id": "B001",
                    "type": "residential"
                }
            }]
        },
        "buffer_zone": 100,
        "include_surroundings": True
    }
   
    response = client.post("/api/v1/structures/analyze", json=test_buildings)
    assert response.status_code == 200
   
    data = response.json()
    assert "buildings" in data
    assert len(data["buildings"]) > 0
    assert "risk_score" in data["buildings"][0]

def test_traffic_analysis(client):
    area_id = "AREA001"
    response = client.get(f"/api/v1/traffic/analysis?area={area_id}")
    assert response.status_code == 200
   
    data = response.json()
    assert "current_flow" in data
    assert "evacuation_capacity" in data
    assert "recommended_routes" in data

@pytest.mark.parametrize("invalid_area", [
    {"area_geometry": None},
    {"area_geometry": "invalid"},
    {"date": "2025-13-45"},
])
def test_invalid_risk_prediction(client, invalid_area):
    response = client.post("/api/v1/predict", json=invalid_area)
    assert response.status_code == 422

def test_rate_limiting(client):
    # Reset rate limiter before test
    app.state.limiter.reset()
   
    # First 10 requests should succeed
    for _ in range(10):
        response = client.get("/health")
        assert response.status_code == 200
   
    # 11th request should fail with 429 Too Many Requests
    response = client.get("/health")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text
