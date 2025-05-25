from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data_processing.data_loader import DataLoader

router = APIRouter(prefix="/api/v1")

class PredictionRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    label_window: int = 1

class PredictionResponse(BaseModel):
    reports: Dict[str, Any]

@router.post("/predict_fire_window", response_model=PredictionResponse)
async def predict_fire_window(req: PredictionRequest):
    # Load region boundary shapefile
    boundary_path = Path("pinelands/pinelands.shp")
    if not boundary_path.exists():
        raise HTTPException(status_code=500, detail=f"Boundary shapefile not found at {boundary_path}")
    boundary = gpd.read_file(boundary_path).to_crs("EPSG:4326")

    # Instantiate loader and load historical fires
    dl = DataLoader(Path("data"))
    fires_gdf = dl._download_fire_history(boundary, req.start_date.year - 1, req.end_date.year)

    # Generate features and labels
    dates = pd.date_range(req.start_date, req.end_date, freq="D")
    rows = []
    fire_dates = fires_gdf["discovery_date"].dt.date
    for date in dates:
        env = dl.load_environmental_data(tuple(boundary.total_bounds), date, date)
        tavg = env["TAVG"].mean() if not env.empty else np.nan
        rhav = env["RHAV"].mean() if not env.empty else np.nan
        awnd = env["AWND"].mean() if not env.empty else np.nan
        next_date = date + timedelta(days=req.label_window)
        fire_flag = int(any(fd >= date.date() and fd < next_date.date() for fd in fire_dates))
        rows.append({"date": date, "TAVG": tavg, "RHAV": rhav, "AWND": awnd, "label": fire_flag})

    df = pd.DataFrame(rows).dropna()
    if df["label"].nunique() < 2:
        raise HTTPException(status_code=400, detail="Not enough class variation for given window.")

    X = df[["TAVG", "RHAV", "AWND"]]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "LightGBM": LGBMClassifier(random_state=42),
        "CatBoost": CatBoostClassifier(verbose=0, random_state=42),
    }
    reports = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        reports[name] = classification_report(y_test, preds, output_dict=True)

    return {"reports": reports}
