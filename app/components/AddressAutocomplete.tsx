'use client';

import { useEffect, useRef, useState } from 'react';
import { loadGoogleMaps } from '../utils/googleMapsLoader';

declare global {
  interface Window {
    initMap: () => void;
    gm_authFailure?: () => void;
  }
}

interface AddressAutocompleteProps {
  value: string;
  onChange: (address: string) => void;
  placeholder?: string;
  required?: boolean;
  className?: string;
}

type Autocomplete = any;
type Maps = {
  places: {
    Autocomplete: new (input: HTMLInputElement, options: any) => Autocomplete;
  };
  event: {
    clearInstanceListeners: (instance: any) => void;
  };
};

export default function AddressAutocomplete({
  value,
  onChange,
  placeholder = 'Enter your address',
  required = false,
  className = '',
}: AddressAutocompleteProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const autocompleteRef = useRef<Autocomplete | null>(null);

  // Track if the component is mounted
  const isMountedRef = useRef(true);

  useEffect(() => {
    // Function to handle Google Maps API errors
    const handleGoogleMapsError = () => {
      if (window.google?.maps) {
        const errorDiv = document.createElement('div');
        errorDiv.id = 'google-maps-error';
        errorDiv.style.display = 'none';
        document.body.appendChild(errorDiv);

        // Listen for Google Maps API errors
        window.gm_authFailure = () => {
          if (isMountedRef.current) {
            setError('Google Maps API key is invalid. Please check your API key configuration.');
            setIsLoading(false);
          }
        };
      }
    };

    const initAutocomplete = async () => {
      try {
        await loadGoogleMaps();
        
        if (!inputRef.current) {return;}
        
        const maps = (window.google?.maps || {}) as Maps;
        autocompleteRef.current = new maps.places.Autocomplete(inputRef.current, {
          componentRestrictions: { country: 'us' },
          fields: ['formatted_address'],
          types: ['address'],
        });

        autocompleteRef.current.addListener('place_changed', () => {
          const place = autocompleteRef.current?.getPlace();
          if (place?.formatted_address) {
            onChange(place.formatted_address);
          }
        });

        setIsLoading(false);
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Error loading Google Maps';
        console.error(message);
        setError(message);
        setIsLoading(false);
      }
    };

    initAutocomplete();
    handleGoogleMapsError();

    return () => {
      isMountedRef.current = false;
      // Clean up error handler
      if (window.gm_authFailure) {
        delete window.gm_authFailure;
      }
      const errorDiv = document.getElementById('google-maps-error');
      if (errorDiv) {
        errorDiv.remove();
      }
      if (autocompleteRef.current) {
        const maps = (window.google?.maps || {}) as Maps;
        maps.event.clearInstanceListeners(autocompleteRef.current);
      }
    };
  }, [onChange]);

  return (
    <div className="relative">
      {error && (
        <div className="absolute -top-6 left-0 right-0 text-red-500 text-sm">
          {error}
        </div>
      )}
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={isLoading ? 'Loading...' : placeholder}
        required={required}
        className={`${className} ${isLoading ? 'cursor-wait' : ''}`}
        disabled={isLoading}
      />
      {isLoading && (
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white/20 border-t-white"></div>
        </div>
      )}
    </div>
  );
}
