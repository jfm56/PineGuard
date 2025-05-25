import os
import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
from shapely.geometry import box

from app.data_processing.data_loader import DataLoader


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data


@pytest.fixture(autouse=True)
def noaa_api(monkeypatch):
    # Stub NOAA API key and requests.get
    monkeypatch.setenv("NOAA_API_KEY", "dummy")
    def fake_get(url, params=None, headers=None):
        return DummyResponse({
            "results": [
                {"date": "2025-05-01T00:00:00", "TAVG": 10.0, "RHAV": 50.0, "AWND": 5.0}
            ]
        })
    monkeypatch.setattr(requests, "get", fake_get)


def test_load_environmental_data_and_alias(tmp_path):
    dl = DataLoader(tmp_path)
    start = datetime(2025, 5, 1)
    end = datetime(2025, 5, 2)
    bbox = (0.0, 0.0, 1.0, 1.0)

    df1 = dl.load_environmental_data(bbox, start, end)
    df2 = dl.load_weather_data(bbox, start, end)

    assert isinstance(df1, pd.DataFrame)
    assert df1.equals(df2)
    assert df1.loc[0, "TAVG"] == 10.0
    assert pd.api.types.is_datetime64_any_dtype(df1["date"])


def test_prepare_model_features_with_stubs(tmp_path, monkeypatch):
    # Prepare dummy region and DataLoader
    region = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
    dl = DataLoader(tmp_path)

    # Stub dependent methods
    env_df = pd.DataFrame({
        "TAVG": [15.0, 25.0],
        "RHAV": [60.0, 40.0],
        "AWND": [3.0, 7.0],
        "date": [datetime(2025, 5, 1), datetime(2025, 5, 2)]
    })
    land_df = gpd.GeoDataFrame({
        "landcover": [2, 2],
        "geometry": [box(0, 0, 1, 1), box(0, 0, 1, 1)]
    }, crs="EPSG:4326")
    fire_df = pd.DataFrame({"date": [datetime(2025, 1, 1), datetime(2025, 4, 1)]})

    monkeypatch.setattr(DataLoader, "load_environmental_data", lambda self, bbox, start, end: env_df)
    monkeypatch.setattr(DataLoader, "load_land_use_data", lambda self, region: land_df)
    monkeypatch.setattr(DataLoader, "load_historical_fires", lambda self, region, sy, ey: fire_df)

    features = dl.prepare_model_features(region, datetime(2025, 5, 3))

    # Validate features
    assert features.loc[0, "temperature"] == pytest.approx(env_df["TAVG"].mean())
    assert features.loc[0, "humidity"] == pytest.approx(env_df["RHAV"].mean())
    assert features.loc[0, "wind_speed"] == pytest.approx(env_df["AWND"].mean())
    assert features.loc[0, "vegetation_type"] == 2
    assert features.loc[0, "historical_fire_count"] == 2
    # days since last fire: max date 2025-04-01 -> 32 days before 2025-05-03
    assert features.loc[0, "days_since_last_fire"] == (datetime(2025, 5, 3) - datetime(2025, 4, 1)).days
