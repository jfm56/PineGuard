
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure the logger
logger = logging.getLogger('pinelands_wildfire')
logger.setLevel(logging.DEBUG)

# Create formatters
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)

# Create rotating file handler for debug logs
debug_log_file = os.path.join(logs_dir, 'debug.log')
file_handler = RotatingFileHandler(
    debug_log_file,
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

# Create rotating file handler for error logs
error_log_file = os.path.join(logs_dir, 'error.log')
error_file_handler = RotatingFileHandler(
    error_log_file,
    maxBytes=10485760,  # 10MB
    backupCount=5
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(file_formatter)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(error_file_handler)
logger.addHandler(console_handler)

def log_action(action, details=None, level=logging.INFO):
    """
    Log an action with optional details.
    
    Args:
        action (str): The action being performed
        details (dict, optional): Additional details about the action
        level (int): Logging level (default: INFO)
    """
    if details:
        logger.log(level, "Action: %s - Details: %s", action, details)
    else:
        logger.log(level, "Action: %s", action)

def log_api_request(method, endpoint, params=None, response_status=None):
    """
    Log API request details.
    
    Args:
        method (str): HTTP method
        endpoint (str): API endpoint
        params (dict, optional): Request parameters
        response_status (int, optional): Response status code
    """
    details = {
        'method': method,
        'endpoint': endpoint,
        'params': params,
        'response_status': response_status,
        'timestamp': datetime.now().isoformat()
    }
    logger.info("API Request - %s", details)

def log_error(error, context=None):
    """
    Log an error with optional context.
    
    Args:
        error (Exception): The error that occurred
        context (dict, optional): Additional context about the error
    """
    error_details = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context
    }
    logger.error("Error occurred: %s", error_details, exc_info=True)
