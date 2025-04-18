'use client';

import MapView from './components/MapView';
import FireRiskAssessment from './components/FireRiskAssessment';
import MainMenu from './components/MainMenu';

import ChatInterface from './components/ChatInterface';
import RiskAssessment from './components/ai/RiskAssessment';
import EmergencyPlanGenerator from './components/ai/EmergencyPlanGenerator';
import WeatherRiskAnalysis from './components/ai/WeatherRiskAnalysis';
import MapLayers from './components/MapLayers';
import WildfireHistory from './components/WildfireHistory';


export default function Home(): JSX.Element {
  return (
    <main className="min-h-screen p-4">
      <div className="container mx-auto relative z-50">
        <div className="flex justify-between items-center mb-8">
          <MainMenu onClose={() => {}} />
          <h1 className="text-4xl font-bold text-center text-white">
            Pinelands Wildfire Assistant
          </h1>
          <div className="w-[100px]"></div> {/* Spacer for alignment */}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Map Container */}
            <div className="relative h-[600px] glass-container p-2 rounded-lg">
              {/* Map View */}
              <div className="absolute inset-0 rounded-lg overflow-hidden">
                <MapView />
              </div>
              {/* Map Layers - Positioned over the map */}
              <div className="absolute left-4 top-4 z-[15] max-h-[calc(100%-2rem)] overflow-y-auto">
                <MapLayers />
              </div>
            </div>
            
            {/* Spacing div */}
            <div className="h-6"></div>
            
            {/* Visual Risk Assessment */}
            <div className="relative z-10">
              <RiskAssessment />
            </div>
            
            {/* Emergency Plan Generator */}
            <div className="relative z-10">
              <EmergencyPlanGenerator />
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Weather Risk Analysis */}
            <div className="relative z-10">
              <WeatherRiskAnalysis />
            </div>

            {/* Fire Risk Assessment */}
            <div className="relative z-10">
              <FireRiskAssessment />
            </div>

            {/* Chat Interface */}
            <div className="glass-container p-6">
              <ChatInterface />
            </div>

            {/* Historical Wildfires */}
            <div className="glass-container p-6">
              <WildfireHistory />
            </div>

          </div>
        </div>
      </div>
    </main>
  );
}
