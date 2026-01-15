import { describe, it, expect } from 'vitest';
import { evaluate } from '../lib/recommender';

describe('recommender', () => {
  it('scores high when SIEM and EDR present', () => {
    const state = { posture: { siem: 'Yes', edr: 'Yes', mttd: 2 }, env: {}, org: { size: 100 } };
    const res = evaluate(state);
    expect(res.score).toBeGreaterThanOrEqual(30);
    expect(res.tier).toBe('Better' || 'Best');
  });

  it('returns Good for minimal config', () => {
    const state = { posture: { siem: 'No', edr: 'No' }, env: {}, org: { size: 10 } };
    const res = evaluate(state);
    expect(res.tier).toBe('Good');
  });
});
