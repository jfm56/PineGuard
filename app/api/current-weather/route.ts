import { NextResponse } from 'next/server';

class OpenWeatherResponse {
  main: { temp: number; humidity: number; };
  wind: { speed: number; deg: number; };
  weather: Array<{ main: string; description: string }>;
  rain?: { '1h'?: number };
  constructor(data: any) {
    this.main = data.main;
    this.wind = data.wind;
    this.weather = data.weather;
    this.rain = data.rain;
  }
}

class WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  windDirection: string;
  conditions: string;
  description: string;
  precipitation: number;
  lastUpdated: string;
  constructor({ temperature, humidity, windSpeed, windDirection, conditions, description, precipitation, lastUpdated }: any) {
    this.temperature = temperature;
    this.humidity = humidity;
    this.windSpeed = windSpeed;
    this.windDirection = windDirection;
    this.conditions = conditions;
    this.description = description;
    this.precipitation = precipitation;
    this.lastUpdated = lastUpdated;
  }
}

export async function GET(): Promise<Response> {
  const apiKey = process.env.OPENWEATHER_API_KEY;
  const lat = parseFloat(process.env.DEFAULT_LAT || '39.6234');
  const lon = parseFloat(process.env.DEFAULT_LON || '-74.3829');

  if (!apiKey) {
    return NextResponse.json(
      { error: 'Weather API key not configured' },
      { status: 500 }
    );
  }

  try {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=imperial`;
    const response = await fetch(url);

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `Weather API error: ${response.status} - ${errorText}` },
        { status: response.status }
      );
    }

    const data = new OpenWeatherResponse(await response.json());

    // Convert wind direction from degrees to cardinal directions
    const getWindDirection = (degrees: number): string => {
      const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
      const index = Math.round(((degrees % 360) / 22.5));
      return directions[index % 16];
    };

    const weatherData = new WeatherData({
      temperature: Math.round(data.main.temp),
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed),
      windDirection: getWindDirection(data.wind.deg),
      conditions: data.weather[0].main,
      description: data.weather[0].description,
      precipitation: data.rain ? data.rain['1h'] || 0 : 0,
      lastUpdated: new Date().toISOString()
    });

    return NextResponse.json(weatherData);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to fetch weather data' },
      { status: 500 }
    );
  }
}
