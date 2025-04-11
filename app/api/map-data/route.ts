import { NextRequest } from 'next/server';

interface MapData {
  fireStations: Array<{
    name: string;
    coords: [number, number];
  }>;
  waterSources: Array<{
    name: string;
    coords: [number, number];
  }>;
  evacuationRoutes: Array<{
    name: string;
    path: Array<[number, number]>;
  }>;
}

export async function GET(_request: NextRequest): Promise<Response> {
  try {
    // This is mock data. In a real application, this would come from your Python backend
    const mapData: MapData = {
      fireStations: [
        { name: 'Chatsworth Fire Station', coords: [39.8158, -74.5349] },
        { name: 'Tabernacle Fire Station', coords: [39.8500, -74.7167] },
        { name: 'Barnegat Fire Station', coords: [39.7500, -74.2167] }
      ],
      waterSources: [
        { name: 'Harrisville Lake', coords: [39.6639, -74.5264] },
        { name: 'Oswego Lake', coords: [39.7167, -74.5000] },
        { name: 'Lake Absegami', coords: [39.6500, -74.4333] }
      ],
      evacuationRoutes: [
        {
          name: 'Route 72 East',
          path: [
            [39.7500, -74.3667],
            [39.7500, -74.2500],
            [39.7500, -74.1333]
          ]
        },
        {
          name: 'Route 70 West',
          path: [
            [39.8833, -74.5000],
            [39.8833, -74.6167],
            [39.8833, -74.7333]
          ]
        }
      ]
    };

    return new Response(JSON.stringify(mapData), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error getting map data:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to fetch map data' }),
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
