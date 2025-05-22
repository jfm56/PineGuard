'use client';

import React from 'react';
import WildfireRiskMap from '../routes/wildfire-risk/page';

export default function RiskPredictionPage(): JSX.Element {
  return (
    <div className="min-h-screen bg-[#1B4332] p-8">
      <h1 className="text-3xl font-bold mb-6 text-white">Wildfire Risk Prediction</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Main Map Area */}
        <div className="lg:col-span-3">
          <div className="bg-[#2D6A4F] rounded-lg p-4 h-[calc(100vh-12rem)] min-h-[600px]">
            <WildfireRiskMap />
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-6">
          {/* Risk Assessment */}
          <div className="bg-[#2D6A4F] p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4 text-white">Risk Assessment</h2>
            <div className="w-full h-2 bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded-full mb-2" />
            <div className="flex justify-between text-sm text-white/80 mb-4">
              <span>Low Risk</span>
              <span>Medium</span>
              <span>High Risk</span>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-[#1B4332] p-4 rounded-lg">
                <h3 className="text-sm font-medium text-white/80 mb-1">High Risk Areas</h3>
                <p className="text-2xl font-bold text-white">9,600</p>
              </div>
              <div className="bg-[#1B4332] p-4 rounded-lg">
                <h3 className="text-sm font-medium text-white/80 mb-1">Historical Fires</h3>
                <p className="text-2xl font-bold text-white">16</p>
              </div>
            </div>
          </div>

          {/* Fire Spread Simulation */}
          <div className="bg-[#2D6A4F] p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4 text-white">Fire Spread Simulation</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">Wind Speed (mph)</label>
                <input 
                  type="range" 
                  className="w-full accent-blue-500" 
                  min="0" 
                  max="30" 
                  defaultValue="10"
                />
                <div className="flex justify-between text-sm text-white/80 mt-1">
                  <span>0</span>
                  <span>15</span>
                  <span>30</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">Wind Direction</label>
                <input 
                  type="range" 
                  className="w-full accent-blue-500" 
                  min="0" 
                  max="360" 
                  defaultValue="0"
                />
                <div className="flex justify-between text-sm text-white/80 mt-1">
                  <span>N</span>
                  <span>E</span>
                  <span>S</span>
                  <span>W</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-white/80 mb-2">Simulation Duration</label>
                <input 
                  type="range" 
                  className="w-full accent-blue-500" 
                  min="1" 
                  max="12" 
                  defaultValue="4"
                />
                <div className="flex justify-between text-sm text-white/80 mt-1">
                  <span>1h</span>
                  <span>6h</span>
                  <span>12h</span>
                </div>
              </div>

              <button className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                Run Simulation
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
