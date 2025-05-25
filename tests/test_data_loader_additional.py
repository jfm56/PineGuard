import pytest
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
from pathlib import Path
from datetime import datetime
from shapely.geometry import box

from app.data_processing.data_loader import DataLoader


def test_load_land_use_data_existing(tmp_path):
    region = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
    loader = DataLoader(tmp_path)
    land_use_gdf = gpd.GeoDataFrame(
        {'landcover': [1], 'geometry': [box(0.5, 0.5, 0.75, 0.75)]},
        crs="EPSG:4326"
    )
    file_path = loader.geo_dir / 'land_use.geojson'
    land_use_gdf.to_file(file_path, driver='GeoJSON')
    result = loader.load_land_use_data(region)
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1
    assert result.iloc[0]['landcover'] == 1


def test_load_land_use_data_download(tmp_path, monkeypatch):
    region = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
    loader = DataLoader(tmp_path)
    mocked_gdf = gpd.GeoDataFrame(
        {'landcover': [2], 'geometry': [box(0.2, 0.2, 0.4, 0.4)]},
        crs="EPSG:4326"
    )
    monkeypatch.setattr(DataLoader, '_download_nlcd_data', lambda self, region: mocked_gdf)
    result = loader.load_land_use_data(region)
    file_path = loader.geo_dir / 'land_use.geojson'
    assert file_path.exists()
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1
    assert result.iloc[0]['landcover'] == 2


def test_load_historical_fires_existing(tmp_path):
    region = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
    loader = DataLoader(tmp_path)
    fire_gdf = gpd.GeoDataFrame(
        {'date': [datetime(2020, 1, 1)], 'geometry': [box(0, 0, 1, 1)]},
        crs="EPSG:4326"
    )
    file_path = loader.geo_dir / 'fire_history.geojson'
    fire_gdf.to_file(file_path, driver='GeoJSON')
    result = loader.load_historical_fires(region, 2019, 2021)
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1


def test_load_historical_fires_download(tmp_path, monkeypatch):
    region = gpd.GeoDataFrame(geometry=[box(0, 0, 1, 1)], crs="EPSG:4326")
    loader = DataLoader(tmp_path)
    mocked_fire = gpd.GeoDataFrame(
        {'date': [datetime(2021, 5, 1)], 'geometry': [box(0, 0, 1, 1)]},
        crs="EPSG:4326"
    )
    monkeypatch.setattr(DataLoader, '_download_fire_history', lambda self, region, sy, ey: mocked_fire)
    result = loader.load_historical_fires(region, 2020, 2022)
    file_path = loader.geo_dir / 'fire_history.geojson'
    assert file_path.exists()
    assert isinstance(result, gpd.GeoDataFrame)
    assert len(result) == 1


def test_load_satellite_imagery_existing(tmp_path):
    date = datetime(2025, 5, 23)
    bbox = (0.0, 0.0, 1.0, 1.0)
    loader = DataLoader(tmp_path)
    filename = f"satellite_{date.strftime('%Y%m%d')}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.tif"
    file_path = loader.raw_dir / filename
    data = np.array([[[7]]], dtype=np.uint8)
    profile = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'count': 1,
        'height': 1,
        'width': 1,
        'transform': from_origin(0, 1, 1, 1)
    }
    with rasterio.open(file_path, 'w', **profile) as dst:
        dst.write(data)
    result = loader.load_satellite_imagery(bbox, date)
    assert isinstance(result, np.ndarray)
    assert result.shape == (1, 1, 1)
    assert result[0, 0, 0] == 7


def test_load_satellite_imagery_download(tmp_path, monkeypatch):
    date = datetime(2025, 5, 23)
    bbox = (0.0, 0.0, 1.0, 1.0)
    loader = DataLoader(tmp_path)
    data = np.array([[[9]]], dtype=np.uint8)
    profile = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'count': 1,
        'height': 1,
        'width': 1,
        'transform': from_origin(0, 1, 1, 1)
    }
    monkeypatch.setattr(
        DataLoader,
        '_download_satellite_imagery',
        lambda self, bbox_arg, date_arg: {'profile': profile, 'data': data}
    )
    result = loader.load_satellite_imagery(bbox, date)
    file_path = loader.raw_dir / f"satellite_{date.strftime('%Y%m%d')}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.tif"
    assert file_path.exists()
    assert isinstance(result, np.ndarray)
    assert result[0, 0, 0] == 9
