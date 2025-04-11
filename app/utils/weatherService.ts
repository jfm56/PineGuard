export interface WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  precipitation: number;
  description: string;
}

export async function getCurrentWeather(lat: number, lng: number): Promise<WeatherData> {
  const apiKey = process.env.NEXT_PUBLIC_OPENWEATHER_API_KEY;
  if (!apiKey) {
    throw new Error('OpenWeather API key is missing');
  }

  const response = await fetch(
    `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${apiKey}&units=imperial`
  );

  if (!response.ok) {
    throw new Error('Failed to fetch weather data');
  }

  const data = await response.json();

  return {
    temperature: Math.round(data.main.temp),
    humidity: data.main.humidity,
    windSpeed: Math.round(data.wind.speed),
    precipitation: data.rain?.['1h'] || 0,
    description: data.weather[0].description
  };
}

export function calculateFireRiskFromWeather(weather: WeatherData): number {
  // Temperature impact (higher temperature = higher risk)
  // Scale from 0-100°F
  const tempRisk = Math.min(Math.max((weather.temperature - 32) / 68, 0), 1);

  // Humidity impact (lower humidity = higher risk)
  // Scale from 0-100%
  const humidityRisk = 1 - (weather.humidity / 100);

  // Wind speed impact (higher wind = higher risk)
  // Scale from 0-30mph
  const windRisk = Math.min(weather.windSpeed / 30, 1);

  // Precipitation impact (more rain = lower risk)
  // Scale from 0-1 inch
  const precipRisk = 1 - Math.min(weather.precipitation, 1);

  // Weighted combination
  const weights = {
    temperature: 0.3,
    humidity: 0.3,
    wind: 0.25,
    precipitation: 0.15
  };

  return (
    tempRisk * weights.temperature +
    humidityRisk * weights.humidity +
    windRisk * weights.wind +
    precipRisk * weights.precipitation
  );
}
