'use client';

import React, { useEffect, useRef, useState } from 'react';
import { loadScript } from '../utils/loadScript';
import { wildfires } from '../data/wildfires';
import { getCurrentWeather, WeatherData } from '../utils/weatherService';
import { simulateFireSpread } from '../utils/fireSpread';
import { 
  createAnalysisGrid, 
  updateRiskMap,
  GridCell,
  calculateSeasonalRisk
} from '../utils/wildfireAnalysis';
import {
  getCurrentFireSeason,
  countHighRiskAreas,
  calculateAverageRisk,
  calculateFireRiskFromWeather,
  getWindDirection
} from '../utils/riskUtils';

/// <reference types="@types/google.maps" />

interface GoogleLatLng {
  lat(): number;
  lng(): number;
}

interface GoogleMapEvent {
  latLng: GoogleLatLng | null;
}

// No need to declare Window interface as it's handled by @types/google.maps

interface SimulationParams {
  windSpeed: number;
  windDirection: number;
  duration: number;
}

const WildfireRiskMap: React.FC = (): JSX.Element => {
  const mapRef = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [heatmap, setHeatmap] = useState<google.maps.visualization.HeatmapLayer | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskData, setRiskData] = useState<GridCell[][]>([]);
  const [currentWeather, setCurrentWeather] = useState<WeatherData | null>(null);
  const [weatherError, setWeatherError] = useState<string | null>(null);
  const [selectedCell, setSelectedCell] = useState<GridCell | null>(null);
  const [showFireSimulation, setShowFireSimulation] = useState(false);
  const [simulationParams, setSimulationParams] = useState<SimulationParams>({
    windSpeed: 10,
    windDirection: 0,
    duration: 4
  });

  // Initialize the map
  const initMap = () => {
    if (!mapRef.current || !window.google?.maps) {return;}

    const mapOptions: google.maps.MapOptions = {
        center: { lat: 39.8, lng: -74.6 }, // Center of Pine Barrens
        zoom: 9,
        mapTypeId: 'satellite',
        styles: [
          {
            featureType: 'administrative',
            elementType: 'labels',
            stylers: [{ visibility: 'off' }]
          }
        ]
      };

      const newMap = new google.maps.Map(mapRef.current, mapOptions);
      setMap(newMap);

      // Initialize heatmap layer
      const heatmapLayer = new google.maps.visualization.HeatmapLayer({
        map: newMap,
        radius: 20,
        opacity: 0.7,
        gradient: [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
      });
      setHeatmap(heatmapLayer);
    };

  const updateRiskData = async () => {
    try {
      // Get current weather for the center of Pine Barrens
      const weather = await getCurrentWeather(39.8, -74.6);
      setCurrentWeather(weather);
      setWeatherError(null);

      // Create and update risk grid
      const grid = createAnalysisGrid();
      const updatedGrid = updateRiskMap(grid, weather, wildfires);
      setRiskData(updatedGrid);

      // Convert grid data to heatmap data
      if (heatmap) {
        const heatmapData = updatedGrid.flatMap(row =>
          row.map(cell => ({
            location: new google.maps.LatLng(cell.lat, cell.lng),
            weight: cell.riskScore * 100 // Scale up for better visualization
          }))
        );

        heatmap.setData(heatmapData);
      }
    } catch (error) {
      console.error('Error updating risk data:', error);
      setWeatherError(error instanceof Error ? error.message : 'Error fetching weather data');
    }
  };

  // Handle click events and fire simulation
  useEffect(() => {
    if (!map || !heatmap) return;

    const clickListener = (e: GoogleMapEvent) => {
      if (!e.latLng) return;
    const clickedLat = e.latLng.lat();
    const clickedLng = e.latLng.lng();

      // Find the nearest cell
      const cell = riskData.flat().find(cell => {
        const latDiff = Math.abs(cell.lat - clickedLat);
        const lngDiff = Math.abs(cell.lng - clickedLng);
        return latDiff < 0.01 && lngDiff < 0.01;
      });

      setSelectedCell(cell || null);

      if (cell && showFireSimulation) {
        // Run fire simulation from clicked point
        const simulated = simulateFireSpread(riskData, {
          ignitionPoint: { lat: cell.lat, lng: cell.lng },
          windConditions: {
            speed: simulationParams.windSpeed,
            direction: simulationParams.windDirection
          },
          duration: simulationParams.duration,
          timeStep: 5 // 5-minute intervals
        });

        // Update heatmap with simulation data
        const simulationData = simulated.flatMap(row =>
          row.map(cell => ({
            location: new google.maps.LatLng(cell.lat, cell.lng),
            weight: cell.burning ? 1 : cell.spreadProbability
          }))
        );

        heatmap.setData(simulationData);
      }
    };

    const listener = (map as any).addListener('click', clickListener);

    return () => {
      listener.remove();
    };
  }, [map, heatmap, showFireSimulation, simulationParams, riskData]);

  // Load Google Maps and initialize
  useEffect(() => {
    const loadGoogleMaps = async (): Promise<void> => {
      try {
        const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
        if (!apiKey) {
          throw new Error('Google Maps API key is not configured');
        }

        // Load Google Maps if not already loaded
        const scriptElement = document.querySelector('script[src*="maps.googleapis.com/maps/api/js"]');
        
        if (!scriptElement) {
          await loadScript(
            `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=visualization`,
            'google-maps-api'
          );
        }
        
        // Wait for Google Maps to be fully loaded
        while (!window.google?.maps?.Map) {
          await new Promise(resolve => setTimeout(resolve, 100));
        }

        // Initialize the map
        await initMap();
        setLoading(false);

        // Update risk data after map is initialized
        await updateRiskData();
      } catch (error) {
        console.error('Error loading Google Maps:', error);
        setLoading(false);
        setWeatherError('Failed to load map');
      }
    };

    loadGoogleMaps();
  }, []);

  useEffect(() => {
    if (!map || !heatmap) {return;}

    const updateRiskData = async () => {
      try {
        // Get current weather for the center of Pine Barrens
        const weather = await getCurrentWeather(39.8, -74.6);
        setCurrentWeather(weather);
        setWeatherError(null);

        // Create and update risk grid
        const grid = createAnalysisGrid();
        const updatedGrid = updateRiskMap(grid, weather, wildfires);
        setRiskData(updatedGrid);

        // Convert grid data to heatmap data
        const heatmapData = updatedGrid.flatMap(row =>
          row.map(cell => ({
            location: new google.maps.LatLng(cell.lat, cell.lng),
            weight: cell.riskScore * 100 // Scale up for better visualization
          }))
        );

        heatmap.setData(heatmapData);

        // Add click listener for cell selection
        const clickListener = (e: { latLng?: { lat: () => number; lng: () => number } }): void => {
          const latLng = e.latLng;
          if (!latLng) {return;}

          const clickedLat = latLng.lat();
          const clickedLng = latLng.lng();

          // Find the nearest cell
          const cell = updatedGrid.flat().find(cell => {
            const latDiff = Math.abs(cell.lat - clickedLat);
            const lngDiff = Math.abs(cell.lng - clickedLng);
            return latDiff < 0.01 && lngDiff < 0.01;
          });

          setSelectedCell(cell || null);

          if (cell && showFireSimulation) {
            // Run fire simulation from clicked point
            const simulated = simulateFireSpread(updatedGrid, {
              ignitionPoint: { lat: cell.lat, lng: cell.lng },
              windConditions: {
                speed: simulationParams.windSpeed,
                direction: simulationParams.windDirection
              },
              duration: simulationParams.duration,
              timeStep: 5 // 5-minute intervals
            });

            // Update heatmap with simulation data
            const simulationData = simulated.flatMap(row =>
              row.map(cell => ({
                location: new google.maps.LatLng(cell.lat, cell.lng),
                weight: cell.burning ? 1 : cell.spreadProbability
              }))
            );

            heatmap.setData(simulationData);
          }
        };

        // Add click listener to map
        const listener = (map as any).addListener('click', clickListener);

        return () => {
          listener.remove();
        };
      } catch (error) {
        console.error('Error updating risk data:', error);
        setWeatherError(error instanceof Error ? error.message : 'Error fetching weather data');
        return () => {}; // Return empty cleanup function in case of error
      }
    };

    updateRiskData();
  }, [map, heatmap]);

  return (
    <div className="relative">
      <h2 className="text-2xl font-bold mb-4 text-left">Wildfire Risk Prediction</h2>
      {loading ? (
        <div className="w-full h-[400px] rounded-lg overflow-hidden flex items-center justify-center bg-gray-100">
          <div data-testid="loading-spinner" className="animate-spin rounded-full h-8 w-8 border-2 border-gray-400 border-t-gray-600" />
        </div>
      ) : (
        <div className="relative">
          <div id="risk-map" data-testid="risk-map" className="w-full h-[400px] rounded-lg overflow-hidden" />
          <div className="absolute top-4 inset-x-4 flex justify-between gap-4">
            {/* Top Left: Risk Level & Current Risk */}
            <div className="bg-white/90 p-4 rounded-lg shadow flex-1">
              <h3 className="text-sm font-semibold mb-3">Risk Assessment</h3>
              <div className="space-y-4 mb-4">
                <div className="w-full h-4 bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded" />
                <div className="flex justify-between w-full text-xs">
                  <span>Low Risk (0-33%)</span>
                  <span className="text-center">Medium</span>
                  <span>High Risk (67-100%)</span>
                </div>
              </div>
              {riskData.length > 0 && (
                <div className="text-xs space-y-2 pt-3 border-t border-gray-200">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="font-semibold mb-1">High Risk Areas</p>
                      <p className="text-2xl font-bold">{countHighRiskAreas(riskData)}</p>
                    </div>
                    <div>
                      <p className="font-semibold mb-1">Historical Fires</p>
                      <p className="text-2xl font-bold">{wildfires.length}</p>
                    </div>
                    <div>
                      <p className="font-semibold mb-1">Average Risk</p>
                      <p className="text-2xl font-bold">{calculateAverageRisk(riskData).toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="font-semibold mb-1">Current Risk</p>
                      <p className="text-2xl font-bold text-red-500">
                        {currentWeather ? (calculateFireRiskFromWeather(
                          currentWeather.temperature,
                          currentWeather.humidity,
                          currentWeather.windSpeed
                        ) * 100).toFixed(1) : '--'}%
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Top Right: Current Weather */}
            <div className="bg-white/90 p-4 rounded-lg shadow w-72">
              <h3 className="text-sm font-semibold mb-3">Current Weather</h3>
              {weatherError ? (
                <div className="text-xs text-red-500">{weatherError}</div>
              ) : currentWeather && (
                <div className="text-xs space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="font-semibold mb-1">Temperature</p>
                      <p className="text-2xl font-bold">{currentWeather.temperature}°F</p>
                    </div>
                    <div>
                      <p className="font-semibold mb-1">Humidity</p>
                      <p className="text-2xl font-bold">{currentWeather.humidity}%</p>
                    </div>
                  </div>
                  <div className="pt-3 border-t border-gray-200">
                    <p className="font-semibold mb-2">Conditions</p>
                    <p>{currentWeather.description}</p>
                    <p className="mt-2">Wind Speed: {currentWeather.windSpeed} mph</p>
                    <p className="mt-2 font-medium">Fire Season: {getCurrentFireSeason()}</p>
                    <p>Seasonal Risk: {(calculateSeasonalRisk(new Date()) * 100).toFixed(1)}%</p>
                  </div>
                </div>
              )}
            </div>
          </div>
          {selectedCell && (
            <div className="text-xs space-y-1 mt-4 border-t pt-4">
              <h4 className="font-semibold">Location Details:</h4>
              <p>Coordinates: {selectedCell.lat.toFixed(4)}, {selectedCell.lng.toFixed(4)}</p>
              <p>Risk Score: {(selectedCell.riskScore * 100).toFixed(1)}%</p>
              <p>Historical Fires: {selectedCell.historicalFires}</p>
              <p>Vegetation Type: {selectedCell.environmentalFactors.vegetation.fuelType}</p>
              <p>Vegetation Density: {(selectedCell.environmentalFactors.vegetation.density * 100).toFixed(1)}%</p>
              <p>Elevation: {selectedCell.environmentalFactors.terrain.elevation.toFixed(1)}m</p>
              <p>Slope: {selectedCell.environmentalFactors.terrain.slope.toFixed(1)}°</p>
            </div>
          )}
          <div className="absolute bottom-4 left-4 bg-white/90 p-4 rounded-lg shadow w-72">
            <h3 className="text-sm font-semibold mb-3">Historical Data</h3>
            <div className="text-xs space-y-2">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="font-semibold mb-1">Total Fires</p>
                  <p className="text-2xl font-bold">{wildfires.length}</p>
                </div>
                <div>
                  <p className="font-semibold mb-1">Active Zones</p>
                  <p className="text-2xl font-bold">{countHighRiskAreas(riskData)}</p>
                </div>
              </div>
              <div className="pt-3 border-t border-gray-200">
                <p className="font-semibold mb-1">Most Recent Fire</p>
                <p>{wildfires[0]?.startDate || 'No data'}</p>
                <p className="mt-2">{wildfires[0]?.location ? `${wildfires[0].location.municipality}, ${wildfires[0].location.county}` : 'Unknown location'}</p>
              </div>
            </div>
          </div>
            {/* Bottom Right: Fire Simulation Controls */}
            <div className="absolute bottom-4 right-4 bg-white/90 p-4 rounded-lg shadow w-72">
            <h3 className="text-sm font-semibold mb-3">Fire Spread Simulation</h3>
            <div className="text-xs space-y-3">
              <div>
                <label className="block mb-1">Wind Speed (mph)</label>
                <input
                  type="range"
                  min="0"
                  max="30"
                  value={simulationParams.windSpeed}
                  onChange={(e) => setSimulationParams(prev => ({ ...prev, windSpeed: parseInt(e.target.value) }))}
                  className="w-full mb-1"
                />
                <span>{simulationParams.windSpeed} mph</span>
              </div>
              <div>
                <label className="block mb-1">Wind Direction (°)</label>
                <input
                  type="range"
                  min="0"
                  max="360"
                  value={simulationParams.windDirection}
                  onChange={(e) => setSimulationParams(prev => ({ ...prev, windDirection: parseInt(e.target.value) }))}
                  className="w-full mb-1"
                />
                <span>{simulationParams.windDirection}° ({getWindDirection(simulationParams.windDirection)})</span>
              </div>
              <div>
                <label className="block mb-1">Simulation Duration (hours)</label>
                <input
                  type="range"
                  min="1"
                  max="12"
                  value={simulationParams.duration}
                  onChange={(e) => setSimulationParams(prev => ({ ...prev, duration: parseInt(e.target.value) }))}
                  className="w-full mb-1"
                />
                <span>{simulationParams.duration} hours</span>
              </div>
              <button
                onClick={() => setShowFireSimulation(!showFireSimulation)}
                className="mt-2 w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
              >
                {showFireSimulation ? 'Hide' : 'Show'} Simulation
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WildfireRiskMap;
