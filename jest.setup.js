// Mock document.getElementById
document.getElementById = jest.fn();

// Mock the google maps API
global.google = {
  maps: {
    Map: jest.fn().mockImplementation(() => ({
      setCenter: jest.fn(),
      setZoom: jest.fn(),
      addListener: jest.fn(),
    })),
    LatLng: jest.fn().mockImplementation((lat, lng) => ({
      lat: () => lat,
      lng: () => lng,
    })),
    visualization: {
      HeatmapLayer: jest.fn().mockImplementation(() => ({
        setData: jest.fn(),
        setMap: jest.fn(),
      })),
    },
    event: {
      addListener: jest.fn(),
    },
  },
};

// Mock window.google
Object.defineProperty(window, 'google', {
  value: global.google,
  writable: true,
});
