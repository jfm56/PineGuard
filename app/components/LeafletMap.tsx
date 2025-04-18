'use client';

import { useEffect, useRef } from 'react';
import MapLayers from './MapLayers';

declare global {
  interface Window {
    L: any;
  }
}

export default function LeafletMap(): JSX.Element {
  const mapRef = useRef<any>(null);
  const layersRef = useRef<{
    fireRisk: any;
    evacuationRoutes: any;
    fireStations: any;
    waterSources: any;
  }>({ fireRisk: null, evacuationRoutes: null, fireStations: null, waterSources: null });

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
    const loadMapData = async () => {
      try {
        const response = await fetch('/api/map-data');
        const data = await response.json();

        // Add fire stations
        data.fireStations.forEach((station: any) => {
          window.L.marker(station.coords, { icon: icons.fireStation })
            .bindPopup(`<b>${station.name}</b>`)
            .addTo(layers.fireStations);
        });

        // Add water sources
        data.waterSources.forEach((source: any) => {
          window.L.marker(source.coords, { icon: icons.waterSource })
            .bindPopup(`<b>${source.name}</b>`)
            .addTo(layers.waterSources);
        });

        // Add evacuation routes
        data.evacuationRoutes.forEach((route: any) => {
          window.L.polyline(route.path, {
            color: 'blue',
            weight: 3,
            opacity: 0.7
          })
            .bindPopup(`<b>${route.name}</b>`)
            .addTo(layers.evacuationRoutes);
        });

        // Initial risk areas update
        updateRiskAreas();
      } catch (error) {
        console.error('Error loading map data:', error);
      }
    };



    // Update risk areas
    const updateRiskAreas = async () => {
      try {
        const timeRange = (document.getElementById('timeRange') as HTMLSelectElement)?.value || '24h';
        layers.fireRisk.clearLayers();

        const response = await fetch(`/api/fire-risk?timeRange=${timeRange}`);
        const data = await response.json();

        // Adjust risk levels based on weather
        // Get current weather data first
        const weatherResponse = await fetch('/api/current-weather');
        const currentWeather = await weatherResponse.json();
        
        data.riskAreas.forEach((area: any) => {
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

          window.L.circle(area.coords, {
            color: color,
            fillColor: color,
            fillOpacity: 0.4,
            radius: radius
          })
            .bindPopup(`
              <div class="p-2">
                <div class="font-bold text-lg mb-2 capitalize">Risk Level: ${area.riskLevel}</div>
                <div class="font-bold mt-2">Current Conditions:</div>
                <ul class="mt-1">
                  ${area.factors.map((f: any) => `<li>• ${f.name}: ${f.value}</li>`).join('')}
                </ul>
              </div>
            `, {
              className: 'custom-popup',
              closeButton: true,
              autoPan: true
            })
            .addTo(layers.fireRisk);
        });
      } catch (error) {
        console.error('Error updating risk areas:', error);
      }
    };

    // Get color based on risk level
    const getRiskColor = (riskLevel: string) => {
      switch (riskLevel.toLowerCase()) {
        case 'extreme': return '#ff0000';
        case 'high': return '#ff6600';
        case 'moderate': return '#ffcc00';
        case 'low': return '#00cc00';
        default: return '#00ff00';
      }
    };

    // Add event listeners
    document.getElementById('fireRiskLayer')?.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.fireRisk);
      } else {
        map.removeLayer(layers.fireRisk);
      }
    });

    document.getElementById('evacuationRoutes')?.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.evacuationRoutes);
      } else {
        map.removeLayer(layers.evacuationRoutes);
      }
    });

    document.getElementById('fireStations')?.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.fireStations);
      } else {
        map.removeLayer(layers.fireStations);
      }
    });

    document.getElementById('waterSources')?.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.checked) {
        map.addLayer(layers.waterSources);
      } else {
        map.removeLayer(layers.waterSources);
      }
    });

    document.getElementById('timeRange')?.addEventListener('change', () => {
      updateRiskAreas();
    });

    // Load initial data
    loadMapData();

    // Cleanup
    return () => {
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
