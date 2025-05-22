// Map-related utility functions

export const getWindDirection = (degrees: number): string => {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const index = Math.round(degrees / 45) % 8;
  return directions[index];
};

export const DEFAULT_MAP_OPTIONS = {

  center: { lat: 39.8283, lng: -74.5411 },
  zoom: 10,
  mapTypeId: 'terrain',
  zoomControl: true,
  scaleControl: true,
  mapTypeControl: false,
  streetViewControl: false,
  rotateControl: false,
  fullscreenControl: true,
  styles: [
    {
      featureType: 'landscape',
      elementType: 'geometry',
      stylers: [{ color: '#1B4332' }]
    }
  ]
};
