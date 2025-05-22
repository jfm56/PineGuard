import { NextResponse } from 'next/server';

interface WeatherApiResponse {
  main: { temp: number; humidity: number };
  wind: { speed: number; deg: number };
  weather: { main: string; description: string }[];
  rain?: { [key: string]: number };
}
function isWeatherApiResponse(obj: unknown): obj is WeatherApiResponse {
  if (typeof obj !== 'object' || obj === null) { return false; }
  const o = obj as Record<string, unknown>;
  if (
    typeof o.main !== 'object' || o.main === null ||
    typeof (o.main as Record<string, unknown>).temp !== 'number' ||
    typeof (o.main as Record<string, unknown>).humidity !== 'number'
  ) { return false; }
  if (
    typeof o.wind !== 'object' || o.wind === null ||
    typeof (o.wind as Record<string, unknown>).speed !== 'number' ||
    typeof (o.wind as Record<string, unknown>).deg !== 'number'
  ) { return false; }
  if (
    !Array.isArray(o.weather) ||
    o.weather.length === 0 ||
    typeof o.weather[0] !== 'object' ||
    o.weather[0] === null ||
    typeof (o.weather[0] as Record<string, unknown>).main !== 'string' ||
    typeof (o.weather[0] as Record<string, unknown>).description !== 'string'
  ) { return false; }
  return true;
}

export async function GET(): Promise<Response> {
  // console.log('Weather API called'); // Remove for production
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
    // const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=imperial`;
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=imperial`;
    // console.log('URL (without API key):', url.replace(apiKey, 'HIDDEN'));

    const response = await fetch(url);
    if (!response.ok) {
      const errorText = await response.text();
      // Only log in catch blocks, not here
      throw new Error(`Weather API request failed: ${response.status} ${errorText}`);
    }

    const data: unknown = await response.json();
    if (!isWeatherApiResponse(data)) {
      return NextResponse.json(
        { error: 'Malformed weather data received from API.' },
        { status: 500 }
      );
    }

    // Convert wind direction from degrees to cardinal directions
    const getWindDirection = (degrees: number): string => {
      const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
      const index = Math.round(((degrees % 360) / 22.5));
      return directions[index % 16];
    };

    const d = data;
    const weatherData = {
      temperature: Math.round(d.main.temp),
      humidity: d.main.humidity,
      windSpeed: Math.round(d.wind.speed),
      windDirection: getWindDirection(d.wind.deg),
      conditions: d.weather[0].main,
      description: d.weather[0].description,
      precipitation: d.rain ? d.rain['1h'] || 0 : 0,
      lastUpdated: new Date().toISOString()
    };

    return NextResponse.json(weatherData);
  } catch (error) {
    // Minimal logging in production
    // eslint-disable-next-line no-console
    console.error('Weather API error:', {
      error,
      apiKey: apiKey ? 'present' : 'missing',
      lat,
      lon
    });
    return NextResponse.json(
      { error: 'Failed to fetch weather data. Please check the server logs.' },
      { status: 500 }
    );
  }
}
