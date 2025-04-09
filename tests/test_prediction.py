import pytest
import geopandas as gpd
from pathlib import Path
from app.prediction import WildfirePredictor

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return gpd.GeoDataFrame({
        'elevation': [100, 200, 300],
        'slope': [5, 10, 15],
        'aspect': [90, 180, 270],
        'vegetation_type': ['forest', 'shrub', 'grass'],
        'soil_moisture': [0.2, 0.3, 0.4],
        'distance_to_roads': [500, 1000, 1500],
        'distance_to_power_lines': [200, 400, 600],
        'temperature': [25, 28, 30],
        'humidity': [60, 55, 50],
        'wind_speed': [10, 15, 20]
    })

def test_prediction_output_format(sample_data):
    """Test that the prediction output has the correct format"""
    model_path = Path("models/wildfire_predictor.pkl")
    predictor = WildfirePredictor(model_path)
    
    result = predictor.predict_risk(sample_data)
    
    assert 'risk_score' in result.columns
    assert 'risk_category' in result.columns
    assert len(result) == len(sample_data)
    assert all(0 <= score <= 1 for score in result['risk_score'])

def test_feature_preparation(sample_data):
    """Test feature preparation pipeline"""
    model_path = Path("models/wildfire_predictor.pkl")
    predictor = WildfirePredictor(model_path)
    
    X = predictor.prepare_features(sample_data)
    
    assert X.shape[0] == len(sample_data)
    assert not X.isna().any().any()  # No missing values
