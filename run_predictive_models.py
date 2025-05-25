#!/usr/bin/env python
from pathlib import Path
import geopandas as gpd
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report

from app.data_processing.data_loader import DataLoader

# Load Pinelands boundary
boundary_path = Path("pinelands/pinelands.shp")
pinelands = gpd.read_file(boundary_path).to_crs("EPSG:4326")

# Instantiate DataLoader
data_dir = Path("data")
dl = DataLoader(data_dir)

# Load cleaned historical fires for 2020
fires_gdf = dl._download_fire_history(pinelands, 2020, 2020)

# Prepare daily environmental data for 2020
start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 12, 31)
env_df = dl.load_environmental_data(tuple(pinelands.total_bounds), start_date, end_date)

# Aggregate daily metrics
daily = (
    env_df.groupby(env_df['date'].dt.date)
    .agg(TAVG=('TAVG', 'mean'), RHAV=('RHAV', 'mean'), AWND=('AWND', 'mean'))
    .reset_index()
    .rename(columns={'date': 'date'})
)

# Label: 1 if any fire occurred that day
fires_dates = fires_gdf['discovery_date'].dt.date
daily['label'] = daily['date'].isin(fires_dates).astype(int)

# Features and target
X = daily[['TAVG', 'RHAV', 'AWND']]
y = daily['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Models
target_models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'LightGBM': LGBMClassifier(random_state=42),
    'CatBoost': CatBoostClassifier(verbose=0, random_state=42)
}

# Train and evaluate
for name, model in target_models.items():
    print(f"--- {name} ---")
    # Skip if only one class present in training data
    if y_train.nunique() < 2:
        print(f"Skipping {name}: only one class in training labels.")
        continue
    try:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        print(classification_report(y_test, preds))
    except Exception as e:
        print(f"Error training {name}: {e}")
