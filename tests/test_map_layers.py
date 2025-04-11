import pytest
import geopandas as gpd
from shapely.geometry import Point, Polygon
from app.map_layers import (
    MapLayer,
    load_base_layers,
    create_risk_layer,
    create_infrastructure_layers,
    generate_sample_risk_predictions
)


@pytest.fixture
def sample_data_dir(tmp_path):
    data_dir = tmp_path / "data" / "geo"
    data_dir.mkdir(parents=True)

    # Create sample GeoJSON files with actual geometries
    sample_polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])

    land_use_gdf = gpd.GeoDataFrame(
        {"category": ["forest"], "geometry": [sample_polygon]})
    fire_history_gdf = gpd.GeoDataFrame(
        {"year": [2024], "geometry": [sample_polygon]})
    vegetation_gdf = gpd.GeoDataFrame(
        {"type": ["dense"], "geometry": [sample_polygon]})

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
    # Test with GeoDataFrame input
    sample_point = Point(39.7825, -74.5338)
    risk_predictions = gpd.GeoDataFrame(
        {
            "risk_level": ["High", "Moderate"],
            "severity": [2.5, 1.5],
            "geometry": [sample_point] * 2
        },
        crs="EPSG:4326"
    )

    layer = create_risk_layer(risk_predictions)
    assert isinstance(layer, MapLayer)
    assert layer.name == "Wildfire Risk"
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.style["fillColor"] == "risk_level"
    assert isinstance(layer.style["colormap"], dict)
    assert layer.style["fillOpacity"] == 0.7
    assert layer.style["weight"] == 1
    assert layer.style["radius"] == "severity"

    # Test with list of dictionaries input
    risk_areas = [
        {
            'coords': [39.7825, -74.5338],
            'risk_level': 'High',
            'severity': 2.5,
            'factors': [
                {'name': 'Vegetation Dryness', 'value': 'Critical'}
            ]
        }
    ]

    layer = create_risk_layer(risk_areas)
    assert isinstance(layer, MapLayer)
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.crs == "EPSG:4326"

    # Test with no input (should use sample data)
    layer = create_risk_layer()
    assert isinstance(layer, MapLayer)
    assert isinstance(layer.data, gpd.GeoDataFrame)
    assert layer.data.crs == "EPSG:4326"


def test_maplayer_validation():
    with pytest.raises(
            ValueError,
            match="Either data or data_path must be provided"):
        MapLayer(name="Invalid Layer")


def test_generate_sample_risk_predictions():
    risk_areas = generate_sample_risk_predictions()
    assert isinstance(risk_areas, list)
    assert len(risk_areas) > 0

    for area in risk_areas:
        assert 'coords' in area
        assert 'risk_level' in area
        assert 'severity' in area
        assert 'factors' in area
        assert isinstance(area['coords'], list)
        assert len(area['coords']) == 2
        assert isinstance(area['severity'], (int, float))
        assert isinstance(area['factors'], list)


def test_create_infrastructure_layers():
    layers = create_infrastructure_layers()
    assert isinstance(layers, list)
    assert len(layers) == 3  # Fire stations, water sources, evac routes

    # Test fire stations layer
    fire_stations = layers[0]
    assert isinstance(fire_stations, MapLayer)
    assert fire_stations.name == "Fire Stations"
    assert isinstance(fire_stations.data, gpd.GeoDataFrame)
    assert fire_stations.data.crs == "EPSG:4326"
    assert fire_stations.style["icon"] == "fire-station"

    # Test water sources layer
    water_sources = layers[1]
    assert isinstance(water_sources, MapLayer)
    assert water_sources.name == "Water Sources"
    assert isinstance(water_sources.data, gpd.GeoDataFrame)
    assert water_sources.data.crs == "EPSG:4326"
    assert water_sources.style["icon"] == "water-source"

    # Test evacuation routes layer
    evac_routes = layers[2]
    assert isinstance(evac_routes, MapLayer)
    assert evac_routes.name == "Evacuation Routes"
    assert isinstance(evac_routes.data, gpd.GeoDataFrame)
    assert evac_routes.data.crs == "EPSG:4326"
    assert evac_routes.style["color"] == "blue"
    assert evac_routes.style["weight"] == 3
