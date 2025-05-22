import { GridCell, SimulationParams } from '../schemas/types';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  async getRiskData(): Promise<GridCell[]> {
    const response = await fetch(`${API_BASE_URL}/risk-data`);
    const data: unknown = await response.json();
    if (
      typeof data === 'object' &&
      data !== null &&
      'data' in data &&
      Array.isArray((data as { data?: unknown }).data)
    ) {
      return (data as { data: GridCell[] }).data;
    }
    throw new Error('Invalid data format from server');
  },

  async simulateFire(params: SimulationParams): Promise<Record<string, unknown>> {
    const response = await fetch(`${API_BASE_URL}/simulate-fire`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });
    const data: unknown = await response.json();
    if (typeof data === 'object' && data !== null) {
      return data as Record<string, unknown>;
    }
    throw new Error('Invalid data format from server');
  },
};
