import { rules as baseRules } from '../data/rules';
import { modules } from '../data/modules';
import { personas } from '../data/personas';

export type Recommendation = {
  score: number;
  tier: 'Good' | 'Better' | 'Best';
  modules: typeof modules;
  rationale: { ruleId: string; description: string; matched: boolean; score: number }[];
  personaNote?: string;
  compareOptions?: Array<{ tier: string; modules: { id: string; name: string }[]; rationaleSummary: string }>;
};

function getActiveRules(){
  if (typeof window !== 'undefined'){
    try{
      const raw = window.localStorage.getItem('aivric-rules-override');
      if(raw){
        const parsed = JSON.parse(raw);
        if(Array.isArray(parsed)) return parsed;
      }
    }catch(e){ /* ignore and fall back */ }
  }
  return baseRules as any;
}

export function evaluate(state: any, personaId?: string): Recommendation {
  const rules = getActiveRules();
  let score = 0;
  const rationale = rules.map((r: any) => {
    const matched = !!r.condition(state);
    // severity multiplier
    const mult = r.severity === 'high' ? 1.5 : r.severity === 'medium' ? 1.25 : 1.0;
    const contributed = matched ? Math.round((r.score || 0) * mult) : 0;
    if (matched) score += contributed;
    return { ruleId: r.id, description: r.description, matched, score: contributed, severity: r.severity, category: r.category } as any;
  });

  // persona-driven boost: small, transparent modifier
  const persona = personas.find(p => p.id === personaId);
  let personaNote = '';
  if (persona) {
    personaNote = persona.narrative;
    // example: boost score for GRC if rule mentions 'compliance' or 'audit'
    if (persona.id === 'grc') {
      rationale.forEach(r => { if (r.description.toLowerCase().includes('compliance') || r.description.toLowerCase().includes('audit')) { score += 3; (r as any).score = (r as any).score + 3; } });
    }
    if (persona.id === 'ciso') {
      rationale.forEach(r => { if (r.description.toLowerCase().includes('risk') || r.description.toLowerCase().includes('large')) { score += 2; (r as any).score = (r as any).score + 2; } });
    }
    if (persona.id === 'product') {
      // product persona cares less about infrastructure-only rules
      rationale.forEach(r => { if (r.description.toLowerCase().includes('endpoint')) { score -= 1; } });
    }
  }

  const tier = score >= 40 ? 'Best' : score >= 20 ? 'Better' : 'Good';

  // simple module selection rules
  const selected = modules.filter((m) => {
    if (m.id === 'siem' && state.posture?.siem === 'Yes') return true;
    if (m.id === 'edr' && state.posture?.edr === 'Yes') return true;
    if (m.id === 'cspm' && state.env?.cloud) return true;
    return false;
  });

  const compareOptions = [
    { tier: 'Good', modules: modules.filter(m=> m.id === 'edr' || m.id === 'cspm').map(m=>({id:m.id,name:m.name})), rationaleSummary: 'Core detection and cloud posture.' },
    { tier: 'Better', modules: modules.filter(m=> m.id === 'siem' || m.id === 'edr' || m.id === 'cspm').map(m=>({id:m.id,name:m.name})), rationaleSummary: 'Adds centralized logging and correlation.' },
    { tier: 'Best', modules: modules.map(m=>({id:m.id,name:m.name})), rationaleSummary: 'Full stack with integrations and advanced tuning.' }
  ];

  return { score, tier, modules: selected, rationale, personaNote, compareOptions } as any;
}
