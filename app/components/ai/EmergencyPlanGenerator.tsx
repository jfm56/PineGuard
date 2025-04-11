'use client';

import { useState } from 'react';
import AddressAutocomplete from '../AddressAutocomplete';

interface PlanDetails {
  address: string;
  familySize: number;
  hasPets: boolean;
  hasSpecialNeeds: boolean;
  specialNeedsDetails?: string;
}

export default function EmergencyPlanGenerator() {
  const [planDetails, setPlanDetails] = useState<PlanDetails>({
    address: '',
    familySize: 1,
    hasPets: false,
    hasSpecialNeeds: false,
  });
  const [plan, setPlan] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('/api/generate-plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(planDetails),
      });

      const data = await response.json();
      setPlan(data.plan);
    } catch (error) {
      console.error('Error generating plan:', error);
      setPlan('Error generating emergency plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-container p-6 space-y-4">
      <h2 className="text-xl font-bold text-white">Emergency Plan Generator</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-white">
            Address
            <AddressAutocomplete
              value={planDetails.address}
              onChange={(address) => setPlanDetails(prev => ({ ...prev, address }))}
              className="mt-1 block w-full rounded-md bg-white/10 border-transparent text-white placeholder-white/50"
              placeholder="Enter your address"
              required
            />
          </label>
        </div>

        <div>
          <label className="block text-white">
            Family Size
            <input
              type="number"
              min="1"
              value={planDetails.familySize}
              onChange={(e) => {
                const value = parseInt(e.target.value);
                if (!isNaN(value) && value > 0) {
                  setPlanDetails(prev => ({ ...prev, familySize: value }));
                }
              }}
              className="mt-1 block w-full rounded-md bg-white/10 border-transparent text-white"
              required
            />
          </label>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="hasPets"
            checked={planDetails.hasPets}
            onChange={(e) => setPlanDetails(prev => ({ ...prev, hasPets: e.target.checked }))}
            className="rounded bg-white/10 border-transparent text-green-600"
          />
          <label htmlFor="hasPets" className="text-white">Have Pets</label>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="hasSpecialNeeds"
            checked={planDetails.hasSpecialNeeds}
            onChange={(e) => setPlanDetails(prev => ({ ...prev, hasSpecialNeeds: e.target.checked }))}
            className="rounded bg-white/10 border-transparent text-green-600"
          />
          <label htmlFor="hasSpecialNeeds" className="text-white">Special Needs</label>
        </div>

        {planDetails.hasSpecialNeeds && (
          <div>
            <label className="block text-white">
              Special Needs Details
              <textarea
                value={planDetails.specialNeedsDetails}
                onChange={(e) => setPlanDetails(prev => ({ ...prev, specialNeedsDetails: e.target.value }))}
                className="mt-1 block w-full rounded-md bg-white/10 border-transparent text-white placeholder-white/50"
                placeholder="Please describe any special needs..."
              />
            </label>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
        >
          {loading ? 'Generating Plan...' : 'Generate Emergency Plan'}
        </button>
      </form>

      {plan && (
        <div className="mt-6 bg-white/10 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Your Emergency Plan:</h3>
          <div className="text-white whitespace-pre-wrap">{plan}</div>
        </div>
      )}
    </div>
  );
}
