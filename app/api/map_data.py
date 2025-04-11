from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np
from ..config import PINE_BARRENS, FIRE_STATIONS, WATER_SOURCES, EVACUATION_ROUTES

router = APIRouter()

def calculate_risk_areas() -> List[Dict[str, Any]]:
    """Calculate fire risk areas based on current conditions and historical data"""
    risk_areas = []
    
    # Example risk areas (in real implementation, this would use ML model predictions)
    high_risk_areas = [
        {'coords': [39.7825, -74.5338], 'severity': 2.5},
        {'coords': [39.8521, -74.6506], 'severity': 2.0}
    ]
    
    moderate_risk_areas = [
        {'coords': [39.6624, -74.7185], 'severity': 1.5},
        {'coords': [39.7083, -74.6895], 'severity': 1.2}
    ]
    
    # Process high risk areas
    for area in high_risk_areas:
        risk_areas.append({
            'coords': area['coords'],
            'riskLevel': 'High',
            'severity': area['severity'],
            'factors': [
                {'name': 'Vegetation Dryness', 'value': 'Critical'},
                {'name': 'Wind Speed', 'value': 'High'},
                {'name': 'Temperature', 'value': 'Above Average'}
            ]
        })
    
    # Process moderate risk areas
    for area in moderate_risk_areas:
        risk_areas.append({
            'coords': area['coords'],
            'riskLevel': 'Moderate',
            'severity': area['severity'],
            'factors': [
                {'name': 'Vegetation Dryness', 'value': 'Moderate'},
                {'name': 'Wind Speed', 'value': 'Moderate'},
                {'name': 'Temperature', 'value': 'Average'}
            ]
        })
    
    return risk_areas

@router.get("/api/map-data")
async def get_map_data():
    """Get all map data including fire stations, water sources, and evacuation routes"""
    try:
        return {
            'fireStations': FIRE_STATIONS,
            'waterSources': WATER_SOURCES,
            'evacuationRoutes': EVACUATION_ROUTES,
            'bounds': PINE_BARRENS['bounds']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/fire-risk")
async def get_fire_risk(timeRange: str = "current"):
    """Get fire risk areas based on time range"""
    try:
        risk_areas = calculate_risk_areas()
        
        # Adjust risk areas based on time range
        if timeRange == "24h":
            # Add predicted risk areas for next 24 hours
            future_risks = [
                {
                    'coords': [39.7449, -74.5621],
                    'riskLevel': 'High',
                    'severity': 2.0,
                    'factors': [
                        {'name': 'Predicted Temperature', 'value': 'Rising'},
                        {'name': 'Wind Forecast', 'value': 'Increasing'},
                        {'name': 'Drought Index', 'value': 'Worsening'}
                    ]
                }
            ]
            risk_areas.extend(future_risks)
        elif timeRange == "week":
            # Add predicted risk areas for next week
            weekly_risks = [
                {
                    'coords': [39.6431, -74.5167],
                    'riskLevel': 'Moderate',
                    'severity': 1.5,
                    'factors': [
                        {'name': 'Long-term Forecast', 'value': 'Dry Conditions'},
                        {'name': 'Seasonal Trend', 'value': 'Above Average'},
                        {'name': 'Vegetation State', 'value': 'Deteriorating'}
                    ]
                }
            ]
            risk_areas.extend(weekly_risks)
        
        return {
            'riskAreas': risk_areas,
            'timestamp': datetime.now().isoformat(),
            'timeRange': timeRange
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
