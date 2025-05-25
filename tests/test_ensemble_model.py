import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import optuna
import joblib

from app.ml.ensemble_wildfire_model import EnsembleWildfireModel

# Dummy study to bypass Optuna optimization
class DummyStudy:
    best_params = {
        'rf': {'n_estimators': 10, 'max_depth': 5, 'min_samples_split': 2},
        'lgbm': {'n_estimators': 10, 'max_depth': 5, 'learning_rate': 0.1},
        'catboost': {'iterations': 10, 'depth': 5, 'learning_rate': 0.1}
    }
    def __init__(self, **kwargs):
        pass
    def optimize(self, func, n_trials):
        return None

@pytest.fixture(autouse=True)
def patch_optuna(monkeypatch):
    monkeypatch.setattr(optuna, 'create_study', lambda **kwargs: DummyStudy())
    return None

def test_preprocess_scaling_and_encoding():
    model = EnsembleWildfireModel()
    # Identity scaler
    model.scaler = type('S', (), {'transform': lambda self, arr: arr})()
    df = pd.DataFrame({'num': [1, 2], 'cat': ['a', 'b']})
    result = model.preprocess(df.copy())
    assert 'num' in result.columns
    # One-hot encoding applied
    assert 'cat_a' in result.columns and 'cat_b' in result.columns


def test_postprocess_outputs_correct_df():
    model = EnsembleWildfireModel()
    preds = np.array([[0.1, 0.3], [0.6, 0.8]])
    df = model.postprocess(preds)
    assert 'risk_score' in df.columns and 'risk_category' in df.columns
    # Scores are means
    assert np.isclose(df['risk_score'].iloc[0], 0.2)
    assert np.isclose(df['risk_score'].iloc[1], 0.7)


def test_predict_without_model_raises():
    model = EnsembleWildfireModel()
    with pytest.raises(ValueError):
        model.predict(pd.DataFrame({'x': [0]}))


def test_save_and_load_model(tmp_path, monkeypatch):
    model = EnsembleWildfireModel()
    # Assign dummy model for save
    dummy_obj = object()
    model.model = dummy_obj
    save_path = tmp_path / 'm.pkl'
    calls = {}
    def fake_dump(obj, path):
        calls['obj'] = obj
        calls['path'] = path
    def fake_load(path):
        assert path == save_path
        return dummy_obj
    monkeypatch.setattr(joblib, 'dump', fake_dump)
    monkeypatch.setattr(joblib, 'load', fake_load)
    model.save_model(save_path)
    assert calls['obj'] is dummy_obj
    assert calls['path'] == save_path
    # Clear and reload
    model.model = None
    model.load_model(save_path)
    assert model.model is dummy_obj


def test_train_and_feature_importance(monkeypatch):
    # Stub cross_val_score in ensemble module and sklearn.model_selection
    import app.ml.ensemble_wildfire_model as ewm_module
    stub = lambda m, X, y, cv: np.ones(cv)
    monkeypatch.setattr(ewm_module, 'cross_val_score', stub)
    import sklearn.model_selection as ms
    monkeypatch.setattr(ms, 'cross_val_score', stub)
    # Stub shap values
    dummy_shap = np.array([[0.1, 0.2]])
    monkeypatch.setattr(EnsembleWildfireModel, '_calculate_shap_values',
                        lambda self, X: {'rf': dummy_shap, 'lgbm': dummy_shap, 'catboost': dummy_shap})
    X = pd.DataFrame({'f1': [0,1,0], 'f2': [1,0,1]})
    y = np.array([0,1,0])
    model = EnsembleWildfireModel()
    # Stub scaler to bypass fit requirement
    model.scaler = type('S', (), {'transform': lambda self, arr: arr})()
    metrics = model.train(X, y)
    # Check metrics keys and values
    for key in ['rf_cv_score', 'lgbm_cv_score', 'catboost_cv_score']:
        assert key in metrics
        assert metrics[key] == 1.0
    fi = model.get_feature_importance()
    assert 'mean_importance' in fi.columns
    # Feature importance shape matches number of features
    assert len(fi) == X.shape[1]
