import { GridCell } from './wildfireAnalysis';

interface WindConditions {
  speed: number;   // mph
  direction: number; // degrees (0-360, 0 = North, 90 = East)
}

interface SpreadParameters {
  ignitionPoint: {
    lat: number;
    lng: number;
  };
  windConditions: WindConditions;
  duration: number; // hours
  timeStep: number; // minutes
}

interface FireCell extends GridCell {
  burning: boolean;
  burnStartTime: number | null;
  burnDuration: number | null;
  spreadProbability: number;
}

const CELL_SIZE_METERS = 100; // Size of each grid cell
const WIND_SPEED_FACTOR = 0.2; // How much wind speed affects spread rate
const SLOPE_FACTOR = 0.1; // How much slope affects spread rate

function createFireGrid(baseGrid: GridCell[][]): FireCell[][] {
  return baseGrid.map(row =>
    row.map(cell => ({
      ...cell,
      burning: false,
      burnStartTime: null,
      burnDuration: null,
      spreadProbability: 0
    }))
  );
}

function calculateSpreadProbability(
  source: FireCell,
  target: FireCell,
  wind: WindConditions,
  currentTime: number
): number {
  if (!source.burning) {return 0;}

  // Calculate basic distance-based probability
  const dx = target.lng - source.lng;
  const dy = target.lat - source.lat;
  const distance = Math.sqrt(dx * dx + dy * dy);
  let probability = 1 - (distance / (CELL_SIZE_METERS * 0.001)); // Normalize by cell size

  // Wind direction effect
  const direction = Math.atan2(dy, dx) * (180 / Math.PI);
  const windDiff = Math.abs(direction - wind.direction);
  const windDirectionFactor = Math.cos(windDiff * (Math.PI / 180));
  
  // Wind speed effect
  const windSpeedFactor = 1 + (wind.speed * WIND_SPEED_FACTOR * Math.max(0, windDirectionFactor));
  probability *= windSpeedFactor;

  // Slope effect
  const elevationDiff = target.environmentalFactors.terrain.elevation - source.environmentalFactors.terrain.elevation;
  const slope = Math.atan2(elevationDiff, CELL_SIZE_METERS) * (180 / Math.PI);
  const slopeFactor = 1 + (slope * SLOPE_FACTOR);
  probability *= slopeFactor;

  // Vegetation effect
  probability *= target.environmentalFactors.vegetationRisk;

  // Time-based decay
  const timeBurning = currentTime - (source.burnStartTime || 0);
  const burnDecay = Math.max(0, 1 - (timeBurning / (source.burnDuration || 1)));
  probability *= burnDecay;

  return Math.min(1, Math.max(0, probability));
}

export function simulateFireSpread(
  baseGrid: GridCell[][],
  params: SpreadParameters
): FireCell[][] {
  const fireGrid = createFireGrid(baseGrid);
  const totalSteps = (params.duration * 60) / params.timeStep;
  let currentStep = 0;

  // Find and ignite starting cell
  const startRow = fireGrid.findIndex(row =>
    row.some(cell =>
      Math.abs(cell.lat - params.ignitionPoint.lat) < 0.001 &&
      Math.abs(cell.lng - params.ignitionPoint.lng) < 0.001
    )
  );
  
  if (startRow >= 0) {
    const startCol = fireGrid[startRow].findIndex(cell =>
      Math.abs(cell.lat - params.ignitionPoint.lat) < 0.001 &&
      Math.abs(cell.lng - params.ignitionPoint.lng) < 0.001
    );
    
    if (startCol >= 0) {
      fireGrid[startRow][startCol].burning = true;
      fireGrid[startRow][startCol].burnStartTime = 0;
      fireGrid[startRow][startCol].burnDuration = 120; // 2 hours in minutes
    }
  }

  // Simulation loop
  while (currentStep < totalSteps) {
    const currentTime = currentStep * params.timeStep;

    // Update each cell
    for (let i = 0; i < fireGrid.length; i++) {
      for (let j = 0; j < fireGrid[i].length; j++) {
        const cell = fireGrid[i][j];
        
        // Skip if already burning or burned out
        if (cell.burning || (cell.burnStartTime !== null && currentTime > (cell.burnStartTime + (cell.burnDuration || 0)))) {
          continue;
        }

        // Check neighboring cells for fire spread
        let maxSpreadProbability = 0;
        for (let di = -1; di <= 1; di++) {
          for (let dj = -1; dj <= 1; dj++) {
            if (di === 0 && dj === 0) {continue;}
            
            const ni = i + di;
            const nj = j + dj;
            
            if (ni >= 0 && ni < fireGrid.length && nj >= 0 && nj < fireGrid[ni].length) {
              const neighbor = fireGrid[ni][nj];
              const spreadProb = calculateSpreadProbability(neighbor, cell, params.windConditions, currentTime);
              maxSpreadProbability = Math.max(maxSpreadProbability, spreadProb);
            }
          }
        }

        // Update cell's spread probability
        cell.spreadProbability = maxSpreadProbability;

        // Check if fire spreads to this cell
        if (Math.random() < maxSpreadProbability) {
          cell.burning = true;
          cell.burnStartTime = currentTime;
          cell.burnDuration = 120; // 2 hours in minutes
        }
      }
    }

    currentStep++;
  }

  return fireGrid;
}

export function getFireSpreadHeatmapData(fireGrid: FireCell[][]): { location: google.maps.LatLng; weight: number }[] {
  return fireGrid.flatMap(row =>
    row.map(cell => ({
      location: new google.maps.LatLng(cell.lat, cell.lng),
      weight: cell.burning ? 1 : cell.spreadProbability
    }))
  );
}
