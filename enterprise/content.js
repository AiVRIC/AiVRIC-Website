/* AiVRIC Enterprise Vision (v0; stills, player clips and the hero flight are Enterprise Vision from 9 Nov 2026; the film is still a stand-in) — content for the shared Vision edition kit (assets/cv-hero/v1/cvh.js).
   Edit copy here; never in the engine. Media paths are relative to this page. */
window.CVH_CONTENT = {
  media: '../assets/cv-hero/v1/media-enterprise/',
  RAIL: [
    { t: 'Nothing hides.',
      d: 'Monitored threat intelligence and actively exploited issues, triaged against your own inventory, so the team works what deserves attention first.',
      clip: 'threats', img: 'screen-threats.jpg', cap: 'Enterprise Vision · Threat Landscape' },
    { t: 'Walk into the board meeting with the same numbers.',
      d: 'Every page of the report comes from the same place the work does, so the numbers never change between the ops review and the boardroom.',
      clip: 'roar', img: 'screen-roar.jpg', cap: 'Enterprise Vision · ROAR report' },
    { t: 'Every gap has a name on it.',
      d: 'And a clock running. Nothing sits in a spreadsheet waiting for someone to remember it.',
      clip: 'poam', img: 'screen-poam.jpg', cap: 'Enterprise Vision · Plan of Action & Milestones' },
    { t: 'Answer any framework in minutes.',
      d: 'ISO 42001, ISO 27001, NIST, SOC 2 — whatever your biggest customer or your regulator asks for next. The work is already mapped to all of them.',
      clip: 'groc', img: 'screen-groc.jpg', cap: 'Enterprise Vision · Control Baseline, each control crosswalked' },
    { t: 'Decisions you can defend later.',
      d: 'Leadership sets how much risk is acceptable. Anything above that line is justified in writing — and it stays on the record.',
      clip: 'decisions', img: 'screen-decisions.jpg', cap: 'Enterprise Vision · Decisions' }
  ],
  STANDARDS: ['ISO/IEC 42001', 'ISO/IEC 27001', 'SOC 2', 'NIST CSF', 'NIST AI RMF', 'EU AI Act',
    'NIST SP 800-53', 'NIST SP 800-171', 'CIS Controls', 'HIPAA', 'PCI DSS', 'GDPR', 'CMMC',
    'FedRAMP'],
  SPINE: [
    { img: 'spine-1.jpg', cap: 'Enterprise Vision · Asset inventory', t: 'Estate: every asset, every cloud.',
      d: 'Services, regions and resource types across your scanned estate, and the estate as a map: every cloud and account with its pass rate and open findings.' },
    { img: 'spine-2.jpg', cap: 'Enterprise Vision · Threat landscape, the proximity radar', t: 'Estate: every threat.',
      d: 'External threat intelligence, triaged for you: the top potential threats ranked by severity and blast radius against your own inventory.' },
    { img: 'spine-3.jpg', cap: 'Enterprise Vision · Risk register', t: 'Govern: every risk and decision.',
      d: 'Likelihood × impact on one scale, against the risk appetite leadership declared, with each decision recorded where the auditor will look.' },
    { img: 'spine-4.jpg', cap: 'Enterprise Vision · a control, crosswalked to every framework', t: 'Govern: mapped to the frameworks that matter.',
      d: 'Map a control once and answer SOC 2, ISO 27001, HIPAA, CMMC, NIST, PCI DSS or GDPR, whatever your customers or regulators ask for next. Nobody starts over.' },
    { img: 'spine-5.jpg', cap: 'Enterprise Vision · Incident Response', t: 'Respond: every incident, step by step, on the record.',
      d: 'Declared, triage, containment, eradication, recovery: every action lands on an append-only timeline, with the response call-tree in one place.' },
    { img: 'spine-6.jpg', cap: 'Enterprise Vision · Third-Party Risk', t: 'Govern: every vendor, graded and watched.',
      d: 'Each vendor scored against the loss it could cause, the weakest first, with what has moved since the last review.' },
    { img: 'spine-7.jpg', cap: 'Enterprise Vision · the Portal, the executive view', t: 'The whole program in one place you can see.',
      d: 'Posture, open findings, decisions waiting and the roadmap, side by side, and one click into any of them.' }
  ],
  ACC_START: {
    items: [
      { t: '1. Start free with CloudSignals.', d: 'Connect a cloud with read-only connectors and your first posture lands the same week. No card, no call.', img: 'partner/start-1.jpg' },
      { t: '2. Your program takes shape.', d: 'Leadership sets the risk appetite, the control baseline goes in once, and the frameworks you answer to are crosswalked to it.', img: 'partner/start-2.jpg' },
      { t: '3. The work gets names and clocks.', d: 'Findings become a Plan of Action & Milestones with owners and dates; nothing waits in a spreadsheet.', img: 'partner/start-3.jpg' },
      { t: '4. Your first business review.', d: 'A frozen, print-ready ROAR with your name on the cover, and a trust page to share when a customer asks.', img: 'partner/start-4.jpg' }
    ]
  },
  ACC_MOM: {
    items: [
      { t: 'A customer sends a questionnaire.', d: 'Answered from what is already mapped in your workspace, and shared from a trust page under your own name.', img: 'moments/moment-1.jpg' },
      { t: 'The board wants a report, not a spreadsheet.', d: 'A frozen ROAR snapshot: posture, findings, risks and the roadmap, ready to print.', img: 'moments/moment-2.jpg' },
      { t: 'Something goes wrong at 2 a.m.', d: 'The incident is declared in one click, the call-tree is in place, and every step records itself on the timeline.', img: 'moments/moment-3.jpg' },
      { t: 'The auditor asks for evidence.', d: 'Every control, decision and action is already on the record, on an append-only audit trail.', img: 'moments/moment-4.jpg' }
    ]
  }
};
