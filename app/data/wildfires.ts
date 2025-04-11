import { Wildfire } from '../types/wildfire';

export const wildfires: Wildfire[] = [
  {
    id: 'bass-river-2024',
    name: 'Bass River Fire',
    startDate: '2024-02-15',
    endDate: '2024-02-18',
    location: {
      lat: 39.6234,
      lng: -74.4421,
      municipality: 'Bass River Township',
      county: 'Burlington'
    },
    size: 270,
    impact: {
      acres: 270,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: 'Affected 270 acres of Pine Barrens forest'
    },
    cause: 'Campfire',
    containment: {
      percentage: 100,
      date: '2024-02-18',
      description: 'Fully contained'
    },
    injuries: 0,
    weatherConditions: {
      temperature: 52,
      windSpeed: 18,
      humidity: 40
    },
    evacuations: {
      ordered: true,
      count: 75,
      description: '75 residents evacuated from New Gretna area'
    },
    resources: [
      '45 firefighters',
      '1 aircraft',
      '15 vehicles'
    ],

    description: 'The Bass River Fire started from an unattended campfire and spread rapidly due to strong winds.',
    sources: ['New Jersey Forest Fire Service', 'Burlington County Emergency Management']
  },
  {
    id: 'jimtown-2024',
    name: 'Jimtown Fire',
    startDate: '2024-03-30',
    endDate: '2024-04-02',
    location: {
      lat: 39.7245,
      lng: -74.5768,
      municipality: 'Shamong Township',
      county: 'Burlington'
    },
    size: 180,
    impact: {
      acres: 180,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '180 acres of Pine Barrens forest affected'
    },
    cause: 'Under Investigation',
    containment: {
      percentage: 100,
      date: '2024-04-02',
      description: 'Fully contained'
    },
    weatherConditions: {
      temperature: 65,
      windSpeed: 15,
      humidity: 45
    },
    evacuations: {
      ordered: false
    },
    resources: [
      '50 firefighters',
      '12 vehicles'
    ],

    description: 'The Jimtown Fire started in Shamong Township and was quickly contained by state and local firefighters.',
    sources: ['New Jersey Forest Fire Service']
  },
  {
    id: 'warren-grove-2023',
    name: 'Warren Grove Fire',
    startDate: '2023-08-15',
    endDate: '2023-08-20',
    location: {
      lat: 39.7450,
      lng: -74.3823,
      municipality: 'Little Egg Harbor Township',
      county: 'Ocean'
    },
    size: 418,
    impact: {
      acres: 418,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '418 acres affected by lightning-caused fire'
    },
    cause: 'Lightning Strike',
    containment: {
      percentage: 100,
      date: '2023-08-20',
      description: 'Fully contained and extinguished'
    },
    injuries: 2,
    weatherConditions: {
      temperature: 88,
      windSpeed: 20,
      humidity: 35
    },
    evacuations: {
      ordered: true,
      count: 150,
      description: '150 residents evacuated from Warren Grove Village'
    },
    resources: [
      '75 firefighters',
      '2 aircraft',
      '18 vehicles'
    ],

    description: 'The Warren Grove Fire was sparked by a lightning strike during a summer thunderstorm. The fire spread quickly due to dry conditions and strong winds.',
    sources: ['New Jersey Forest Fire Service', 'Ocean County Emergency Management']
  },
  {
    id: 'mullica-2023',
    name: 'Mullica River Complex',
    startDate: '2023-06-02',
    endDate: '2023-06-08',
    location: {
      lat: 39.6789,
      lng: -74.6543,
      municipality: 'Washington Township',
      county: 'Burlington'
    },
    size: 1200,
    impact: {
      acres: 1200,
      structures: {
        threatened: 5,
        damaged: 0,
        destroyed: 2
      },
      description: '1,200 acres burned, 2 structures destroyed'
    },
    cause: 'Lightning',
    containment: {
      percentage: 100,
      date: '2023-06-08',
      description: 'Fully contained and extinguished'
    },
    injuries: 1,
    weatherConditions: {
      temperature: 85,
      windSpeed: 25,
      humidity: 30
    },
    evacuations: {
      ordered: true,
      count: 250,
      description: '250 residents evacuated from Lower Bank and Green Bank areas'
    },
    resources: [
      '120 firefighters',
      '3 aircraft',
      '25 vehicles'
    ],

    description: 'The Mullica River Complex consisted of multiple lightning-sparked fires that merged into a significant blaze.',
    sources: ['NJ Forest Fire Service', 'Burlington County Fire Marshal']
  },
  {
    id: 'wharton-2023',
    name: 'Wharton State Forest Fire',
    startDate: '2023-04-12',
    endDate: '2023-04-16',
    location: {
      lat: 39.7123,
      lng: -74.5678,
      municipality: 'Shamong Township',
      county: 'Burlington'
    },
    size: 750,
    impact: {
      acres: 750,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '750 acres of forest affected'
    },
    cause: 'Human Activity',
    containment: {
      percentage: 100,
      date: '2023-04-15',
      description: 'Fully contained'
    },
    weatherConditions: {
      temperature: 68,
      windSpeed: 15,
      humidity: 45
    },
    evacuations: {
      ordered: false
    },
    resources: [
      '85 firefighters',
      '2 aircraft',
      '20 vehicles'
    ],

    description: 'A significant spring fire in Wharton State Forest that threatened several hiking trails and campgrounds.',
    sources: ['NJ DEP', 'NJ Forest Fire Service']
  },
  {
    id: 'penn-2022',
    name: 'Penn State Forest Fire',
    startDate: '2022-09-08',
    endDate: '2022-09-12',
    location: {
      lat: 39.8234,
      lng: -74.5289,
      municipality: 'Washington Township',
      county: 'Burlington'
    },
    size: 520,
    impact: {
      acres: 520,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '520 acres of forest affected'
    },
    cause: 'Lightning Strike',
    containment: {
      percentage: 100,
      date: '2022-09-12',
      description: 'Fully contained'
    },
    weatherConditions: {
      temperature: 82,
      windSpeed: 12,
      humidity: 55
    },
    evacuations: {
      ordered: true,
      count: 100,
      description: 'Evacuation ordered for Jenkins Neck area'
    },
    resources: [
      '65 firefighters',
      '1 aircraft',
      '18 vehicles'
    ],

    description: 'Late summer fire in Penn State Forest that required significant resources to contain.',
    sources: ['NJ Forest Fire Service']
  },
  {
    id: 'brendan-byrne-2022',
    name: 'Brendan T. Byrne Fire',
    startDate: '2022-05-02',
    endDate: '2022-05-05',
    location: {
      lat: 39.8721,
      lng: -74.5234,
      municipality: 'Pemberton Township',
      county: 'Burlington'
    },
    size: 315,
    impact: {
      acres: 315,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '315 acres of forest affected'
    },
    cause: 'Prescribed Burn Escape',
    containment: {
      percentage: 100,
      date: '2022-05-05',
      description: 'Fully contained'
    },
    injuries: 0,
    weatherConditions: {
      temperature: 75,
      windSpeed: 20,
      humidity: 38
    },
    evacuations: {
      ordered: false
    },
    resources: [
      '55 firefighters',
      '1 aircraft',
      '14 vehicles'
    ],

    description: 'A prescribed burn that escaped control lines due to unexpected wind conditions.',
    sources: ['NJ Forest Fire Service', 'Pemberton Township Fire Department']
  },
  {
    id: 'tabernacle-2021',
    name: 'Tabernacle Fire',
    startDate: '2021-08-18',
    endDate: '2021-08-22',
    location: {
      lat: 39.8123,
      lng: -74.6234,
      municipality: 'Tabernacle Township',
      county: 'Burlington'
    },
    size: 420,
    impact: {
      acres: 420,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '420 acres of forest affected'
    },
    cause: 'Lightning',
    containment: {
      percentage: 100,
      date: '2021-08-22',
      description: 'Fully contained'
    },
    injuries: 0,
    weatherConditions: {
      temperature: 88,
      windSpeed: 15,
      humidity: 35
    },
    evacuations: {
      ordered: false
    },
    resources: [
      '60 firefighters',
      '1 aircraft',
      '18 vehicles'
    ],

    description: 'Summer lightning-caused fire that threatened several residential areas.',
    sources: ['NJ Forest Fire Service', 'Burlington County Emergency Management']
  },
  {
    id: 'chatsworth-2021',
    name: 'Chatsworth Complex',
    startDate: '2021-06-12',
    endDate: '2021-06-18',
    location: {
      lat: 39.7345,
      lng: -74.5432,
      municipality: 'Woodland Township',
      county: 'Burlington'
    },
    size: 890,
    impact: {
      acres: 890,
      structures: {
        threatened: 5,
        damaged: 0,
        destroyed: 1
      },
      description: '890 acres burned, 1 structure destroyed'
    },
    cause: 'Human Activity',
    containment: {
      percentage: 100,
      date: '2021-06-18',
      description: 'Fully contained'
    },
    injuries: 2,
    weatherConditions: {
      temperature: 82,
      windSpeed: 22,
      humidity: 42
    },
    evacuations: {
      ordered: true,
      count: 150,
      description: 'Evacuation ordered for Chatsworth Village area'
    },

    resources: [
      '95 firefighters',
      '2 aircraft',
      '22 vehicles'
    ],

    description: 'Multiple fires that merged into a complex, threatening the historic village of Chatsworth.',
    sources: ['NJ Forest Fire Service', 'Burlington County Fire Marshal']
  },
  {
    id: 'franklin-parker-2020',
    name: 'Franklin Parker Preserve Fire',
    startDate: '2020-09-08',
    endDate: '2020-09-12',
    location: {
      lat: 39.7789,
      lng: -74.5234,
      municipality: 'Woodland Township',
      county: 'Burlington'
    },
    size: 280,
    impact: {
      acres: 280,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '280 acres of forest affected'
    },
    cause: 'Drought Lightning',
    containment: {
      percentage: 100,
      date: '2020-09-12',
      description: 'Fully contained'
    },
    injuries: 0,
    weatherConditions: {
      temperature: 78,
      windSpeed: 12,
      humidity: 48
    },
    evacuations: {
      ordered: false
    },
    resources: [
      '45 firefighters',
      '1 aircraft',
      '14 vehicles'
    ],

    description: 'Fire in the Franklin Parker Preserve during drought conditions.',
    sources: ['NJ Forest Fire Service', 'NJ Conservation Foundation']
  },
  {
    id: 'oswego-lake-2020',
    name: 'Oswego Lake Fire',
    startDate: '2020-05-15',
    endDate: '2020-05-19',
    location: {
      lat: 39.7234,
      lng: -74.4987,
      municipality: 'Washington Township',
      county: 'Burlington'
    },
    size: 620,
    impact: {
      acres: 620,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '620 acres of forest affected'
    },
    cause: 'Human Activity',
    containment: {
      percentage: 100,
      date: '2020-05-19',
      description: 'Fully contained'
    },
    injuries: 1,
    weatherConditions: {
      temperature: 72,
      windSpeed: 18,
      humidity: 52
    },
    evacuations: {
      ordered: true,
      count: 85,
      description: 'Evacuation ordered for Oswego Lake Estates area'
    },
    resources: [
      '75 firefighters',
      '2 aircraft',
      '20 vehicles'
    ],
    description: 'Spring fire that threatened homes near Oswego Lake.',
    sources: ['NJ Forest Fire Service', 'Burlington County Emergency Management']
  },
  {
    id: 'jackson-road-2024',
    name: 'Jackson Road Wildfire',
    startDate: '2024-04-24',
    endDate: '2024-04-25',
    location: {
      lat: 39.7234,
      lng: -74.7812,
      description: 'Near Jackson Road, Wharton State Forest (Waterford Twp, Camden & Shamong Twp, Burlington)'
    },
    size: 510,
    cause: 'Under investigation',
    weatherConditions: {
      drought: false,
      description: 'Dry spell following earlier rains, creating conditions for rapid fire spread'
    },
    resources: [
      'NJ Forest Fire Service ground crews',
      'Firelines'
    ],
    evacuations: {
      ordered: false,
      description: 'No civilian evacuations; Goshen Pond campground and some trails closed as precaution'
    },
    impact: {
      acres: 510,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '510 acres of Pine Barrens forest burned. No injuries or structure damage reported.'
    },
    containment: {
      percentage: 100,
      date: '2024-04-25',
      description: '100% contained by April 25, 8:00 AM'
    }
  },
  {
    id: 'tea-time-hill-2024',
    name: 'Tea Time Hill Wildfire',
    startDate: '2024-07-04',
    endDate: '2024-07-10',
    location: {
      lat: 39.7856,
      lng: -74.6234,
      description: 'Batona Trail area near Batona Campground and Apple Pie Hill, Wharton State Forest'
    },
    size: 4300,
    cause: 'Human – illegal fireworks',
    weatherConditions: {
      temperature: 105,
      description: 'Extreme heat wave (100-110°F), moderate winds, low humidity'
    },
    resources: [
      'Ground crews',
      'Backfiring operations',
      'Helicopters',
      'Fire engines',
      'Bulldozers'
    ],
    evacuations: {
      ordered: true,
      description: 'Batona Campground evacuated; local roads closed'
    },
    impact: {
      acres: 4300,
      structures: {
        threatened: 2,
        damaged: 0,
        destroyed: 0
      },
      description: '4,300 acres burned; 2 buildings threatened but protected'
    },
    containment: {
      percentage: 90,
      date: '2024-07-08',
      description: '90% contained by July 8, full containment achieved later that week'
    }
  },
  {
    id: 'shotgun-2024',
    name: 'Shotgun Wildfire',
    startDate: '2024-11-06',
    endDate: '2024-11-11',
    location: {
      lat: 40.0845,
      lng: -74.3567,
      description: 'Colliers Mills Wildlife Management Area, Jackson Township'
    },
    size: 350,
    cause: 'Under investigation (suspected human cause)',
    weatherConditions: {
      humidity: 20,
      windSpeed: 30,
      drought: true,
      description: 'Severe drought conditions, gusty winds, low humidity (~20%), Red Flag Warning'
    },
    resources: [
      'Backfiring operations',
      'Bulldozers',
      'Fire engines',
      'Ground crews'
    ],
    evacuations: {
      ordered: true,
      count: 25,
      description: '25 homes threatened, evacuations ordered and lifted same day'
    },
    impact: {
      acres: 350,
      structures: {
        threatened: 25,
        damaged: 0,
        destroyed: 0
      },
      description: '350 acres of Pinelands forest burned; no structures destroyed'
    },
    containment: {
      percentage: 90,
      date: '2024-11-08',
      description: '90% contained by Nov 8, full containment by Nov 11'
    }
  },
  {
    id: 'bethany-run-2024',
    name: 'Bethany Run Wildfire',
    startDate: '2024-11-07',
    endDate: '2024-11-10',
    location: {
      lat: 39.8567,
      lng: -74.9234,
      description: 'Border of Evesham Township and Voorhees Township'
    },
    size: 360,
    cause: 'Under investigation',
    weatherConditions: {
      windSpeed: 25,
      drought: true,
      description: 'Exceptional drought, Red Flag conditions, winds 20-30 mph, very low humidity'
    },
    resources: [
      'NJFFS helicopter',
      '10 fire engines',
      'Bulldozers',
      '75+ NJFFS personnel'
    ],
    evacuations: {
      ordered: true,
      count: 100,
      description: 'Mandatory evacuations for ~100 homes, lifted same night'
    },
    impact: {
      acres: 360,
      structures: {
        threatened: 104,
        damaged: 0,
        destroyed: 0
      },
      description: '360 acres burned in wildland-urban interface; no homes damaged'
    },
    containment: {
      percentage: 90,
      date: '2024-11-09',
      description: '90% contained by Nov 9, full containment by Nov 10'
    }
  },
  {
    id: 'pheasant-run-2024',
    name: 'Pheasant Run Wildfire',
    startDate: '2024-11-07',
    endDate: '2024-11-12',
    location: {
      lat: 39.6789,
      lng: -75.0123,
      description: 'Glassboro Wildlife Management Area (Franklin/Monroe Townships)'
    },
    size: 133,
    cause: 'Under investigation',
    weatherConditions: {
      drought: true,
      description: 'Extreme drought, low humidity, windy conditions'
    },
    resources: [
      'NJFFS engines',
      'Bulldozers',
      'Ground crews'
    ],
    evacuations: {
      ordered: false,
      description: 'No evacuations required - no structures threatened'
    },
    impact: {
      acres: 133,
      structures: {
        threatened: 0,
        damaged: 0,
        destroyed: 0
      },
      description: '133 acres of Pine Barrens habitat burned in WMA'
    },
    containment: {
      percentage: 75,
      date: '2024-11-09',
      description: '75% contained by Nov 9, fully contained by Nov 12'
    }
  }
];
