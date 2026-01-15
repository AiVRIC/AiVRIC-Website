"use client";
import React, { useEffect, useState } from 'react';
import Card from '../../../components/ui/Card';
import Button from '../../../components/ui/Button';
import { rules as defaultRules } from '../../../data/rules';

export default function RulesEditor(){
  const [text, setText] = useState('');
  const [message, setMessage] = useState<string | null>(null);

  useEffect(()=>{
    try{
      const override = window.localStorage.getItem('aivric-rules-override');
      if(override) setText(override);
      else setText(JSON.stringify(defaultRules, null, 2));
    }catch(e){ setText(JSON.stringify(defaultRules, null, 2)); }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[]);

  function save(){
    try{
      const parsed = JSON.parse(text);
      if(!Array.isArray(parsed)) throw new Error('Expected an array of rules');
      window.localStorage.setItem('aivric-rules-override', JSON.stringify(parsed));
      setMessage('Saved to localStorage; recommendations will use the override.');
    }catch(e:any){ setMessage('Error: '+(e.message||String(e))); }
  }

  function resetDefaults(){
    window.localStorage.removeItem('aivric-rules-override');
    setText(JSON.stringify(defaultRules, null, 2));
    setMessage('Reset to defaults.');
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Rule Editor</h1>
      <p className="text-sm text-gray-600 mb-4">Edit the rules JSON and <strong>Save</strong> to apply locally (stored in `localStorage`). This does not change repository files.</p>
      <Card>
        <textarea className="w-full h-96 p-2 font-mono text-sm border rounded" value={text} onChange={(e)=>setText(e.target.value)} />
        <div className="flex gap-2 mt-3">
          <Button onClick={save}>Save</Button>
          <Button variant="secondary" onClick={resetDefaults}>Reset</Button>
        </div>
        {message && <div className="mt-3 text-sm text-gray-700">{message}</div>}
      </Card>
    </div>
  );
}
