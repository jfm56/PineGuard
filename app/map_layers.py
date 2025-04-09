from pathlib import Path
import geopandas as gpd
from windsurf import Layer

def load_base_layers():
    """Load and configure all base map layers"""
    layers = []
    
    # Load land use layer
    land_use = Layer(
        name="Land Use",
        data_path=Path("data/geo/land_use.geojson"),
        style={
            "fillColor": "category",
            "fillOpacity": 0.7,
            "weight": 1
        }
    )
    
    # Load fire history layer
    fire_history = Layer(
        name="Historical Fires",
        data_path=Path("data/geo/fire_history.geojson"),
        style={
            "color": "red",
            "fillOpacity": 0.5,
            "weight": 2
        }
    )
    
    # Load vegetation layer
    vegetation = Layer(
        name="Vegetation",
        data_path=Path("data/geo/vegetation.geojson"),
        style={
            "fillColor": "category",
            "fillOpacity": 0.6,
            "weight": 1
        }
    )
    
    layers.extend([land_use, fire_history, vegetation])
    return layers

def create_risk_layer(risk_predictions):
    """Create a new layer showing wildfire risk predictions"""
    return Layer(
        name="Wildfire Risk",
        data=risk_predictions,
        style={
            "fillColor": "risk_score",
            "colormap": "RdYlGn_r",
            "fillOpacity": 0.7,
            "weight": 1
        }
    )
