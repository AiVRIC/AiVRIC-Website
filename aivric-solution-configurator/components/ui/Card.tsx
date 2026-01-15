import React from 'react';

export default function Card({ children, className = '' }: any) {
  return (
    <div className={`bg-white border border-gray-200 rounded-lg p-4 shadow-sm ${className}`}>
      {children}
    </div>
  );
}
