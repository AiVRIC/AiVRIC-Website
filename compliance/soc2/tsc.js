/* The Trust Services Criteria wheel on /compliance/soc2/: five criteria around the ring; pick one to see what it covers,
   when it is included, and where Enterprise Vision proves it. */
(function () {
  'use strict';
  const wheel = document.getElementById('fw-wheel'), arc = document.getElementById('fw-wheel-arc');
  if (!wheel || !arc) return;
  // [name, colour, when it is included, what it covers, where Enterprise Vision proves it]
  const TSC = [
    ['Security', '#00b8ff', 'Required in every SOC 2 report', 'Protection against unauthorized access, disclosure and damage — the common criteria (CC1 to CC9) every report covers.', 'In Enterprise Vision: controls cross-walked to CC6 (access) and CC7 (operations), with MFA, access reviews and remediation on the record.'],
    ['Availability', '#17a34a', 'Included when uptime is part of your commitment', 'Systems are available for operation and use as committed or agreed.', 'In Enterprise Vision: backup and restoration control BCD-01 mapped to A1.2, with recovery posture derived from the live estate.'],
    ['Processing Integrity', '#ec835a', 'Included when you process transactions for customers', 'Processing is complete, valid, accurate, timely and authorized.', 'In Enterprise Vision: change and remediation records on the POA&M, with owners and deadlines for every failing check.'],
    ['Confidentiality', '#7b2cbf', 'Included when you handle confidential data', 'Information designated as confidential is protected as committed or agreed.', 'In Enterprise Vision: encryption-in-transit control NET-02 mapped to CC6.7, with exceptions carried knowingly and set to expire.'],
    ['Privacy', '#0077b6', 'Included when you collect personal information', 'Personal information is collected, used, retained and disclosed in line with your commitments.', 'In Enterprise Vision: privacy controls in the same baseline, cross-walked to privacy frameworks such as GDPR alongside SOC 2.'],
  ];
  const C = 1068;   // the ring's circumference (r = 170)
  const btns = TSC.map(([n, c], i) => {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = n; b.style.setProperty('--c', c);
    const a = (-90 + i * 72) * Math.PI / 180;
    b.style.left = (50 + Math.cos(a) * 37) + '%'; b.style.top = (50 + Math.sin(a) * 37) + '%';
    b.setAttribute('aria-pressed', 'false');
    wheel.append(b);
    return b;
  });
  const pick = (i) => {
    btns.forEach((b, j) => b.setAttribute('aria-pressed', String(j === i)));
    const [n, , req, d, cv] = TSC[i];
    document.getElementById('fw-tsc-name').textContent = n;
    document.getElementById('fw-tsc-req').textContent = req;
    document.getElementById('fw-tsc-desc').textContent = d;
    document.getElementById('fw-tsc-cv').textContent = cv;
    arc.setAttribute('stroke-dashoffset', String(C * (1 - (i + 1) / 5)));
  };
  btns.forEach((b, i) => b.addEventListener('click', () => pick(i)));
  pick(0);
})();
