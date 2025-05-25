# Shim module to support tests patching api.fire_risk
from app.api.fire_risk import fetch_weather_data

__all__ = ["fetch_weather_data"]
