import { NextRequest } from 'next/server';

interface RiskData {
  level: string;
  description: string;
  recommendations: string[];
}

export async function GET(_request: NextRequest): Promise<Response> {
  try {
    // This is a mock response. In a real application, this would come from your Python backend
    const riskData: RiskData = {
      level: 'Moderate',
      description: 'Current conditions indicate a moderate risk of wildfires in the Pinelands area. Weather patterns and vegetation conditions require attention.',
      recommendations: [
        'Clear dead vegetation from around your property',
        'Keep a water source readily available',
        'Monitor local fire alerts and warnings',
        'Review your evacuation plan with family members'
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
