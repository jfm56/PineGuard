'use client';

import { useEffect, useRef } from 'react';
import MapLayers from './MapLayers';

declare global {
  interface Window {
    L: typeof import('leaflet');
  }
}

type LayerGroupMap = {
  fireRisk: L.LayerGroup;
  evacuationRoutes: L.LayerGroup;
  fireStations: L.LayerGroup;
  waterSources: L.LayerGroup;
};

export default function LeafletMap(): JSX.Element {
  const mapRef = useRef<L.Map | null>(null);
  const layersRef = useRef<LayerGroupMap | null>(null);

  useEffect(() => {
    // Wait for Leaflet to be available
    if (typeof window === 'undefined' || !window.L) {
      console.error('Leaflet not loaded');
      return;
    }

    // Initialize map
    const map = window.L.map('map').setView([39.8, -74.5], 9);
    mapRef.current = map;

    // Add OpenStreetMap tiles
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Initialize layer groups
    const layers = {
      fireRisk: window.L.layerGroup().addTo(map),
      evacuationRoutes: window.L.layerGroup(),
      fireStations: window.L.layerGroup(),
      waterSources: window.L.layerGroup()
    };
    layersRef.current = layers;

    // Initialize icons
    const icons = {
      fireStation: window.L.icon({
        iconUrl: '/static/icons/fire-station.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
      }),
      waterSource: window.L.icon({
        iconUrl: '/static/icons/water-source.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
      })
    };

    // Load initial map data
    interface FireStation {
  coords: [number, number];
  name: string;
}
interface WaterSource {
  coords: [number, number];
  name: string;
}
interface EvacuationRoute {
  path: [number, number][];
  name: string;
}
interface MapData {
  fireStations: FireStation[];
  waterSources: WaterSource[];
  evacuationRoutes: EvacuationRoute[];
}

const loadMapData = async (): Promise<void> => {
  try {
    const response = await fetch('/api/map-data');
    const data: unknown = await response.json();
    if (
      typeof data === 'object' && data !== null &&
      Array.isArray((data as MapData).fireStations) &&
      Array.isArray((data as MapData).waterSources) &&
      Array.isArray((data as MapData).evacuationRoutes)
    ) {
      const mapData = data as MapData;
      // Add fire stations
      mapData.fireStations.forEach((station) => {
        if (Array.isArray(station.coords) && station.coords.length === 2 && typeof station.name === 'string') {
          window.L.marker(station.coords as [number, number], { icon: icons.fireStation })
            .bindPopup(`<b>${station.name}</b>`)
            .addTo(layers.fireStations);
        }
      });
      // Add water sources
      mapData.waterSources.forEach((source) => {
        if (Array.isArray(source.coords) && source.coords.length === 2 && typeof source.name === 'string') {
          window.L.marker(source.coords as [number, number], { icon: icons.waterSource })
            .bindPopup(`<b>${source.name}</b>`)
            .addTo(layers.waterSources);
        }
      });
      // Add evacuation routes
      mapData.evacuationRoutes.forEach((route) => {
        if (Array.isArray(route.path) && typeof route.name === 'string') {
          window.L.polyline(route.path, {
            color: 'blue',
            weight: 3,
            opacity: 0.7
          })
            .bindPopup(`<b>${route.name}</b>`)
            .addTo(layers.evacuationRoutes);
        }
      });
      // Initial risk areas update
      void updateRiskAreas();
    } else {
      throw new Error('Invalid map data format');
    }
  } catch (error) {
    console.error('Error loading map data:', error);
  }
};



    // Update risk areas
    interface RiskArea {
  coords: [number, number];
  severity: number;
  riskLevel: string;
  factors: { name: string; value: string }[];
}
interface FireRiskData {
  riskAreas: RiskArea[];
}
interface WeatherData {
  windSpeed: number;
  windDirection: string;
  humidity: number;
  temperature: number;
}

const updateRiskAreas = async (): Promise<void> => {
  try {
    const timeRange = (document.getElementById('timeRange') as HTMLSelectElement)?.value || '24h';
    layers.fireRisk.clearLayers();
    const response = await fetch(`/api/fire-risk?timeRange=${timeRange}`);
    const data: unknown = await response.json();
    // Get current weather data first
    const weatherResponse = await fetch('/api/current-weather');
    const currentWeatherRaw: unknown = await weatherResponse.json();
    let currentWeather: WeatherData = { windSpeed: 0, windDirection: '', humidity: 0, temperature: 0 };
    if (
      typeof currentWeatherRaw === 'object' && currentWeatherRaw !== null &&
      typeof (currentWeatherRaw as WeatherData).windSpeed === 'number' &&
      typeof (currentWeatherRaw as WeatherData).windDirection === 'string' &&
      typeof (currentWeatherRaw as WeatherData).humidity === 'number' &&
      typeof (currentWeatherRaw as WeatherData).temperature === 'number'
    ) {
      currentWeather = currentWeatherRaw as WeatherData;
    }
    if (
      typeof data === 'object' && data !== null &&
      Array.isArray((data as FireRiskData).riskAreas)
    ) {
      const fireRiskData = data as FireRiskData;
      fireRiskData.riskAreas.forEach((area: RiskArea) => {
        if (
          Array.isArray(area.coords) && area.coords.length === 2 &&
          typeof area.severity === 'number' && typeof area.riskLevel === 'string'
        ) {
          // Use current weather data to update risk levels
          const windSpeed = currentWeather.windSpeed;
          const humidity = currentWeather.humidity;
          // Update area's weather factors
          area.factors = [
            { name: 'Temperature', value: `${currentWeather.temperature}°F` },
            { name: 'Wind Speed', value: `${windSpeed} mph ${currentWeather.windDirection}` },
            { name: 'Humidity', value: `${humidity}%` }
          ];
          // Adjust risk level based on current conditions
          if (humidity < 30 && windSpeed > 15) {
            area.riskLevel = 'extreme';
          } else if (humidity < 40 && windSpeed > 10) {
            area.riskLevel = 'high';
          } else if (humidity > 60 && currentWeather.temperature < 50) {
            area.riskLevel = 'low';
          }
          const color = getRiskColor(area.riskLevel);
          const radius = area.severity * 1000; // Convert to meters
          window.L.circle(area.coords as [number, number], {
            color: color,
            fillColor: color,
            fillOpacity: 0.4,
            radius: radius
          })
            .bindPopup(`
              <div class="p-2">
                <div class="font-bold text-lg mb-2 capitalize">Risk Level: ${String(area.riskLevel)}</div>
                <div class="font-bold mt-2">Current Conditions:</div>
                <ul class="mt-1">
                  ${(Array.isArray(area.factors) ? area.factors : []).map((f: { name: string; value: string }) => `<li>• ${f.name}: ${f.value}</li>`).join('')}
                </ul>
              </div>
            `, {
              className: 'custom-popup',
              closeButton: true,
              autoPan: true
            })
            .addTo(layers.fireRisk);
        }
      });
    } else {
      throw new Error('Invalid fire risk data format');
    }
  } catch (error) {
    console.error('Error updating risk areas:', error);
  }
};

    // Get color based on risk level
    const getRiskColor = (riskLevel: string): string => {
      switch (riskLevel.toLowerCase()) {
        case 'extreme': return '#ff0000';
        case 'high': return '#ff6600';
        case 'moderate': return '#ffcc00';
        case 'low': return '#00cc00';
        default: return '#00ff00';
      }
    };

    // Add event listeners
    document.getElementById('fireRiskLayer')?.addEventListener('change', (e: Event): void => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.fireRisk);
      } else {
        map.removeLayer(layers.fireRisk);
      }
    });

    document.getElementById('evacuationRoutes')?.addEventListener('change', (e: Event): void => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.evacuationRoutes);
      } else {
        map.removeLayer(layers.evacuationRoutes);
      }
    });

    document.getElementById('fireStations')?.addEventListener('change', (e: Event): void => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.fireStations);
      } else {
        map.removeLayer(layers.fireStations);
      }
    });

    document.getElementById('waterSources')?.addEventListener('change', (e: Event): void => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.waterSources);
      } else {
        map.removeLayer(layers.waterSources);
      }
    });

    document.getElementById('timeRange')?.addEventListener('change', (): void => {
      void updateRiskAreas();
    });

    // Load initial data
    void loadMapData();

    // Cleanup
    return (): void => {
      map.remove();
    };
  }, []);

  return (
    <div className="w-full h-full relative">
      <div id="map" className="w-full h-full rounded-lg overflow-hidden shadow-lg" />
      <div className="absolute top-4 right-4 z-[1000]">
        <MapLayers />
      </div>
    </div>
  );
}
