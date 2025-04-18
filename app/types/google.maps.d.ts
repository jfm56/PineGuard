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
    class LatLng {
      private _lat: number;
      private _lng: number;
      constructor(lat: number, lng: number) {
        this._lat = lat;
        this._lng = lng;
      }
      lat(): number { return this._lat; }
      lng(): number { return this._lng; }
    }

    class Map {
      addListener(eventName: string, handler: Function): google.maps.MapsEventListener {
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
        eventName: string,
        handler: Function
      ): google.maps.MapsEventListener;
    }
  }
}
