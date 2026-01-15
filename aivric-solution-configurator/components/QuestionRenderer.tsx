import React from 'react';
import { Question } from '../data/questions';

export default function QuestionRenderer({ q, value, onChange }: { q: Question; value: any; onChange: (v:any)=>void }) {
  if (q.type === 'number') {
    return (
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">{q.label}</label>
        <input type="number" value={value ?? ''} onChange={(e)=>onChange(Number(e.target.value))} className="border rounded p-2 w-full" />
      </div>
    );
  }

  if (q.type === 'radio' || q.type === 'select') {
    return (
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">{q.label}</label>
        <select value={value ?? ''} onChange={(e)=>onChange(e.target.value)} className="border rounded p-2 w-full">
          <option value="">Select...</option>
          {q.options?.map(o=> <option key={o} value={o}>{o}</option>)}
        </select>
      </div>
    );
  }

  if (q.type === 'multiselect') {
    return (
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">{q.label}</label>
        <div className="grid grid-cols-2 gap-2">
          {q.options?.map(o => (
            <label key={o} className="inline-flex items-center space-x-2">
              <input type="checkbox" checked={(value||[]).includes(o)} onChange={(e)=>{
                const next = new Set(value||[]);
                if (e.target.checked) next.add(o); else next.delete(o);
                onChange(Array.from(next));
              }} />
              <span className="text-sm">{o}</span>
            </label>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium mb-1">{q.label}</label>
      <input type="text" value={value ?? ''} onChange={(e)=>onChange(e.target.value)} className="border rounded p-2 w-full" />
    </div>
  );
}
