'use client';

import { useState } from 'react';
import { Wildfire } from '../types/wildfire';
import { wildfires } from '../data/wildfires';

export default function WildfireHistory(): JSX.Element {
  const [selectedFire, setSelectedFire] = useState<Wildfire | null>(null);
  const [sortField, setSortField] = useState<keyof Pick<Wildfire, 'startDate' | 'name' | 'size'>>('startDate');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  const sortedFires = [...wildfires].sort((a, b) => {
    if (sortField === 'size') {
      const sizeA = a.impact?.acres || a.size || 0;
      const sizeB = b.impact?.acres || b.size || 0;
      return sortDirection === 'desc' 
        ? sizeB - sizeA
        : sizeA - sizeB;
    }
    if (sortField === 'startDate') {
      return sortDirection === 'desc'
        ? new Date(b.startDate).getTime() - new Date(a.startDate).getTime()
        : new Date(a.startDate).getTime() - new Date(b.startDate).getTime();
    }
    return sortDirection === 'desc'
      ? b[sortField].localeCompare(a[sortField])
      : a[sortField].localeCompare(b[sortField]);
  });

  const handleSort = (field: typeof sortField): void => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">Historical Wildfires in the Pine Barrens</h2>
      
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('name')}
                >
                  Name
                  {sortField === 'name' && (
                    <span className="ml-1">{sortDirection === 'asc' ? '↑' : '↓'}</span>
                  )}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('startDate')}
                >
                  Date
                  {sortField === 'startDate' && (
                    <span className="ml-1">{sortDirection === 'asc' ? '↑' : '↓'}</span>
                  )}
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('size')}
                >
                  Size
                  {sortField === 'size' && (
                    <span className="ml-1">{sortDirection === 'asc' ? '↑' : '↓'}</span>
                  )}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sortedFires.map((fire) => (
                <tr 
                  key={fire.id}
                  onClick={() => setSelectedFire(fire)}
                  className="hover:bg-gray-50 cursor-pointer"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {fire.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(fire.startDate).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {(fire.impact?.acres || fire.size || 0).toLocaleString()} acres
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {fire.location.municipality}, {fire.location.county} County
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full
                      ${fire.containment.percentage === 100 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}
                    `}>
                      {fire.containment.percentage === 100 ? 'Contained' : 'Active'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Fire Details Modal */}
      {selectedFire && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-bold">{selectedFire.name}</h3>
                <button
                  onClick={() => setSelectedFire(null)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <span className="sr-only">Close</span>
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="mt-4 space-y-4">
                <div>
                  <h4 className="font-semibold">Date</h4>
                  <p>{new Date(selectedFire.startDate).toLocaleDateString()} - 
                     {selectedFire.endDate ? new Date(selectedFire.endDate).toLocaleDateString() : 'Ongoing'}</p>
                </div>

                <div>
                  <h4 className="font-semibold">Location</h4>
                  <p>{selectedFire.location.municipality}, {selectedFire.location.county} County</p>
                  <p className="text-sm text-gray-500">
                    Coordinates: {selectedFire.location.lat}, {selectedFire.location.lng}
                  </p>
                </div>

                <div>
                  <h4 className="font-semibold">Size</h4>
                  <p>{(selectedFire.impact?.acres || selectedFire.size || 0).toLocaleString()} acres</p>
                </div>

                {selectedFire.cause && (
                  <div>
                    <h4 className="font-semibold">Cause</h4>
                    <p>{selectedFire.cause}</p>
                  </div>
                )}

                <div>
                  <h4 className="font-semibold">Status</h4>
                  <p>
                    <span className={`px-2 py-1 text-sm font-semibold rounded-full
                      ${selectedFire.containment.percentage === 100 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}
                    `}>
                      {selectedFire.containment.percentage === 100 ? 'Contained' : 'Active'}
                    </span>
                    {selectedFire.containment.percentage < 100 && (
                      <span className="ml-2">{selectedFire.containment.percentage}% contained</span>
                    )}
                  </p>
                </div>

                {selectedFire.weatherConditions && (
                  <div>
                    <h4 className="font-semibold">Weather Conditions</h4>
                    <ul className="list-disc list-inside space-y-1">
                      {selectedFire.weatherConditions.temperature && (
                        <li>Temperature: {selectedFire.weatherConditions.temperature}°F</li>
                      )}
                      {selectedFire.weatherConditions.windSpeed && (
                        <li>Wind Speed: {selectedFire.weatherConditions.windSpeed} mph</li>
                      )}
                      {selectedFire.weatherConditions.humidity && (
                        <li>Humidity: {selectedFire.weatherConditions.humidity}%</li>
                      )}
                    </ul>
                  </div>
                )}

                {selectedFire.evacuations?.ordered && (
                  <div>
                    <h4 className="font-semibold">Evacuations</h4>
                    <p>
                      {selectedFire.evacuations.count 
                        ? `${selectedFire.evacuations.count.toLocaleString()} people evacuated`
                        : 'Evacuations ordered'}
                    </p>
                    {selectedFire.evacuations.description && (
                      <p className="text-sm text-gray-500">{selectedFire.evacuations.description}</p>
                    )}
                  </div>
                )}

                {selectedFire.resources && (
                  <div>
                    <h4 className="font-semibold">Resources Deployed</h4>
                    <ul className="list-disc list-inside space-y-1">
                      {selectedFire.resources.map((resource, index) => (
                        <li key={index}>{resource}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {selectedFire.description && (
                  <div>
                    <h4 className="font-semibold">Description</h4>
                    <p className="text-gray-700">{selectedFire.description}</p>
                  </div>
                )}

                {selectedFire.sources && selectedFire.sources.length > 0 && (
                  <div>
                    <h4 className="font-semibold">Sources</h4>
                    <ul className="list-disc list-inside">
                      {selectedFire.sources.map((source, index) => (
                        <li key={index} className="text-sm text-gray-600">{source}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
