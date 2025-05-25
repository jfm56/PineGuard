import numpy as np
import pandas as pd
import pytest
import shap
from app.ml.ensemble_wildfire_model import EnsembleWildfireModel


class DummyTrial:
    def suggest_int(self, name, low, high):
        return low
    def suggest_float(self, name, low, high):
        return low


def test_objective_returns_mean_score(monkeypatch):
    import app.ml.ensemble_wildfire_model as ewm
    # Stub cross_val_score to return array of 1s
    monkeypatch.setattr(ewm, 'cross_val_score', lambda model, X, y, cv: np.ones(cv))
    model = EnsembleWildfireModel()
    X = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    y = np.array([0, 1, 0])
    trial = DummyTrial()
    result = model._objective(trial, X, y)
    assert isinstance(result, float)
    assert np.isclose(result, 1.0)


def test_calculate_shap_values(monkeypatch):
    # Stub TreeExplainer to return ones
    class FakeExplainer:
        def __init__(self, model): pass
        def shap_values(self, X): return np.ones((X.shape[0], X.shape[1]))
    monkeypatch.setattr(shap, 'TreeExplainer', FakeExplainer)
    model = EnsembleWildfireModel()
    # Use minimal models dict
    model.models = {'rf': object(), 'lgbm': object()}
    X = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    shap_vals = model._calculate_shap_values(X)
    assert set(shap_vals.keys()) == {'rf', 'lgbm'}
    for arr in shap_vals.values():
        assert isinstance(arr, np.ndarray)
        assert arr.shape == (2, 2)


def test_get_feature_importance_multiclass():
    model = EnsembleWildfireModel()
    # Two-class list for multiclass branch
    arr1 = np.array([[1, 2, 3], [4, 5, 6]])
    arr2 = np.array([[2, 3, 4], [5, 6, 7]])
    model.feature_importance = {'rf': [arr1, arr2], 'lgbm': [arr1, arr2]}
    fi = model.get_feature_importance()
    assert 'mean_importance' in fi.columns
    assert set(fi.columns) == {'rf', 'lgbm', 'mean_importance'}
    assert len(fi) == 3


def test_get_feature_importance_no_train():
    model = EnsembleWildfireModel()
    model.feature_importance = None
    with pytest.raises(ValueError):
        model.get_feature_importance()


def test_generate_alerts():
    model = EnsembleWildfireModel()
    result = model.generate_alerts({'risk_score': 0.5})
    assert result == []
