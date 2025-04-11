'use client';

import { useEffect, useState } from 'react';

export default function ApiTest() {
  const [status, setStatus] = useState<{
    success?: boolean;
    error?: string;
    status?: string;
    apis?: { 
      places: boolean;
      maps: boolean;
    };
    details?: {
      places: {
        status: string;
        error: string | null;
      };
      maps: {
        status: string;
        error: string | null;
      };
    };
  }>({});

  useEffect(() => {
    const checkApiKey = async () => {
      try {
        const response = await fetch('/api/verify-google-key');
        const data = await response.json();
        setStatus(data);
      } catch (error) {
        setStatus({ 
          success: false, 
          error: error instanceof Error ? error.message : 'Failed to check API key' 
        });
      }
    };

    checkApiKey();
  }, []);

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Google Maps API Key Test</h1>
      
      <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${status.success ? 'bg-green-500' : 'bg-red-500'}`} />
          <strong className="text-lg">
            {status.success ? 'API Key Valid' : 'API Key Invalid'}
          </strong>
        </div>

        {/* Overall Error */}
        {status.error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <strong className="text-red-700">Error:</strong>
            <p className="text-red-600 mt-1">{status.error}</p>
          </div>
        )}

        {/* API Status */}
        {status.apis && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">API Status</h2>
            
            {/* Places API */}
            <div className="p-4 bg-gray-50 rounded-md">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Places API</h3>
                <span className={`px-2 py-1 rounded-full text-sm ${status.apis.places ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {status.apis.places ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              {status.details?.places.error && (
                <p className="mt-2 text-sm text-red-600">{status.details.places.error}</p>
              )}
            </div>

            {/* Maps JavaScript API */}
            <div className="p-4 bg-gray-50 rounded-md">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">Maps JavaScript API</h3>
                <span className={`px-2 py-1 rounded-full text-sm ${status.apis.maps ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {status.apis.maps ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              {status.details?.maps.error && (
                <p className="mt-2 text-sm text-red-600">{status.details.maps.error}</p>
              )}
            </div>
          </div>
        )}

        {/* Next Steps */}
        {!status.success && status.apis && (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <h3 className="font-semibold text-blue-800">Next Steps</h3>
            <ul className="mt-2 space-y-2 text-blue-700 list-disc list-inside">
              {!status.apis.places && (
                <li>Enable the Places API in your Google Cloud Console</li>
              )}
              {!status.apis.maps && (
                <li>Enable the Maps JavaScript API in your Google Cloud Console</li>
              )}
              {(status.details?.maps.error?.includes('domain') || status.details?.places.error?.includes('domain')) && (
                <li>Add localhost:3000 to your API key's allowed domains</li>
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
