"use client";
import React, { useState } from 'react';
import { useWizardStore } from '../../store/useWizardStore';
import { evaluate } from '../../lib/recommender';
import Link from 'next/link';

export default function ResultsPage(){
  const data = useWizardStore(s=>s.data);
  const persona = useWizardStore(s=>s.persona);
  const rec = evaluate(data || {}, persona);
  const [busy, setBusy] = useState(false);

  async function exportPdf(){
    setBusy(true);
    try{
      const res = await fetch('/api/pdf', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ data, rec }) });
      if(!res.ok){ const j = await res.json().catch(()=>null); alert('PDF error: '+(j?.error||res.status)); return; }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'aivric-results.pdf'; a.click();
      URL.revokeObjectURL(url);
    }catch(err){ alert('PDF error: '+String(err)); }
    setBusy(false);
  }

  async function emailMe(){
    setBusy(true);
    try{
      const res = await fetch('/api/email', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ data, rec, to: undefined }) });
      const j = await res.json();
      if(!j.ok) alert('Email error: '+j.error); else alert('Email queued (check console in dev)');
    }catch(err){ alert('Email error: '+String(err)); }
    setBusy(false);
  }

  return (
    <div>
      <Header />
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Recommendation Results</h1>
        <div className="space-x-2">
          <Button onClick={exportPdf} disabled={busy} className="px-3 py-1">Export PDF</Button>
          <Button onClick={emailMe} disabled={busy} variant="secondary" className="px-3 py-1">Email me</Button>
        </div>
      </div>

      <Card>
        <h2 className="text-lg font-medium">Recommended Tier: {rec.tier}</h2>
        <p className="text-sm text-gray-600">Score: {rec.score}</p>

        <div className="mt-4">
          <h3 className="font-medium">Persona note</h3>
          <p className="text-sm text-gray-600">{rec.personaNote ?? '—'}</p>
        </div>

        <div className="mt-4">
          <h3 className="font-medium">Compare Options</h3>
          <CompareTabs options={rec.compareOptions || []} />
        </div>

        <div className="mt-4">
          <Button variant="ghost" onClick={()=>{ const blob = new Blob([JSON.stringify(rec, null, 2)], { type: 'application/json' }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'aivric-recommendation.json'; a.click(); URL.revokeObjectURL(url); }}>Download scoring breakdown</Button>
        </div>

        <h3 className="mt-4 font-medium">Modules</h3>
        <ul className="list-disc ml-5">
          {rec.modules.map(m => <li key={m.id}>{m.name}</li>)}
        </ul>

        <h3 className="mt-4 font-medium">Rationale</h3>
        <ul className="ml-5 list-decimal">
          {rec.rationale.map((r:any) => (
            <li key={r.ruleId} className={r.matched? 'text-black':'text-gray-400'}>
              <span className="inline-flex items-center mr-2">
                <span className={`text-xs px-2 py-0.5 rounded ${r.severity === 'high' ? 'bg-red-100 text-red-700' : r.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-700'}`}>{r.severity ?? 'low'}</span>
              </span>
              {r.description} — {r.matched ? `+${r.score}` : '0'}
              <span className="text-xs text-gray-500 ml-2">{r.category ? `(${r.category})` : ''}</span>
            </li>
          ))}
        </ul>

        <h3 className="mt-4 font-medium">Estimated deployment</h3>
        <p className="text-sm">{estimateTimeline(rec.tier)}</p>

        <h3 className="mt-4 font-medium">What you'll need from the customer</h3>
        <ul className="ml-5 list-disc text-sm">
          <li>Admin access to cloud accounts (least privilege)</li>
          <li>Designated security contact</li>
          <li>Time for onboarding workshops (2-5 days)</li>
        </ul>

        <div className="mt-6">
          <Link href="/configurator"><Button variant="ghost">Back to Edit</Button></Link>
        </div>
      </Card>
    </div>
  );
}

import Header from '../../components/ui/Header';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

function estimateTimeline(tier:string){
  if(tier==='Best') return '8-16 weeks (includes integration, onboarding, tuning). Assumes dedicated resources.';
  if(tier==='Better') return '6-10 weeks (standard integrations, some tuning).';
  return '4-8 weeks (core modules, minimal integrations).';
}

function CompareTabs({ options }: { options: Array<{ tier: string; modules: { id: string; name: string }[]; rationaleSummary: string }> }){
  const [tab, setTab] = React.useState(0);
  if(!options || !options.length) return <div className="text-sm text-gray-500">No compare options available.</div>;
  return (
    <div>
      <div className="flex space-x-2">
        {options.map((o, i) => (
          <button key={o.tier} onClick={()=>setTab(i)} className={`px-3 py-1 rounded ${i===tab? 'bg-sky-600 text-white':'bg-gray-100'}`}>{o.tier}</button>
        ))}
      </div>
      <div className="mt-3">
        <h4 className="font-medium">{options[tab].tier} — {options[tab].rationaleSummary}</h4>
        <ul className="list-disc ml-5 mt-2">
          {options[tab].modules.map(m => <li key={m.id}>{m.name}</li>)}
        </ul>
      </div>
    </div>
  );
}
