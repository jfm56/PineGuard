interface ElevationData {
  elevation: number;  // meters
  slope: number;     // degrees
}

export interface VegetationData {
  ndvi: number;      // Normalized Difference Vegetation Index (0-1)
  fuelType: keyof typeof VEGETATION_TYPES;  // Must be a key of VEGETATION_TYPES
  density: number;   // 0-1 scale
}

// Simulated elevation data for the Pine Barrens region
const ELEVATION_DATA = new Map<string, ElevationData>();

// Initialize elevation data (this would normally come from a DEM service)
for (let lat = 39.2; lat <= 40.4; lat += 0.01) {
  for (let lng = -75.0; lng <= -74.2; lng += 0.01) {
    const key = `${lat.toFixed(3)},${lng.toFixed(3)}`;
    
    // Simulate elevation based on real Pine Barrens topography
    // Higher elevations in the northwest, lower in the southeast
    const baseElevation = 30; // base elevation in meters
    const nwGradient = (40.4 - lat) * 20 + (-75.0 - lng) * 15;
    
    ELEVATION_DATA.set(key, {
      elevation: Math.max(0, baseElevation + nwGradient + Math.random() * 5),
      slope: Math.random() * 15 // 0-15 degree slopes
    });
  }
}

// Vegetation classifications for the Pine Barrens
export interface VegetationType {
  name: string;
  category: 'Pine' | 'Oak' | 'Mixed' | 'Wetland' | 'Shrub';
  flammability: number;     // 0-1 scale
  fuelLoad: number;        // tons per acre
  moistureContent: number; // percentage
  canopyCover: number;    // percentage
  description: string;
}

export const VEGETATION_TYPES: Record<string, VegetationType> = {
  PITCH_PINE: {
    name: 'Pitch Pine',
    category: 'Pine',
    flammability: 0.9,
    fuelLoad: 15,
    moistureContent: 30,
    canopyCover: 70,
    description: 'Dominant pine species, highly flammable with resinous needles'
  },
  SHORTLEAF_PINE: {
    name: 'Shortleaf Pine',
    category: 'Pine',
    flammability: 0.85,
    fuelLoad: 12,
    moistureContent: 35,
    canopyCover: 65,
    description: 'Common pine species with moderate to high flammability'
  },
  VIRGINIA_PINE: {
    name: 'Virginia Pine',
    category: 'Pine',
    flammability: 0.8,
    fuelLoad: 10,
    moistureContent: 40,
    canopyCover: 60,
    description: 'Pine species with dense branches and high resin content'
  },
  SCARLET_OAK: {
    name: 'Scarlet Oak',
    category: 'Oak',
    flammability: 0.6,
    fuelLoad: 8,
    moistureContent: 45,
    canopyCover: 75,
    description: 'Deciduous oak with moderate flammability'
  },
  WHITE_OAK: {
    name: 'White Oak',
    category: 'Oak',
    flammability: 0.5,
    fuelLoad: 7,
    moistureContent: 50,
    canopyCover: 80,
    description: 'Large deciduous oak with lower flammability'
  },
  SCRUB_OAK: {
    name: 'Scrub Oak',
    category: 'Oak',
    flammability: 0.7,
    fuelLoad: 5,
    moistureContent: 35,
    canopyCover: 40,
    description: 'Small, dense oak species common in understory'
  },
  MIXED_PINE_OAK: {
    name: 'Mixed Pine-Oak',
    category: 'Mixed',
    flammability: 0.75,
    fuelLoad: 11,
    moistureContent: 40,
    canopyCover: 70,
    description: 'Mixed forest type with both pine and oak species'
  },
  PINE_SHRUBLAND: {
    name: 'Pine Shrubland',
    category: 'Shrub',
    flammability: 0.85,
    fuelLoad: 8,
    moistureContent: 30,
    canopyCover: 45,
    description: 'Open areas with scattered pines and dense shrub understory'
  },
  WETLAND_FOREST: {
    name: 'Wetland Forest',
    category: 'Wetland',
    flammability: 0.3,
    fuelLoad: 6,
    moistureContent: 70,
    canopyCover: 85,
    description: 'Forested wetlands with high moisture content'
  },
  CEDAR_SWAMP: {
    name: 'Cedar Swamp',
    category: 'Wetland',
    flammability: 0.4,
    fuelLoad: 9,
    moistureContent: 65,
    canopyCover: 90,
    description: 'Atlantic white cedar swamps with high moisture'
  },
  SHRUB_WETLAND: {
    name: 'Shrub Wetland',
    category: 'Wetland',
    flammability: 0.25,
    fuelLoad: 4,
    moistureContent: 75,
    canopyCover: 50,
    description: 'Wetland areas dominated by shrubs'
  }
};

