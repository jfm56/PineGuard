'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { api } from '../../services/api';
import { GridCell, SimulationParams } from '../../schemas/types';
import { MapFactory } from '../../factories/mapFactory';
import { getWindDirection } from '../../utils/mapUtils';

// Constants
const DEFAULT_SIMULATION_PARAMS: SimulationParams = {
  windSpeed: 10,
  windDirection: 0,
  humidity: 30,
  temperature: 25,
  duration: 6
};

function isSimulationResult(obj: unknown): obj is { success: boolean; prediction: unknown } {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    !Array.isArray(obj) &&
    'success' in obj &&
    'prediction' in obj
  );
}

const WildfireRiskMap: React.FC = (): JSX.Element => {
  // Refs
  const mapRef = useRef<HTMLDivElement>(null);
  
  // State management
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [heatmap, setHeatmap] = useState<google.maps.visualization.HeatmapLayer | null>(null);
  const [riskData, setRiskData] = useState<GridCell[]>([]);
  const [selectedCell, setSelectedCell] = useState<GridCell | null>(null);
  const [simulationParams, setSimulationParams] = useState<SimulationParams>(DEFAULT_SIMULATION_PARAMS);
  const [showFireSimulation, setShowFireSimulation] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  // Initialize map and fetch data
  useEffect(() => {
    const fetchRiskData = async (): Promise<void> => {
      try {
        setLoading(true);
        const data = await api.getRiskData();
        setRiskData(data);
      } catch (error) {
        /* error intentionally ignored for production build; consider handling/logging in dev */
      } finally {
        setLoading(false);
      }
    };

    const initMap = (): void => {
      if (!mapRef.current) { return; }

      const map = MapFactory.createMap(mapRef.current);
      setMap(map);

      // Initialize heatmap
      const heatmap = MapFactory.createHeatmap(map, []);
      setHeatmap(heatmap);
    };

    // Load Google Maps API and initialize
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=visualization`;
    script.async = true;
    script.onload = (): void => {
      initMap();
      void fetchRiskData();
    };
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, []);

  // Update heatmap when risk data changes
  useEffect(() => {
    if (!heatmap || !riskData.length) { return; }

    const heatmapData = riskData.map((cell: GridCell): { location: google.maps.LatLng; weight: number } => ({
  location: new google.maps.LatLng(cell.lat, cell.lng),
  weight: cell.riskScore
}));

    heatmap.setData(heatmapData);
  }, [heatmap, riskData]);

  // Handle map click
  const handleMapClick = useCallback(async (event: google.maps.MapMouseEvent): Promise<void> => {
    if (!event.latLng) { return; }
    const clickedLat = event.latLng.lat();
    const clickedLng = event.latLng.lng();

    // Find the clicked cell
    const cell = riskData.find(
      (cell) =>
        Math.abs(cell.lat - clickedLat) < 0.01 &&
        Math.abs(cell.lng - clickedLng) < 0.01
    );

    if (cell) {
      setSelectedCell(cell);
      if (showFireSimulation) {
        try {
          setLoading(true);
          const simulation = await api.simulateFire({
            ...simulationParams,
            ignitionPoint: { lat: clickedLat, lng: clickedLng }
          });
          
          if (isSimulationResult(simulation)) {
            if (simulation.success) {
              if (Array.isArray(simulation.prediction)) {
                simulation.prediction.forEach((pred) => {
  if (
    typeof pred === 'object' && pred !== null &&
    'lat' in pred && typeof (pred as { lat: unknown }).lat === 'number' &&
    'lng' in pred && typeof (pred as { lng: unknown }).lng === 'number' &&
    'intensity' in pred && typeof (pred as { intensity: unknown }).intensity === 'number' &&
    'timeStep' in pred && typeof (pred as { timeStep: unknown }).timeStep === 'number'
  ) {
    // Safe access to pred.lat, pred.lng, pred.intensity, pred.timeStep
  }
});
              }
            }
          }
        } catch (error) {
          /* error intentionally ignored for production build; consider handling/logging in dev */
        } finally {
          setLoading(false);
        }
      }
    }
  }, [riskData, showFireSimulation, simulationParams]);

  // Add click listener when map is ready
  useEffect(() => {
    if (!map) { return; }

    const listener = google.maps.event.addListener(map, 'click', handleMapClick);
    return () => {
      listener.remove();
    };
  }, [map, handleMapClick]);

  return (
    <div className="relative w-full h-screen">
      <div ref={mapRef} className="w-full h-full" />

      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50">
          <div className="text-white">Loading...</div>
        </div>
      )}

      {selectedCell && (
        <div className="absolute top-4 left-4 bg-[#1B4332]/90 p-4 rounded-lg shadow-lg w-72">
        <h3 className="text-sm font-semibold mb-3 text-white">Cell Information</h3>
        <div className="text-xs space-y-2">
          <div className="flex justify-between">
            <span>Risk Score:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.riskScore === 'number' ? (selectedCell.riskScore * 100).toFixed(1) + '%' : 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span>Historical Fires:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.historicalFires === 'number' ? selectedCell.historicalFires : 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span>Vegetation Type:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.environmentalFactors?.vegetation?.fuelType === 'string' ? selectedCell.environmentalFactors.vegetation.fuelType : 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span>Vegetation Density:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.environmentalFactors?.vegetation?.density === 'number' ? (selectedCell.environmentalFactors.vegetation.density * 100).toFixed(1) + '%' : 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span>Elevation:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.environmentalFactors?.terrain?.elevation === 'number' ? selectedCell.environmentalFactors.terrain.elevation.toFixed(1) + 'm' : 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span>Slope:</span>
            <span className="font-semibold text-white">{typeof selectedCell?.environmentalFactors?.terrain?.slope === 'number' ? selectedCell.environmentalFactors.terrain.slope.toFixed(1) + '°' : 'N/A'}</span>
          </div>
          <div className="mt-2 text-xs text-white/60">
            Coordinates: {typeof selectedCell?.lat === 'number' && typeof selectedCell?.lng === 'number' ? `${selectedCell.lat.toFixed(4)}, ${selectedCell.lng.toFixed(4)}` : 'N/A'}
          </div>
        </div>
      </div>
      )}

      <div className="absolute bottom-4 right-4 bg-[#1B4332]/90 p-4 rounded-lg shadow-lg w-72">
        <h3 className="text-sm font-semibold mb-3 text-white">Prediction Controls</h3>
        <div className="text-xs space-y-3">
          <div>
            <label className="block mb-1 text-white/80">Wind Speed (mph)</label>
            <input
              type="range"
              min="0"
              max="30"
              value={simulationParams.windSpeed}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
  const value = parseInt(e.target.value, 10);
  if (!isNaN(value)) {
    setSimulationParams(prev => ({ ...prev, windSpeed: value }));
  }
}}
              className="w-full mb-1 accent-blue-500"
            />
            <span className="text-white/80">{simulationParams.windSpeed} mph</span>
          </div>
          <div>
            <label className="block mb-1 text-white/80">Wind Direction</label>
            <input
              type="range"
              min="0"
              max="360"
              value={simulationParams.windDirection}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
  const value = parseInt(e.target.value, 10);
  if (!isNaN(value)) {
    setSimulationParams(prev => ({ ...prev, windDirection: value }));
  }
}}
              className="w-full mb-1 accent-blue-500"
            />
            <span className="text-white/80">{getWindDirection(simulationParams.windDirection)}</span>
          </div>
          <div>
            <label className="block mb-1 text-white/80">Prediction Window</label>
            <input
              type="range"
              min="1"
              max="12"
              value={simulationParams.duration}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
  const value = parseInt(e.target.value, 10);
  if (!isNaN(value)) {
    setSimulationParams(prev => ({ ...prev, duration: value }));
  }
}}
              className="w-full mb-1 accent-blue-500"
            />
            <span className="text-white/80">{simulationParams.duration} hours</span>
          </div>
          <button
            onClick={() => setShowFireSimulation(!showFireSimulation)}
            className="mt-2 w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors text-sm"
          >
            {showFireSimulation ? 'Hide' : 'Show'} Prediction
          </button>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 bg-[#1B4332]/90 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold mb-2 text-white">Risk Level</h3>
        <div className="space-y-2">
          <div className="w-48 h-2 bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded-full" />
          <div className="flex justify-between text-xs text-white/80">
            <span>Low</span>
            <span>Medium</span>
            <span>High</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WildfireRiskMap;
