import pytest
from app.ml.ensemble_wildfire_model import EnsembleWildfireModel
from app.cv.satellite_analyzer import SatelliteAnalyzer
from app.risk_analysis.fuel_analyzer import FuelAnalyzer
from app.risk_analysis.structure_analyzer import StructureAnalyzer
from app.data_processing.data_loader import DataLoader
from pathlib import Path
import numpy as np

@pytest.fixture
def test_data_dir():
    return Path("tests/data")

@pytest.fixture
def model(test_data_dir):
    return EnsembleWildfireModel(test_data_dir / "models")

@pytest.fixture
def satellite_analyzer():
    return SatelliteAnalyzer()

@pytest.fixture
def fuel_analyzer(test_data_dir):
    return FuelAnalyzer(test_data_dir)

@pytest.fixture
def structure_analyzer(test_data_dir):
    return StructureAnalyzer(test_data_dir)

@pytest.fixture
def data_loader(test_data_dir):
    return DataLoader(test_data_dir)

def test_end_to_end_prediction(model, satellite_analyzer, fuel_analyzer, structure_analyzer, data_loader):
    # Test area coordinates (Pine Barrens region)
    test_area = {
        "type": "Polygon",
        "coordinates": [[
            [-74.5, 39.8],
            [-74.5, 39.9],
            [-74.4, 39.9],
            [-74.4, 39.8],
            [-74.5, 39.8]
        ]]
    }
    
    # Load environmental data
    env_data = data_loader.load_environmental_data(test_area)
    assert env_data is not None
    assert "temperature" in env_data
    assert "humidity" in env_data
    assert "wind_speed" in env_data
    
    # Analyze satellite imagery
    satellite_data = satellite_analyzer.analyze_area(test_area)
    assert satellite_data is not None
    assert "ndvi" in satellite_data
    assert "land_cover" in satellite_data
    
    # Analyze fuel conditions
    fuel_data = fuel_analyzer.analyze_area(test_area)
    assert fuel_data is not None
    assert "fuel_type" in fuel_data
    assert "fuel_moisture" in fuel_data
    
    # Analyze structures
    structure_data = structure_analyzer.analyze_area(test_area)
    assert structure_data is not None
    assert "buildings" in structure_data
    assert "infrastructure" in structure_data
    
    # Combine all features
    features = {
        "environmental": env_data,
        "satellite": satellite_data,
        "fuel": fuel_data,
        "structure": structure_data
    }
    
    # Get prediction
    prediction = model.predict(features)
    assert isinstance(prediction, dict)
    assert "risk_score" in prediction
    assert 0 <= prediction["risk_score"] <= 1
    assert "confidence" in prediction
    assert "risk_factors" in prediction

def test_data_pipeline_integrity(data_loader):
    # Test data loading pipeline
    weather_data = data_loader.load_weather_data()
    assert weather_data is not None
    assert not np.isnan(weather_data).any()
    
    satellite_data = data_loader.load_satellite_data()
    assert satellite_data is not None
    assert not np.isnan(satellite_data).any()
    
    historical_fires = data_loader.load_historical_fires()
    assert historical_fires is not None
    assert len(historical_fires) > 0

def test_model_ensemble_consistency(model):
    # Test that ensemble predictions are consistent
    test_features = {
        "temperature": 25.0,
        "humidity": 40.0,
        "wind_speed": 15.0,
        "ndvi": 0.6,
        "fuel_moisture": 0.3
    }
    
    # Multiple predictions should be similar
    predictions = [model.predict(test_features)["risk_score"] for _ in range(5)]
    assert max(predictions) - min(predictions) < 0.1  # Check consistency

def test_alert_system_integration(model, data_loader):
    # Test alert generation based on predictions
    high_risk_features = {
        "temperature": 35.0,
        "humidity": 20.0,
        "wind_speed": 30.0,
        "ndvi": 0.2,
        "fuel_moisture": 0.1
    }
    
    prediction = model.predict(high_risk_features)
    assert prediction["risk_score"] > 0.7  # Should trigger high-risk alert
    
    # Test alert delivery system
    alerts = model.generate_alerts(prediction)
    assert len(alerts) > 0
    assert any(alert["priority"] == "high" for alert in alerts)
