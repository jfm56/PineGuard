from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union
import joblib
from pathlib import Path

class BaseModel(ABC):
    """Base class for all ML models in the application"""
    
    def __init__(self, model_path: Optional[Path] = None):
        self.model = None
        self.model_path = model_path
        if model_path and model_path.exists():
            self.load_model(model_path)
    
    @abstractmethod
    def preprocess(self, data: Union[pd.DataFrame, np.ndarray]) -> Union[pd.DataFrame, np.ndarray]:
        """Preprocess input data before prediction"""
        pass
    
    @abstractmethod
    def postprocess(self, predictions: np.ndarray) -> Union[pd.DataFrame, np.ndarray]:
        """Postprocess model predictions"""
        pass
    
    @abstractmethod
    def train(self, X: Union[pd.DataFrame, np.ndarray], y: np.ndarray, **kwargs) -> Dict[str, float]:
        """Train the model and return metrics"""
        pass
    
    def predict(self, data: Union[pd.DataFrame, np.ndarray]) -> Union[pd.DataFrame, np.ndarray]:
        """Make predictions using the model"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        
        processed_data = self.preprocess(data)
        predictions = self.model.predict(processed_data)
        return self.postprocess(predictions)
    
    def save_model(self, path: Path) -> None:
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")
        joblib.dump(self.model, path)
        self.model_path = path
    
    def load_model(self, path: Path) -> None:
        """Load model from disk"""
        self.model = joblib.load(path)
        self.model_path = path
