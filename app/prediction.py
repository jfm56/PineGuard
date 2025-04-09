from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import numpy as np
import pandas as pd
import geopandas as gpd

from .ml.ensemble_wildfire_model import EnsembleWildfireModel
from .cv.satellite_analyzer import SatelliteAnalyzer
from .nlp.report_generator import ReportGenerator
from .risk_analysis.structure_analyzer import StructureAnalyzer
from .risk_analysis.fuel_analyzer import FuelAnalyzer
from .data_processing.data_loader import DataLoader

class WildfirePredictor:
    def __init__(self, model_path: Optional[Path] = None, data_dir: Optional[Path] = None):
        """Initialize the wildfire prediction system with ML, CV, NLP, and risk analysis components"""
        # Initialize ML model
        self.ml_model = EnsembleWildfireModel(model_path)
        
        # Initialize CV analyzer
        self.cv_analyzer = SatelliteAnalyzer()
        
        # Initialize NLP report generator
        self.report_generator = ReportGenerator()
        
        # Initialize risk analyzers
        self.structure_analyzer = StructureAnalyzer(data_dir) if data_dir else None
        self.fuel_analyzer = FuelAnalyzer(data_dir) if data_dir else None
        self.data_loader = DataLoader(data_dir) if data_dir else None
    
    def analyze_area(self, 
                     area_data: gpd.GeoDataFrame,
                     satellite_image: Optional[np.ndarray] = None,
                     location_name: str = "selected area",
                     date: Optional[pd.Timestamp] = None) -> Dict[str, Any]:
        """Comprehensive area analysis using ML, CV, NLP, and risk analysis components"""
        date = date or pd.Timestamp.now()
        
        # Get ML predictions
        ml_predictions = self.ml_model.predict(area_data)
        
        # Initialize results dictionary
        results = {
            'risk_predictions': ml_predictions,
            'feature_importance': self.ml_model.get_feature_importance()
        }
        
        # Add satellite analysis
        vegetation_indices = None
        if satellite_image is not None:
            vegetation_indices = self.cv_analyzer.analyze_vegetation(satellite_image)
            burn_analysis = self.cv_analyzer.detect_burn_scars(satellite_image)
            
            results.update({
                'vegetation_analysis': vegetation_indices,
                'burn_analysis': burn_analysis
            })
        
        # Add structure and infrastructure analysis
        if self.structure_analyzer and self.data_loader:
            # Load additional data
            weather_data = self.data_loader.load_weather_data(area_data, date)
            traffic_data = self.data_loader.load_traffic_data(area_data, date)
            buildings = self.data_loader.load_buildings(area_data)
            camping_sites = self.data_loader.load_camping_sites(area_data)
            road_network = self.data_loader.load_road_network(area_data)
            
            # Analyze structures and infrastructure
            structure_risks = self.structure_analyzer.analyze_building_vulnerability(buildings)
            traffic_analysis = self.structure_analyzer.analyze_traffic_patterns(
                road_network,
                traffic_data
            )
            camping_risks = self.structure_analyzer.analyze_camping_areas(
                camping_sites,
                {
                    'weather': weather_data,
                    'vegetation': vegetation_indices
                }
            )
            
            results.update({
                'structure_risks': structure_risks.to_dict(orient='records'),
                'traffic_analysis': traffic_analysis,
                'camping_risks': camping_risks.to_dict(orient='records')
            })
            
            # Add fuel hazard analysis
            if self.fuel_analyzer:
                fuel_hazards = self.fuel_analyzer.analyze_fuel_hazards(
                    area_data,
                    weather_data,
                    vegetation_indices
                )
                results['fuel_hazards'] = fuel_hazards
        
        # Generate natural language report
        report_data = {
            'risk_category': ml_predictions['risk_category'].mode()[0],
            'risk_score': float(ml_predictions['risk_score'].mean()),
            'temperature': float(area_data['temperature'].mean()),
            'humidity': float(area_data['humidity'].mean()),
            'wind_speed': float(area_data['wind_speed'].mean())
        }
        
        if satellite_image is not None:
            report_data.update({
                'vegetation_density': vegetation_indices['ndvi_mean'],
                'burn_area_percentage': burn_analysis['burn_area_percentage']
            })
        
        # Add structure and fuel hazard data to report if available
        if 'structure_risks' in results:
            report_data.update({
                'high_risk_structures': len([s for s in results['structure_risks'] if s['total_risk'] > 0.7]),
                'high_risk_camps': len([c for c in results['camping_risks'] if c['risk_score'] > 0.7])
            })
        
        if 'fuel_hazards' in results:
            report_data['fuel_hazard_score'] = results['fuel_hazards']['hazard_score']
        
        report = self.report_generator.generate_risk_report(
            risk_data=report_data,
            location=location_name
        )
        
        results['report'] = report
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate comprehensive risk mitigation recommendations"""
        recommendations = []
        
        # Add general risk level recommendation
        risk_category = analysis_results['risk_predictions']['risk_category'].mode()[0]
        recommendations.append(f"Current Risk Level: {risk_category}")
        
        # Structure recommendations
        if 'structure_risks' in analysis_results:
            high_risk_structures = [
                s for s in analysis_results['structure_risks']
                if s['total_risk'] > 0.7
            ]
            if high_risk_structures:
                recommendations.append(
                    f"Prioritize protection of {len(high_risk_structures)} high-risk structures"
                )
        
        # Camping recommendations
        if 'camping_risks' in analysis_results:
            high_risk_camps = [
                c for c in analysis_results['camping_risks']
                if c['risk_score'] > 0.7
            ]
            if high_risk_camps:
                recommendations.append(
                    f"Consider closing {len(high_risk_camps)} high-risk camping areas"
                )
        
        # Traffic and evacuation recommendations
        if 'traffic_analysis' in analysis_results:
            traffic = analysis_results['traffic_analysis']
            if traffic['congestion_risk'].mean() > 0.7:
                recommendations.append(
                    "High traffic congestion risk. Review evacuation routes."
                )
        
        # Fuel management recommendations
        if 'fuel_hazards' in analysis_results:
            recommendations.extend(
                analysis_results['fuel_hazards']['recommendations']
            )
        
        return recommendations
    
    def train_model(self, 
                    X: Union[pd.DataFrame, gpd.GeoDataFrame], 
                    y: np.ndarray,
                    **kwargs) -> Dict[str, float]:
        """Train the ML model with the provided data"""
        return self.ml_model.train(X, y, **kwargs)
    
    def save_model(self, path: Path) -> None:
        """Save the ML model to disk"""
        self.ml_model.save_model(path)
    
    def load_model(self, path: Path) -> None:
        """Load the ML model from disk"""
        self.ml_model.load_model(path)
