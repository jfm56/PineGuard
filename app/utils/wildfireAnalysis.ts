import { Wildfire } from '../types/wildfire';
import { getTerrainData, getVegetationData, calculateVegetationRisk } from './terrainService';

export interface GridCell {
  lat: number;
  lng: number;
  riskScore: number;
  historicalFires: number;
  environmentalFactors: {
    vegetation: {
      density: number;    // 0-1 scale
      fuelType: string;   // type of vegetation
      ndvi: number;       // vegetation health
    };
    terrain: {
      elevation: number;   // meters
      slope: number;      // degrees
    };
    vegetationRisk: number; // 0-1 scale
  };
}

export interface RiskFactors {
  temperature: number;      // normalized 0-1
  humidity: number;         // normalized 0-1
  windSpeed: number;        // normalized 0-1
  seasonality: number;      // normalized 0-1
  historicalDensity: number;// normalized 0-1
}

// Pine Barrens region boundaries
const REGION_BOUNDS = {
  north: 40.4,
  south: 39.2,
  east: -74.2,
  west: -75.0
};

const GRID_SIZE = 0.01; // approximately 1km grid cells

export function createAnalysisGrid(): GridCell[][] {
  const rows = Math.ceil((REGION_BOUNDS.north - REGION_BOUNDS.south) / GRID_SIZE);
  const cols = Math.ceil((REGION_BOUNDS.east - REGION_BOUNDS.west) / GRID_SIZE);
  
  const grid: GridCell[][] = [];
  
  for (let i = 0; i < rows; i++) {
    grid[i] = [];
    for (let j = 0; j < cols; j++) {
      const lat = REGION_BOUNDS.south + (i * GRID_SIZE);
      const lng = REGION_BOUNDS.west + (j * GRID_SIZE);
      
      const terrain = getTerrainData(lat, lng);
      const vegetation = getVegetationData(lat, lng);
      const vegetationRisk = calculateVegetationRisk(vegetation, terrain);

      grid[i][j] = {
        lat,
        lng,
        riskScore: 0,
        historicalFires: 0,
        environmentalFactors: {
          vegetation: {
            density: vegetation.density,
            fuelType: vegetation.fuelType,
            ndvi: vegetation.ndvi
          },
          terrain: {
            elevation: terrain.elevation,
            slope: terrain.slope
          },
          vegetationRisk
        }
      };
    }
  }
  
  return grid;
}

export function calculateSeasonalRisk(date: Date): number {
  const month = date.getMonth();
  // Higher risk during spring (March-May) and fall (September-November)
  const seasonalRisk = {
    0: 0.4,  // January
    1: 0.5,  // February
    2: 0.8,  // March
    3: 0.9,  // April
    4: 0.8,  // May
    5: 0.6,  // June
    6: 0.5,  // July
    7: 0.5,  // August
    8: 0.7,  // September
    9: 0.8,  // October
    10: 0.7, // November
    11: 0.4  // December
  }[month] || 0.5;
  
  return seasonalRisk;
}

export function normalizeWeatherData(weatherConditions: Wildfire['weatherConditions']): RiskFactors {
  if (!weatherConditions) {
    return {
      temperature: 0.5,
      humidity: 0.5,
      windSpeed: 0.5,
      seasonality: 0.5,
      historicalDensity: 0
    };
  }

  // Temperature normalization (0°F to 100°F range)
  const tempNorm = Math.min(Math.max((weatherConditions.temperature || 70) / 100, 0), 1);
  
  // Humidity normalization (0-100% range, inverse relationship with risk)
  const humidityNorm = 1 - Math.min(Math.max((weatherConditions.humidity || 50) / 100, 0), 1);
  
  // Wind speed normalization (0-30mph range)
  const windNorm = Math.min(Math.max((weatherConditions.windSpeed || 10) / 30, 0), 1);

  return {
    temperature: tempNorm,
    humidity: humidityNorm,
    windSpeed: windNorm,
    seasonality: calculateSeasonalRisk(new Date()),
    historicalDensity: 0 // Will be calculated separately
  };
}

export function calculateHistoricalDensity(fires: Wildfire[], grid: GridCell[][]): void {
  // Count historical fires in each grid cell
  fires.forEach(fire => {
    const row = Math.floor((fire.location.lat - REGION_BOUNDS.south) / GRID_SIZE);
    const col = Math.floor((fire.location.lng - REGION_BOUNDS.west) / GRID_SIZE);
    
    if (row >= 0 && row < grid.length && col >= 0 && col < grid[0].length) {
      grid[row][col].historicalFires++;
    }
  });

  // Find maximum number of fires in any cell for normalization
  let maxFires = 0;
  grid.forEach(row => {
    row.forEach(cell => {
      maxFires = Math.max(maxFires, cell.historicalFires);
    });
  });

  // Normalize historical fire density
  if (maxFires > 0) {
    grid.forEach(row => {
      row.forEach(cell => {
        cell.riskScore = cell.historicalFires / maxFires;
      });
    });
  }
}

export function calculateRiskScore(factors: RiskFactors, cell: GridCell): number {
  // Base weights for weather factors
  const weatherWeights = {
    temperature: 0.15,
    humidity: 0.20,
    windSpeed: 0.15,
    seasonality: 0.10,
    historicalDensity: 0.15
  };

  // Calculate weather-based risk
  const weatherRisk = Object.entries(weatherWeights).reduce((score, [factor, weight]) => {
    return score + (factors[factor as keyof RiskFactors] * weight);
  }, 0);

  // Environmental risk weight (25% of total)
  const environmentalRisk = cell.environmentalFactors.vegetationRisk * 0.25;

  // Combine risks
  const baseRisk = weatherRisk + environmentalRisk;

  // Apply terrain modifiers
  const slope = cell.environmentalFactors.terrain.slope;
  const slopeModifier = 1 + (slope / 45); // Steeper slopes increase risk

  // Calculate final risk score
  let finalRisk = baseRisk * slopeModifier;

  // Normalize to 0-1 range
  finalRisk = Math.min(1, Math.max(0, finalRisk));

  return finalRisk;
}

export function updateRiskMap(
  grid: GridCell[][],
  fires: Wildfire[]
): GridCell[][] {
  // Calculate historical fire density
  calculateHistoricalDensity(fires, grid);

  // Update risk scores for each cell
  grid.forEach(row => {
    row.forEach(cell => {
      // Calculate final risk score based on historical density and environmental factors
      cell.riskScore = calculateRiskScore({
        historicalDensity: cell.riskScore, // Use previously calculated historical density
        temperature: 75, // Default moderate temperature
        humidity: 50, // Default moderate humidity
        windSpeed: 10, // Default moderate wind speed
        seasonality: 0.5 // Default moderate season risk
      }, cell);
    });
  });

  return grid;
}
