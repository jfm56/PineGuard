import { NextResponse } from 'next/server';

export async function GET(): Promise<Response> {
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

  if (!apiKey) {
    return NextResponse.json({
      success: false,
      error: 'API key is not configured in .env.local',
      status: 'MISSING_KEY'
    });
  }
  try {
    // First, test the Places API
    const placesResponse = await fetch(
      `https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&key=${apiKey}`
    );
    
    const placesData = await placesResponse.json();
    
    // Next, test the Maps JavaScript API
    const mapsResponse = await fetch(
      `https://maps.googleapis.com/maps/api/js/AuthenticationService.Authenticate?1shttp%3A%2F%2F127.0.0.1%3A50283&4sair&callback=_xdc_._&key=${apiKey}`,
      {
        headers: {
          'Referer': 'http://127.0.0.1:50283'
        }
      }
    );
    
    const mapsText = await mapsResponse.text();
    const mapsSuccess = !mapsText.includes('InvalidKeyMapError') && !mapsText.includes('error');
    
    // Compile results
    const results = {
      success: placesData.status === 'OK' && mapsSuccess,
      apis: {
        places: placesData.status === 'OK',
        maps: mapsSuccess
      },
      details: {
        places: {
          status: placesData.status,
          error: placesData.error_message
        },
        maps: {
          status: mapsSuccess ? 'OK' : 'ERROR',
          error: mapsSuccess ? null : 'Invalid key or domain not allowed'
        }
      }
    };
    
    return NextResponse.json(results);
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error',
      details: {
        places: {
          status: 'ERROR',
          error: 'Failed to test Places API'
        },
        maps: {
          status: 'ERROR',
          error: 'Failed to test Maps API'
        }
      }
    }, { status: 500 });
  }
}
