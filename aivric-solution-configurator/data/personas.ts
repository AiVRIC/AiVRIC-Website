export const personas = [
  {
    id: 'ciso',
    name: 'CISO',
    emphasis: ['risk', 'compliance', 'visibility'],
    stepOrder: ['org','posture','priorities','env','constraints'],
    narrative: 'Executive-focused: prioritize risk reduction, compliance readiness, and organization-wide visibility.'
  },
  {
    id: 'itops',
    name: 'IT Ops',
    emphasis: ['resilience', 'operability', 'automation'],
    stepOrder: ['env','posture','org','priorities','constraints'],
    narrative: 'Operations-focused: prioritize resilience, automation, and operational visibility.'
  },
  { id: 'grc', name: 'GRC', emphasis: ['controls', 'evidence', 'audit'], stepOrder: ['posture','org','priorities','constraints','env'], narrative: 'Governance-focused: emphasize controls, evidence collection, and audit readiness.' },
  { id: 'product', name: 'Product', emphasis: ['velocity', 'developer-experience', 'release-safety'], stepOrder: ['priorities','env','org','posture','constraints'], narrative: 'Product-focused: balance security with developer velocity and release safety.' }
];
