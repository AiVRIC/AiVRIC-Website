/* Client Vision for Providers — content for the shared Vision edition kit (assets/cv-hero/v1/cvh.js).
   Edit copy here; never in the engine. Media paths are relative to this page. */
window.CVH_CONTENT = {
  media: '../assets/cv-hero/v1/media/',
  RAIL: [
    { t: 'Nothing hides.',
      d: 'Track monitored threat intelligence and actively exploited issues against the workspace, then triage what deserves attention.',
      clip: 'threats', img: 'screen-threats.jpg', cap: 'Client Vision · Threat Landscape' },
    { t: 'Walk into the board meeting with the same numbers.',
      d: 'From the risk landscape to the remediation roadmap, every page of the report comes from the same place the work does — so the numbers never change between rooms.',
      clip: 'roar', img: 'screen-roar.jpg', cap: 'Client Vision · ROAR report' },
    { t: 'Every gap has a name on it.',
      d: 'And a clock running. Nothing sits in a spreadsheet waiting for someone to remember it.',
      clip: 'poam', img: 'screen-poam.jpg', cap: 'Client Vision · Plan of Action & Milestones' },
    { t: 'Answer any framework in minutes.',
      d: 'ISO 42001, ISO 27001, NIST — whatever your biggest customer asks for next. The work is already mapped to all of them.',
      clip: 'groc', img: 'screen-groc.jpg', cap: 'Client Vision · GROC, compliance snapshot' },
    { t: 'Decisions you can defend later.',
      d: 'Leadership sets how much risk is acceptable. Anything above that line has to be justified in writing — and it stays on the record.',
      clip: 'decisions', img: 'screen-decisions.jpg', cap: 'Client Vision · Decisions' }
  ],
  STANDARDS: ['ISO/IEC 42001', 'ISO/IEC 27001', 'SOC 2', 'NIST CSF', 'NIST AI RMF', 'EU AI Act',
    'NIST SP 800-53', 'NIST SP 800-171', 'CIS Controls', 'HIPAA', 'PCI DSS', 'GDPR', 'CMMC',
    'FedRAMP'],
  SPINE: [
    { img: 'spine-1.jpg', cap: 'Client Vision · Asset inventory and Tech Landscape', t: 'Estate: every asset, every cloud.',
      d: 'Services, regions and resource types across each client’s scanned estate, and the estate as a map: every cloud and account with its pass rate and open findings.' },
    { img: 'spine-2.jpg', cap: 'Client Vision · Threat landscape, the proximity radar', t: 'Estate: every threat.',
      d: 'External threat intelligence, triaged for each client: the top potential threats ranked by severity and blast radius against that client’s own inventory.' },
    { img: 'spine-3.jpg', cap: 'Client Vision · Risk register and Decisions', t: 'Govern: every risk and decision.',
      d: 'Likelihood × impact on one scale for every client, against the risk appetite they declared, with each decision recorded where the auditor will look.' },
    { img: 'spine-4.jpg', cap: 'Client Vision · a control, crosswalked to every framework', t: 'Govern: mapped to the frameworks that matter.',
      d: 'Map a control once and answer SOC 2, ISO 27001, HIPAA, CMMC, NIST, PCI DSS or GDPR, whatever each client’s customers or regulators ask for next. Nobody starts over.' },
    { img: 'spine-5.jpg', cap: 'Client Vision · Incident Response', t: 'Respond: every incident, step by step, on the record.',
      d: 'Declared, triage, containment, eradication, recovery: every action lands on an append-only timeline, with the response call-tree in one place.' },
    { img: 'spine-6.jpg', cap: 'Client Vision · Delivery', t: 'Operate: every project, milestone and hour, live.',
      d: 'Each client’s engagement, live from the delivery workspace: project health, milestones late-first, throughput and hours, in the client’s own view.' },
    { img: 'spine-7.jpg', cap: 'Client Vision · the Provider Console, under a partner brand', t: 'Every client in one place you can see.',
      d: 'Your console: every client’s health, open work and progress side by side, who needs you first, and one click into any of them.' }
  ],
  ACC_START: {
    items: [
      { t: '1. A partner call.', d: 'Bring two or three clients. We’ll show you Client Vision running their programs side by side, and walk you through buying direct or joining the Service Delivery Partner Program.', img: 'partner/partner-1.jpg' },
      { t: '2. Your brand goes on.', d: 'Your logos, favicon and palettes in the branding studio, your domain and your sign-in page. A dedicated onboarding session, a sandbox for client demos, and your partner portal.', img: 'partner/partner-2.jpg' },
      { t: '3. Your first clients, in their own workspaces.', d: 'Each client sealed in its own workspace on your console. Connect a client’s cloud with read-only connectors and their first posture lands the same week.', img: 'partner/partner-3.jpg' },
      { t: '4. Your first business review.', d: 'A frozen, print-ready board report with your name on the cover, and a trust page to share when it counts.', img: 'partner/partner-4.jpg' }
    ]
  },
  ACC_MOM: {
    items: [
      { t: 'A client’s customer sends a questionnaire.', d: 'Answered from what is already mapped in that client’s workspace, and shared from a trust page under your name.', img: 'moments/moment-1.jpg' },
      { t: 'The board wants a report, not a spreadsheet.', d: 'A frozen ROAR snapshot, prepared by you: posture, findings, risks and the roadmap, ready to print.', img: 'moments/moment-2.jpg' },
      { t: 'Something goes wrong at 2 a.m. at one client.', d: 'The incident is declared in one click, the call-tree is in place, and every step records itself on the timeline.', img: 'moments/moment-3.jpg' }
    ]
  }
};
