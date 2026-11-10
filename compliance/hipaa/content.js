/* HIPAA compliance page: the data the shared compliance kit (assets/compliance/v1/fw.js) renders. The page copy is in
   index.html; the walkthrough's screens and steps are in screens.js. Edit the readiness check here. */
window.FW_CHECK = {
  key: 'aivric.hipaa.readiness',     // answers stay in this browser (localStorage), nothing is sent
  // [id, item, what "ready" means, citation, key item (the ones OCR starts with)]
  items: [
    ['ra', 'Enterprise-wide risk analysis', 'Every system holding ePHI, dated within the last year.', '164.308(a)(1)(ii)(A) · OCR’s most-cited', 1],
    ['rm', 'Risk management plan', 'Each risk from the analysis has an owner, a fix and a date.', '164.308(a)(1)(ii)(B)', 1],
    ['baa', 'Business associate agreements', 'A signed BAA for every vendor that touches PHI.', '164.308(b)(1)', 0],
    ['trn', 'Workforce security training', 'Everyone trained, with records you can produce.', '164.308(a)(5)', 0],
    ['acc', 'Unique user IDs and access control', 'No shared accounts; access granted and removed on a process.', '164.312(a)', 0],
    ['aud', 'Audit logs, reviewed', 'Activity on ePHI systems is logged and someone looks.', '164.312(b)', 0],
    ['enc', 'Encryption, or a documented reason why not', 'At rest and in transit, decided and written down.', '164.312(a)(2)(iv) · (e)(2)(ii)', 0],
    ['bkp', 'Backups you’ve test-restored', 'A contingency plan with a restore test on record.', '164.308(a)(7)', 0],
    ['inc', 'Security incident procedures', 'Declare, respond and document every incident.', '164.308(a)(6)', 0],
    ['brn', 'Breach notification workflow', 'Assess, decide and notify within 60 days.', '164.404–164.410', 0],
    ['doc', 'Policies retained six years', 'Current policies and prior versions you can produce.', '164.316(b)(2)', 0],
    ['eva', 'Periodic evaluation', 'A review when things change, at least annually in practice.', '164.308(a)(8)', 0],
  ],
  // what the meter says: none ticked; a key item missing; all ticked; otherwise ({left} is how many remain)
  messages: {
    none: 'Start with the risk analysis. It’s the finding OCR cites most.',
    keyMissing: 'The risk analysis and risk management plan come first. They’re behind most OCR settlements.',
    all: 'All twelve. Make sure each one is dated and current; that’s what OCR checks.',
    some: '{left} to go. Your risk analysis and plan are in place, which is where OCR starts.',
  },
};
