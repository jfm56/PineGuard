"""Test configuration and fixtures."""
import os
import sys
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.fire_risk import router

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def app_fixture():
    """Alias for FastAPI app fixture used in tests."""
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def test_client_fixture(app_fixture):
    """Alias for TestClient fixture used in tests."""
    return TestClient(app_fixture)
