'use client';

import { useEffect, useState } from 'react';

interface WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  windDirection: string;
  conditions: string;
}

export default function WeatherInfo(): JSX.Element {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        // This would be replaced with actual API call in production
        const mockWeather: WeatherData = {
          temperature: 78,
          humidity: 45,
          windSpeed: 12,
          windDirection: 'NW',
          conditions: 'Partly Cloudy'
        };
        setWeather(mockWeather);
      } catch (error) {
        console.error('Error fetching weather:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, []);

  if (loading) {
    return (
      <div className="glass-container p-6">
        <p className="text-gray-500">Loading weather information...</p>
      </div>
    );
  }

  if (!weather) {
    return (
      <div className="glass-container p-6">
        <p className="text-red-500">Failed to load weather information</p>
      </div>
    );
  }

  return (
    <div className="glass-container p-6">
      <h2 className="text-xl font-bold mb-4 text-white">Current Weather</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-white/70">Temperature</p>
          <p className="text-2xl font-semibold text-white">{weather.temperature}°F</p>
        </div>
        <div>
          <p className="text-white/70">Humidity</p>
          <p className="text-2xl font-semibold text-white">{weather.humidity}%</p>
        </div>
        <div>
          <p className="text-white/70">Wind</p>
          <p className="text-2xl font-semibold text-white">{weather.windSpeed} mph {weather.windDirection}</p>
        </div>
        <div>
          <p className="text-white/70">Conditions</p>
          <p className="text-2xl font-semibold text-white">{weather.conditions}</p>
        </div>
      </div>
    </div>
  );
}
