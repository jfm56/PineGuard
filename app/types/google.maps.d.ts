/// <reference types="@types/google.maps" />

declare global {
  class Window {
    google: typeof google;
    initMap: () => void;
    constructor(google: typeof google, initMap: () => void) {
      this.google = google;
      this.initMap = initMap;
    }
  }

  namespace google.maps {
    

    class Map {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-unsafe-assignment
      addListener(_unused: string, __unused: (...args: unknown[]) => unknown): google.maps.MapsEventListener {
        // Dummy implementation
        return new google.maps.MapsEventListener();
      }
    }

    class MapsEventListener {
      remove(): void {
        // Dummy implementation
      }
    }

    namespace event {
      function addListener(
        instance: google.maps.Map,
        _: string,
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        __unused: (...args: unknown[]) => unknown
      ): google.maps.MapsEventListener;
    }
  }
}
