import { render, screen } from '@testing-library/react';
import WildfireRiskMap from '../WildfireRiskMap';

// Mock the google maps API
const mockAddListener = jest.fn();
const mockRemove = jest.fn();

beforeAll(() => {
  // Mock the google maps API
  global.google = {
    maps: {
      Map: jest.fn().mockImplementation(() => ({
        addListener: mockAddListener.mockReturnValue({ remove: mockRemove }),
      })),
      LatLng: jest.fn(),
      visualization: {
        HeatmapLayer: jest.fn().mockImplementation(() => ({
          setData: jest.fn(),
        })),
      },
    },
  } as any;

  // Mock the window object
  Object.defineProperty(window, 'google', {
    value: global.google,
  });
});

describe('WildfireRiskMap', () => {
  it('initially shows loading state', () => {
    render(<WildfireRiskMap />);
    const loadingSpinner = screen.getByTestId('loading-spinner');
    expect(loadingSpinner).toBeInTheDocument();
  });

  it('renders the map container after loading', async () => {
    render(<WildfireRiskMap />);
    const mapElement = await screen.findByTestId('risk-map');
    expect(mapElement).toBeInTheDocument();
  });

  // Add more tests as needed
});
