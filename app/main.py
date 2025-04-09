from datetime import datetime
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
async def predict_risk(area: Area, analysis_mode: str = "basic"):
    """Predict wildfire risk for an area with specified analysis mode (basic or professional)"""
    # Validate analysis mode
    if analysis_mode not in ["basic", "professional"]:
        raise HTTPException(status_code=400, detail="Invalid analysis mode. Must be 'basic' or 'professional'")
    try:
        # Basic environmental factors (always included)
        environmental_factors = {
            "temperature": 0.8,  # High temperature risk
            "humidity": 0.7,    # Low humidity risk
            "wind_speed": 0.6,  # Moderate wind risk
        }
        
        # Add detailed factors for professional analysis
        if analysis_mode == "professional":
            environmental_factors.update({
                "precipitation": 0.3,  # Low precipitation risk
                "soil_moisture": 0.4,  # Moderate soil moisture
                "drought_index": 0.8,  # High drought risk
                "fuel_moisture": 0.6   # Moderate fuel moisture
            })
        
        # Historical fire data with mode-specific detail
        if analysis_mode == "professional":
            historical_data = {
                "previous_fires": [
                    {
                        "year": 2024,
                        "size_hectares": 450,
                        "cause": "lightning",
                        "containment_time": "72h",
                        "resources_deployed": {
                            "personnel": 120,
                            "vehicles": 15,
                            "aircraft": 2
                        }
                    },
                    {
                        "year": 2023,
                        "size_hectares": 200,
                        "cause": "human",
                        "containment_time": "48h",
                        "resources_deployed": {
                            "personnel": 80,
                            "vehicles": 10,
                            "aircraft": 1
                        }
                    }
                ],
                "fire_frequency": 0.85,
                "seasonal_risk": 0.9,
                "historical_weather_patterns": {
                    "avg_temperature": 28.5,
                    "avg_humidity": 45.2,
                    "avg_wind_speed": 15.3
                },
                "vegetation_recovery": {
                    "rate": "moderate",
                    "years_to_recovery": 5
                }
            }
        else:
            historical_data = {
                "fire_frequency": 0.85,
                "seasonal_risk": 0.9,
                "recent_fires": 2
            }
        
        # Infrastructure analysis based on mode
        if analysis_mode == "professional":
            infrastructure_risk = {
                "power_lines": 0.7,
                "roads": 0.5,
                "buildings": 0.6,
                "fuel_types": 0.8,
                "water_sources": 0.4,
                "fire_stations": 0.3,
                "evacuation_routes": 0.6,
                "communication_towers": 0.5,
                "critical_facilities": {
                    "hospitals": 0.3,
                    "schools": 0.4,
                    "emergency_shelters": 0.5
                }
            }
        else:
            infrastructure_risk = {
                "buildings": 0.6,
                "roads": 0.5,
                "fuel_types": 0.8
            }
        
        # Calculate overall risk score
        risk_factors = {
            "environmental": sum(environmental_factors.values()) / len(environmental_factors),
            "historical": historical_data["fire_frequency"],
            "infrastructure": sum(infrastructure_risk.values()) / len(infrastructure_risk)
        }
        
        risk_score = sum(risk_factors.values()) / len(risk_factors)
        confidence = 0.85
        
        # Generate mode-specific recommendations
        if analysis_mode == "professional":
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
                    "time_frame": "1 month",
                    "resources_needed": {
                        "equipment": ["bulldozers", "chainsaws", "water trucks"],
                        "personnel": 20,
                        "permits_required": ["environmental", "local"]
                    },
                    "impact_assessment": {
                        "environmental": "moderate",
                        "effectiveness": 0.8
                    }
                },
                {
                    "priority": "medium",
                    "action": "Controlled burn",
                    "location": {
                        "type": "Polygon",
                        "coordinates": [area.coordinates]
                    },
                    "estimated_cost": 75000,
                    "time_frame": "3 months",
                    "resources_needed": {
                        "equipment": ["fire engines", "hand tools", "drip torches"],
                        "personnel": 35,
                        "permits_required": ["fire", "air quality", "environmental"]
                    },
                    "weather_requirements": {
                        "wind_speed": "< 15 mph",
                        "humidity": "> 30%",
                        "temperature": "< 85°F"
                    }
                }
            ]
        else:
            recommendations = [
                {
                    "priority": "high",
                    "action": "Clear firebreaks",
                    "location": {
                        "type": "LineString",
                        "coordinates": [[area.coordinates[0][0], area.coordinates[0][1]],
                                      [area.coordinates[0][0] + 0.1, area.coordinates[0][1]]]
                    },
                    "time_frame": "1 month"
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
