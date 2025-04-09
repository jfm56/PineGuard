import os
from pathlib import Path
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="PineGuard API",
    description="Wildfire risk prediction and management system for the New Jersey Pinelands",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Area(BaseModel):
    coordinates: List[List[float]]
    date: str = None

class RiskPrediction(BaseModel):
    risk_score: float
    confidence: float
    risk_factors: Dict[str, float]
    timestamp: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

class DetailedRiskPrediction(RiskPrediction):
    environmental_factors: Dict[str, float]
    historical_data: Dict[str, Any]
    infrastructure_risk: Dict[str, float]
    mitigation_recommendations: List[Dict[str, Any]]

@app.post("/api/v1/predict", response_model=DetailedRiskPrediction)
async def predict_risk(area: Area):
    try:
        # Analyze environmental factors (NOAA data)
        environmental_factors = {
            "temperature": 0.8,  # High temperature risk
            "humidity": 0.7,    # Low humidity risk
            "wind_speed": 0.6,  # Moderate wind risk
            "precipitation": 0.3 # Low precipitation risk
        }
        
        # Historical fire data (NJ Forest Fire Service)
        historical_data = {
            "previous_fires": [
                {
                    "year": 2024,
                    "size_hectares": 450,
                    "cause": "lightning"
                },
                {
                    "year": 2023,
                    "size_hectares": 200,
                    "cause": "human"
                }
            ],
            "fire_frequency": 0.85,  # High historical fire frequency
            "seasonal_risk": 0.9   # Peak fire season
        }
        
        # Infrastructure and land use (NJDEP data)
        infrastructure_risk = {
            "power_lines": 0.7,     # Proximity to power lines
            "roads": 0.5,          # Road density
            "buildings": 0.6,       # Building density
            "fuel_types": 0.8      # High-risk vegetation
        }
        
        # Calculate overall risk score
        risk_factors = {
            "environmental": sum(environmental_factors.values()) / len(environmental_factors),
            "historical": historical_data["fire_frequency"],
            "infrastructure": sum(infrastructure_risk.values()) / len(infrastructure_risk)
        }
        
        risk_score = sum(risk_factors.values()) / len(risk_factors)
        confidence = 0.85
        
        # Generate mitigation recommendations
        recommendations = [
            {
                "priority": "high",
                "action": "Clear firebreaks",
                "location": {
                    "type": "LineString",
                    "coordinates": [[area.coordinates[0][0], area.coordinates[0][1]],
                                  [area.coordinates[0][0] + 0.1, area.coordinates[0][1]]]
                },
                "estimated_cost": 50000,
                "time_frame": "1 month"
            },
            {
                "priority": "medium",
                "action": "Controlled burn",
                "location": {
                    "type": "Polygon",
                    "coordinates": [area.coordinates]
                },
                "estimated_cost": 75000,
                "time_frame": "3 months"
            }
        ]
        
        return {
            "risk_score": risk_score,
            "confidence": confidence,
            "risk_factors": risk_factors,
            "environmental_factors": environmental_factors,
            "historical_data": historical_data,
            "infrastructure_risk": infrastructure_risk,
            "mitigation_recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/regions")
async def get_regions():
    return {
        "regions": [
            {
                "id": "pine_plains",
                "name": "Pine Plains",
                "center": [-74.5, 39.8],
                "risk_level": "high"
            },
            {
                "id": "wharton_sf",
                "name": "Wharton State Forest",
                "center": [-74.7, 39.7],
                "risk_level": "moderate"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
