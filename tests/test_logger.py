import pytest
from app.logger import log_action, log_api_request, log_error
import logging
import json
from pathlib import Path
import os

@pytest.fixture(autouse=True)
def setup_logging():
    """Set up test logging configuration"""
    # Set up a test log file
    test_log_dir = Path("logs")
    test_log_dir.mkdir(exist_ok=True)
    
    # Reset logging configuration
    logging.getLogger('pinelands_wildfire').handlers = []
    
    # Configure test logger
    logger = logging.getLogger('pinelands_wildfire')
    logger.setLevel(logging.DEBUG)
    
    # Create a test handler that writes to the captured log
    test_handler = logging.StreamHandler()
    test_handler.setLevel(logging.DEBUG)
    test_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(test_handler)
    
    yield logger
    
    # Cleanup
    logger.handlers = []

def test_log_action(caplog):
    """Test action logging functionality"""
    test_action = "Test action"
    test_details = {"key": "value"}
    
    with caplog.at_level(logging.INFO):
        log_action(test_action, test_details)
    
    assert "Action: Test action" in caplog.text
    assert "key" in caplog.text
    assert "value" in caplog.text

def test_log_error(caplog):
    """Test error logging functionality"""
    test_error = ValueError("Test error")
    test_context = {"source": "test"}
    
    with caplog.at_level(logging.ERROR):
        log_error(test_error, test_context)
    
    assert "Error occurred" in caplog.text
    assert "ValueError" in caplog.text
    assert "Test error" in caplog.text
    assert "source" in caplog.text
    assert "test" in caplog.text

def test_log_api_request(caplog):
    """Test API request logging"""
    test_method = "POST"
    test_endpoint = "/api/test"
    test_params = {"param": "value"}
    test_status = 200
    
    with caplog.at_level(logging.INFO):
        log_api_request(test_method, test_endpoint, test_params, test_status)
    
    assert "API Request" in caplog.text
    assert "POST" in caplog.text
    assert "/api/test" in caplog.text
    assert "param" in caplog.text
    assert "200" in str(caplog.text)

def test_log_action_without_details(caplog):
    """Test action logging without details"""
    test_action = "Simple action"
    
    with caplog.at_level(logging.INFO):
        log_action(test_action)
    
    assert "Action: Simple action" in caplog.text
    assert "Details" not in caplog.text

def test_log_error_without_context(caplog):
    """Test error logging without context"""
    test_error = RuntimeError("Simple error")
    
    with caplog.at_level(logging.ERROR):
        log_error(test_error)
    
    assert "Error occurred" in caplog.text
    assert "RuntimeError" in caplog.text
    assert "Simple error" in caplog.text
