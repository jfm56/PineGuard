// Common type definitions for the application

export interface GridCell {
  lat: number;
  lng: number;
  riskScore: number;
  historicalFires: number;
  environmentalFactors: {
    vegetation: {
      density: number;
      fuelType: string;
      ndvi: number;
    };
    terrain: {
      elevation: number;
      slope: number;
    };
    vegetationRisk: number;
  };
}

export interface SimulationParams {
  windSpeed: number;
  windDirection: number;
  humidity: number;
  temperature: number;
  duration: number;
  ignitionPoint?: {
    lat: number;
    lng: number;
  };
}

export interface FireSimulationResult {
  success: boolean;
  prediction: Array<{
    lat: number;
    lng: number;
    intensity: number;
    timeStep: number;
  }>;
}

// Google Maps types
declare global {
  interface Window {
    google: typeof google;
    initMap: () => void;
  }
}
