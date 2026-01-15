"use client";
import React, { useEffect } from 'react';
import { useWizardStore } from '../../store/useWizardStore';
import { steps as baseSteps, questions } from '../../data/questions';
import ProgressHeader from '../../components/ProgressHeader';
import QuestionRenderer from '../../components/QuestionRenderer';
import TooltipTerm from '../../components/TooltipTerm';
import Link from 'next/link';
import Header from '../../components/ui/Header';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { getSchemaForStep } from '../../data/schemas';
import { personas } from '../../data/personas';

export default function ConfiguratorPage(){
  const stepIndex = useWizardStore(s=>s.stepIndex);
  const setStep = useWizardStore(s=>s.setStep);
  const data = useWizardStore(s=>s.data);
  const setData = useWizardStore(s=>s.setData);

  const persona = useWizardStore(s=>s.persona);
  const setPersona = useWizardStore(s=>s.setPersona);

  const steps = getStepsForPersona(persona);
  const step = steps[stepIndex];
  const qs = questions[step.id];

  const schema = getSchemaForStep(step.id);
  const { register, handleSubmit, reset, getValues } = useForm({ resolver: zodResolver(schema), mode: 'onChange' });

  useEffect(()=>{
    // build defaults from store data for this step
    const defaults: any = {};
    qs.forEach(q => {
      const val = getValue(data, q.field);
      defaults[q.id] = val === undefined ? (q.type==='multiselect'?[]:'') : val;
    });
    reset(defaults);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[stepIndex, persona]);

  const handleNext = ()=>{
    if(stepIndex < steps.length-1) setStep(stepIndex+1);
  };
  const handleBack = ()=>{ if(stepIndex>0) setStep(stepIndex-1); };

  const onSubmit = (formValues:any)=>{
    // build patch from questions
    const patch: any = {};
    qs.forEach(q => {
      const v = formValues[q.id];
      deepAssign(patch, q.field.split('.'), v);
    });
    setData(patch);
    handleNext();
  };

  return (
    <div>
      <Header />
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-semibold">Configurator</h1>
        <div className="text-sm">Terms: <TooltipTerm term="SIEM" title="Security Information and Event Management" /> <span className="mx-1">·</span> <TooltipTerm term="EDR" title="Endpoint Detection & Response" /></div>
      </div>
      {!persona && (
        <div className="mt-4 grid grid-cols-4 gap-4">
          {personas.map(p => (
            <button key={p.id} onClick={()=>{ setPersona(p.id); }} className="p-4 border rounded hover:bg-gray-100">
              <div className="font-medium">{p.name}</div>
              <div className="text-sm text-gray-600 mt-1">{p.narrative}</div>
            </button>
          ))}
        </div>
      )}
      <ProgressHeader steps={steps} index={stepIndex} />

      <Card>
        <form onSubmit={handleSubmit(onSubmit)}>
          {qs.map(q => (
            <QuestionWrapper key={q.id} q={q} register={register} getValues={getValues} />
          ))}

          <div className="flex justify-between mt-6">
            <Button variant="secondary" onClick={handleBack} type="button">Back</Button>
            <div className="space-x-2">
              {stepIndex < steps.length-1 ? <Button type="submit">Next</Button> : <Link href="/results"><Button variant="primary">Finish</Button></Link>}
            </div>
          </div>
        </form>
      </Card>
    </div>
  );
}

function QuestionWrapper({ q, register, getValues }: any){
  const value = getValues(q.id);
  // adapt QuestionRenderer to use register where possible
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium mb-1">{q.label}</label>
      {q.type === 'number' && <input {...register(q.id, { valueAsNumber: true })} type="number" className="border rounded p-2 w-full" />}
      {(q.type === 'select' || q.type === 'radio') && (
        <select {...register(q.id)} className="border rounded p-2 w-full">
          <option value="">Select...</option>
          {q.options?.map((o:string)=> <option key={o} value={o}>{o}</option>)}
        </select>
      )}
      {q.type === 'multiselect' && (
        <div className="grid grid-cols-2 gap-2">
          {q.options?.map((o:string)=> (
            <label key={o} className="inline-flex items-center space-x-2">
              <input type="checkbox" {...register(q.id)} value={o} defaultChecked={(value||[]).includes(o)} />
              <span className="text-sm">{o}</span>
            </label>
          ))}
        </div>
      )}
      {q.type === 'text' && <input {...register(q.id)} type="text" className="border rounded p-2 w-full" />}
    </div>
  );
}

function getValue(data:any, path:string){
  const parts = path.split('.');
  let cur = data;
  for(const p of parts){ if(!cur) return undefined; cur = cur[p]; }
  return cur;
}

function deepAssign(obj:any, parts:string[], value:any){
  let cur = obj;
  for(let i=0;i<parts.length;i++){
    const p = parts[i];
    if(i === parts.length-1) cur[p] = value;
    else { cur[p] = cur[p] || {}; cur = cur[p]; }
  }
}

function getStepsForPersona(persona?: string){
  if(!persona) return baseSteps;
  const p = personas.find(x=>x.id===persona);
  if(!p || !p.stepOrder) return baseSteps;
  // map order ids to step objects, fallback to base order
  const map = Object.fromEntries(baseSteps.map(s=>[s.id,s]));
  const ordered = p.stepOrder.map((id:any)=> map[id]).filter(Boolean);
  // append any missing steps
  baseSteps.forEach(s=>{ if(!ordered.find((x:any)=>x.id===s.id)) ordered.push(s); });
  return ordered;
}

