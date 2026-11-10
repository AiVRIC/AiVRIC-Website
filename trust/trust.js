/* The Trust Center (/trust/): the six disciplines wheel, where your data lives (one map per deployment model, with the
   subprocessors that apply), the request basket and Trust Intake, which writes the request out in the visitor's own
   email app. Nothing is sent from the page. The basket (item names only, never the form) is kept in this browser. */
(function () {
  'use strict';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var P = document.documentElement.getAttribute('data-root') || '../';

  /* ---- the six disciplines --------------------------------------------------------------------------------- */
  var DISC = [
    { k: 'Identity & Access', l1: 'Identity', l2: '& Access', d: 'Strong authentication, least privilege, and lifecycle control for privileged and standard access.',
      t: ['Role-based access control and separation of duties', 'SSO / SAML, with optional SCIM provisioning on enterprise plans', 'MFA enforced for privileged access'],
      docs: [['access-control.html', 'Access Control']] },
    { k: 'Data Protection', l1: 'Data', l2: 'Protection', d: 'Control of customer data is built into the architecture, down to the database.',
      t: ['Encryption in transit (TLS), and at rest where applicable', 'Row-level security: each workspace sees only its own data, with no access by default', 'Read-only cloud connectors with scoped access'],
      docs: [['encryption-in-transit.html', 'Encryption in transit'], ['encryption-at-rest.html', 'Encryption at rest'], ['data-retention-policy.html', 'Data Retention']] },
    { k: 'Secure Engineering', l1: 'Secure', l2: 'Engineering', d: 'Security is built into the software lifecycle through review gates and operational assurance.',
      t: ['Secure SDLC, code review and dependency hygiene', 'Automated scanning and vulnerability management workflows', 'Change management and release controls'],
      docs: [['platform-security-overview.html', 'Platform Security Overview']] },
    { k: 'Monitoring & Detection', l1: 'Monitoring', l2: '& Detection', d: 'We watch operational health and security signals so we can respond, and recover.',
      t: ['Centralized logging and alerting for security-relevant events', 'Incident triage playbooks and escalation paths', 'AiVRIC events can feed your own SIEM'],
      docs: [['logging-monitoring.html', 'Logging & Monitoring']] },
    { k: 'Incident Response', l1: 'Incident', l2: 'Response', d: 'A response program built for containment, communication and learning.',
      t: ['A documented plan, with roles and severity handling', 'Post-incident reviews and corrective actions', 'Customer notification aligned to contractual and legal requirements'],
      docs: [['incident-response-playbook.html', 'Incident Response Playbook']] },
    { k: 'People & Governance', l1: 'People &', l2: 'Governance', d: 'Policy management, training and risk oversight, owned and reviewed.',
      t: ['Security awareness training and acceptable use standards', 'Vendor risk management and procurement controls', 'Risk assessments tied to product and operational changes'],
      docs: [['data-security.html', 'Security & Technology Policies']] }
  ];
  var wheel = document.getElementById('sx-wheel'), panel = document.getElementById('sx-disc-panel');
  if (wheel && panel) {
    var C = 270, R0 = 118, R1 = 252, gap = 0.035;
    var svg = el('svg', { viewBox: '0 0 540 540', role: 'tablist', 'aria-label': 'Security disciplines' }, wheel);
    var defs = el('defs', {}, svg), g1 = el('radialGradient', { id: 'sx-seg-on', cx: '50%', cy: '50%', r: '60%' }, defs);
    el('stop', { offset: '0%', 'stop-color': 'rgba(0,209,255,0.32)' }, g1); el('stop', { offset: '100%', 'stop-color': 'rgba(0,209,255,0.08)' }, g1);
    el('circle', { class: 'ring', cx: C, cy: C, r: 266 }, svg);
    var segs = DISC.map(function (d, i) {
      var a0 = -Math.PI / 2 + (i / 6) * 2 * Math.PI + gap, a1 = -Math.PI / 2 + ((i + 1) / 6) * 2 * Math.PI - gap;
      var p = function (r, a) { return (C + r * Math.cos(a)).toFixed(2) + ' ' + (C + r * Math.sin(a)).toFixed(2); };
      var g = el('g', { class: 'seg', role: 'tab', tabindex: i ? -1 : 0, 'aria-label': d.k, 'aria-controls': 'sx-disc-panel' }, svg);
      el('path', { class: 'arc', d: 'M' + p(R1, a0) + ' A' + R1 + ' ' + R1 + ' 0 0 1 ' + p(R1, a1) + ' L' + p(R0, a1) + ' A' + R0 + ' ' + R0 + ' 0 0 0 ' + p(R0, a0) + ' Z' }, g);
      var am = (a0 + a1) / 2, rm = (R0 + R1) / 2, tx = C + rm * Math.cos(am), ty = C + rm * Math.sin(am);
      var t = el('text', { x: tx, y: ty - 4, 'text-anchor': 'middle' }, g); t.textContent = d.l1;
      var t2 = el('text', { x: tx, y: ty + 14, 'text-anchor': 'middle' }, g); t2.textContent = d.l2;
      return g;
    });
    el('circle', { class: 'core', cx: C, cy: C, r: 100 }, svg);
    var sh = el('path', { d: 'M270 214 l38 14 v28 c0 26 -17 44 -38 52 c-21 -8 -38 -26 -38 -52 v-28 z', fill: 'none', stroke: '#7ce8ff', 'stroke-width': 1.6 }, svg);
    el('path', { d: 'M254 262 l11 11 l22 -24', fill: 'none', stroke: '#2ee59d', 'stroke-width': 2.4, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, svg);
    var ct = el('text', { x: C, y: 336, 'text-anchor': 'middle', fill: '#b6bfce', 'font-size': 12, 'font-weight': 600, 'letter-spacing': '2' }, svg); ct.textContent = 'DEFENSE IN DEPTH';
    sh.setAttribute('opacity', '0.95');
    var cur = -1, auto = null;
    function show(i, focus) {
      if (i === cur) return; cur = i;
      segs.forEach(function (g, k) { g.classList.toggle('on', k === i); g.setAttribute('aria-selected', String(k === i)); g.setAttribute('tabindex', k === i ? 0 : -1); });
      var d = DISC[i];
      panel.innerHTML = '<span class="sx-num">' + String(i + 1).padStart(2, '0') + ' / 06</span><h3>' + esc(d.k) + '</h3><p>' + esc(d.d) + '</p><ul class="sx-ticks">'
        + d.t.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul><div class="sx-actions" style="gap:18px">'
        + d.docs.map(function (x) { return '<a class="sx-link" href="' + P + x[0] + '">' + esc(x[1]) + ' <span aria-hidden="true">→</span></a>'; }).join('') + '</div>';
      panel.classList.remove('swap'); void panel.offsetWidth; panel.classList.add('swap');
      if (focus) segs[i].focus();
    }
    var touched = false;      // once someone picks a discipline, it stays where they put it
    function stopAuto() { touched = true; if (auto) { clearInterval(auto); auto = null; } }
    segs.forEach(function (g, i) {
      g.addEventListener('click', function () { stopAuto(); show(i); });
      g.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { stopAuto(); show(i); } });
      g.addEventListener('keydown', function (e) {
        var k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (k) { e.preventDefault(); stopAuto(); show((i + k + 6) % 6, true); }
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); stopAuto(); show(i); }
      });
    });
    show(0);
    if (!reduce && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        if (es[0].isIntersecting && !auto && !touched) auto = setInterval(function () { show((cur + 1) % 6); }, 4200);
        if (!es[0].isIntersecting && auto) { clearInterval(auto); auto = null; }
      }, { threshold: 0.4 }).observe(wheel);
    }
  }

  /* ---- where your data lives ------------------------------------------------------------------------------------ */
  var MODES = {
    hosted: {
      zones: { you: 'Your environment', aivric: 'AiVRIC · Google Cloud, US', hot: 'aivric' },
      at: { clouds: [85, 190], engine: [435, 135], data: [435, 270], support: [435, 270, 0], ai: [795, 200] },
      sub: { engine: 'The hosted service', data: 'Isolated by row-level security' },
      facts: [['Where it lives', 'On Google Cloud in the US. Your workspace sits in the platform\u2019s database, separated from every other workspace by row-level security, with no access by default.'],
        ['Who can touch it', 'Named users in your workspace, through single sign-on with MFA at your identity provider. Every change lands on an append-only, hash-chained audit trail.'],
        ['Your AI', 'AI features run on Anthropic, through AiVRIC\u2019s key or your workspace\u2019s own. Prompts aren\u2019t stored, and a person approves every draft.']]
    },
    dedicated: {
      zones: { you: 'Your environment', aivric: 'AiVRIC · Google Cloud, US', hot: 'aivric' },
      at: { clouds: [85, 190], engine: [435, 135], data: [435, 270], support: [435, 270, 0], ai: [795, 200] },
      sub: { engine: 'Your own namespace', data: 'Your own database' },
      facts: [['Where it lives', 'Still on Google Cloud in the US, in a namespace and a database of your own.'],
        ['Who can touch it', 'The same controls as the hosted service: named users, single sign-on with MFA, and the audit trail.'],
        ['When', 'On request, for teams whose security review asks for their own environment. Talk to us about self-hosted or air-gapped.']]
    },
    cv: {
      zones: { you: 'Your clients\u2019 environments', aivric: 'AiVRIC · Google Cloud, US', hot: 'aivric' },
      at: { clouds: [85, 190], engine: [435, 135], data: [435, 270], support: [435, 270, 0], ai: [795, 200] },
      sub: { engine: 'The provider console', data: 'A database per provider' },
      facts: [['Where it lives', 'Each provider gets its own database instance, and every client workspace inside it is sealed from the next.'],
        ['Who can touch it', 'Provider access is by authority, not membership: a band on every screen shows it, and the client\u2019s audit trail records it.'],
        ['Their connectors', 'Each client\u2019s connectors pull only what that client allows, and the keys are sealed on arrival.']]
    }
  };
  var map = document.getElementById('sx-map'), facts = document.getElementById('sx-facts'), modes = document.getElementById('sx-modes');
  if (map && facts && modes && window.SX) {
    var W = 230, H = 64;
    var m = el('svg', { viewBox: '0 0 1100 440', role: 'img', 'aria-label': 'Where your data lives for the selected deployment model' }, map);
    var Z = {
      you: el('rect', { class: 'zone', x: 20, y: 40, width: 350, height: 370, rx: 18 }, m),
      aivric: el('rect', { class: 'zone', x: 390, y: 40, width: 320, height: 370, rx: 18 }, m),
      ai: el('rect', { class: 'zone', x: 730, y: 40, width: 350, height: 370, rx: 18 }, m)
    };
    var ZL = { you: el('text', { class: 'zone-label', x: 44, y: 76 }, m), aivric: el('text', { class: 'zone-label', x: 414, y: 76 }, m), ai: el('text', { class: 'zone-label', x: 754, y: 76 }, m) };
    ZL.aivric.textContent = 'AiVRIC'; ZL.ai.textContent = 'AI provider';
    var wires = { a: el('path', { class: 'wire' }, m), b: el('path', { class: 'wire' }, m), c: el('path', { class: 'wire ai' }, m), d: el('path', { class: 'wire' }, m) };
    function node(key, title, sub, cls) {
      var g = el('g', { class: 'node' + (cls ? ' ' + cls : '') }, m);
      el('rect', { width: W, height: H, rx: 12 }, g);
      var t = el('text', { x: 18, y: 28 }, g); t.textContent = title;
      var s = el('text', { class: 'sub', x: 18, y: 47 }, g); s.textContent = sub;
      return { g: g, sub: s, x: 0, y: 0, o: 1 };
    }
    var N = {
      clouds: node('clouds', 'Your clouds & tools', 'AWS · Azure · GCP · OCI'),
      engine: node('engine', 'AiVRIC', ''),
      data: node('data', 'Workspace data', '', 'data'),
      support: node('support', 'Email & support', 'Contact info, support artifacts'),
      ai: node('ai', 'Anthropic', 'AiVRIC\u2019s key, or your own')
    };
    function curve(a, b) {
      var x1 = a.x + W, y1 = a.y + H / 2, x2 = b.x, y2 = b.y + H / 2;
      if (Math.abs(a.x - b.x) < 5) { x1 = a.x + W / 2; y1 = a.y + H; x2 = b.x + W / 2; y2 = b.y; return 'M' + x1 + ' ' + y1 + ' L' + x2 + ' ' + y2; }
      if (b.x < a.x) { x1 = a.x; x2 = b.x + W; }
      var mx = (x1 + x2) / 2; return 'M' + x1 + ' ' + y1 + ' C' + mx + ' ' + y1 + ' ' + mx + ' ' + y2 + ' ' + x2 + ' ' + y2;
    }
    function paint() {
      for (var k in N) { var n = N[k]; n.g.setAttribute('transform', 'translate(' + n.x.toFixed(1) + ' ' + n.y.toFixed(1) + ')'); n.g.style.opacity = n.o; }
      wires.a.setAttribute('d', curve(N.clouds, N.engine));
      wires.b.setAttribute('d', curve(N.engine, N.data));
      wires.c.setAttribute('d', curve(N.engine, N.ai));
      wires.d.setAttribute('d', curve(N.engine, N.support)); wires.d.style.opacity = N.support.o > 0.5 ? 0.5 : 0;
    }
    var anim = 0, first = true;
    function setMode(key) {
      var M = MODES[key]; if (!M) return;
      ZL.you.textContent = M.zones.you; ZL.aivric.textContent = M.zones.aivric;
      for (var z in Z) Z[z].classList.toggle('hot', z === M.zones.hot);
      N.engine.sub.textContent = M.sub.engine; N.data.sub.textContent = M.sub.data;
      var from = {}, to = {};
      for (var k in N) { from[k] = [N[k].x, N[k].y, N[k].o]; var t = M.at[k]; to[k] = [t[0], t[1], t[2] === undefined ? 1 : t[2]]; }
      cancelAnimationFrame(anim);
      var t0 = performance.now(), dur = first || reduce ? 0 : 850; first = false;
      (function step(now) {
        var u = dur ? Math.min(1, (now - t0) / dur) : 1, e = 1 - Math.pow(1 - u, 3);
        for (var k in N) { N[k].x = from[k][0] + (to[k][0] - from[k][0]) * e; N[k].y = from[k][1] + (to[k][1] - from[k][1]) * e; N[k].o = from[k][2] + (to[k][2] - from[k][2]) * e; }
        paint(); if (u < 1) anim = requestAnimationFrame(step);
      })(t0);
      facts.innerHTML = M.facts.map(function (f, i) { return '<div class="sx-fact swap" style="animation-delay:' + (i * 0.06) + 's"><b>' + esc(f[0]) + '</b><p>' + esc(f[1]) + '</p></div>'; }).join('');
      [].slice.call(document.querySelectorAll('#sx-subs tbody tr')).forEach(function (tr) {
        var on = (' ' + tr.getAttribute('data-models') + ' ').indexOf(' ' + key + ' ') !== -1;
        tr.classList.toggle('dim', !on); tr.classList.toggle('lit', on);
      });
    }
    SX.tabs(modes, setMode);
  }

  /* ---- the request basket, the tray and Trust Intake ------------------------------------------------------------------ */
  var KEY = 'aivric.trust.request';
  var store = {
    get: function () { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } },
    set: function (v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* private mode: the basket still works */ } }
  };
  var picked = store.get();
  var rows = [].slice.call(document.querySelectorAll('#sx-ledger .sx-row'));
  var basket = document.getElementById('sx-basket'), tray = document.getElementById('sx-tray'), trayN = document.getElementById('sx-tray-n');
  var emptyHTML = basket ? basket.innerHTML : '';
  var intakeIn = false;
  function sync(bump) {
    rows.forEach(function (r) {
      var on = picked.indexOf(r.getAttribute('data-item')) !== -1, b = r.querySelector('.sx-add');
      r.classList.toggle('picked', on); b.setAttribute('aria-pressed', String(on));
      if (!b.dataset.label) b.dataset.label = b.textContent.trim();
      b.lastChild.textContent = on ? 'Added' : b.dataset.label;
    });
    if (basket) {
      basket.innerHTML = picked.length ? picked.map(function (x, i) { return '<span class="sx-chip">' + esc(x) + '<button type="button" data-i="' + i + '" aria-label="Remove ' + esc(x) + '">×</button></span>'; }).join('') : emptyHTML;
    }
    if (tray) {
      trayN.textContent = picked.length;
      tray.classList.toggle('show', picked.length > 0 && !intakeIn);
      if (bump) { tray.classList.remove('bump'); void tray.offsetWidth; tray.classList.add('bump'); }
    }
    store.set(picked);
  }
  rows.forEach(function (r) {
    r.querySelector('.sx-add').addEventListener('click', function () {
      var item = r.getAttribute('data-item'), i = picked.indexOf(item);
      if (i === -1) picked.push(item); else picked.splice(i, 1);
      sync(i === -1);
    });
  });
  if (basket) basket.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-i]'); if (!b) return;
    picked.splice(+b.getAttribute('data-i'), 1); sync();
  });
  var intake = document.getElementById('contact');
  if (intake && 'IntersectionObserver' in window) new IntersectionObserver(function (es) { intakeIn = es[0].isIntersecting; sync(); }, { threshold: 0.15 }).observe(intake);
  sync();

  var form = document.getElementById('sx-intake-form'), msg = document.getElementById('sx-form-msg');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { return (form.elements[n].value || '').trim(); };
    var missing = [];
    if (!v('name')) missing.push(form.elements.name);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) missing.push(form.elements.email);
    if (!v('company')) missing.push(form.elements.company);
    [form.elements.name, form.elements.email, form.elements.company].forEach(function (f) { f.setAttribute('aria-invalid', String(missing.indexOf(f) !== -1)); });
    if (missing.length) { msg.textContent = 'Add your name, a work email and your company, and we’ll take it from there.'; missing[0].focus(); return; }
    var lines = ['Trust Intake request', '', 'Requested:'].concat(picked.length ? picked.map(function (x) { return '- ' + x; }) : ['- (see notes)']);
    lines.push('', 'Name: ' + v('name'), 'Work email: ' + v('email'), 'Company: ' + v('company'));
    if (v('role')) lines.push('Role: ' + v('role'));
    if (v('due')) lines.push('Needed by: ' + v('due'));
    if (v('notes')) lines.push('', 'Notes:', v('notes'));
    var href = 'mailto:trust@aivric.com?subject=' + encodeURIComponent('Trust Intake request - ' + v('company')) + '&body=' + encodeURIComponent(lines.join('\n'));
    msg.textContent = 'Your email app should open with the request written out. If it doesn’t, write to trust@aivric.com.';
    location.href = href;
  });
})();
