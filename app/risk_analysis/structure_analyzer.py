from typing import Dict, List, Any, Optional
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from pathlib import Path

class StructureAnalyzer:
    """Analyzes risks related to structures, infrastructure, and human activity areas"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        
    def analyze_building_vulnerability(self, buildings: gpd.GeoDataFrame) -> pd.DataFrame:
        """Analyze building vulnerability based on construction, age, and materials"""
        vulnerability_scores = pd.DataFrame(index=buildings.index)
        
        # Building material risk factors
        material_risk = {
            'wood': 0.9,
            'brick': 0.4,
            'concrete': 0.2,
            'metal': 0.3,
            'mixed': 0.6
        }
        
        vulnerability_scores['material_risk'] = buildings['material'].map(material_risk)
        
        # Age risk factor (older buildings might have less fire-resistant materials)
        current_year = pd.Timestamp.now().year
        vulnerability_scores['age_risk'] = (
            (current_year - buildings['year_built']) / 100
        ).clip(0, 1)
        
        # Distance to water sources (fire hydrants, water bodies)
        vulnerability_scores['water_access'] = self._calculate_water_access(buildings)
        
        # Defensible space around buildings
        vulnerability_scores['defensible_space'] = self._analyze_defensible_space(buildings)
        
        # Calculate final vulnerability score
        weights = {
            'material_risk': 0.4,
            'age_risk': 0.2,
            'water_access': 0.2,
            'defensible_space': 0.2
        }
        
        vulnerability_scores['total_risk'] = sum(
            vulnerability_scores[col] * weight 
            for col, weight in weights.items()
        )
        
        return vulnerability_scores
    
    def analyze_camping_areas(self, 
                            camping_sites: gpd.GeoDataFrame,
                            current_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risks specific to camping areas"""
        camping_risk = {
            'site_id': [],
            'risk_score': [],
            'risk_factors': [],
            'evacuation_routes': [],
            'capacity': []
        }
        
        for _, site in camping_sites.iterrows():
            # Basic site characteristics
            site_risk = self._calculate_base_site_risk(site)
            
            # Evacuation analysis
            evacuation_routes = self._analyze_evacuation_routes(site)
            
            # Capacity vs. emergency exit capability
            capacity_risk = self._analyze_capacity_risk(
                site['capacity'],
                len(evacuation_routes)
            )
            
            # Amenity risks (fire pits, grills, etc.)
            amenity_risk = self._analyze_amenity_risks(site['amenities'])
            
            # Combine risk factors
            total_risk = (site_risk * 0.4 + 
                         capacity_risk * 0.3 +
                         amenity_risk * 0.3)
            
            camping_risk['site_id'].append(site['site_id'])
            camping_risk['risk_score'].append(total_risk)
            camping_risk['risk_factors'].append(self._get_risk_factors(site))
            camping_risk['evacuation_routes'].append(evacuation_routes)
            camping_risk['capacity'].append(site['capacity'])
        
        return pd.DataFrame(camping_risk)
    
    def analyze_traffic_patterns(self, 
                               road_network: gpd.GeoDataFrame,
                               traffic_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze traffic patterns and their impact on fire risk and evacuation"""
        
        # Merge road network with traffic data
        roads_with_traffic = road_network.merge(
            traffic_data,
            on='road_id',
            how='left'
        )
        
        # Calculate congestion risk
        congestion_risk = self._calculate_congestion_risk(roads_with_traffic)
        
        # Identify critical evacuation routes
        evacuation_routes = self._identify_evacuation_routes(roads_with_traffic)
        
        # Calculate accessibility scores
        accessibility = self._calculate_accessibility(roads_with_traffic)
        
        return {
            'congestion_risk': congestion_risk,
            'evacuation_routes': evacuation_routes,
            'accessibility_scores': accessibility
        }
    
    def _calculate_water_access(self, buildings: gpd.GeoDataFrame) -> pd.Series:
        """Calculate water access score based on distance to water sources"""
        # Load water sources (hydrants, water bodies)
        hydrants = gpd.read_file(self.data_dir / 'infrastructure/hydrants.geojson')
        water_bodies = gpd.read_file(self.data_dir / 'infrastructure/water_bodies.geojson')
        
        # Calculate distances
        hydrant_distances = buildings.geometry.apply(
            lambda x: hydrants.distance(x).min()
        )
        water_distances = buildings.geometry.apply(
            lambda x: water_bodies.distance(x).min()
        )
        
        # Normalize distances and convert to risk scores (closer = better access = lower risk)
        max_distance = 1000  # meters
        water_access = 1 - (
            (0.7 * (hydrant_distances / max_distance).clip(0, 1) +
             0.3 * (water_distances / max_distance).clip(0, 1))
        )
        
        return water_access
    
    def _analyze_defensible_space(self, buildings: gpd.GeoDataFrame) -> pd.Series:
        """Analyze defensible space around buildings using satellite imagery"""
        # Load vegetation data
        vegetation = gpd.read_file(self.data_dir / 'vegetation/vegetation_density.geojson')
        
        # Create buffers around buildings (30m standard defensible space)
        building_buffers = buildings.geometry.buffer(30)
        
        # Calculate vegetation density in buffers
        defensible_space_scores = pd.Series(index=buildings.index)
        
        for idx, buffer in building_buffers.items():
            # Clip vegetation to buffer
            buffer_vegetation = vegetation[vegetation.intersects(buffer)]
            
            # Calculate average vegetation density (higher density = higher risk)
            if len(buffer_vegetation) > 0:
                defensible_space_scores[idx] = 1 - buffer_vegetation['density'].mean()
            else:
                defensible_space_scores[idx] = 1.0  # No vegetation = best score
        
        return defensible_space_scores
    
    def _calculate_base_site_risk(self, site: gpd.GeoSeries) -> float:
        """Calculate base risk score for a camping site"""
        risk_factors = {
            'vegetation_density': 0.3,
            'slope': 0.2,
            'distance_to_water': 0.2,
            'cell_coverage': 0.15,
            'distance_to_road': 0.15
        }
        
        total_risk = 0
        for factor, weight in risk_factors.items():
            if factor in site:
                total_risk += site[factor] * weight
        
        return total_risk
    
    def _analyze_evacuation_routes(self, site: gpd.GeoSeries) -> List[Dict[str, Any]]:
        """Analyze evacuation routes from a camping site"""
        # Load road network
        roads = gpd.read_file(self.data_dir / 'infrastructure/roads.geojson')
        
        # Find nearest roads and calculate routes
        nearest_roads = roads[roads.distance(site.geometry) <= 1000]  # Within 1km
        
        routes = []
        for _, road in nearest_roads.iterrows():
            route = {
                'road_id': road['road_id'],
                'distance': road.geometry.distance(site.geometry),
                'type': road['road_type'],
                'condition': road['condition'],
                'is_paved': road['is_paved']
            }
            routes.append(route)
        
        return routes
    
    def _analyze_capacity_risk(self, capacity: int, num_exits: int) -> float:
        """Analyze risk based on site capacity and number of evacuation routes"""
        # Calculate persons per exit
        persons_per_exit = capacity / max(num_exits, 1)
        
        # Risk increases with more persons per exit
        capacity_risk = min(persons_per_exit / 50, 1.0)  # Normalize to 50 persons per exit
        
        return capacity_risk
    
    def _analyze_amenity_risks(self, amenities: List[str]) -> float:
        """Analyze risks from camping amenities"""
        risk_scores = {
            'fire_pit': 0.8,
            'grill': 0.6,
            'stove': 0.4,
            'electrical_hookup': 0.3
        }
        
        if not amenities:
            return 0.0
        
        return sum(risk_scores.get(amenity, 0.0) for amenity in amenities) / len(amenities)
    
    def _get_risk_factors(self, site: gpd.GeoSeries) -> List[str]:
        """Get list of risk factors for a camping site"""
        factors = []
        
        if site['vegetation_density'] > 0.7:
            factors.append('Dense vegetation')
        if site['slope'] > 15:
            factors.append('Steep terrain')
        if site['distance_to_water'] > 500:
            factors.append('Limited water access')
        if not site['cell_coverage']:
            factors.append('Poor cell coverage')
        if site['distance_to_road'] > 200:
            factors.append('Remote location')
        
        return factors
    
    def _calculate_congestion_risk(self, roads: gpd.GeoDataFrame) -> pd.Series:
        """Calculate congestion risk based on traffic patterns"""
        # Calculate volume/capacity ratio
        roads['congestion_ratio'] = roads['traffic_volume'] / roads['capacity']
        
        # Higher ratio = higher risk
        congestion_risk = roads['congestion_ratio'].clip(0, 1)
        
        return congestion_risk
    
    def _identify_evacuation_routes(self, roads: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Identify and prioritize evacuation routes"""
        # Calculate route priority based on:
        # - Road capacity
        # - Number of connections
        # - Distance to major highways
        # - Current traffic conditions
        
        roads['evacuation_priority'] = (
            roads['capacity'] * 0.4 +
            roads['num_connections'] * 0.3 +
            (1 / roads['distance_to_highway'].clip(1, None)) * 0.2 +
            (1 - roads['congestion_ratio']) * 0.1
        )
        
        return roads.sort_values('evacuation_priority', ascending=False)
    
    def _calculate_accessibility(self, roads: gpd.GeoDataFrame) -> pd.DataFrame:
        """Calculate accessibility scores for different areas"""
        # Group roads by area
        areas = roads.groupby('area_id')
        
        accessibility = pd.DataFrame()
        accessibility['num_routes'] = areas['road_id'].count()
        accessibility['avg_capacity'] = areas['capacity'].mean()
        accessibility['avg_congestion'] = areas['congestion_ratio'].mean()
        accessibility['emergency_access_score'] = (
            accessibility['num_routes'] * 0.4 +
            accessibility['avg_capacity'] * 0.4 +
            (1 - accessibility['avg_congestion']) * 0.2
        )
        
        return accessibility
