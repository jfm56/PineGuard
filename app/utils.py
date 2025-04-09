from pathlib import Path

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import mapping

def reproject_raster(src_path: Path, dst_path: Path, dst_crs: str):
    """Reproject a raster to a new coordinate system"""
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(dst_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                )

def calculate_zonal_statistics(vector_path: Path, raster_path: Path):
    """Calculate zonal statistics for vector features using a raster"""
    with rasterio.open(raster_path) as src:
        gdf = gpd.read_file(vector_path)
        stats = []

        for geom in gdf.geometry:
            out_image, _ = mask(src, [mapping(geom)], crop=True)

            # Calculate statistics
            data = out_image[0]
            stats.append({
                'mean': float(np.mean(data)),
                'std': float(np.std(data)),
                'min': float(np.min(data)),
                'max': float(np.max(data))
            })

        # Add statistics to GeoDataFrame
        for stat in ['mean', 'std', 'min', 'max']:
            gdf[f'raster_{stat}'] = [s[stat] for s in stats]

        return gdf

def generate_report(output_path: Path):
    """Generate a PDF report with risk analysis results"""
    # Add report generation logic here
