import pytest
from pathlib import Path
import numpy as np
import geopandas as gpd
import rasterio
from app.utils import reproject_raster, calculate_zonal_statistics, generate_report

@pytest.fixture
def test_data_dir(tmp_path):
    return tmp_path / "test_data"

@pytest.fixture
def sample_raster(test_data_dir):
    test_data_dir.mkdir(exist_ok=True)
    raster_path = test_data_dir / "test.tif"
    
    # Create a simple test raster
    data = np.random.rand(100, 100)
    transform = rasterio.transform.from_bounds(0, 0, 1, 1, 100, 100)
    
    with rasterio.open(
        raster_path,
        'w',
        driver='GTiff',
        height=data.shape[0],
        width=data.shape[1],
        count=1,
        dtype=data.dtype,
        crs='EPSG:4326',
        transform=transform
    ) as dst:
        dst.write(data, 1)
    
    return raster_path

@pytest.fixture
def sample_vector(test_data_dir):
    test_data_dir.mkdir(exist_ok=True)
    vector_path = test_data_dir / "test.geojson"
    
    # Create a simple test vector with a polygon
    from shapely.geometry import Polygon
    gdf = gpd.GeoDataFrame(
        geometry=[Polygon([(0.2, 0.2), (0.8, 0.2), (0.8, 0.8), (0.2, 0.8), (0.2, 0.2)])],
        crs="EPSG:4326"
    )
    gdf.to_file(vector_path, driver="GeoJSON")
    
    return vector_path

def test_reproject_raster(sample_raster, test_data_dir):
    dst_path = test_data_dir / "reprojected.tif"
    dst_crs = "EPSG:3857"
    
    reproject_raster(sample_raster, dst_path, dst_crs)
    
    with rasterio.open(dst_path) as dst:
        assert dst.crs == dst_crs

def test_calculate_zonal_statistics(sample_raster, sample_vector):
    result = calculate_zonal_statistics(sample_vector, sample_raster)
    
    assert isinstance(result, gpd.GeoDataFrame)
    assert "raster_mean" in result.columns
    assert "raster_std" in result.columns
    assert "raster_min" in result.columns
    assert "raster_max" in result.columns

def test_generate_report(test_data_dir):
    output_path = test_data_dir / "report.pdf"
    generate_report(output_path)
    # Since this is a stub function, we just verify it runs without error
