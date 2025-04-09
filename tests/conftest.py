import pytest
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / 'test_data'

@pytest.fixture
def sample_features():
    return pd.DataFrame({
        'temperature': [25, 30, 35],
        'humidity': [60, 50, 40],
        'wind_speed': [10, 15, 20],
        'vegetation_density': [0.4, 0.6, 0.8]
    })

@pytest.fixture
def sample_labels():
    return np.array([0, 1, 1])  # Binary labels for fire risk