// Simulated vegetation data
const VEGETATION_DATA = new Map<string, VegetationData>();

// Initialize vegetation data (this would normally come from satellite imagery)
for (let lat = 39.2; lat <= 40.4; lat += 0.01) {
  for (let lng = -75.0; lng <= -74.2; lng += 0.01) {
    const key = `${lat.toFixed(3)},${lng.toFixed(3)}`;
    
    // Simulate vegetation patterns based on elevation and location
    const elevation = ELEVATION_DATA.get(key)?.elevation || 0;
    const isWetland = Math.random() < 0.2; // 20% chance of wetland
    
    let fuelType: keyof typeof VEGETATION_TYPES;
    if (isWetland) {
      fuelType = 'WETLAND_FOREST';
    } else if (elevation > 40) {
      fuelType = Math.random() < 0.6 ? 'PITCH_PINE' : 'MIXED_PINE_OAK';
    } else {
      const r = Math.random();
      if (r < 0.4) {fuelType = 'MIXED_PINE_OAK';}
      else if (r < 0.6) {fuelType = 'SCRUB_OAK';}
      else if (r < 0.8) {fuelType = 'PITCH_PINE';}
      else {fuelType = 'SHORTLEAF_PINE';}
    }
    
    // Calculate NDVI (higher for denser vegetation)
    const baseNDVI = isWetland ? 0.7 : 0.5;
    const ndvi = Math.min(0.9, Math.max(0.2, baseNDVI + Math.random() * 0.3));
    
    VEGETATION_DATA.set(key, {
      ndvi,
      fuelType: fuelType,
      density: ndvi * 0.8 + Math.random() * 0.2 // correlate density with NDVI but add some variation
    });
  }
}

export function getTerrainData(lat: number, lng: number): ElevationData {
  const key = `${lat.toFixed(3)},${lng.toFixed(3)}`;
  return (
    ELEVATION_DATA.get(key) || {
      elevation: 30,
      slope: 5
    }
  );
}

export function getVegetationData(lat: number, lng: number): VegetationData {
  const key = `${lat.toFixed(3)},${lng.toFixed(3)}`;
  return (
    VEGETATION_DATA.get(key) || {
      ndvi: 0.5,
      fuelType: 'MIXED_PINE_OAK',
      density: 0.5
    }
  );
}

export function calculateVegetationRisk(vegetation: VegetationData, terrain: ElevationData): number {
  const vegType = VEGETATION_TYPES[vegetation.fuelType];
  if (!vegType) {return 0.5;} // Default risk if type not found

  // Base risk factors
  const flammabilityRisk = vegType.flammability * 0.3;
  const fuelLoadRisk = (vegType.fuelLoad / 15) * 0.2; // Normalize to 0-1
  const moistureRisk = (100 - vegType.moistureContent) / 100 * 0.2; // Inverse relationship
  const canopyRisk = (vegType.canopyCover / 100) * 0.1;
  const densityRisk = vegetation.density * 0.2;

  // Calculate base risk
  let risk = flammabilityRisk + fuelLoadRisk + moistureRisk + canopyRisk + densityRisk;

  // Adjust for NDVI (vegetation health)
  const ndviModifier = 1 + ((1 - vegetation.ndvi) * 0.5); // Unhealthy vegetation is more flammable
  risk *= ndviModifier;

  // Terrain adjustments
  // Slope effect (fires spread faster uphill)
  const slopeRisk = 1 + (terrain.slope / 45); // 45° slope doubles risk
  risk *= slopeRisk;

  // Elevation effect (higher elevations tend to be drier)
  const elevationModifier = 1 + ((terrain.elevation / 100) * 0.2);
  risk *= elevationModifier;

  // Normalize to 0-1 range
  return Math.min(1, Math.max(0, risk));
}

export const VEGETATION_TYPES_ARRAY = Object.values(VEGETATION_TYPES);
