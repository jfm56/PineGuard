import { GridCell, SimulationParams } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  async getRiskData(): Promise<GridCell[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/risk-data`);
      const data = await response.json();
      return data.data;
    } catch (error) {
      console.error('Error fetching risk data:', error);
      throw error;
    }
  },

  async simulateFire(params: SimulationParams): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/simulate-fire`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error simulating fire:', error);
      throw error;
    }
  },
};
