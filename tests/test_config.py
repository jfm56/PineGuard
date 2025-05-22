import pytest
import app.config as config

def test_config_import():
    assert hasattr(config, "__doc__")
