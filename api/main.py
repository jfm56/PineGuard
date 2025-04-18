from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnvironmentalFactors(BaseModel):
    vegetation: dict
    terrain: dict
    vegetationRisk: float

class GridCell(BaseModel):
    lat: float
    lng: float
    riskScore: float
    historicalFires: int
    environmentalFactors: EnvironmentalFactors

class SimulationParams(BaseModel):
    windSpeed: float
    windDirection: float
    humidity: float
    temperature: float
    duration: int

@app.get("/api/risk-data")
async def get_risk_data():
    # Mock data - replace with actual data processing
    return {
        "data": [
            {
                "lat": 39.8283,
                "lng": -74.5411,
                "riskScore": 0.75,
                "historicalFires": 3,
                "environmentalFactors": {
                    "vegetation": {
                        "density": 0.8,
                        "fuelType": "pine",
                        "ndvi": 0.6
                    },
                    "terrain": {
                        "elevation": 50,
                        "slope": 5
                    },
                    "vegetationRisk": 0.7
                }
            }
        ]
    }

@app.post("/api/simulate-fire")
async def simulate_fire(params: SimulationParams):
    try:
        # Mock simulation - replace with actual fire spread simulation
        return {
            "success": True,
            "prediction": [
                {
                    "lat": 39.8283,
                    "lng": -74.5411,
                    "intensity": 0.8,
                    "timeStep": 1
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
