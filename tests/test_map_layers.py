import pytest
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Polygon
from app.map_layers import MapLayer, load_base_layers, create_risk_layer

@pytest.fixture
def sample_data_dir(tmp_path):
    data_dir = tmp_path / "data" / "geo"
    data_dir.mkdir(parents=True)
    
    # Create sample GeoJSON files with actual geometries
    sample_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    
    land_use_gdf = gpd.GeoDataFrame(
        {"category": ["forest"], "geometry": [sample_polygon]}
    )
    fire_history_gdf = gpd.GeoDataFrame(
        {"year": [2024], "geometry": [sample_polygon]}
    )
    vegetation_gdf = gpd.GeoDataFrame(
        {"type": ["dense"], "geometry": [sample_polygon]}
    )
    
    land_use_gdf.to_file(data_dir / "land_use.geojson", driver="GeoJSON")
    fire_history_gdf.to_file(data_dir / "fire_history.geojson", driver="GeoJSON")
    vegetation_gdf.to_file(data_dir / "vegetation.geojson", driver="GeoJSON")
    
    return data_dir

def test_load_base_layers(sample_data_dir):
    # Call load_base_layers with the sample data directory
    layers = load_base_layers(data_dir=sample_data_dir)
    assert len(layers) == 3
    
    # Check land use layer
    land_use = layers[0]
    assert isinstance(land_use, MapLayer)
    assert land_use.name == "Land Use"
    assert land_use.style["fillColor"] == "category"
    assert land_use.style["fillOpacity"] == 0.7
    assert land_use.style["weight"] == 1
    assert isinstance(land_use.data, gpd.GeoDataFrame)
    
    # Check fire history layer
    fire_history = layers[1]
    assert isinstance(fire_history, MapLayer)
    assert fire_history.name == "Historical Fires"
    assert fire_history.style["color"] == "red"
    assert fire_history.style["fillOpacity"] == 0.5
    assert fire_history.style["weight"] == 2
    assert isinstance(fire_history.data, gpd.GeoDataFrame)
    
    # Check vegetation layer
    vegetation = layers[2]
    assert isinstance(vegetation, MapLayer)
    assert vegetation.name == "Vegetation"
    assert vegetation.style["fillColor"] == "category"
    assert vegetation.style["fillOpacity"] == 0.6
    assert vegetation.style["weight"] == 1
    assert isinstance(vegetation.data, gpd.GeoDataFrame)

def test_create_risk_layer():
    # Create sample risk predictions
    sample_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    risk_predictions = gpd.GeoDataFrame(
        {
            "risk_score": [0.75, 0.25, 0.90],
            "geometry": [sample_polygon] * 3
        }
    )
    
    layer = create_risk_layer(risk_predictions)
    assert isinstance(layer, MapLayer)
    assert layer.name == "Wildfire Risk"
    assert layer.data is risk_predictions
    assert layer.style["fillColor"] == "risk_score"
    assert layer.style["colormap"] == "RdYlGn_r"
    assert layer.style["fillOpacity"] == 0.7
    assert layer.style["weight"] == 1

def test_maplayer_validation():
    with pytest.raises(ValueError, match="Either data or data_path must be provided"):
        MapLayer(name="Invalid Layer")
