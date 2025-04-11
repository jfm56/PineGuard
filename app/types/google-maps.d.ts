declare global {
  interface Window {
    google: typeof google;
  }
}

declare namespace google.maps {
  class places {
    static Autocomplete: new (
      inputField: HTMLInputElement,
      opts?: google.maps.places.AutocompleteOptions
    ) => google.maps.places.Autocomplete;
  }

  namespace places {
    interface AutocompleteOptions {
      componentRestrictions?: {
        country: string | string[];
      };
      fields?: string[];
      types?: string[];
    }

    class Autocomplete extends google.maps.MVCObject {
      getPlace(): google.maps.places.PlaceResult;
    }

    interface PlaceResult {
      formatted_address?: string;
    }
  }

  namespace event {
    function clearInstanceListeners(instance: any): void;
  }

  class MVCObject {
    addListener(eventName: string, handler: Function): google.maps.MapsEventListener;
  }

  interface MapsEventListener {
    remove(): void;
  }
}

export {};
