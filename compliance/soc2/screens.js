// The SOC 2 page's walkthrough: seven words on the shared Enterprise Vision screens (assets/compliance/v1/ui/screens.js:
// UI.groc, UI.poam and UI2.*).
// The seven words (assets/compliance/v1/fw.js): each a screen in its finished state (rest, which also shows anything
// the film starts hidden) with a short entrance (play); region = the part of the 1600 x 1000 window the view frames,
// kept at the view's 16:10 so it shows exactly that.
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const anim = (el, kf, o) => (reduce || !el || !el.animate) ? null : el.animate(kf, Object.assign({ duration: 800, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' }, o));
  const FULL = [236, 98, 1364, 852];
  window.FW_STEPS = [
    { w: 'Criteria', def: 'Your SOC 2 pass rate, live from every scan, beside every other framework you answer to.', chip: 'GROC · compliance snapshot', make: () => UI.groc(0, 0), region: [900, 260, 688, 430],
      rest(r) { (r.fw || []).forEach((f) => { if (f.bar) f.bar.style.transform = 'none'; if (f.pct && f.p != null) f.pct.textContent = f.p + '%'; }); },
      play(r) { r.fw.forEach((f, i) => anim(f.bar, [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { delay: i * 80 })); } },
    { w: 'Control', def: 'Your baseline, cross-walked to SOC 2. Each control maps to the criterion it satisfies.', chip: 'SOC 2 · TSC 2017 · 11 of 12 mapped', make: () => UI2.controls(0, 0), region: FULL,
      rest(r) { r.xw.textContent = 'Crosswalk: SOC 2'; r.menu.style.display = 'none'; r.count.textContent = '11 shown'; r.rows.forEach((x) => { if (!x.mapped) x.row.style.display = 'none'; }); r.rows[10].row.style.top = (180 + 9 * 33) + 'px'; r.rows[11].row.style.top = (180 + 10 * 33) + 'px';
        r.banner.style.opacity = 1; r.refHead.style.opacity = 1; r.rows.forEach((x) => { x.refEl.style.opacity = x.mapped ? 1 : 0; }); },
      play(r) { r.rows.filter((x) => x.mapped).forEach((x, i) => anim(x.refEl, [{ opacity: 0, transform: 'scale(.6)' }, { opacity: 1, transform: 'none' }], { delay: 200 + i * 70, duration: 500 })); } },
    { w: 'Gap', def: 'Every failing check becomes an owned fix on a 90-day clock, tracked until it closes.', chip: 'POA&M · owners · 90-day SLA', make: () => UI.poam(0, 0), region: FULL,
      play(r) { r.rows.forEach((x, i) => { anim(x.row, [{ opacity: 0, transform: 'translateX(40px)' }, { opacity: 1, transform: 'none' }], { delay: i * 90, duration: 600 }); anim(x.bar, [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }], { delay: 250 + i * 90 }); }); } },
    { w: 'Exception', def: 'Risks carried on purpose: approved, with compensating controls and an expiry date, written back to CloudSignals.', chip: 'Decisions · expires Oct 19, 2026', make: () => UI2.exceptions(0, 0), region: FULL,
      rest(r) { r.comment.textContent = 'Approved while partner OAuth onboarding completes.'; r.caret.style.display = 'none'; }, play(r) { anim(r.modal, [{ opacity: 0, transform: 'translateY(14px) scale(.97)' }, { opacity: 1, transform: 'none' }], { duration: 500 }); } },
    { w: 'Incident', def: 'Declare in one click. Triage, contain, recover, close — every step on an append-only timeline.', chip: 'INC-2026-002 · closed · CC7.3–7.5', make: () => UI2.incidents(0, 0), region: FULL,
      rest(r) { r.modal.style.display = 'none'; r.chips.forEach((c) => { c.className = 'tag low'; }); r.newPhase.textContent = 'CLOSED'; r.newPhase.className = 'tag low'; r.oldRow.style.transform = 'none';
        r.newRow.style.opacity = 1; r.k[3].nEl.textContent = '2'; r.tl.forEach((e) => { e.style.opacity = 1; }); },
      play(r) { r.tl.forEach((e, i) => anim(e, [{ opacity: 0, transform: 'translateX(-20px)' }, { opacity: 1, transform: 'none' }], { delay: 150 + i * 120, duration: 450 })); } },
    { w: 'Evidence', def: 'Every action hash-chained at the database. Verify integrity re-computes the chain on demand.', chip: 'Chain intact · 16 events verified', make: () => UI2.audit(0, 0), region: FULL,
      rest(r) { r.chip.style.opacity = 1; r.rows.forEach((x) => { x.ok.style.opacity = 1; }); },
      play(r) { r.rows.forEach((x, i) => anim(x.ok, [{ opacity: 0 }, { opacity: 1 }], { delay: 150 + i * 70, duration: 300 })); anim(r.chip, [{ opacity: 0, transform: 'scale(.8)' }, { opacity: 1, transform: 'none' }], { delay: 900, duration: 400 }); } },
    { w: 'Report', def: 'Your SOC 2 report in your trust center — gated, by request. Customers get proof, never raw findings.', chip: 'TrustSignals · assurance 31 / 100', make: () => UI2.trust(0, 0), region: FULL,
      rest(r) { r.empty.style.display = 'none'; r.titleF.firstChild.textContent = ''; r.caret.style.display = 'none'; r.libN.textContent = '1'; r.conf.textContent = '31'; r.confBar.style.width = '31%'; r.pubN.textContent = '1 (0 public · 1 by request)'; r.item.style.opacity = 1; },
      play(r) { anim(r.item, [{ opacity: 0, transform: 'translateY(-10px)' }, { opacity: 1, transform: 'none' }], { duration: 500 }); anim(r.confBar, [{ width: '25%' }, { width: '31%' }], { delay: 300, duration: 900 }); } },
  ];
})();
