declare namespace google.maps {
  class Map {
    constructor(mapDiv: Element, opts?: MapOptions);
  }

  class LatLng {
    constructor(lat: number, lng: number);
  }

  interface MapOptions {
    center: { lat: number; lng: number };
    zoom: number;
    mapTypeId?: string;
    styles?: Array<{
      featureType?: string;
      elementType?: string;
      stylers: Array<{ [key: string]: any }>;
    }>;
  }

  namespace visualization {
    class HeatmapLayer {
      constructor(opts?: HeatmapLayerOptions);
      setData(data: any[]): void;
      setMap(map: Map | null): void;
    }

    interface HeatmapLayerOptions {
      map?: Map;
      data?: any[];
      radius?: number;
      opacity?: number;
      gradient?: string[];
    }
  }
}
