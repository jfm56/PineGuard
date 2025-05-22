'use client';

import { useState } from 'react';
import Image from 'next/image';

export default function RiskAssessment(): JSX.Element {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0];
    if (!file) {return;}

    // Convert to base64
    const reader = new FileReader();
    reader.onloadend = async (): Promise<void> => {
      const base64String = reader.result as string;
      setSelectedImage(base64String);

      setLoading(true);
      try {
        const response = await fetch('/api/analyze-risk', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image: base64String,
          }),
        });

        const data: unknown = await response.json();
        if (typeof data === 'object' && data !== null && 'analysis' in data && typeof (data as { analysis?: unknown }).analysis === 'string') {
          setAnalysis((data as { analysis: string }).analysis);
        } else {
          setAnalysis('Error: Invalid response from server.');
        }
      } catch (error) {
        /* error intentionally ignored for production build; consider handling/logging in dev */
        setAnalysis('Error analyzing image. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="glass-container p-6 space-y-4">
      <h2 className="text-xl font-bold text-white">Visual Risk Assessment</h2>
      
      <div className="space-y-4">
        <label className="block">
          <span className="text-white">Upload property photo for analysis</span>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => { void handleImageUpload(e); }}
            className="mt-1 block w-full text-sm text-white
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-green-600 file:text-white
              hover:file:bg-green-700"
          />
        </label>

        {selectedImage && (
          <div className="relative w-full h-48">
            <Image
              src={selectedImage}
              alt="Selected property"
              fill
              style={{ objectFit: 'cover' }}
              className="rounded-lg"
            />
          </div>
        )}

        {loading && (
          <div className="text-white">Analyzing image...</div>
        )}

        {analysis && (
          <div className="bg-white/10 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-white mb-2">Risk Analysis:</h3>
            <p className="text-white whitespace-pre-wrap">{analysis}</p>
          </div>
        )}
      </div>
    </div>
  );
}
