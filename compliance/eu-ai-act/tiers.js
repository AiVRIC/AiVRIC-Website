/* The EU AI Act risk tier check on /compliance/eu-ai-act/: tick how you use AI, and each use is sorted into the Act's
   risk tiers with the date that applies. A first pass, not legal advice. Answers stay in this browser. */
(function () {
  'use strict';
  const list = document.getElementById('fw-list'), tiersEl = document.getElementById('fw-tiers'), msg = document.getElementById('fw-msg');
  if (!list || !tiersEl) return;
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: the check still works */ } },
  };
  const KEY = 'aivric.euai.tiers';
  // tier → [name, what applies and when]
  const TIER = {
    P: ['Unacceptable risk', 'Prohibited since Feb 2, 2025 (Art. 5)'],
    H: ['High risk', 'Obligations apply from Dec 2, 2027 (Annex III)'],
    T: ['Transparency risk', 'Disclosure required since Aug 2, 2026 (Art. 50)'],
    M: ['Minimal or no risk', 'No new duties beyond supporting AI literacy (Art. 4)'],
  };
  // [id, use, why, tier]
  const USES = [
    ['hire', 'Screening or ranking job applicants', 'Employment', 'H'],
    ['work', 'Allocating tasks or monitoring employee performance', 'Worker management', 'H'],
    ['credit', 'Credit scoring of individuals', 'Essential services · not fraud detection', 'H'],
    ['ins', 'Pricing life or health insurance', 'Essential services', 'H'],
    ['edu', 'Grading exams or deciding admissions', 'Education', 'H'],
    ['grid', 'Safety component in critical infrastructure (energy, water, traffic)', 'Critical infrastructure', 'H'],
    ['bot', 'Customer-service chatbot', 'People must know it’s AI', 'T'],
    ['gen', 'Generating images, video or text for publication', 'Label AI-generated content', 'T'],
    ['emo', 'Emotion recognition of employees at work', 'Except medical or safety reasons', 'P'],
    ['score', 'Social scoring of people', 'Banned outright', 'P'],
    ['spam', 'Spam filtering, demand forecasting or code assistants', 'Everyday business AI', 'M'],
  ];
  const saved = store.get(KEY) || {}, boxes = [];
  USES.forEach(([id, name, why, t]) => {
    const lab = document.createElement('label');
    lab.className = 'fw-item'; lab.htmlFor = 'fw-u-' + id;
    lab.innerHTML = '<input type="checkbox"><div><b></b><span></span><em></em></div>';
    const cb = lab.querySelector('input'); cb.id = 'fw-u-' + id;
    lab.querySelector('b').textContent = name;
    lab.querySelector('span').textContent = why;
    const em = lab.querySelector('em'); em.textContent = TIER[t][0]; em.dataset.tier = t;
    cb.checked = !!saved[id];
    cb.addEventListener('change', () => { saved[id] = cb.checked; store.set(KEY, saved); meter(); });
    boxes.push([cb, t]);
    list.append(lab);
  });
  const rows = {};
  ['P', 'H', 'T', 'M'].forEach((t) => {
    const r = document.createElement('div');
    r.className = 'fw-tier t-' + t;
    r.innerHTML = '<b>0</b><div><strong></strong><span></span></div>';
    r.querySelector('strong').textContent = TIER[t][0];
    r.querySelector('span').textContent = TIER[t][1];
    tiersEl.append(r); rows[t] = r;
  });
  function meter() {
    const n = { P: 0, H: 0, T: 0, M: 0 };
    boxes.forEach(([cb, t]) => { if (cb.checked) n[t]++; });
    Object.entries(n).forEach(([t, k]) => { rows[t].querySelector('b').textContent = k; rows[t].classList.toggle('on', k > 0); });
    msg.textContent = n.P ? 'Stop first: at least one use looks prohibited. Those bans have applied since February 2, 2025.'
      : n.H ? `${n.H} high-risk use${n.H > 1 ? 's' : ''}. Each needs risk management, logging, documentation and a named human overseer by December 2, 2027.`
      : n.T ? 'Transparency duties apply now: tell people when they’re dealing with AI, and label what it generates.'
      : n.M ? 'Minimal risk. Keep an inventory and train the people who use it.'
      : 'Tick a use to see its tier.';
  }
  meter();
})();
