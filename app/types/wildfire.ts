export interface WildfireLocation {
  lat: number;
  lng: number;
  municipality?: string;
  county?: string;
  description?: string;
}

export interface WeatherConditions {
  temperature?: number; // in Fahrenheit
  windSpeed?: number; // in mph
  humidity?: number; // percentage
  precipitation?: number; // in inches
  drought?: boolean;
  description?: string;
}

export interface WildfireImpact {
  acres: number;
  structures: {
    threatened: number;
    damaged: number;
    destroyed: number;
  };
  description?: string;
}

export interface WildfireContainment {
  percentage: number;
  date: string;
  description?: string;
}

export interface Wildfire {
  id: string;
  name: string;
  startDate: string;
  endDate?: string;
  location: WildfireLocation;

  size: number; // in acres
  impact: WildfireImpact;

  cause?: string;
  injuries?: number;
  fatalities?: number;
  weatherConditions?: WeatherConditions;

  evacuations?: {
    ordered: boolean;
    count?: number;
    description?: string;
  };
  resources?: string[];

  containment: WildfireContainment;
  description?: string;
  sources?: string[];
}
