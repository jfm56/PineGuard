"""Tests for fire_risk.py API endpoints."""
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.fire_risk import (
    router,
    get_cached_data,
    fetch_weather_data,
    get_historical_fires,
    get_vegetation_index,
    get_soil_moisture,
    cache,
    CACHE_DURATION,
)


@pytest.fixture
def app():
    """Create a FastAPI test application."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def test_app():
    """Create a test app."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def test_client(test_app):
    """Create a test client."""
    client = TestClient(test_app)
    return client


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear the cache before each test."""
    cache.clear()
    cache.update({
        'weather': None,
        'weather_timestamp': None,
        'historical_fires': None,
        'vegetation_index': None,
        'soil_moisture': None
    })


def test_get_cached_data_empty():
    """Test getting data from empty cache."""
    assert get_cached_data('weather') is None


def test_get_cached_data_expired():
    """Test getting expired data from cache."""
    cache['weather'] = {'temp': 75}
    cache['weather_timestamp'] = datetime.now() - CACHE_DURATION - timedelta(minutes=1)
    assert get_cached_data('weather') is None


def test_get_cached_data_valid():
    """Test getting valid data from cache."""
    test_data = {'temp': 75}
    cache['weather'] = test_data
    cache['weather_timestamp'] = datetime.now()
    assert get_cached_data('weather') == test_data


@pytest.mark.asyncio
async def test_fetch_weather_data_success():
    """Test successful weather data fetch."""
    mock_response = {
        'currentConditions': {
            'temp': 75,
            'humidity': 50,
            'windspeed': 10,
            'conditions': 'Clear'
        }
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = await fetch_weather_data()

        assert result == {
            'temp': 75,
            'humidity': 50,
            'windSpeed': 10,
            'conditions': 'Clear'
        }
        assert cache['weather'] == result


@pytest.mark.asyncio
async def test_fetch_weather_data_cached():
    """Test fetching cached weather data."""
    test_data = {
        'temp': 75,
        'humidity': 50,
        'windSpeed': 10,
        'conditions': 'Clear'
    }
    cache['weather'] = test_data
    cache['weather_timestamp'] = datetime.now()

    result = await fetch_weather_data()
    assert result == test_data


@pytest.mark.asyncio
async def test_get_historical_fires():
    """Test getting historical fire data."""
    result = await get_historical_fires()
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(fire, dict) for fire in result)
    assert all('date' in fire for fire in result)


@pytest.mark.asyncio
async def test_get_vegetation_index():
    """Test getting vegetation index."""
    result = await get_vegetation_index()
    assert isinstance(result, float)
    assert 0 <= result <= 1


@pytest.mark.asyncio
async def test_get_soil_moisture():
    """Test getting soil moisture."""
    result = await get_soil_moisture()
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_fire_risk_endpoint_success(test_client):
    """Test successful fire risk endpoint."""
    response = test_client.get("/api/fire-risk")
    assert response.status_code == 200
    data = response.json()
    assert 'currentWeather' in data
    assert 'historicalFires' in data
    assert 'vegetationIndex' in data
    assert 'soilMoisture' in data


def test_fire_risk_endpoint_weather_error(test_client):
    """Test fire risk endpoint with weather API error."""
    with patch('api.fire_risk.fetch_weather_data',
              side_effect=Exception("API Error")):
        response = test_client.get("/api/fire-risk")
        assert response.status_code == 500
        assert "API Error" in response.json()['detail']
