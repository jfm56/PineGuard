import { render } from '@testing-library/react';
import WildfireRiskMap from '../../routes/wildfire-risk/page';

class WildfireRiskMapTest {
  beforeEach() {
    jest.clearAllMocks();
  }

  testRendersMapContainer() {
    const { container } = render(<WildfireRiskMap />);
    expect(container.querySelector('div[class="w-full h-full"]')).toBeTruthy();
  }

  testLoadsGoogleMapsScript() {
    render(<WildfireRiskMap />);
    const scripts = document.getElementsByTagName('script');
    const mapsScript = Array.from(scripts).find(script => 
      script.src.includes('maps.googleapis.com')
    );
    expect(mapsScript).toBeTruthy();
    expect(mapsScript?.src).toContain('libraries=visualization');
  }
}

const wildfireRiskMapTest = new WildfireRiskMapTest();
describe('WildfireRiskMap', () => {
  beforeEach(() => wildfireRiskMapTest.beforeEach());
  it('renders the map container', () => wildfireRiskMapTest.testRendersMapContainer());
  it('loads Google Maps script', () => wildfireRiskMapTest.testLoadsGoogleMapsScript());
  // Add more tests as needed
});
