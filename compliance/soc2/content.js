/* SOC 2 page: the data the shared compliance kit (assets/compliance/v1/fw.js) renders. The page copy is in index.html;
   the walkthrough's screens and steps are in screens.js; the Trust Services Criteria wheel is tsc.js. */
window.FW_CHECK = {
  key: 'aivric.soc2.checklist',     // answers stay in this browser (localStorage), nothing is sent
  percent: true,
  // [heading, [[id, item, what it means, where it lives], …]]
  groups: [
    ['Scope', [
      ['c0-0', 'Define what’s in scope', 'Systems, data, locations and third parties that touch customer data.', 'Scope'],
      ['c0-1', 'Pick your criteria', 'Security is required; add availability, processing integrity, confidentiality or privacy as they apply.', 'Trust Services Criteria'],
      ['c0-2', 'Choose Type I or Type II', 'Design at a point in time, or operation across an observation period.', 'Report type'],
    ]],
    ['Controls', [
      ['c1-0', 'Map controls to the criteria', 'Cross-walk your control baseline to SOC 2 (TSC 2017).', 'Control Baseline'],
      ['c1-1', 'Run a gap assessment', 'Find every control that is missing, partial or failing.', 'ROAR · GROC'],
      ['c1-2', 'Give every gap an owner and a date', 'Track remediation to closure, not to a spreadsheet.', 'POA&M'],
    ]],
    ['Operations', [
      ['c2-0', 'Enforce MFA and review access', 'Privileged access first, then quarterly recertification.', 'CC6.1 · CC6.2 · CC6.6'],
      ['c2-1', 'Test your incident response plan', 'Declare, work and close incidents on a timeline you can show an auditor.', 'CC7.3 – CC7.5'],
      ['c2-2', 'Document exceptions', 'Approve risks you carry, with compensating controls and an expiry.', 'Decisions'],
    ]],
    ['Evidence & report', [
      ['c3-0', 'Keep an audit trail you can verify', 'Append-only, tamper-evident, exportable.', 'Audit Trail'],
      ['c3-1', 'Collect evidence continuously', 'Through the whole Type II observation period, not the week before.', 'CloudSignals'],
      ['c3-2', 'Engage an independent CPA firm', 'Only a licensed CPA firm can issue the SOC 2 report.', 'Auditor'],
      ['c3-3', 'Share the report by request', 'List it gated in your trust center; never expose raw findings.', 'TrustSignals'],
    ]],
  ],
  message(got, total, pct) {
    if (pct === 100) return 'Every box ticked. Time to engage your CPA firm, with the evidence already on the record.';
    if (pct >= 60) return 'You’re close. Find the last gaps in Enterprise Vision before your auditor does.';
    if (pct > 0) return `${total - got} items to go. Most teams stall on evidence, not controls.`;
    return 'Start with scope. Everything else builds on it.';
  },
};
