import pytest
from app.ml import base_model

class DummyModel(base_model.BaseModel):
    def preprocess(self, data):
        return data
    def postprocess(self, predictions):
        return predictions
    def train(self, X, y, **kwargs):
        return {"accuracy": 1.0}
    def predict(self, X):
        return [0 for _ in X]
    def fit(self, X, y):
        raise NotImplementedError

def test_base_model_instantiation():
    model = DummyModel()
    assert isinstance(model, base_model.BaseModel)

def test_predict_method():
    model = DummyModel()
    X = [[1, 2], [3, 4]]
    preds = model.predict(X)
    assert preds == [0, 0]
    assert isinstance(preds, list)

def test_fit_not_implemented():
    model = DummyModel()
    with pytest.raises(NotImplementedError):
        model.fit([[1, 2]], [0])
