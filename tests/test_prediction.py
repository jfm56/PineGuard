import pytest
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
from unittest.mock import MagicMock
from shapely.geometry import Point
from app.prediction import WildfirePredictor
from app.risk_category import RiskCategory

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    data = {
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
    }
    geometry = [Point(x, y) for x, y in zip(range(3), range(3))]
    return gpd.GeoDataFrame(data, geometry=geometry)

@pytest.fixture
def mock_predictor():
    """Create a mock predictor with mocked ML model"""
    model_path = Path("models/wildfire_predictor.pkl")
    predictor = WildfirePredictor(model_path)
    
    # Mock the ML model
    predictor.ml_model = MagicMock()
    predictor.ml_model.predict.return_value = pd.DataFrame({
        'risk_score': [0.3, 0.6, 0.8],
        'risk_category': [0.2, 0.6, 0.8]
    })
    
    # Mock the data loader
    predictor.data_loader = MagicMock()
    
    # Mock the structure analyzer
    predictor.structure_analyzer = MagicMock()
    predictor.structure_analyzer.analyze_structures = MagicMock(return_value=[
        {'id': 1, 'total_risk': 0.8}
    ])
    predictor.structure_analyzer.analyze_camping_sites = MagicMock(return_value=[
        {'id': 1, 'risk_score': 0.8}
    ])
    
    return predictor

def test_prediction_output_format(sample_data, mock_predictor):
    
    result = mock_predictor.predict_risk(sample_data)
    
    # Check basic output structure
    assert isinstance(result, gpd.GeoDataFrame)
    assert 'risk_score' in result.columns
    assert 'risk_category' in result.columns
    assert len(result) == len(sample_data)
    
    # Check value ranges and types
    assert all(0 <= score <= 1 for score in result['risk_score'])
    assert all(isinstance(cat, RiskCategory) for cat in result['risk_category'])
    
    # Check geometry preservation
    assert all(result.geometry == sample_data.geometry)

def test_feature_preparation(sample_data, mock_predictor):
    """Test feature preparation pipeline"""
    
    X = mock_predictor.prepare_features(sample_data)
    
    # Check dimensions
    assert X.shape[0] == len(sample_data)
    assert X.shape[1] == mock_predictor.n_features
    
    # Check data quality
    assert not X.isna().any().any()  # No missing values
    assert not np.isinf(X).any().any()  # No infinite values
    
    # Check feature scaling
    assert all(-5 <= X.mean()) and all(X.mean() <= 5)  # Reasonable means
    assert all(0 <= X.std()) and all(X.std() <= 5)  # Reasonable standard deviations

@pytest.mark.parametrize("risk_score,expected_category", [
    (0.1, RiskCategory.LOW),
    (0.4, RiskCategory.MODERATE),
    (0.8, RiskCategory.HIGH)
])
def test_risk_categorization(risk_score, expected_category, mock_predictor):
    """Test risk score to category conversion"""
    
    category = mock_predictor.get_risk_category(risk_score)
    assert category == expected_category

def test_invalid_input(sample_data, mock_predictor):
    """Test handling of invalid input data"""
    
    # Test with missing required column
    invalid_data = sample_data.drop(columns=['elevation'])
    with pytest.raises(ValueError, match=r".*Missing required features.*"):
        mock_predictor.predict_risk(invalid_data)
    
    # Test with invalid data types
    invalid_data = sample_data.copy()
    invalid_data['slope'] = 'invalid'
    with pytest.raises(ValueError, match=r".*Invalid data type.*"):
        mock_predictor.predict_risk(invalid_data)

def test_batch_prediction(sample_data, mock_predictor):
    """Test prediction on batches of data"""
    
    # Mock the ML model's predict method
    mock_predictions = pd.DataFrame({
        'risk_score': [0.3] * 300,
        'risk_category': [0.3] * 300
    })
    mock_predictor.ml_model.predict = MagicMock(return_value=mock_predictions)
    
    # Create a larger dataset
    large_data = gpd.GeoDataFrame(pd.concat([sample_data] * 100, ignore_index=True))
    
    result = mock_predictor.predict_risk(large_data)
    
    assert len(result) == len(large_data)
    assert all(isinstance(score, float) for score in result['risk_score'])
    assert all(isinstance(cat, RiskCategory) for cat in result['risk_category'])

def test_analyze_area_basic(sample_data, mock_predictor):
    """Test basic area analysis"""
    
    # Mock ML model predictions
    mock_predictions = pd.DataFrame({
        'risk_score': [0.3, 0.6, 0.8],
        'risk_category': [0.2, 0.6, 0.8]
    })
    mock_predictor.ml_model.predict = MagicMock(return_value=mock_predictions)
    
    # Mock satellite analyzer
    mock_predictor.cv_analyzer.analyze_vegetation = MagicMock(return_value={
        'ndvi_mean': 0.6,
        'ndvi_std': 0.1
    })
    
    # Create a dummy satellite image
    satellite_image = np.zeros((100, 100, 3))
    
    result = mock_predictor.analyze_area(
        area_data=sample_data,
        satellite_image=satellite_image,
        location_name="test area",
        analysis_mode="basic"
    )
    
    assert isinstance(result, dict)
    assert 'risk_predictions' in result
    assert 'analysis_mode' in result
    assert 'vegetation_analysis' in result
    assert result['analysis_mode'] == 'basic'

