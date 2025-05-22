'use client';

import { useState, useEffect, useCallback } from 'react';

interface WeatherData {
  temperature: number;
  humidity: number;
  windSpeed: number;
  windDirection: string;
  precipitation: number;
  conditions: string;
  description: string;
  lastUpdated: string;
}

export default function WeatherRiskAnalysis(): JSX.Element {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeRisk = useCallback(async () => {
    if (!weatherData) { return; }

    setLoading(true);
    try {
      const response = await fetch('/api/analyze-weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(weatherData),
      });

      const data = await response.json() as { analysis: string };
      setAnalysis(data.analysis);
    } catch (error) {
      setAnalysis('Error analyzing weather risk. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [weatherData]);

  const fetchWeatherData = useCallback(async () => {
    try {
      const response = await fetch('/api/current-weather', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      if (!response.ok) { 
        const errorText = await response.text();
        throw new Error(`Failed to fetch weather data: ${response.status} ${errorText}`);
      }

      const data = await response.json() as WeatherData & { error?: string };
      if (data.error) { 
        throw new Error(data.error);
      }

      setWeatherData(data);
    } catch (error) {
      setWeatherData(null);
    }
  }, []);

  useEffect(() => {
    void fetchWeatherData();
  }, [fetchWeatherData]);

  useEffect(() => {
    if (weatherData) { 
      void analyzeRisk();
    }
  }, [weatherData, analyzeRisk]);

  if (!weatherData) { 
    return (
      <div className="glass-container p-6 space-y-4">
        <h2 className="text-xl font-bold text-white">Weather Risk Analysis</h2>
        <div className="bg-white/10 p-4 rounded-lg">
          <p className="text-white">Loading weather data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-container p-6 space-y-4">
      <h2 className="text-xl font-bold text-white">Weather Risk Analysis</h2>
      
      <div className="space-y-4">
        <div className="bg-white/10 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Current Conditions</h3>
          <div className="grid grid-cols-2 gap-4">
            <ul className="space-y-2 text-white">
              <li>Temperature: {weatherData.temperature}°F</li>
              <li>Humidity: {weatherData.humidity}%</li>
              <li>Wind: {weatherData.windSpeed} mph {weatherData.windDirection}</li>
            </ul>
            <ul className="space-y-2 text-white">
              <li>Conditions: {weatherData.description}</li>
              <li>Precipitation: {weatherData.precipitation} inches</li>
              <li className="text-xs mt-4">Last updated: {new Date(weatherData.lastUpdated).toLocaleTimeString()}</li>
            </ul>
          </div>
        </div>

        <div className="bg-white/10 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Fire Risk Level</h3>
          {loading ? (
            <p className="text-white">Analyzing risk...</p>
          ) : (
            <div className="text-white whitespace-pre-wrap">{analysis}</div>
          )}
        </div>
      </div>

      <button
        onClick={() => void analyzeRisk()}
        disabled={loading}
        className="w-full py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? 'Analyzing...' : 'Refresh Analysis'}
      </button>
    </div>
  );
}
