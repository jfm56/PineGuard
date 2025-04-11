import { GridCell } from './wildfireAnalysis';

export function getCurrentFireSeason(): string {
  const month = new Date().getMonth();
  if (month >= 2 && month <= 4) {return 'Spring';}
  if (month >= 5 && month <= 7) {return 'Summer';}
  if (month >= 8 && month <= 10) {return 'Fall';}
  return 'Winter';
}

export function countHighRiskAreas(grid: GridCell[][]): number {
  return grid.flat().filter(cell => cell.riskScore >= 0.67).length;
}

export function calculateAverageRisk(grid: GridCell[][]): number {
  const cells = grid.flat();
  const totalRisk = cells.reduce((sum, cell) => sum + cell.riskScore, 0);
  return totalRisk / cells.length;
}

export function calculateFireRiskFromWeather(temperature: number, humidity: number, windSpeed: number): number {
  // Normalize values
  const tempNorm = Math.min(Math.max((temperature - 32) / 68, 0), 1); // 32°F to 100°F
  const humidityNorm = 1 - Math.min(Math.max(humidity / 100, 0), 1); // inverse relationship
  const windNorm = Math.min(Math.max(windSpeed / 30, 0), 1); // 0-30mph

  // Weighted combination
  return (tempNorm * 0.4) + (humidityNorm * 0.4) + (windNorm * 0.2);
}

export function getWindDirection(degrees: number): string {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const index = Math.round(degrees / 45) % 8;
  return directions[index];
}
