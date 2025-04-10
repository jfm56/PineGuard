from pathlib import Path
from typing import Dict, Optional

import numpy as np
import optuna
import pandas as pd
import shap
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

from .base_model import BaseModel

class EnsembleWildfireModel(BaseModel):
    """Ensemble model combining multiple algorithms for wildfire prediction"""
    
    def __init__(self, model_path: Optional[Path] = None):
        super().__init__(model_path)
        self.models = {
            'rf': RandomForestClassifier(random_state=42),
            'lgbm': LGBMClassifier(random_state=42),
            'catboost': CatBoostClassifier(random_state=42, verbose=False)
        }
        self.scaler = StandardScaler()
        self.feature_importance = None
    
    def preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the input data"""
        numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        # Scale numerical features
        if numerical_cols.any():
            data[numerical_cols] = self.scaler.transform(data[numerical_cols])
        
        # Encode categorical features
        if categorical_cols.any():
            data = pd.get_dummies(data, columns=categorical_cols)
        
        return data
    
    def postprocess(self, predictions: np.ndarray) -> pd.DataFrame:
        """Convert predictions to risk scores and categories"""
        risk_scores = predictions.mean(axis=1)  # Average predictions from all models
        
        return pd.DataFrame({
            'risk_score': risk_scores,
            'risk_category': pd.cut(
                risk_scores,
                bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
            )
        })
    
    def train(self, X: pd.DataFrame, y: np.ndarray, **kwargs) -> Dict[str, float]:
        """Train all models in the ensemble"""
        X_processed = self.preprocess(X)
        
        # Optimize hyperparameters using Optuna
        study = optuna.create_study(direction='maximize')
        study.optimize(lambda trial: self._objective(trial, X_processed, y), 
                      n_trials=50)
        
        # Train models with best parameters
        metrics = {}
        for name, model in self.models.items():
            model.set_params(**study.best_params[name])
            model.fit(X_processed, y)
            score = cross_val_score(model, X_processed, y, cv=5).mean()
            metrics[f'{name}_cv_score'] = score
        
        # Calculate feature importance using SHAP
        self.feature_importance = self._calculate_shap_values(X_processed)
        
        return metrics
    
    def _objective(self, trial: optuna.Trial, X: pd.DataFrame, y: np.ndarray) -> float:
        """Optimization objective for Optuna"""
        params = {
            'rf': {
                'n_estimators': trial.suggest_int('rf_n_estimators', 100, 500),
                'max_depth': trial.suggest_int('rf_max_depth', 5, 30),
                'min_samples_split': trial.suggest_int('rf_min_samples_split', 2, 10)
            },
            'lgbm': {
                'n_estimators': trial.suggest_int('lgbm_n_estimators', 100, 500),
                'max_depth': trial.suggest_int('lgbm_max_depth', 5, 30),
                'learning_rate': trial.suggest_float('lgbm_learning_rate', 0.01, 0.1)
            },
            'catboost': {
                'iterations': trial.suggest_int('catboost_iterations', 100, 500),
                'depth': trial.suggest_int('catboost_depth', 5, 30),
                'learning_rate': trial.suggest_float('catboost_learning_rate', 0.01, 0.1)
            }
        }
        
        scores = []
        for name, model in self.models.items():
            model.set_params(**params[name])
            score = cross_val_score(model, X, y, cv=5).mean()
            scores.append(score)
        
        return np.mean(scores)
    
    def _calculate_shap_values(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate SHAP values for feature importance"""
        shap_values = {}
        for name, model in self.models.items():
            explainer = shap.TreeExplainer(model)
            shap_values[name] = explainer.shap_values(X)
        return shap_values
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance based on SHAP values"""
        if self.feature_importance is None:
            raise ValueError("Model must be trained first to get feature importance")
        
        importance_df = pd.DataFrame()
        for name, shap_values in self.feature_importance.items():
            if isinstance(shap_values, list):  # For multi-class
                shap_values = np.abs(np.array(shap_values)).mean(axis=0)
            importance_df[name] = np.abs(shap_values).mean(axis=0)
        
        importance_df['mean_importance'] = importance_df.mean(axis=1)
        return importance_df.sort_values('mean_importance', ascending=False)
