

interface RiskArea {
  coords: [number, number];
  riskLevel: string;
  severity: number;
  factors: Array<{
    name: string;
    value: string;
  }>;
}

interface RiskData {
  riskAreas: RiskArea[];
}

export async function GET(): Promise<Response> {
  await Promise.resolve();
  try {


    // This is mock data. In a real application, this would come from your Python backend
    const riskData: RiskData = {
      riskAreas: [
        {
          coords: [39.8158, -74.5349],
          riskLevel: 'High',
          severity: 2,
          factors: [
            { name: 'Temperature', value: '85°F' },
            { name: 'Wind Speed', value: '15 mph' },
            { name: 'Humidity', value: '30%' }
          ]
        },
        {
          coords: [39.7500, -74.3667],
          riskLevel: 'Extreme',
          severity: 3,
          factors: [
            { name: 'Temperature', value: '90°F' },
            { name: 'Wind Speed', value: '20 mph' },
            { name: 'Humidity', value: '25%' }
          ]
        },
        {
          coords: [39.6639, -74.5264],
          riskLevel: 'Moderate',
          severity: 1.5,
          factors: [
            { name: 'Temperature', value: '80°F' },
            { name: 'Wind Speed', value: '10 mph' },
            { name: 'Humidity', value: '40%' }
          ]
        }
      ]
    };

    return new Response(JSON.stringify(riskData), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error getting fire risk data:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to fetch fire risk data' }),
      { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
