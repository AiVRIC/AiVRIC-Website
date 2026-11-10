// The compliance hub's walkthrough: the eight words, each on one of the shared Enterprise Vision screens
// (assets/compliance/v1/ui/screens.js).
// The eight words (assets/compliance/v1/fw.js): each a screen in its finished state (rest) with a short entrance
// (play); where = the part of the app it lives in; region = the part of the 1600 x 1000 window the view frames, kept at the view’s 16:10 so it shows exactly that.
(function () {
  const { clamp } = L;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const anim = (el, kf, o) => (reduce || !el || !el.animate) ? null : el.animate(kf, Object.assign({ duration: 900, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' }, o));
  const count = (el, to, suf = '', dur = 1100, dec = 0) => {
    if (reduce) { el.textContent = to.toLocaleString('en-US') + suf; return; }
    const t0 = performance.now();
    const step = (now) => { const p = clamp((now - t0) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = (to * e).toLocaleString('en-US', { maximumFractionDigits: dec }) + suf; if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  const setArc = (arc, c, p) => arc.setAttribute('stroke-dashoffset', String(c * (1 - p)));
  window.FW_STEPS = [
    { w: 'See', where: 'Portal', def: 'One view of every cloud account, resource and finding, refreshed with every scan.', chip: '642 resources · AWS + Azure',
      make: () => UI.portal(0, 0), region: [236, 98, 1364, 852],
      rest(r) { setArc(r.heroRing.arc, r.heroRing.c, .71); r.post.textContent = '71'; },
      play(r) { r.sev.forEach((b, i) => anim(b, [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { delay: 150 + i * 120 })); count(r.res, 642); } },
    { w: 'Score', where: 'ROAR · Executive summary', def: 'A severity-weighted pass ratio across every check, graded out of 100. One formula, every view.', chip: '71 / 100 · grade B− · 2,835 checks',
      make: () => UI.roar(0, 0), region: [494, 98, 1106, 691],
      rest(r) { setArc(r.gArc, r.gC, .71); r.tLine.setAttribute('stroke-dashoffset', '0'); r.pucks.forEach((p) => p.style.transform = 'scale(1)'); },
      play(r) { anim(r.gArc, [{ strokeDashoffset: r.gC }, { strokeDashoffset: r.gC * .29 }], { duration: 1300 }); count(r.gNum, 71, '', 1300); anim(r.tLine, [{ strokeDashoffset: 400 }, { strokeDashoffset: 0 }], { duration: 1400, delay: 300 }); } },
    { w: 'Remediate', where: 'POA&M', def: 'Every gap becomes an owned action, ranked and tracked to closure. Nothing ages quietly past 90 days.', chip: 'POAM.2026.007 · 95 days open',
      make: () => UI.poam(0, 0), region: [236, 98, 1364, 852],
      play(r) { r.rows.forEach((x, i) => { anim(x.row, [{ opacity: 0, transform: 'translateX(40px)' }, { opacity: 1, transform: 'none' }], { delay: i * 90, duration: 600 }); anim(x.bar, [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { delay: 250 + i * 90 }); }); } },
    { w: 'Report', where: 'ROAR', def: 'Every scan becomes an executive summary: top risks scored likelihood × impact, opportunities and a roadmap.', chip: 'Top risk · L4 × I5 = 20',
      make: () => UI.roar(0, 0), region: [236, 98, 1364, 852],
      rest(r) { setArc(r.gArc, r.gC, .71); r.tLine.setAttribute('stroke-dashoffset', '0'); r.pucks.forEach((p) => p.style.transform = 'scale(1)'); },
      play(r) { r.risks.forEach((x, i) => anim(x, [{ opacity: .2 }, { opacity: 1 }], { delay: i * 110, duration: 500 })); r.pucks.forEach((p, i) => anim(p, [{ transform: 'scale(0)' }, { transform: 'scale(1)' }], { delay: 300 + i * 130, duration: 500, easing: 'cubic-bezier(.3,1.6,.5,1)' })); } },
    { w: 'Govern', where: 'GROC', def: 'Governance, risk, operations and compliance in one ISMS-level report, derived from the same governed stores.', chip: '12 controls · 70% implemented',
      make: () => UI.groc(0, 0), region: [236, 98, 1364, 852],
      play(r) { r.q.forEach((c, i) => anim(c, [{ opacity: 0, transform: 'translateY(24px)' }, { opacity: 1, transform: 'none' }], { delay: i * 120, duration: 600 })); r.fw.forEach((f, i) => anim(f.bar, [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { delay: 300 + i * 90 })); } },
    { w: 'Expose', where: 'Threats', def: 'Threat intelligence from CISA and the security press, triaged against what you actually run.', chip: '31 actively exploited · CISA KEV',
      make: () => UI.threats(0, 0), region: [236, 98, 1364, 852],
      rest(r) { r.sweep.style.transformOrigin = r.rc[0] + 'px ' + r.rc[1] + 'px'; r.sweep.style.transformBox = 'view-box'; },
      play(r) { if (!reduce) { r.sweepAnim = r.sweepAnim || r.sweep.animate([{ transform: 'rotate(0deg)' }, { transform: 'rotate(360deg)' }], { duration: 4200, iterations: Infinity }); } r.items.forEach((x, i) => anim(x, [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }], { delay: i * 110, duration: 500 })); } },
    { w: 'Decide', where: 'Decisions · Audit Trail', def: 'Treatments and exceptions wait for your call, and every decision lands in an append-only audit trail.', chip: 'Written back to CloudSignals',
      make: () => UI.decisions(0, 0), region: [236, 98, 1364, 852],
      rest(r) { r.opts[0].style.background = '#e6f6fd'; },
      play(r) { anim(r.pop, [{ opacity: 0, transform: 'translateY(12px) scale(.97)' }, { opacity: 1, transform: 'none' }], { delay: 200, duration: 450 }); r.events.forEach((e, i) => anim(e, [{ opacity: 0, transform: 'translateY(-14px)' }, { opacity: 1, transform: 'none' }], { delay: 500 + i * 120, duration: 500 })); } },
    { w: 'Trust', where: 'TrustSignals', def: 'Publish a living trust page for your customers: bands and coverage from an approved snapshot, never raw findings.', chip: 'SOC 2 · ISO 27001 · by request',
      make: () => UI.trust(0, 0), region: [236, 98, 1364, 852],
      rest(r) { r.checks.forEach((c) => { c.dot.style.background = '#17a34a'; c.dot.style.borderColor = '#17a34a'; c.st.textContent = 'done'; c.st.className = 'tag low'; }); },
      play(r) { r.bands.forEach((b, i) => anim(b, [{ opacity: 0, transform: 'translateX(24px)' }, { opacity: 1, transform: 'none' }], { delay: 150 + i * 110, duration: 550 })); } },
  ];
})();
