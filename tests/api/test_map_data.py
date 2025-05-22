import pytest
import app.api.map_data as map_data

def test_map_data_import():
    assert hasattr(map_data, "__doc__")
