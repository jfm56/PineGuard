'use client';

import { useState } from 'react';

export default function MapControls(): JSX.Element {
  const [layers, setLayers] = useState({
    fireRisk: true,
    evacuationRoutes: false,
    fireStations: false,
    waterSources: false
  });

  const handleLayerChange = (layerName: keyof typeof layers): void => {
    setLayers(prev => ({
      ...prev,
      [layerName]: !prev[layerName]
    }));
  };

  return (
    <div className="glass-container p-6">
      <h3 className="text-lg font-semibold mb-4 text-white">Map Layers</h3>
      <div className="space-y-2">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="fireRiskLayer"
            className="mr-2"
            checked={layers.fireRisk}
            onChange={() => handleLayerChange('fireRisk')}
          />
          <label htmlFor="fireRiskLayer" className="text-white">Fire Risk Areas</label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="evacuationRoutes"
            className="mr-2"
            checked={layers.evacuationRoutes}
            onChange={() => handleLayerChange('evacuationRoutes')}
          />
          <label htmlFor="evacuationRoutes" className="text-white">Evacuation Routes</label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="fireStations"
            className="mr-2"
            checked={layers.fireStations}
            onChange={() => handleLayerChange('fireStations')}
          />
          <label htmlFor="fireStations" className="text-white">Fire Stations</label>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="waterSources"
            className="mr-2"
            checked={layers.waterSources}
            onChange={() => handleLayerChange('waterSources')}
          />
          <label htmlFor="waterSources" className="text-white">Water Sources</label>
        </div>
      </div>
      <div className="mt-4">
        <label htmlFor="timeRange" className="block mb-2 text-white">Time Range:</label>
        <select
          id="timeRange"
          className="w-full p-2 bg-opacity-20 bg-white backdrop-blur-sm border border-white/20 rounded text-white"
          defaultValue="24h"
        >
          <option value="24h" className="text-black">Next 24 Hours</option>
          <option value="48h" className="text-black">Next 48 Hours</option>
          <option value="72h" className="text-black">Next 72 Hours</option>
          <option value="7d" className="text-black">Next 7 Days</option>
        </select>
      </div>
    </div>
  );
}
