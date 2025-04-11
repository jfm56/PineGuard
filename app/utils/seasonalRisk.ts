interface SeasonalConditions {
  month: number;
  rainfall: number;     // mm
  temperature: number;  // °F
  humidity: number;     // %
  windSpeed: number;    // mph
  drought: number;      // 0-1 scale
}

// Historical seasonal data for the Pine Barrens
const SEASONAL_DATA: Record<number, SeasonalConditions> = {
  1: { month: 1, rainfall: 88.9, temperature: 35, humidity: 65, windSpeed: 12, drought: 0.3 },
  2: { month: 2, rainfall: 76.2, temperature: 38, humidity: 62, windSpeed: 13, drought: 0.3 },
  3: { month: 3, rainfall: 101.6, temperature: 45, humidity: 60, windSpeed: 14, drought: 0.4 },
  4: { month: 4, rainfall: 94.0, temperature: 55, humidity: 58, windSpeed: 13, drought: 0.5 },
  5: { month: 5, rainfall: 96.5, temperature: 65, humidity: 65, windSpeed: 11, drought: 0.6 },
  6: { month: 6, rainfall: 91.4, temperature: 74, humidity: 70, windSpeed: 10, drought: 0.7 },
  7: { month: 7, rainfall: 116.8, temperature: 79, humidity: 72, windSpeed: 9, drought: 0.8 },
  8: { month: 8, rainfall: 109.2, temperature: 77, humidity: 73, windSpeed: 9, drought: 0.9 },
  9: { month: 9, rainfall: 94.0, temperature: 70, humidity: 71, windSpeed: 10, drought: 0.7 },
  10: { month: 10, rainfall: 91.4, temperature: 59, humidity: 68, windSpeed: 11, drought: 0.5 },
  11: { month: 11, rainfall: 88.9, temperature: 49, humidity: 66, windSpeed: 12, drought: 0.4 },
  12: { month: 12, rainfall: 96.5, temperature: 38, humidity: 65, windSpeed: 12, drought: 0.3 }
};

// Fire seasons in the Pine Barrens
export const FIRE_SEASONS = {
  SPRING: { start: 3, end: 5 },    // March to May
  SUMMER: { start: 6, end: 8 },    // June to August
  FALL: { start: 9, end: 11 },     // September to November
  WINTER: { start: 12, end: 2 }    // December to February
};

export function calculateSeasonalRisk(date: Date = new Date()): number {
  const month = date.getMonth() + 1; // JavaScript months are 0-based
  const seasonalData = SEASONAL_DATA[month];

  // Base risk factors
  const temperatureRisk = (seasonalData.temperature - 32) / 100; // Convert to normalized scale
  const humidityRisk = (100 - seasonalData.humidity) / 100;
  const windRisk = seasonalData.windSpeed / 30; // Normalize to 0-1
  const rainfallRisk = 1 - (seasonalData.rainfall / 150); // Inverse relationship
  const droughtRisk = seasonalData.drought;

  // Season-specific risk modifiers
  let seasonalModifier = 1.0;
  
  // Spring fire season (highest risk)
  if (month >= FIRE_SEASONS.SPRING.start && month <= FIRE_SEASONS.SPRING.end) {
    seasonalModifier = 1.3;
  }
  // Summer fire season (high risk)
  else if (month >= FIRE_SEASONS.SUMMER.start && month <= FIRE_SEASONS.SUMMER.end) {
    seasonalModifier = 1.2;
  }
  // Fall fire season (moderate risk)
  else if (month >= FIRE_SEASONS.FALL.start && month <= FIRE_SEASONS.FALL.end) {
    seasonalModifier = 1.1;
  }
  // Winter (lower risk)
  else {
    seasonalModifier = 0.8;
  }

  // Calculate combined risk
  const baseRisk = (
    temperatureRisk * 0.2 +
    humidityRisk * 0.2 +
    windRisk * 0.2 +
    rainfallRisk * 0.2 +
    droughtRisk * 0.2
  );

  // Apply seasonal modifier
  const finalRisk = baseRisk * seasonalModifier;

  // Normalize to 0-1 range
  return Math.min(1, Math.max(0, finalRisk));
}

export function getCurrentFireSeason(date: Date = new Date()): string {
  const month = date.getMonth() + 1;
  
  if (month >= FIRE_SEASONS.SPRING.start && month <= FIRE_SEASONS.SPRING.end) {
    return 'Spring Fire Season';
  } else if (month >= FIRE_SEASONS.SUMMER.start && month <= FIRE_SEASONS.SUMMER.end) {
    return 'Summer Fire Season';
  } else if (month >= FIRE_SEASONS.FALL.start && month <= FIRE_SEASONS.FALL.end) {
    return 'Fall Fire Season';
  } else {
    return 'Winter Season';
  }
}

export function getSeasonalTrends(): SeasonalConditions[] {
  return Object.values(SEASONAL_DATA);
}
