export function getWindDirection(degrees: number): string {
  const directions = [
    'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW'
  ];
  
  // Normalize degrees to 0-360
  degrees = ((degrees % 360) + 360) % 360;
  
  // Each direction covers 22.5 degrees
  const index = Math.round(degrees / 22.5) % 16;
  return directions[index];
}
