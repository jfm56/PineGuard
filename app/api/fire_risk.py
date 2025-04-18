"""Fire risk assessment API endpoints."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Cache for weather and fire data
cache = {
    'weather': None,
    'weather_timestamp': None,
    'historical_fires': None,
    'vegetation_index': None,
    'soil_moisture': None
}

CACHE_DURATION = timedelta(minutes=15)



def get_cached_data(key: str) -> Optional[dict]:
    """Get data from cache if it's still valid."""
    if cache[key] and cache[f'{key}_timestamp']:
        if datetime.now() - cache[f'{key}_timestamp'] < CACHE_DURATION:
            return cache[key]
    return None



async def fetch_weather_data() -> Dict:
    """Fetch current weather data for Pine Barrens."""
    cached = get_cached_data('weather')
    if cached:
        return cached

    try:
        # Using Visual Crossing Weather API for Pine Barrens
        url = ('https://weather.visualcrossing.com/VisualCrossingWebServices/'
               'rest/services/timeline/39.8,-74.5')
        params = {
            'unitGroup': 'us',
            'key': 'YOUR_API_KEY'  # Replace with your API key
        }
        response = requests.get(url, params=params)
        data = response.json()

        weather_data = {
            'temp': data['currentConditions']['temp'],
            'humidity': data['currentConditions']['humidity'],
            'windSpeed': data['currentConditions']['windspeed'],
            'conditions': data['currentConditions']['conditions']
        }

        cache['weather'] = weather_data
        cache['weather_timestamp'] = datetime.now()

        return weather_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather API error: {str(e)}"
        )



async def get_historical_fires() -> List[Dict]:
    """Get historical fire data for the Pine Barrens region."""
    cached = get_cached_data('historical_fires')
    if cached:
        return cached

    # This would typically come from a database
    # For now, using sample historical data
    historical_data = [
        {
            'date': '2023-04-15',
            'size_acres': 1500,
            'cause': 'lightning',
            'weather_conditions': {
                'temp': 85,
                'humidity': 30,
                'wind_speed': 15
            }
        },
        {
            'date': '2022-05-20',
            'size_acres': 800,
            'cause': 'human',
            'weather_conditions': {
                'temp': 82,
                'humidity': 35,
                'wind_speed': 12
            }
        },
    ]

    cache['historical_fires'] = historical_data
    cache['historical_fires_timestamp'] = datetime.now()

    return historical_data


async def get_vegetation_index() -> float:
    """Get current vegetation dryness index."""
    cached = get_cached_data('vegetation_index')
    if cached:
        return cached

    # This would typically come from satellite data or ground sensors
    # For now, using a simulated value between 0 (very dry) and 1 (well hydrated)
    index = np.random.uniform(0.3, 0.7)

    cache['vegetation_index'] = index
    cache['vegetation_index_timestamp'] = datetime.now()

    return index


async def get_soil_moisture() -> float:
    """Get current soil moisture level."""
    cached = get_cached_data('soil_moisture')
    if cached:
        return cached

    # This would typically come from ground sensors
    # For now, using a simulated value between 0 (dry) and 1 (saturated)
    moisture = np.random.uniform(0.2, 0.8)

    cache['soil_moisture'] = moisture
    cache['soil_moisture_timestamp'] = datetime.now()

    return moisture


@router.get("/api/fire-risk")
async def get_fire_risk() -> Dict:
    """Calculate current fire risk based on multiple factors."""
    try:
        # Gather all required data
        weather = await fetch_weather_data()
        historical_fires = await get_historical_fires()
        vegetation_index = await get_vegetation_index()
        soil_moisture = await get_soil_moisture()

        # Return all data needed for client-side risk calculation
        return {
            'currentWeather': weather,
            'historicalFires': historical_fires,
            'vegetationIndex': vegetation_index,
            'soilMoisture': soil_moisture
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
