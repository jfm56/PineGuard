'use client';

import React from 'react';

type MapLayersState = {
  isVisible: boolean;
  isExiting: boolean;
};

export default class MapLayers extends React.Component<{}, MapLayersState> {
  state: MapLayersState = {
    isVisible: true,
    isExiting: false,
  };

  handleClose = () => {
    this.setState({ isExiting: true });
    setTimeout(() => {
      this.setState({ isVisible: false, isExiting: false });
    }, 300); // Match animation duration
  };

  handleShow = () => {
    this.setState({ isVisible: true });
  };

  render() {
    const { isVisible, isExiting } = this.state;
    return (
      <div className="relative">
        {/* Toggle button */}
        {!isVisible && (
          <button 
            onClick={this.handleShow}
            className="bg-[#1b4332] text-white p-3 rounded-lg shadow-lg hover:bg-[#2d6a4f] transition-colors flex items-center space-x-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            <span>Show Layers</span>
          </button>
        )}

        {/* Layers panel */}
        {isVisible && (
          <div className={`bg-[#1b4332] backdrop-blur-sm rounded-lg shadow-lg p-4 space-y-3 border border-white/20 w-[350px] ${isExiting ? 'animate-slide-out-right' : 'animate-slide-in-right'}`}>
            <div className="absolute top-0 right-0 mt-2 mr-2">
              <button 
                className="text-white/60 hover:text-white/90 transition-colors p-2" 
                onClick={this.handleClose}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            <div className="bg-[#2d6a4f] p-4 -m-4 mb-4 rounded-t-lg border-b border-white/20">
              <div className="flex justify-between items-center">
                <h3 className="text-xl font-semibold text-white">Map Layers</h3>
              </div>
            </div>
            <div className="space-y-5 px-3">
              <label className="flex items-center space-x-4 text-white text-xl hover:text-white/90 transition-colors cursor-pointer">
                <input
                  type="checkbox"
                  id="fireRiskLayer"
                  defaultChecked
                  className="form-checkbox h-6 w-6 text-emerald-500 bg-white border-white/50 rounded cursor-pointer hover:border-white/80 transition-colors"
                />
                <span>Fire Risk Areas</span>
              </label>
              <label className="flex items-center space-x-4 text-white text-xl hover:text-white/90 transition-colors cursor-pointer">
                <input
                  type="checkbox"
                  id="evacuationRoutes"
                  className="form-checkbox h-6 w-6 text-emerald-500 bg-white border-white/50 rounded cursor-pointer hover:border-white/80 transition-colors"
                />
                <span>Evacuation Routes</span>
              </label>
              <label className="flex items-center space-x-4 text-white text-xl hover:text-white/90 transition-colors cursor-pointer">
                <input
                  type="checkbox"
                  id="fireStations"
                  className="form-checkbox h-6 w-6 text-emerald-500 bg-white border-white/50 rounded cursor-pointer hover:border-white/80 transition-colors"
                />
                <span>Fire Stations</span>
              </label>
              <label className="flex items-center space-x-4 text-white text-xl hover:text-white/90 transition-colors cursor-pointer">
                <input
                  type="checkbox"
                  id="waterSources"
                  className="form-checkbox h-6 w-6 text-emerald-500 bg-white border-white/50 rounded cursor-pointer hover:border-white/80 transition-colors"
                />
                <span>Water Sources</span>
              </label>
              <div className="mt-4">
                <label className="block text-white text-xl mb-3">Time Range</label>
                <select
                  id="timeRange"
                  className="w-full bg-[#2d6a4f]/50 text-white text-lg rounded p-3 border border-white/20 backdrop-blur-sm"
                >
                  <option value="24h">Next 24 Hours</option>
                  <option value="48h">Next 48 Hours</option>
                  <option value="72h">Next 72 Hours</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
}
