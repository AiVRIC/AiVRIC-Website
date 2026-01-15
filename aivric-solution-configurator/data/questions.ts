export type Question = {
  id: string;
  label: string;
  field: string;
  type: 'select' | 'multiselect' | 'text' | 'number' | 'radio';
  options?: string[];
  tooltip?: string;
};

export const steps = [
  { id: 'org', title: 'Org Profile' },
  { id: 'posture', title: 'Current Posture' },
  { id: 'priorities', title: 'Priorities & Outcomes' },
  { id: 'env', title: 'Environment & Integrations' },
  { id: 'constraints', title: 'Constraints' }
];

export const questions: Record<string, Question[]> = {
  org: [
    { id: 'size', label: 'Organization size (employees)', field: 'org.size', type: 'number' },
    { id: 'industry', label: 'Industry', field: 'org.industry', type: 'select', options: ['Finance','Healthcare','SaaS','Retail','Other'] },
    { id: 'persona', label: 'Persona', field: 'org.persona', type: 'radio', options: ['CISO','IT Ops','GRC','Product'] }
  ],
  posture: [
    { id: 'has_siem', label: 'SIEM in place', field: 'posture.siem', type: 'radio', options: ['Yes','No'], tooltip: 'SIEM: Security Information and Event Management' },
    { id: 'has_edr', label: 'EDR deployed', field: 'posture.edr', type: 'radio', options: ['Yes','No'], tooltip: 'EDR: Endpoint Detection & Response' },
    { id: 'mean_time_detect', label: 'Mean time to detect (days)', field: 'posture.mttd', type: 'number', tooltip: 'MTTD: Mean Time To Detect' }
  ],
  priorities: [
    { id: 'priorities', label: 'Top priorities', field: 'priorities.top', type: 'multiselect', options: ['Compliance','Detection','Response','Visibility','Developer Experience'] }
  ],
  env: [
    { id: 'cloud', label: 'Cloud provider', field: 'env.cloud', type: 'select', options: ['AWS','Azure','GCP','On-prem'] },
    { id: 'idp', label: 'Identity Provider', field: 'env.idp', type: 'select', options: ['Okta','Azure AD','Auth0','Other'], tooltip: 'IdP: Identity Provider' }
  ],
  constraints: [
    { id: 'budget', label: 'Budget (monthly)', field: 'constraints.budget', type: 'number' },
    { id: 'timeline', label: 'Target deployment (weeks)', field: 'constraints.timeline', type: 'number' }
  ]
};
