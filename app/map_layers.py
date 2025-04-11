from pathlib import Path
from typing import List, Dict, Any, Union

import geopandas as gpd
from shapely.geometry import Point, LineString

from .config import FIRE_STATIONS, WATER_SOURCES, EVACUATION_ROUTES


class MapLayer:
    def __init__(self, name: str, data: gpd.GeoDataFrame = None,
                 data_path: Path = None, style: Dict[str, Any] = None):
        self.name = name
        self.style = style or {}
        if data is not None:
            self.data = data
        elif data_path is not None:
            self.data = gpd.read_file(data_path)
        else:
            raise ValueError("Either data or data_path must be provided")


# Default data directory
DATA_DIR = Path("data/geo")


def load_base_layers(data_dir: Path = None) -> List[MapLayer]:
    """Load and configure all base map layers
    Args:
        data_dir: Optional directory path where GeoJSON files are stored.
                 If not provided, uses the default data directory.
    """
    data_dir = data_dir or DATA_DIR
    layers = []
    # Load land use layer
    land_use = MapLayer(
        name="Land Use",
        data_path=data_dir / "land_use.geojson",
        style={
            "fillColor": "category",
            "fillOpacity": 0.7,
            "weight": 1
        }
    )
    # Load fire history layer
    fire_history = MapLayer(
        name="Historical Fires",
        data_path=data_dir / "fire_history.geojson",
        style={
            "color": "red",
            "fillOpacity": 0.5,
            "weight": 2
        }
    )
    # Load vegetation layer
    vegetation = MapLayer(
        name="Vegetation",
        data_path=data_dir / "vegetation.geojson",
        style={
            "fillColor": "category",
            "fillOpacity": 0.6,
            "weight": 1
        }
    )
    layers.extend([land_use, fire_history, vegetation])
    return layers


def create_risk_layer(
        risk_predictions: Union[gpd.GeoDataFrame, List[Dict[str, Any]]] = None
) -> MapLayer:
    """Create a new layer showing wildfire risk predictions.

    Args:
        risk_predictions: Either a GeoDataFrame with risk predictions or a list
                         of risk area dictionaries
    Returns:
        MapLayer: A new map layer with risk predictions
    """
    if risk_predictions is None:
        # Generate sample risk predictions if none provided
        risk_predictions = generate_sample_risk_predictions()

    if isinstance(risk_predictions, list):
        # Convert list of dictionaries to GeoDataFrame
        geometries = [Point(area['coords']) for area in risk_predictions]
        gdf = gpd.GeoDataFrame(
            risk_predictions,
            geometry=geometries,
            crs="EPSG:4326")
    else:
        gdf = risk_predictions

    return MapLayer(
        name="Wildfire Risk",
        data=gdf,
        style={
            "fillColor": "risk_level",
            "colormap": {
                "Extreme": "#ff0000",
                "High": "#ff6600",
                "Moderate": "#ffcc00",
                "Low": "#00cc00"
            },
            "fillOpacity": 0.7,
            "weight": 1,
            "radius": "severity"
        })



def generate_sample_risk_predictions() -> List[Dict[str, Any]]:
    """Generate sample risk predictions for testing."""
    risk_areas = [
        {
            'coords': [39.7825, -74.5338],
            'risk_level': 'High',
            'severity': 2.5,
            'factors': [
                {'name': 'Vegetation Dryness', 'value': 'Critical'},
                {'name': 'Wind Speed', 'value': 'High'},
                {'name': 'Temperature', 'value': 'Above Average'}
            ]
        },
        {
            'coords': [39.6624, -74.7185],
            'risk_level': 'Moderate',
            'severity': 1.5,
            'factors': [
                {'name': 'Vegetation Dryness', 'value': 'Moderate'},
                {'name': 'Wind Speed', 'value': 'Moderate'},
                {'name': 'Temperature', 'value': 'Average'}
            ]
        }
    ]
    return risk_areas


def create_infrastructure_layers() -> List[MapLayer]:
    """Create layers for fire stations, water sources, and evacuation routes."""
    layers = []

    # Fire stations layer
    fire_station_points = [
        Point(station['coords']) for station in FIRE_STATIONS
    ]
    fire_stations_gdf = gpd.GeoDataFrame(
        FIRE_STATIONS, geometry=fire_station_points, crs="EPSG:4326")
    layers.append(MapLayer(
        name="Fire Stations",
        data=fire_stations_gdf,
        style={
            "icon": "fire-station",
            "iconSize": [32, 32],
            "iconAnchor": [16, 32],
            "popupAnchor": [0, -32]
        }))

    # Water sources layer
    water_source_points = [
        Point(source['coords']) for source in WATER_SOURCES
    ]
    water_sources_gdf = gpd.GeoDataFrame(
        WATER_SOURCES, geometry=water_source_points, crs="EPSG:4326")
    layers.append(MapLayer(
        name="Water Sources",
        data=water_sources_gdf,
        style={
            "icon": "water-source",
            "iconSize": [32, 32],
            "iconAnchor": [16, 32],
            "popupAnchor": [0, -32]
        }))

    # Evacuation routes layer
    route_lines = [
        LineString(route['path']) for route in EVACUATION_ROUTES
    ]
    routes_gdf = gpd.GeoDataFrame(
        EVACUATION_ROUTES, geometry=route_lines, crs="EPSG:4326")
    layers.append(MapLayer(
        name="Evacuation Routes",
        data=routes_gdf,
        style={
            "color": "blue",
            "weight": 3,
            "opacity": 0.7
        }))

    return layers
