import { NextResponse } from 'next/server';

export async function GET(): Promise<Response> {
  console.log('Weather API called');
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
    console.log('Fetching from OpenWeather API...');
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=imperial`;
    console.log('URL (without API key):', url.replace(apiKey, 'HIDDEN'));
    
    const response = await fetch(url);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('OpenWeather API error:', {
        status: response.status,
        statusText: response.statusText,
        body: errorText
      });
      throw new Error(`Weather API request failed: ${response.status} ${errorText}`);
    }

    const data = await response.json();

    // Convert wind direction from degrees to cardinal directions
    const getWindDirection = (degrees: number) => {
      const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
      const index = Math.round(((degrees % 360) / 22.5));
      return directions[index % 16];
    };

    const weatherData = {
      temperature: Math.round(data.main.temp),
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed),
      windDirection: getWindDirection(data.wind.deg),
      conditions: data.weather[0].main,
      description: data.weather[0].description,
      precipitation: data.rain ? data.rain['1h'] || 0 : 0,
      lastUpdated: new Date().toISOString()
    };

    return NextResponse.json(weatherData);
  } catch (error) {
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
