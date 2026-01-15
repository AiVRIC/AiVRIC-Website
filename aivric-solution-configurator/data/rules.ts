type Rule = {
  id: string;
  description: string;
  score: number;
  severity?: 'low' | 'medium' | 'high';
  category?: string;
  type Rule = {
    id: string;
    description: string;
    score: number;
    severity?: 'low' | 'medium' | 'high';
    category?: string;
    condition: (state: any) => boolean;
  };

  export const rules: Rule[] = [
    {
      id: 'has-siem',
      description: 'Has SIEM deployed',
      score: 20,
      severity: 'high',
      category: 'detection',
      condition: (s) => s.posture?.siem === 'Yes'
    },
    {
      id: 'has-edr',
      description: 'Has EDR deployed',
      score: 15,
      severity: 'high',
      category: 'endpoint',
      condition: (s) => s.posture?.edr === 'Yes'
    },
    {
      id: 'mfa-admins',
      description: 'MFA for administrators enabled',
      score: 18,
      severity: 'high',
      category: 'identity',
      condition: (s) => s.env?.mfaAdmins === 'Yes' || (s.env?.idp && String(s.env.idp).length>0)
    },
    {
      id: 'idp-sso',
      description: 'Identity provider / SSO in use',
      score: 10,
      severity: 'medium',
      category: 'identity',
      condition: (s) => !!s.env?.idp
    },
    {
      id: 'iac-scanning',
      description: 'Infrastructure-as-code scanning in CI',
      score: 12,
      severity: 'medium',
      category: 'devsecops',
      condition: (s) => s.env?.iacScans === 'Yes' || s.env?.ciCd === 'Yes'
    },
    {
      id: 'vuln-scanning',
      description: 'Regular vulnerability scanning / SCA',
      score: 14,
      severity: 'high',
      category: 'vulnerability-management',
      condition: (s) => s.env?.vulnScanning === 'Yes'
    },
    {
      id: 'logging-retention',
      description: 'Log retention >= 30 days',
      score: 8,
      severity: 'medium',
      category: 'data-retention',
      condition: (s) => (s.env?.logRetentionDays || 0) >= 30
    },
    {
      id: 'multi-cloud',
      description: 'Multi-cloud environment',
      score: 10,
      severity: 'medium',
      category: 'cloud',
      condition: (s) => Array.isArray(s.env?.clouds) && s.env.clouds.length > 1
    },
    {
      id: 'ci-cd',
      description: 'CI/CD pipelines in use',
      score: 8,
      severity: 'low',
      category: 'devops',
      condition: (s) => !!s.env?.ciCd
    },
    {
      id: 'pentest-regular',
      description: 'Regular penetration testing',
      score: 9,
      severity: 'medium',
      category: 'assurance',
      condition: (s) => s.constraints?.pentest === 'Yes' || (s.constraints?.pentestFrequency || 0) > 0
    },
    {
      id: 'compliance-pci',
      description: 'PCI scope / requirement',
      score: 16,
      severity: 'high',
      category: 'compliance',
      condition: (s) => (s.org?.industry || '').toLowerCase?.().includes('finance') || s.org?.pci === 'Yes'
    },
    {
      id: 'compliance-soc2',
      description: 'SOC 2 / audit programs active',
      score: 14,
      severity: 'high',
      category: 'compliance',
      condition: (s) => s.org?.soc2 === 'Yes' || s.org?.grc === 'SOC2'
    },
    {
      id: 'backup-tested',
      description: 'Backups configured and tested',
      score: 7,
      severity: 'medium',
      category: 'resilience',
      condition: (s) => s.env?.backups === 'Yes' && s.env?.backupTested === 'Yes'
    }
  ];
