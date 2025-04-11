'use client';

import { useEffect, useState } from 'react';

interface RiskData {
  level: string;
  description: string;
  recommendations: string[];
}

export default function FireRiskAssessment(): JSX.Element {
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRiskData = async (): Promise<void> => {
      try {
        const response = await fetch('/api/fire_risk');
        const data = await response.json();
        setRiskData(data);
      } catch (error) {
        console.error('Error fetching risk data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRiskData();
  }, []);

  if (loading) {
    return (
      <div className="glass-container p-6">
        <p className="text-gray-500">Loading risk assessment...</p>
      </div>
    );
  }

  if (!riskData) {
    return (
      <div className="glass-container p-6">
        <p className="text-red-500">Failed to load risk assessment</p>
      </div>
    );
  }

  const riskColors = {
    low: 'border-green-400',
    moderate: 'border-yellow-400',
    high: 'border-orange-400',
    extreme: 'border-red-400',
  };

  const riskColor = riskColors[riskData.level.toLowerCase() as keyof typeof riskColors] || 'border-gray-400';

  return (
    <div className={`glass-container p-6 border-l-4 ${riskColor}`}>
      <h2 className="text-xl font-bold mb-2 text-white">Current Fire Risk Level</h2>
      <div className="mb-4">
        <span className="font-semibold text-white/70">Level: </span>
        <span className="text-lg text-white">{riskData.level}</span>
      </div>
      <p className="mb-4 text-white">{riskData.description}</p>
      {riskData.recommendations.length > 0 && (
        <div>
          <h3 className="font-semibold mb-2 text-white">Recommendations:</h3>
          <ul className="list-disc list-inside space-y-1 text-white">
            {riskData.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
