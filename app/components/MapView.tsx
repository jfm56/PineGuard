'use client';

import dynamic from 'next/dynamic';
import MapControls from './MapControls';

// Dynamically import Leaflet with no SSR
const LeafletMap = dynamic(() => import('./LeafletMap'), {
  ssr: false,
  loading: () => (
    <div className="glass-container p-6 flex items-center justify-center h-full">
      <p className="text-white">Loading map...</p>
    </div>
  ),
});

export default function MapView(): JSX.Element {
  return (
    <div className="h-full relative">
      <LeafletMap />
      <div className="absolute bottom-4 right-4 z-10">
        <MapControls />
      </div>
    </div>
  );
}
