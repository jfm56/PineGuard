"""Test configuration and fixtures."""
import os
import sys
from pathlib import Path

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
