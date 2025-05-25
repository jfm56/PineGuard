from pathlib import Path
import geopandas as gpd

from app.data_processing.data_loader import DataLoader

# Load pinelands boundary shapefile
boundary_path = Path("pinelands/pinelands.shp")
if not boundary_path.exists():
    raise FileNotFoundError(f"Boundary shapefile not found at {boundary_path}")
pinelands = gpd.read_file(boundary_path).to_crs("EPSG:4326")

# Instantiate DataLoader with data directory
data_dir = Path("data")
dl = DataLoader(data_dir)

# Run fire history download and cleaning
start_year = 2000
end_year = 2020
fires_gdf = dl._download_fire_history(pinelands, start_year, end_year)

# Print the cleaned GeoDataFrame's key columns
print(f"Total fires: {len(fires_gdf)}")
print(fires_gdf[['FOD_ID', 'discovery_date', 'containment_date']].head(20).to_string(index=False))
