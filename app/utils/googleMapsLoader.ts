import { LoadScript } from './loadScript';

let isLoading = false;
let isLoaded = false;
const callbacks: (() => void)[] = [];

export async function loadGoogleMaps(): Promise<void> {
  if (isLoaded) {
    return Promise.resolve();
  }

  if (isLoading) {
    return new Promise((resolve) => callbacks.push(resolve));
  }

  isLoading = true;

  try {
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
    if (!apiKey) {
      throw new Error('Google Maps API key is missing');
    }

    await LoadScript.load(
      `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`,
      'google-maps-script'
    );

    isLoaded = true;
    callbacks.forEach(cb => cb());
    callbacks.length = 0;
  } catch (error) {
    isLoading = false;
    throw error;
  }
}
