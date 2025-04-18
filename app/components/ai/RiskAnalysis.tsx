'use client';

import { useState, useEffect, useCallback } from 'react';

interface RiskData {
  historicalDensity: number;
  riskScore: number;
  description: string;
  lastUpdated: string;
}

export default function RiskAnalysis(): JSX.Element {
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeRisk = useCallback(async () => {
    if (!riskData) return;

    setLoading(true);
    try {
      const response = await fetch('/api/analyze-risk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(riskData),
      });

      const data = await response.json() as { analysis: string };
      setAnalysis(data.analysis);
    } catch (error) {
      setAnalysis('Error analyzing fire risk. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [riskData]);

  const fetchRiskData = useCallback(async () => {
    try {
      const response = await fetch('/api/current-risk', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch risk data: ${response.status} ${errorText}`);
      }

      const data = await response.json() as RiskData & { error?: string };
      if (data.error) {
        throw new Error(data.error);
      }

      setRiskData(data);
    } catch (error) {
      setRiskData(null);
    }
  }, []);

  useEffect(() => {
    void fetchRiskData();
  }, [fetchRiskData]);

  useEffect(() => {
    if (riskData) {
      void analyzeRisk();
    }
  }, [riskData, analyzeRisk]);

  if (!riskData) {
    return (
      <div className="glass-container p-6 space-y-4">
        <h2 className="text-xl font-bold text-white">Fire Risk Analysis</h2>
        <div className="bg-white/10 p-4 rounded-lg">
          <p className="text-white">Loading risk data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-container p-6 space-y-4">
      <h2 className="text-xl font-bold text-white">Fire Risk Analysis</h2>
      
      <div className="space-y-4">
        <div className="bg-white/10 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Current Risk Level</h3>
          <div className="grid grid-cols-2 gap-4">
            <ul className="space-y-2 text-white">
              <li>Historical Fire Density: {riskData.historicalDensity}</li>
              <li>Risk Score: {riskData.riskScore}</li>
              <li className="text-xs mt-4">Last updated: {new Date(riskData.lastUpdated).toLocaleTimeString()}</li>
            </ul>
            <ul className="space-y-2 text-white">
              <li>Description: {riskData.description}</li>
            </ul>
          </div>
        </div>

        <div className="bg-white/10 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Risk Assessment</h3>
          {loading ? (
            <p className="text-white">Analyzing risk...</p>
          ) : (
            <div className="text-white whitespace-pre-wrap">{analysis}</div>
          )}
        </div>
      </div>

      <button
        onClick={() => void analyzeRisk()}
        disabled={loading}
        className="w-full py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? 'Analyzing...' : 'Refresh Analysis'}
      </button>
    </div>
  );
}
