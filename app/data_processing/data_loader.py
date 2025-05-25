from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import os
import pandas as pd
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import requests
import zipfile
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
            "datasetid": "GHCND",
            "locationid": f"BBOX:{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "startdate": start_date.strftime("%Y-%m-%d"),
            "enddate": end_date.strftime("%Y-%m-%d"),
            "units": "metric"
        }
        headers = {"token": os.getenv("NOAA_API_KEY")}
        # Attempt NOAA API fetch
        try:
            resp = requests.get(base_url, params=params, headers=headers)
            data = resp.json()
            results = data.get("results")
        except Exception:
            results = None
        if results:
            df = pd.DataFrame(results)
            df["date"] = pd.to_datetime(df["date"])
            return df
        # Fallback deterministic synthetic data
        dates = pd.date_range(start_date, end_date, freq="D")
        seed = int(start_date.strftime("%Y%m%d")) ^ int(end_date.strftime("%Y%m%d"))
        rng = np.random.default_rng(seed)
        synth = pd.DataFrame({
            "date": dates,
            "TAVG": rng.uniform(0, 30, size=len(dates)),
            "RHAV": rng.uniform(10, 90, size=len(dates)),
            "AWND": rng.uniform(0, 15, size=len(dates)),
        })
        return synth
    
    def load_weather_data(self, *args, **kwargs) -> Any:
        """Alias for load_environmental_data"""
        return self.load_environmental_data(*args, **kwargs)

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
        
        return gpd.sjoin(land_use, region, how='inner', predicate='intersects')
    
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

    def load_satellite_data(self, *args, **kwargs) -> Any:
        """Alias for load_satellite_imagery"""
        return self.load_satellite_imagery(*args, **kwargs)
    
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
        
        return gpd.sjoin(fire_history, region, how='inner', predicate='intersects')
    
    def prepare_model_features(self,
                             region: gpd.GeoDataFrame,
                             date: datetime) -> pd.DataFrame:
        """Prepare features for the ML model"""
        # Get environmental data
        env_data = self.load_environmental_data(
            region.total_bounds,
            date - timedelta(days=30),
            date
        )
        
        # Get land use data
        land_use = self.load_land_use_data(region)
        
        # Get historical fires
        historical_fires = self.load_historical_fires(
            region,
            date.year - 10,
            date.year
        )
        
        # Combine all features into a single-row DataFrame
        data = {
            'temperature': env_data['TAVG'].mean(),
            'humidity': env_data['RHAV'].mean(),
            'wind_speed': env_data['AWND'].mean(),
            'vegetation_type': land_use['landcover'].mode()[0],
            'historical_fire_count': len(historical_fires),
            'days_since_last_fire': (date - historical_fires['date'].max()).days if len(historical_fires) > 0 else 9999
        }
        features = pd.DataFrame([data])
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
        file = self.raw_dir / 'fire_occurrence.csv'
        # If missing, download the national Interagency Fire Occurrence dataset
        if not file.exists():
            url = 'https://www.fs.usda.gov/rds/archive/products/RDS-2013-0009.4/FPA_FOD_20170508.zip'
            # Download the zipped dataset
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            zip_path = self.raw_dir / 'FPA_FOD_20170508.zip'
            with open(zip_path, 'wb') as zf:
                for chunk in resp.iter_content(chunk_size=8192):
                    zf.write(chunk)
            # Extract CSV and rename to fire_occurrence.csv
            with zipfile.ZipFile(zip_path, 'r') as zf:
                csv_file = next((n for n in zf.namelist() if n.endswith('.csv')), None)
                if csv_file:
                    zf.extract(csv_file, path=self.raw_dir)
                    (self.raw_dir / csv_file).rename(file)
            zip_path.unlink()
        # Read full dataset
        df = pd.read_csv(file)
        # Drop invalid coordinates
        df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
        # Parse dates
        df['discovery_date'] = pd.to_datetime(df.get('DISCOVERY_DATE', df.get('discovery_date')), errors='coerce')
        df['containment_date'] = pd.to_datetime(df.get('CONTAINMENT_DATE', df.get('containment_date')), errors='coerce')
        # Filter by year window
        df = df[(df['discovery_date'].dt.year >= start_year) & (df['discovery_date'].dt.year <= end_year)]
        # Remove coordinate outliers
        df = df[~((df['LATITUDE'] == 0) & (df['LONGITUDE'] == 0))]
        # Deduplicate by FOD_ID if present
        if 'FOD_ID' in df.columns:
            df = df.drop_duplicates(subset=['FOD_ID'])
        # Prune to needed fields
        fields = ['FOD_ID', 'LATITUDE', 'LONGITUDE', 'discovery_date', 'containment_date']
        fields = [f for f in fields if f in df.columns]
        df = df[fields]
        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']), crs='EPSG:4326')
        # Filter to the provided region-of-interest
        region = region.to_crs(gdf.crs)
        try:
            gdf = gpd.sjoin(gdf, region, how='inner', predicate='within')
        except Exception:
            # If spatial join fails, proceed without filtering
            pass
        # Write out CSV for spot-checking
        out_csv = self.processed_dir / 'cleaned_fire_history.csv'
        df.to_csv(out_csv, index=False)
        return gdf
