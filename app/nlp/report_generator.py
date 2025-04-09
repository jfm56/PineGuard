from typing import Dict, Any, List
import pandas as pd
from pathlib import Path
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import spacy
from flair.data import Sentence
from flair.models import SequenceTagger

class ReportGenerator:
    """Generates natural language reports from wildfire analysis data"""
    
    def __init__(self):
        # Load language models
        self.nlp = spacy.load("en_core_web_lg")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.generator = pipeline("text-generation", model="gpt2")
        self.ner = SequenceTagger.load("flair/ner-english-large")
        
        # Load report templates
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load report templates for different risk levels"""
        return {
            'very_high': """The analysis indicates a very high wildfire risk in the {location} area. 
            Key factors contributing to this assessment include {factors}. Immediate preventive 
            measures are strongly recommended.""",
            
            'high': """The {location} area shows high wildfire risk potential. Notable risk 
            factors include {factors}. Implementation of preventive measures should be considered.""",
            
            'moderate': """Moderate wildfire risk has been identified in the {location} area. 
            While the immediate threat is not severe, monitoring of {factors} is recommended.""",
            
            'low': """The analysis suggests low wildfire risk in the {location} area. Regular 
            monitoring should be maintained, particularly focusing on {factors}.""",
            
            'very_low': """The {location} area currently shows very low wildfire risk. 
            Standard monitoring procedures are sufficient."""
        }
    
    def generate_risk_report(self, 
                           risk_data: Dict[str, Any],
                           location: str,
                           additional_context: Dict[str, Any] = None) -> str:
        """Generate a detailed risk assessment report"""
        # Extract risk level and factors
        risk_level = risk_data['risk_category'].lower().replace(' ', '_')
        risk_factors = self._analyze_risk_factors(risk_data)
        
        # Generate initial report from template
        template = self.templates[risk_level]
        base_report = template.format(
            location=location,
            factors=', '.join(risk_factors)
        )
        
        # Enhance report with additional analysis
        enhanced_report = self._enhance_report(
            base_report,
            risk_data,
            additional_context or {}
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_level,
            risk_factors,
            risk_data
        )
        
        # Combine all sections
        full_report = f"{enhanced_report}\n\nRecommendations:\n{recommendations}"
        
        # Generate executive summary
        summary = self._generate_summary(full_report)
        
        return {
            'summary': summary,
            'full_report': full_report,
            'risk_factors': risk_factors,
            'recommendations': recommendations
        }
    
    def _analyze_risk_factors(self, risk_data: Dict[str, Any]) -> List[str]:
        """Analyze and extract key risk factors from the data"""
        factors = []
        
        # Analyze numerical features
        for feature, value in risk_data.items():
            if isinstance(value, (int, float)):
                if feature == 'temperature' and value > 30:
                    factors.append('high temperature')
                elif feature == 'humidity' and value < 30:
                    factors.append('low humidity')
                elif feature == 'wind_speed' and value > 20:
                    factors.append('high wind speed')
        
        # Analyze vegetation data
        if 'vegetation_density' in risk_data:
            if risk_data['vegetation_density'] > 0.7:
                factors.append('dense vegetation')
        
        return factors
    
    def _enhance_report(self, 
                       base_report: str,
                       risk_data: Dict[str, Any],
                       additional_context: Dict[str, Any]) -> str:
        """Enhance the base report with additional analysis and context"""
        # Extract named entities
        doc = self.nlp(base_report)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Generate additional context
        context_prompt = f"Given the following risk factors: {', '.join(self._analyze_risk_factors(risk_data))}, "
        context_prompt += "provide detailed analysis of wildfire prevention measures."
        
        additional_analysis = self.generator(
            context_prompt,
            max_length=200,
            num_return_sequences=1
        )[0]['generated_text']
        
        # Combine base report with additional analysis
        enhanced_report = f"{base_report}\n\nDetailed Analysis:\n{additional_analysis}"
        
        return enhanced_report
    
    def _generate_recommendations(self,
                                risk_level: str,
                                risk_factors: List[str],
                                risk_data: Dict[str, Any]) -> str:
        """Generate specific recommendations based on risk assessment"""
        recommendations = []
        
        # Basic recommendations based on risk level
        if risk_level in ['very_high', 'high']:
            recommendations.append("- Implement immediate fire prevention measures")
            recommendations.append("- Increase monitoring frequency")
            recommendations.append("- Alert local fire authorities")
        
        # Factor-specific recommendations
        for factor in risk_factors:
            if 'temperature' in factor:
                recommendations.append("- Monitor weather conditions closely")
            elif 'humidity' in factor:
                recommendations.append("- Consider controlled humidification measures")
            elif 'vegetation' in factor:
                recommendations.append("- Implement vegetation management plan")
        
        return '\n'.join(recommendations)
    
    def _generate_summary(self, full_report: str) -> str:
        """Generate an executive summary of the full report"""
        summary = self.summarizer(
            full_report,
            max_length=130,
            min_length=30,
            do_sample=False
        )[0]['summary_text']
        
        return summary
