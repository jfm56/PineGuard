'use client';

import { useState } from 'react';

export default function AiTest() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const generateHaiku = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [
            { role: 'user', content: 'write a haiku about ai' }
          ]
        }),
      });

      const data = await response.json();
      if (data.result) {
        setResult(data.result.content);
      }
    } catch (error) {
      console.error('Error:', error);
      setResult('Error generating haiku');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <button
        onClick={generateHaiku}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        {loading ? 'Generating...' : 'Generate AI Haiku'}
      </button>
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <pre className="whitespace-pre-wrap">{result}</pre>
        </div>
      )}
    </div>
  );
}
