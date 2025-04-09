from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import requests
from datetime import datetime, timedelta

class DataLoader:
    """Handles loading and preprocessing of various data sources"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_dir = data_dir / 'raw'
        self.processed_dir = data_dir / 'processed'
        self.geo_dir = data_dir / 'geo'
        
        # Create directories if they don't exist
        for dir_path in [self.raw_dir, self.processed_dir, self.geo_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def load_environmental_data(self, 
                              bbox: Tuple[float, float, float, float],
                              start_date: datetime,
                              end_date: datetime) -> pd.DataFrame:
        """Load environmental data from NOAA API"""
        base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
        
        params = {
            "datasetid": "GHCND",  # Global Historical Climatology Network Daily
            "locationid": f"BBOX:{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "startdate": start_date.strftime("%Y-%m-%d"),
            "enddate": end_date.strftime("%Y-%m-%d"),
            "units": "metric"
        }
        
        headers = {
            "token": os.getenv("NOAA_API_KEY")
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        data = response.json()
        
        # Process and structure the data
        df = pd.DataFrame(data['results'])
        df['date'] = pd.to_datetime(df['date'])
        
        return df
    
    def load_land_use_data(self, region: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Load land use data from local files or NLCD"""
        land_use_path = self.geo_dir / 'land_use.geojson'
        
        if land_use_path.exists():
            land_use = gpd.read_file(land_use_path)
        else:
            # Download from NLCD (National Land Cover Database)
            # This is a placeholder - actual implementation would use NLCD API
            land_use = self._download_nlcd_data(region)
            land_use.to_file(land_use_path, driver='GeoJSON')
        
        return gpd.sjoin(land_use, region, how='inner', op='intersects')
    
    def load_satellite_imagery(self,
                             bbox: Tuple[float, float, float, float],
                             date: datetime) -> np.ndarray:
        """Load satellite imagery for the specified region and date"""
        # Create a filename based on bbox and date
        filename = f"satellite_{date.strftime('%Y%m%d')}_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}.tif"
        image_path = self.raw_dir / filename
        
        if image_path.exists():
            with rasterio.open(image_path) as src:
                return src.read()
        else:
            # Download new imagery
            # This is a placeholder - actual implementation would use specific satellite API
            imagery = self._download_satellite_imagery(bbox, date)
            
            # Save to file
            with rasterio.open(image_path, 'w', **imagery['profile']) as dst:
                dst.write(imagery['data'])
            
            return imagery['data']
    
    def load_historical_fires(self, 
                            region: gpd.GeoDataFrame,
                            start_year: int,
                            end_year: int) -> gpd.GeoDataFrame:
        """Load historical fire data for the specified region and time period"""
        fire_history_path = self.geo_dir / 'fire_history.geojson'
        
        if fire_history_path.exists():
            fire_history = gpd.read_file(fire_history_path)
        else:
            # Download from federal fire occurrence database
            # This is a placeholder - actual implementation would use specific API
            fire_history = self._download_fire_history(region, start_year, end_year)
            fire_history.to_file(fire_history_path, driver='GeoJSON')
        
        return gpd.sjoin(fire_history, region, how='inner', op='intersects')
    
    def prepare_model_features(self,
                             region: gpd.GeoDataFrame,
                             date: datetime) -> pd.DataFrame:
        """Prepare features for the ML model"""
        # Get environmental data
        env_data = self.load_environmental_data(
            bbox=region.total_bounds,
            start_date=date - timedelta(days=30),
            end_date=date
        )
        
        # Get land use data
        land_use = self.load_land_use_data(region)
        
        # Get historical fires
        historical_fires = self.load_historical_fires(
            region=region,
            start_year=date.year - 10,
            end_year=date.year
        )
        
        # Combine all features
        features = pd.DataFrame()
        features['temperature'] = env_data['TAVG'].mean()  # Average temperature
        features['humidity'] = env_data['RHAV'].mean()  # Average relative humidity
        features['wind_speed'] = env_data['AWND'].mean()  # Average wind speed
        
        # Add land use features
        features['vegetation_type'] = land_use['landcover'].mode()[0]
        
        # Add fire history features
        features['historical_fire_count'] = len(historical_fires)
        features['days_since_last_fire'] = (
            date - historical_fires['date'].max()).days if len(historical_fires) > 0 else 9999
        
        return features
    
    def _download_nlcd_data(self, region: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Download land cover data from NLCD"""
        # Placeholder - implement actual NLCD API interaction
        pass
    
    def _download_satellite_imagery(self,
                                  bbox: Tuple[float, float, float, float],
                                  date: datetime) -> Dict[str, Any]:
        """Download satellite imagery for the specified region and date"""
        # Placeholder - implement actual satellite imagery API interaction
        pass
    
    def _download_fire_history(self,
                             region: gpd.GeoDataFrame,
                             start_year: int,
                             end_year: int) -> gpd.GeoDataFrame:
        """Download historical fire data"""
        # Placeholder - implement actual fire history API interaction
        pass
