import { DEFAULT_MAP_OPTIONS } from '../utils/mapUtils';

export class MapFactory {
  static createMap(element: HTMLElement): google.maps.Map {
    return new window.google.maps.Map(element, DEFAULT_MAP_OPTIONS);
  }

  static createHeatmap(map: google.maps.Map, data: Array<{ location: google.maps.LatLng; weight: number }>): google.maps.visualization.HeatmapLayer {
    return new window.google.maps.visualization.HeatmapLayer({
      map,
      data,
      radius: 30,
      opacity: 0.7,
      gradient: [
        'rgba(0, 255, 0, 0)',
        'rgba(0, 255, 0, 1)',
        'rgba(255, 255, 0, 1)',
        'rgba(255, 0, 0, 1)'
      ]
    });
  }
}
