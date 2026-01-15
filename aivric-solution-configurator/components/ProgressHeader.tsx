import React from 'react';

export default function ProgressHeader({ steps, index }: { steps: { id: string; title: string }[]; index: number }) {
  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-medium">{steps[index].title}</h2>
        <div className="text-sm text-gray-600">Step {index + 1} of {steps.length}</div>
      </div>
      <div className="w-full bg-gray-200 h-2 rounded">
        <div className="h-2 bg-sky-600 rounded" style={{ width: `${((index+1)/steps.length)*100}%` }} />
      </div>
    </div>
  );
}
