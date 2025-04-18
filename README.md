# PineGuard: Advanced Wildfire Risk Prediction System

[![Docker](https://img.shields.io/docker/v/jmullen029/pineguard?label=Docker)](https://hub.docker.com/r/jmullen029/pineguard)
[![GitHub](https://img.shields.io/github/v/release/jfm56/PineGuard?label=GitHub)](https://github.com/jfm56/PineGuard)
[![License](https://img.shields.io/github/license/jfm56/PineGuard)](https://github.com/jfm56/PineGuard/blob/main/LICENSE)

PineGuard is a comprehensive wildfire risk prediction and management system specifically designed for the New Jersey Pinelands. It leverages state-of-the-art machine learning models, real-time satellite imagery analysis, and natural language processing to provide accurate risk assessments and actionable recommendations. The system is particularly focused on protecting critical infrastructure, camping areas, and managing evacuation routes in the unique ecosystem of the Pinelands.

## Target Users & Use Cases

### Primary Stakeholders

1. **Government Agencies**
   - NJ Pinelands Commission: Land use planning and conservation
   - Local Fire Departments: Resource allocation and response planning
   - Municipal Governments: Emergency preparedness
   - County Emergency Services: Evacuation planning

2. **Commercial Users**
   - Insurance Companies: Risk assessment and policy pricing
   - Environmental Consultants: Impact studies and recommendations
   - Property Developers: Site selection and risk mitigation
   - Forestry Companies: Resource management

3. **Research & Education**
   - Universities: Environmental research
   - Conservation Groups: Ecosystem protection
   - Educational Institutions: Environmental education

### Subscription Tiers

#### Basic (Free)
- Basic risk assessment
- Public data access
- Standard resolution maps
- Daily updates

#### Professional ($199/month)
- Real-time risk monitoring
- High-resolution satellite imagery
- Custom area analysis
- API access
- Email alerts
- PDF report generation

#### Enterprise (Custom Pricing)
- Custom model training
- Integration support
- SLA guarantees
- Dedicated support
- White-label options
- Custom features

## How It Works

PineGuard employs a multi-layered approach to wildfire risk prediction and visualization:

1. **Data Collection and Integration**
   - Real-time weather data integration
   - Google Maps Platform for visualization
   - Historical wildfire incident data
   - Environmental sensor networks
   - Terrain and vegetation analysis
   - Wind patterns and weather conditions

2. **Risk Analysis**
   - Machine Learning: Ensemble of RandomForest, LightGBM, and CatBoost models
   - Computer Vision: U-Net model for vegetation and burn scar detection
   - Natural Language Processing: BERT-based model for report generation
   - Time Series Analysis: Prophet model for trend prediction

3. **Real-time Monitoring**
   - Continuous satellite imagery analysis
   - Weather condition tracking
   - Traffic flow monitoring
   - Camping site occupancy tracking

4. **Automated Response**
   - Dynamic evacuation route generation
   - Real-time safety alerts
   - Resource allocation recommendations
   - Preventive measure suggestions

## Key Features

### 1. Advanced Risk Prediction
- Ensemble machine learning model combining RandomForest, LightGBM, and CatBoost
- Real-time satellite imagery analysis
- Natural language report generation
- Time series forecasting capabilities

### 2. Structure and Infrastructure Analysis
- Building vulnerability assessment
- Traffic pattern analysis
- Evacuation route planning
- Infrastructure risk mapping

### 3. Camping Area Safety
- Site-specific risk assessment
- Evacuation route analysis
- Capacity management
- Real-time safety recommendations

### 4. Fuel Hazard Analysis
- Comprehensive fuel assessment
- Moisture content monitoring
- Seasonal risk adjustment
- Vegetation analysis

### 5. Interactive Visualization
- Real-time risk maps with Google Maps integration
- Dynamic heatmap visualization of fire risk
- Weather-based risk assessment
- Fire spread simulation with wind factors
- Historical wildfire data overlay
- Interactive controls for risk analysis

## Installation

### Development Setup
```bash
# Clone the repository
git clone https://github.com/jfm56/PineGuard.git
cd PineGuard

# Install dependencies
npm install

# Run the development server
npm run dev
```

### Using Docker
```bash
# Pull the Docker image
docker pull jmullen029/pineguard

# Run the container
docker run -p 3000:3000 jmullen029/pineguard
```

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/jfm56/PineGuard.git
cd PineGuard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
# API Keys
NOAA_API_KEY=your_noaa_api_key
SENTINEL_HUB_API_KEY=your_sentinel_hub_key

# Data Paths
DATA_DIR=path/to/data/directory
MODEL_DIR=path/to/model/directory

# Server Configuration
PORT=8080
DEBUG=False
```

### Data Sources & Requirements

### Primary Data Sources

1. **New Jersey Forest Fire Service (NJFFS)**
   - Historical wildfire records
   - Fire occurrence patterns
   - Suppression effort data
   - Contact: [NJFFS Official Website](https://www.nj.gov/dep/parksandforests/fire/)

2. **New Jersey Department of Environmental Protection (NJDEP)**
   - Environmental datasets
   - Geospatial data
   - Access: [NJDEP Open Data Portal](https://njdep.maps.arcgis.com/home/index.html)

3. **Fire History Spatial Database (1927-2007)**
   - 80-year historical data
   - Division B and northern Division C coverage
   - Access: [Figshare Dataset](https://figshare.com)

4. **U.S. Forest Service FPA FOD**
   - National wildfire records (1992-2015)
   - New Jersey-specific incidents
   - Comprehensive metadata

5. **New Jersey Pinelands Commission**
   - Ecological assessments
   - Land use data
   - Environmental factors
   - Access: [Commission Data Resources](https://www.nj.gov/pinelands/)

### Additional Data Requirements

1. **Weather Data**
   - NOAA API access
   - Real-time weather feeds
   - Historical weather patterns

2. **Satellite Imagery**
   - Sentinel Hub access
   - 10m resolution imagery
   - Multi-spectral bands

3. **Infrastructure Data**
   - Building footprints
   - Road networks
   - Evacuation routes

4. **Environmental Sensors**
   - Temperature sensors
   - Humidity monitors
   - Wind speed meters

### Data Integration Guidelines

1. **Format Standardization**
   - Consistent coordinate systems
   - Unified temporal resolution
   - Standard data schemas

2. **Quality Control**
   - Data validation
   - Missing value handling
   - Outlier detection

3. **Update Frequency**
   - Real-time: Weather, sensors
   - Daily: Satellite imagery
   - Monthly: Infrastructure updates
   - Yearly: Historical records

4. **Access Control**
   - API key management
   - Data usage agreements
   - Privacy compliance

### Data Processing Pipeline

```plaintext
                                 ┌─────────────────┐
                                 │  Data Sources   │
                                 └────────┬────────┘
                                          ▼
┌─────────────────┐  ┌──────────────────────────────┐  ┌─────────────────┐
│  Raw Data APIs  │──▶│      Data Collectors        │──▶│  Data Storage   │
└─────────────────┘  │  - NJFFS Collector          │  └────────┬────────┘
                     │  - NJDEP Collector          │           ▼
┌─────────────────┐  │  - Weather Collector        │  ┌─────────────────┐
│  File Uploads   │──▶│  - Satellite Collector     │──▶│ Data Processing │
└─────────────────┘  └──────────────────────────────┘  └────────┬────────┘
                                                                ▼
                     ┌──────────────────────────────┐  ┌─────────────────┐
                     │      Feature Pipeline        │◀─▶│   Data Lake    │
                     │  - Temporal Features        │  └────────┬────────┘
                     │  - Spatial Features         │           ▼
                     │  - Weather Features         │  ┌─────────────────┐
                     │  - Historical Features      │──▶│  Model Input   │
                     └──────────────────────────────┘  └─────────────────┘
```

#### Data Collection

1. **NJFFS Data**
   ```python
   # Example data collection from NJFFS API
   from app.collectors import NJFFSCollector
   
   collector = NJFFSCollector()
   historical_data = collector.get_historical_fires(
       start_date="1927-01-01",
       end_date="2007-12-31",
       division="B"
   )
   ```

2. **Satellite Data**
   ```python
   # Example Sentinel Hub data collection
   from app.collectors import SentinelCollector
   
   collector = SentinelCollector()
   imagery = collector.get_latest_imagery(
       bbox=(39.5, -74.8, 40.0, -74.3),  # Pinelands area
       bands=["B02", "B03", "B04", "B08"],  # RGB + NIR
       resolution=10  # meters per pixel
   )
   ```

3. **Weather Data**
   ```python
   # Example NOAA data collection
   from app.collectors import NOAACollector
   
   collector = NOAACollector()
   weather_data = collector.get_weather_data(
       stations=["KACY", "KMIV"],  # Atlantic City and Millville
       parameters=["TEMP", "WIND", "PRECIP", "RH"],
       frequency="hourly"
   )
   ```

#### Data Processing

1. **Standardization**
   ```python
   # Example data standardization
   from app.processors import DataStandardizer
   
   standardizer = DataStandardizer()
   standardized_data = standardizer.process(
       raw_data,
       target_crs="EPSG:4326",  # WGS 84
       target_resolution="1H",   # 1 hour
       fill_method="interpolate"
   )
   ```

2. **Feature Engineering**
   ```python
   # Example feature generation
   from app.processors import FeatureGenerator
   
   generator = FeatureGenerator()
   features = generator.create_features(
       data=standardized_data,
       temporal_features=["hour", "month", "season"],
       spatial_features=["elevation", "slope", "aspect"],
       weather_features=["temp_max", "wind_speed", "rh_min"],
       historical_features=["previous_fires", "fire_frequency"]
   )
   ```

3. **Quality Control**
   ```python
   # Example data validation
   from app.validators import DataValidator
   
   validator = DataValidator()
   validation_results = validator.validate(
       data=features,
       rules=[
           {"type": "range", "column": "temperature", "min": -20, "max": 50},
           {"type": "missing", "threshold": 0.1},  # Max 10% missing values
           {"type": "spatial", "bounds": "NJ_PINELANDS_BOUNDARY"}
       ]
   )
   ```

## Usage

### Interactive Map Interface

#### Map Features
1. **Base Layers**
   - Satellite imagery (Sentinel-2, 10m resolution)
   - Topographic maps
   - Land use/land cover
   - Infrastructure overlay

2. **Risk Visualization**
   - Real-time fire risk heatmap
   - Historical fire locations
   - Evacuation routes
   - High-risk zones

3. **Analysis Tools**
   - Area selection (polygon/radius)
   - Distance measurement
   - Elevation profiling
   - Time-series comparison

4. **Data Layers**
   ```javascript
   // Example layer configuration
   const mapLayers = {
     base: [
       { id: 'satellite', source: 'sentinel-2' },
       { id: 'topo', source: 'usgs' }
     ],
     risk: [
       { 
         id: 'fire-risk',
         type: 'heatmap',
         paint: {
           'heatmap-weight': [
             'interpolate', ['linear'],
             ['get', 'risk_score'],
             0, 0,
             1, 1
           ]
         }
       }
     ],
     infrastructure: [
       { id: 'roads', source: 'osm' },
       { id: 'buildings', source: 'njdep' }
     ]
   }
   ```

#### Interactive Features

1. **Time Control**
   ```javascript
   // Example time slider configuration
   const timeControl = {
     range: {
       start: '2025-01-01',
       end: '2025-12-31'
     },
     intervals: ['day', 'week', 'month'],
     animation: {
       duration: 30000,  // 30 seconds
       framerate: 24
     }
   }
   ```

2. **Risk Analysis**
   ```javascript
   // Example risk analysis response
   {
     area: {
       name: 'Selected Region',
       size_hectares: 1250,
       center: [-74.5, 39.8]
     },
     risk_factors: {
       current: {
         overall: 0.85,
         breakdown: {
           weather: 0.9,
           vegetation: 0.8,
           topography: 0.7
         }
       },
       forecast: [
         {
           date: '2025-04-09',
           risk: 0.82
         }
       ]
     },
     recommendations: [
       {
         priority: 'high',
         action: 'Clear firebreaks',
         location: { type: 'LineString', coordinates: [...] }
       }
     ]
   }
   ```

3. **Export Options**
   - PDF reports with maps and analysis
   - GeoJSON/Shapefile export
   - CSV data export
   - Image export (PNG/JPEG)

4. **Real-time Updates**
   ```javascript
   // Example WebSocket subscription
   socket.subscribe({
     area: selectedArea,
     updates: [
       'risk_score',
       'weather',
       'alerts'
     ],
     frequency: 300  // 5 minutes
   })
   ```

### Alert & Monitoring System

#### Alert Types

1. **Risk Level Alerts**
   ```python
   # Example alert configuration
   {
     "type": "risk_threshold",
     "conditions": {
       "risk_score": {
         "threshold": 0.7,
         "operator": ">"
       },
       "area_size": {
         "threshold": 1000,  # hectares
         "operator": ">"
       }
     },
     "notification": {
       "channels": ["email", "sms", "webhook"],
       "priority": "high",
       "recipients": ["fire_dept@nj.gov", "emergency@county.gov"]
     }
   }
   ```

2. **Weather Alerts**
   ```python
   # Example weather trigger
   {
     "type": "weather_condition",
     "conditions": {
       "temperature": {
         "threshold": 35,  # Celsius
         "operator": ">"
       },
       "wind_speed": {
         "threshold": 30,  # km/h
         "operator": ">"
       },
       "humidity": {
         "threshold": 30,  # percent
         "operator": "<"
       }
     },
     "notification": {
       "channels": ["api_webhook"],
       "endpoint": "https://api.emergency.nj.gov/alerts"
     }
   }
   ```

3. **Infrastructure Monitoring**
   ```python
   # Example infrastructure alert
   {
     "type": "infrastructure_risk",
     "monitors": [
       {
         "type": "power_line",
         "buffer_zone": 100,  # meters
         "risk_threshold": 0.6
       },
       {
         "type": "evacuation_route",
         "conditions": {
           "blocked_segments": {
             "threshold": 1,
             "operator": ">"
           }
         }
       }
     ],
     "response": {
       "automated_actions": [
         "reroute_traffic",
         "notify_utility_company"
       ],
       "notification": {
         "channels": ["emergency_broadcast", "mobile_app"]
       }
     }
   }
   ```

#### Monitoring Dashboard

1. **Real-time Metrics**
   - Active fire risk zones
   - Weather conditions
   - Resource deployment status
   - Alert history

2. **System Health**
   - Data feed status
   - Model performance metrics
   - API response times
   - Error rates

3. **Resource Tracking**
   - Emergency response units
   - Equipment locations
   - Water sources
   - Evacuation centers

### API Reference

#### Risk Prediction
```python
# Predict wildfire risk for an area
POST /api/v1/predict
{
    "area_geometry": GeoJSON,          # Area polygon in GeoJSON format
    "date": "2025-04-08",            # Target date for prediction
    "include_factors": [              # Optional risk factors to include
        "weather",
        "vegetation",
        "structures",
        "traffic"
    ],
    "time_range": {                   # Optional time range for prediction
        "start": "2025-04-08T00:00:00Z",
        "end": "2025-04-09T00:00:00Z"
    }
}

Response:
{
    "risk_score": 0.85,              # Overall risk score (0-1)
    "confidence": 0.92,              # Model confidence (0-1)
    "risk_factors": {                # Breakdown of risk factors
        "weather": 0.7,
        "vegetation": 0.9,
        "structures": 0.6,
        "traffic": 0.4
    },
    "recommendations": [              # List of recommended actions
        {
            "priority": "high",
            "action": "Close camping sites",
            "reason": "High vegetation risk"
        }
    ]
}

# Analyze camping site safety
GET /api/v1/camping-sites/{site_id}/risk
Response:
{
    "site_risk": 0.75,               # Site-specific risk score
    "max_capacity": 200,             # Current max safe capacity
    "evacuation_time": 45,          # Estimated evacuation time (minutes)
    "nearest_exits": [              # Ranked evacuation routes
        {
            "route": GeoJSON,
            "distance_km": 2.5,
            "estimated_time": 15
        }
    ]
}

# Assess structure vulnerability
POST /api/v1/structures/analyze
{
    "buildings": GeoJSON,            # Building polygons
    "buffer_zone": 100,             # Analysis buffer in meters
    "include_surroundings": true    # Consider surrounding structures
}

Response:
{
    "buildings": [                   # Per-building analysis
        {
            "id": "b123",
            "risk_score": 0.65,
            "factors": {
                "material": 0.4,
                "vegetation_proximity": 0.8,
                "access_routes": 0.7
            },
            "recommendations": [
                "Clear vegetation within 30m",
                "Improve fire-resistant materials"
            ]
        }
    ],
    "cluster_analysis": {            # Analysis of building clusters
        "high_risk_clusters": 2,
        "avg_cluster_risk": 0.55
    }
}

# Analyze traffic and evacuation
GET /api/v1/traffic/analysis?area={area_id}
Response:
{
    "current_flow": {                # Current traffic conditions
        "vehicles_per_hour": 150,
        "congestion_level": "medium"
    },
    "evacuation_capacity": {         # Evacuation analysis
        "max_throughput": 500,      # Vehicles per hour
        "bottlenecks": [            # Potential bottlenecks
            {
                "location": GeoJSON,
                "severity": "high",
                "mitigation": "Use alternate route 2"
            }
        ]
    },
    "recommended_routes": [          # Prioritized evacuation routes
        {
            "route": GeoJSON,
            "capacity": 300,
            "estimated_time": 25
        }
    ]
}
```

### Model Architecture

#### Machine Learning Pipeline
```plaintext
Input Data → Preprocessing → Feature Engineering → Model Ensemble → Post-processing → Output

1. Preprocessing:
   - Weather normalization
   - Satellite image enhancement
   - Missing data imputation
   - Coordinate system alignment

2. Feature Engineering:
   - Temporal features (time of day, season)
   - Spatial features (elevation, slope)
   - Weather patterns (wind, humidity)
   - Historical fire patterns

3. Model Ensemble:
   RandomForest (0.4)     → 
   LightGBM (0.3)         → Weighted
   CatBoost (0.3)         → Average

4. Post-processing:
   - Confidence calculation
   - Risk factor decomposition
   - Recommendation generation
```

#### Computer Vision Components
```plaintext
Satellite Image → Preprocessing → U-Net Segmentation → Risk Analysis

- Input: 10-band Sentinel-2 imagery
- Resolution: 10m/pixel
- Architecture: U-Net with ResNet50 backbone
- Output: Pixel-wise risk map
```

#### NLP Pipeline
```plaintext
Data → BERT Encoder → Custom Decoder → Report

- Input: Structured risk data
- Model: Fine-tuned BERT
- Output: Natural language reports
```

## Deployment & Scaling

### Cloud Deployment
```bash
# Using Docker Compose
docker-compose up -d

# Using Kubernetes
kubectl apply -f k8s/
```

### Scaling Considerations

1. **Horizontal Scaling**
   - Stateless API design allows easy replication
   - Redis-based caching layer for performance
   - Load balancing across multiple instances

2. **Data Management**
   - Distributed storage for satellite imagery
   - Time-series database for sensor data
   - Geospatial database for location data

3. **Performance Optimization**
   - Model quantization for faster inference
   - Batch processing for bulk analysis
   - Incremental updates for real-time data

4. **High Availability**
   - Multi-region deployment
   - Automated failover
   - Regular data backups

### Resource Requirements

#### Minimum Requirements (Single Instance)
```yaml
CPU: 2 cores
RAM: 8GB
Storage: 50GB SSD
Node.js: v18 or higher
NPM: v9 or higher
```

#### Recommended Production Setup
```yaml
API Servers:
  Instances: 3+
  CPU: 8 cores each
  RAM: 32GB each

ML Workers:
  Instances: 2+
  CPU: 16 cores each
  RAM: 64GB each
  GPU: NVIDIA T4 or better

Database:
  Type: PostgreSQL with PostGIS
  Storage: 500GB+ SSD
  Replicas: 2 (Primary + Standby)

Cache Layer:
  Type: Redis Cluster
  Nodes: 3+
  RAM: 16GB each
```

## Development

### Project Structure
```
PineGuard/
├── app/
│   ├── components/     # React components
│   │   ├── WildfireRiskMap.tsx    # Main risk visualization
│   │   ├── WeatherInfo.tsx        # Weather information
│   │   └── ai/                    # AI-powered components
│   ├── api/           # API routes
│   ├── data/          # Data and types
│   ├── utils/         # Utility functions
│   │   ├── fireSpread.ts          # Fire spread simulation
│   │   ├── weatherService.ts      # Weather data fetching
│   │   └── wildfireAnalysis.ts    # Risk analysis
│   ├── ml/            # Machine learning models
│   ├── cv/            # Computer vision components
│   └── nlp/           # Natural language processing
├── public/            # Static files
├── tests/             # Test suite
└── docker/            # Docker configuration
```

### Running Tests
```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Building Docker Image
```bash
docker build -t jmullen029/pineguard .
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- NOAA for weather data
- Sentinel Hub for satellite imagery
- New Jersey Forest Fire Service for domain expertise
- Open source community for various libraries and tools

## Contact
- Project Link: [https://github.com/jfm56/PineGuard](https://github.com/jfm56/PineGuard)
- Docker Hub: [https://hub.docker.com/r/jmullen029/pineguard](https://hub.docker.com/r/jmullen029/pineguard)