def test_analyze_area_professional(sample_data, tmp_path, mock_predictor):
    """Test professional area analysis"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create reference data directories
    ref_dir = data_dir / "reference"
    ref_dir.mkdir()
    
    # Create dummy reference files
    pd.DataFrame({
        'fuel_type': ['forest', 'grass'],
        'risk_factor': [0.8, 0.6]
    }).to_csv(ref_dir / 'fuel_types.csv')
    
    pd.DataFrame({
        'structure_type': ['house', 'barn'],
        'risk_factor': [0.7, 0.5]
    }).to_csv(ref_dir / 'structure_types.csv')
    
    # Mock ML model predictions and feature importance
    mock_predictions = pd.DataFrame({
        'risk_score': [0.3, 0.6, 0.8],
        'risk_category': [RiskCategory.LOW, RiskCategory.MODERATE, RiskCategory.HIGH]
    })
    mock_predictor.ml_model.predict = MagicMock(return_value=mock_predictions)
    mock_predictor.ml_model.get_feature_importance = MagicMock(return_value={
        'elevation': 0.3,
        'slope': 0.2
    })
    
    # Mock satellite analyzer
    mock_predictor.cv_analyzer.analyze_vegetation = MagicMock(return_value={
        'ndvi_mean': 0.6,
        'ndvi_std': 0.1
    })
    mock_predictor.cv_analyzer.detect_burn_scars = MagicMock(return_value={
        'burn_area': 0.1,
        'severity': 'low'
    })
    
    # Mock data loader
    mock_weather = pd.DataFrame({'temperature': [25, 28, 30]})
    mock_traffic = pd.DataFrame({'congestion_risk': [0.8, 0.9, 0.7]})
    mock_buildings = gpd.GeoDataFrame({'risk': [0.8, 0.9]}, geometry=[Point(0,0), Point(1,1)])
    mock_camping = gpd.GeoDataFrame({'risk_score': [0.8]}, geometry=[Point(0,0)])
    
    mock_predictor.data_loader.load_weather_data = MagicMock(return_value=mock_weather)
    mock_predictor.data_loader.load_traffic_data = MagicMock(return_value=mock_traffic)
    mock_predictor.data_loader.load_buildings = MagicMock(return_value=mock_buildings)
    mock_predictor.data_loader.load_camping_sites = MagicMock(return_value=mock_camping)
    
    # Mock structure and fuel analyzers
    mock_predictor.structure_analyzer.analyze_structures = MagicMock(return_value=[
        {'id': 1, 'total_risk': 0.8}
    ])
    mock_predictor.structure_analyzer.analyze_camping_sites = MagicMock(return_value=[
        {'id': 1, 'risk_score': 0.8}
    ])
    mock_predictor.fuel_analyzer.analyze_fuel_hazards = MagicMock(return_value={
        'fuel_load': 'high',
        'recommendations': ['Clear vegetation']
    })
    
    # Create a dummy satellite image
    satellite_image = np.zeros((100, 100, 3))
    
    result = mock_predictor.analyze_area(
        area_data=sample_data,
        satellite_image=satellite_image,
        location_name="test area",
        analysis_mode="professional"
    )
    
    assert isinstance(result, dict)
    assert 'risk_predictions' in result
    assert 'analysis_mode' in result
    assert 'feature_importance' in result
    assert 'vegetation_analysis' in result
    assert 'burn_analysis' in result
    assert 'structure_risks' in result
    assert 'camping_risks' in result
    assert 'traffic_analysis' in result
    assert 'fuel_hazards' in result
    assert result['analysis_mode'] == 'professional'

def test_generate_recommendations(sample_data, mock_predictor):
    """Test recommendation generation"""
    
    analysis_results = {
        'risk_predictions': {'risk_category': RiskCategory.HIGH},
        'structure_risks': [
            {'total_risk': 0.8, 'id': 1},
            {'total_risk': 0.9, 'id': 2}
        ],
        'camping_risks': [
            {'risk_score': 0.8, 'id': 1}
        ],
        'traffic_analysis': pd.DataFrame({'congestion_risk': [0.8, 0.9]}),
        'fuel_hazards': {
            'recommendations': ['Clear vegetation', 'Create firebreak']
        }
    }
    
    recommendations = mock_predictor._generate_recommendations(analysis_results)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    assert any('high-risk structures' in r.lower() for r in recommendations)
    assert any('camping' in r.lower() for r in recommendations)
    assert any('traffic' in r.lower() for r in recommendations)
    assert any('vegetation' in r.lower() for r in recommendations)

def test_model_save_load(sample_data, tmp_path, mock_predictor):
    """Test model saving and loading"""
    
    # Mock training data
    X = mock_predictor.prepare_features(sample_data)
    y = np.array([0, 1, 0])
    
    # Mock training results
    mock_metrics = {'accuracy': 0.9, 'f1': 0.85}
    mock_predictor.ml_model.train = MagicMock(return_value=mock_metrics)
    
    # Test training
    metrics = mock_predictor.train_model(X, y)
    assert isinstance(metrics, dict)
    assert 'accuracy' in metrics
    
    # Test save/load
    save_path = tmp_path / "test_model.pkl"
    mock_predictor.ml_model.save_model = MagicMock()
    mock_predictor.ml_model.load_model = MagicMock()
    
    mock_predictor.save_model(save_path)
    mock_predictor.load_model(save_path)
    
    mock_predictor.ml_model.save_model.assert_called_once_with(save_path)
    mock_predictor.ml_model.load_model.assert_called_once_with(save_path)
