// The Enterprise Vision app window the compliance pages' screens are rebuilt in: browser chrome, the sidebar as the
// product shows it (sections and items from the Enterprise Vision captures, 9 Nov 2026), the top bar and an empty
// content area each screen draws into. Light theme; styles in ui.css under .cvui. Needs lib.js (window.L).
(function () {
  const { h } = L;
  const NAV = [
    ['', [['Home', 'home']]],
    ['REPORT', [['ROAR', 'roar'], ['GROC', 'groc']]],
    ['ESTATE', [['Posture', 'posture'], ['Assets', 'assets'], ['Landscape', 'landscape'], ['Exposure', 'exposure']]],
    ['GOVERN', [['Registers', 'registers'], ['POA&M', 'poam'], ['Control Baseline', 'controls'], ['Decisions', 'decisions'], ['Third-Party Risk', 'tprm'], ['Threats', 'threats']]],
    ['RESPOND', [['Incident Response', 'incidents']]],
    ['TRUST', [['TrustSignals', 'trustsignals'], ['Audit Trail', 'audit']]],
  ];
  // the app's mark: a rounded tile with the A, beside "AiVRIC / Enterprise Vision"
  const brand = () => h('div', { class: 'brandrow' },
    h('span', { class: 'mark', style: 'display:grid;place-items:center;border-radius:9px;background:linear-gradient(135deg,#0ea5e9,#6366f1);color:#fff;font:800 15px var(--ui)' }, 'A'),
    h('span', { style: 'display:grid;line-height:1.15' },
      h('span', { style: 'font:700 9.5px var(--ui);letter-spacing:.14em;color:var(--mute)' }, 'AIVRIC'),
      h('span', { style: 'font:700 15px var(--ui)' }, 'Enterprise Vision')));

  function appWindow({ x, y, route, active, crumb = 'Whole organization' }) {
    const navEls = {};
    const side = h('div', { class: 'side' },
      brand(),
      h('div', { class: 'search' }, 'Search or jump…'),
      NAV.map(([head, items]) => [head ? h('div', { class: 'navh' }, head) : null,
        items.map(([label, id]) => (navEls[id] = h('div', { class: 'nav' + (id === active ? ' on' : '') }, h('i', { class: 'ic' }), label)))]));
    const content = h('div', { class: 'content' });
    const el = h('div', { class: 'win', style: `left:${x}px;top:${y}px` },
      h('div', { class: 'chrome' }, h('div', { class: 'dots' }, h('i'), h('i'), h('i')), h('div', { class: 'url' }, 'vision.your-domain.com/', h('b', {}, route))),
      h('div', { class: 'shell' }, side, h('div', { class: 'main' },
        h('div', { class: 'topbar' }, h('span', { class: 'crumb' }, h('b', {}, 'Big Venture Incorporated'), ' · ' + crumb), h('span', { style: 'flex:1' }), h('span', { class: 'pill' }, h('span', { class: 'dot' }), 'Demo data'), h('span', { class: 'pill' }, 'Big Venture Incorporated ▾')),
        content)));
    return { el, content, navEls, x, y, w: 1600, h: 1000 };
  }

  window.UI = { appWindow };
})();
