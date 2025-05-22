'use client';

import Link from 'next/link';
import { useState } from 'react';

interface MainMenuProps {
  onClose: () => void;
}

export default function MainMenu({ onClose }: MainMenuProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
      >
        <div className="flex items-center space-x-2">
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
          <span>Menu</span>
        </div>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-48 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
          <div className="py-1">
            <Link
              href="/"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Dashboard
            </Link>
            <Link
              href="/risk-prediction"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Risk Prediction
            </Link>
            <Link
              href="/fire-preparedness"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Fire Preparedness
            </Link>
            <Link
              href="/evacuation-routes"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Evacuation Routes
            </Link>
            <Link
              href="/resources"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Resources
            </Link>
            <Link
              href="/contact"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => {
                setIsOpen(false);
                onClose();
              }}
            >
              Emergency Contacts
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
