from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
VISUAL_CROSSING_API_KEY = os.getenv('VISUAL_CROSSING_API_KEY', 'YOUR_API_KEY')

# Pine Barrens Region Configuration
PINE_BARRENS = {
    'center': [39.8, -74.5],  # Latitude, Longitude
    'zoom': 9,
    'bounds': {
        'north': 40.2,  # Northern boundary
        'south': 39.4,  # Southern boundary
        'east': -74.2,  # Eastern boundary
        'west': -74.8   # Western boundary
    }
}

# Fire Stations in Pine Barrens
FIRE_STATIONS = [
    {'name': 'Chatsworth Fire Company', 'coords': [39.8155, -74.5338]},
    {'name': 'Indian Mills Fire Company', 'coords': [39.7825, -74.7185]},
    {'name': 'Tabernacle Fire Company', 'coords': [39.8521, -74.7185]},
    {'name': 'Green Bank Fire Company', 'coords': [39.6338, -74.5621]},
]

# Water Sources
WATER_SOURCES = [
    {'name': 'Batsto Lake', 'coords': [39.6431, -74.6506]},
    {'name': 'Atsion Lake', 'coords': [39.7449, -74.7285]},
    {'name': 'Harrisville Lake', 'coords': [39.6624, -74.5271]},
    {'name': 'Lake Oswego', 'coords': [39.7083, -74.5167]},
]

# Evacuation Routes
EVACUATION_ROUTES = [
    {
        'name': 'Route 72 East',
        'path': [
            [39.7438, -74.3813],
            [39.7456, -74.5338],
            [39.7465, -74.6895]
        ]
    },
    {
        'name': 'Route 70 East',
        'path': [
            [39.8854, -74.3729],
            [39.8863, -74.5271],
            [39.8872, -74.6784]
        ]
    },
    {
        'name': 'Garden State Parkway North',
        'path': [
            [39.4672, -74.4813],
            [39.6338, -74.4729],
            [39.8155, -74.4646]
        ]
    }
]
