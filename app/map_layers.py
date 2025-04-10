from pathlib import Path
from typing import List, Dict, Any

import geopandas as gpd

class MapLayer:
    def __init__(self, name: str, data: gpd.GeoDataFrame = None, data_path: Path = None, style: Dict[str, Any] = None):
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

def create_risk_layer(risk_predictions: gpd.GeoDataFrame) -> MapLayer:
    """Create a new layer showing wildfire risk predictions"""
    return MapLayer(
        name="Wildfire Risk",
        data=risk_predictions,
        style={
            "fillColor": "risk_score",
            "colormap": "RdYlGn_r",
            "fillOpacity": 0.7,
            "weight": 1
        }
    )
