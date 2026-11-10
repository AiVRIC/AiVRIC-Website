/* CMMC page: the data the shared compliance kit (assets/compliance/v1/fw.js) renders. The page copy is in index.html;
   the walkthrough's screens and steps are in screens.js. */
window.FW_CHECK = {
  key: 'aivric.cmmc.l2.check',     // answers stay in this browser (localStorage), nothing is sent
  // the 14 NIST SP 800-171 Rev 2 families and their requirement counts (110 in all), each weighted by its count:
  // [id, family, what it covers, family code and count, key, weight]
  items: [
    ['AC', 'Access Control', 'Who can reach CUI, from where, and with what privileges.', 'AC · 22 practices', 1, 22],
    ['AT', 'Awareness & Training', 'People know the risks and their security duties.', 'AT · 3 practices', 0, 3],
    ['AU', 'Audit & Accountability', 'Events are logged, protected and reviewed.', 'AU · 9 practices', 0, 9],
    ['CM', 'Configuration Management', 'Baselines, change control and least functionality.', 'CM · 9 practices', 0, 9],
    ['IA', 'Identification & Authentication', 'Unique IDs, MFA, and password rules.', 'IA · 11 practices', 0, 11],
    ['IR', 'Incident Response', 'Handle, track, report and test incidents.', 'IR · 3 practices', 0, 3],
    ['MA', 'Maintenance', 'Controlled, supervised system maintenance.', 'MA · 6 practices', 0, 6],
    ['MP', 'Media Protection', 'CUI on media is marked, protected and sanitized.', 'MP · 9 practices', 0, 9],
    ['PS', 'Personnel Security', 'Screening, and access removed at separation.', 'PS · 2 practices', 0, 2],
    ['PE', 'Physical Protection', 'Facilities, visitors and equipment are controlled.', 'PE · 6 practices', 0, 6],
    ['RA', 'Risk Assessment', 'Assess risk, scan for vulnerabilities, remediate.', 'RA · 3 practices', 0, 3],
    ['CA', 'Security Assessment', 'Assess controls, keep a POA&M, maintain the SSP.', 'CA · 4 practices', 0, 4],
    ['SC', 'System & Communications Protection', 'Boundaries, encryption and network separation.', 'SC · 16 practices', 0, 16],
    ['SI', 'System & Information Integrity', 'Flaws fixed, malware stopped, systems monitored.', 'SI · 7 practices', 0, 7],
  ],
  message(got, total) {
    if (got === total) return 'All 110 claimed. Now make sure every one has evidence an assessor can see.';
    if (got >= 88) return 'Close. The last families are where assessments stall; find them in Enterprise Vision first.';
    if (got > 0) return `${total - got} practices to go.`;
    return 'Start with Access Control. It’s 22 of the 110.';
  },
};
