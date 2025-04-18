from datetime import datetime
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel

from app.api import fire_risk, map_data  # Import the fire risk and map data modules

from app.logger import logger, log_action, log_api_request, log_error

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PineGuard API",
    description="Wildfire risk prediction and management system for the New Jersey Pinelands",
    version="1.0.0"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the routers
app.include_router(fire_risk.router)
app.include_router(map_data.router)

@app.get("/")
async def read_root():
    log_action("Serving index page")
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
    area_geometry: Dict[str, Any]
    date: str = None

class RiskPrediction(BaseModel):
    risk_score: float
    confidence: float
    risk_factors: Dict[str, float]
    timestamp: str

@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    log_action("Health check request")
    return {"status": "healthy"}

class DetailedRiskPrediction(RiskPrediction):
    environmental_factors: Dict[str, float]
    historical_data: Dict[str, Any]
    infrastructure_risk: Dict[str, float]
    mitigation_recommendations: List[Dict[str, Any]]

@app.post("/api/v1/predict", response_model=DetailedRiskPrediction)
async def predict_risk(area: Area, analysis_mode: str = "basic", request: Request = None):
    """Predict wildfire risk for an area with specified analysis mode (basic or professional)"""
    # Log API request
    log_api_request(
        method="POST",
        endpoint="/api/v1/predict",
        params={"analysis_mode": analysis_mode, "area": area.area_geometry}
    )

    # Validate analysis mode
    if analysis_mode not in ["basic", "professional"]:
        log_error(ValueError("Invalid analysis mode"), {"analysis_mode": analysis_mode})
        raise HTTPException(status_code=400, detail="Invalid analysis mode. Must be 'basic' or 'professional'")
    try:
        # Basic environmental factors (always included)
        environmental_factors = {
            "temperature": 0.8,  # High temperature risk
            "humidity": 0.7,    # Low humidity risk
            "wind_speed": 0.6,  # Moderate wind risk
        }
        
        # Calculate risk score based on environmental factors
        risk_score = 0.75  # Example risk score
        confidence = 0.85  # Example confidence
        risk_factors = {
            "temperature": 0.8,
            "wind_speed": 0.7,
            "vegetation": 0.6
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
                        "coordinates": [[area.area_geometry["coordinates"][0][0][0], area.area_geometry["coordinates"][0][0][1]],
                                      [area.area_geometry["coordinates"][0][0][0] + 0.1, area.area_geometry["coordinates"][0][0][1]]]
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
                        "coordinates": [[area.area_geometry["coordinates"][0][0][0], area.area_geometry["coordinates"][0][0][1]],
                                      [area.area_geometry["coordinates"][0][0][0] + 0.1, area.area_geometry["coordinates"][0][0][1]]]
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
        log_error(e, {
            "analysis_mode": analysis_mode,
            "coordinates": area.coordinates,
        })
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/regions")
async def get_regions(request: Request = None):
    log_api_request(method="GET", endpoint="/api/v1/regions")
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

@app.post("/api/v1/log-error")
async def log_frontend_error(request: Request):
    try:
        error_data = await request.json()
        log_error(
            Exception(error_data.get('message', 'Unknown frontend error')),
            context={
                'source': 'frontend',
                'details': error_data.get('details'),
                'stack': error_data.get('stack')
            }
        )
        return {"status": "logged"}
    except Exception as e:
        log_error(e, {"context": "Error logging frontend error"})
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/camping-sites/{site_id}/risk")
async def get_camping_site_risk(site_id: str, request: Request = None):
    log_api_request(method="GET", endpoint=f"/api/v1/camping-sites/{site_id}/risk")
    return {
        "site_risk": 0.7,
        "max_capacity": 100,
        "evacuation_time": 15
    }

@app.post("/api/v1/structures/analyze")
async def analyze_structures(request: Request):
    data = await request.json()
    log_api_request(method="POST", endpoint="/api/v1/structures/analyze", params=data)
    return {
        "buildings": [
            {
                "id": "B001",
                "risk_score": 0.7,
                "evacuation_priority": "high"
            }
        ]
    }

@app.get("/api/v1/traffic/analysis")
async def analyze_traffic(area: str, request: Request = None):
    log_api_request(method="GET", endpoint="/api/v1/traffic/analysis", params={"area": area})
    return {
        "current_flow": "moderate",
        "evacuation_capacity": 1000,
        "recommended_routes": [
            {
                "id": "R1",
                "congestion": "low",
                "estimated_time": 15
            }
        ]
    }

@app.get("/api/v1/weather/current")
async def get_current_weather(request: Request = None):
    """Get current weather conditions for the Pinelands area"""
    log_api_request(method="GET", endpoint="/api/v1/weather/current")
    
    # These values are more typical for the New Jersey Pinelands
    # Temperature range: 75-80°F in summer
    # Humidity range: 50-70% (coastal influence)
    # Wind speed: 5-10 mph average
    return {
        "temperature": 78,  # °F
        "humidity": 65,    # %
        "wind_speed": 8,   # mph
        "conditions": "Partly Cloudy",
        "timestamp": datetime.now().isoformat(),
        "location": "New Jersey Pinelands"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting PineGuard application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
