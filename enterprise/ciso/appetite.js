/* The risk appetite statement builder on /enterprise/ciso/: pick a tolerance per area, and the overall appetite is the
   median of what you declare (the rule Enterprise Vision uses), never typed in. Choices stay in this browser.
   Areas and levels come from the screens (window.UI3.AREAS, UI3.LEVELS in screens.js). */
(function () {
  'use strict';
  const areasEl = document.getElementById('fw-areas');
  if (!areasEl || !window.UI3) return;
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: the builder still works */ } },
  };
  const KEY = 'aivric.ciso.appetite';
  const LV = UI3.LEVELS, AREAS = UI3.AREAS.map((a) => a[0]);
  const DEF = [0, 0, 1, 1, 0, 2, 1, 2, 2, 3, 1, 2];
  const saved = store.get(KEY) || {};
  const lv = AREAS.map((_, i) => (Number.isInteger(saved['a' + i]) ? saved['a' + i] : DEF[i] || 0));

  AREAS.forEach((name, i) => {
    const row = document.createElement('div');
    row.className = 'fw-area';
    row.setAttribute('role', 'radiogroup');
    row.setAttribute('aria-labelledby', 'fw-al' + i);
    const lab = document.createElement('div');
    lab.id = 'fw-al' + i; lab.className = 'fw-area-name'; lab.textContent = name;
    row.append(lab);
    const seg = document.createElement('div');
    seg.className = 'fw-seg';
    LV.forEach((l, k) => {
      const w = document.createElement('label');
      const inp = document.createElement('input');
      inp.type = 'radio'; inp.name = 'fw-a' + i; inp.value = k; inp.checked = lv[i] === k;
      inp.setAttribute('aria-label', `${name}: ${l}`);
      inp.addEventListener('change', () => { lv[i] = k; saved['a' + i] = k; store.set(KEY, saved); update(); });
      const sp = document.createElement('span'); sp.textContent = l;
      w.append(inp, sp); seg.append(w);
    });
    row.append(seg);
    areasEl.append(row);
  });

  const org = document.getElementById('fw-org');
  org.value = saved.org || '';
  org.addEventListener('input', () => { saved.org = org.value; store.set(KEY, saved); update(); });
  const lc = (s0) => (/^[A-Z]{2}/.test(s0) ? s0 : s0.charAt(0).toLowerCase() + s0.slice(1));
  const list = (arr) => (arr.length < 2 ? arr.join('') : arr.slice(0, -1).join(', ') + ' and ' + arr[arr.length - 1]);

  function update() {
    const sorted = [...lv].sort((a, b) => a - b);
    const med = sorted[Math.floor((sorted.length - 1) / 2)];
    document.getElementById('fw-ovr').textContent = LV[med];
    document.getElementById('fw-spread').hidden = !(Math.max(...lv) - Math.min(...lv) >= 3);
    const name = org.value.trim() || 'The organization';
    const groups = LV.map((l, k) => AREAS.filter((_, i) => lv[i] === k).map(lc));
    const phr = [`are averse to risk in ${list(groups[0])}`, `accept only minimal, well-mitigated risk in ${list(groups[1])}`,
      `take a cautious approach to ${list(groups[2])}`, `are open to measured risk in ${list(groups[3])}`,
      `will seek the upside in ${list(groups[4])}`].filter((_, k) => groups[k].length);
    document.getElementById('fw-stmt').textContent = `${name} has an overall ${LV[med].toLowerCase()} appetite for information security risk.\n\n` +
      `We ${phr.join('; we ')}.\n\nRisks above these tolerances require a written justification and senior approval before they are accepted. ` +
      'Leadership reviews this statement quarterly and reports against it to the board.';
  }
  update();

  const copied = document.getElementById('fw-copied');
  document.getElementById('fw-copy').addEventListener('click', async () => {
    const txt = document.getElementById('fw-stmt').textContent;
    try { await navigator.clipboard.writeText(txt); copied.textContent = 'Copied.'; }
    catch (e) {
      const r = document.createRange(); r.selectNodeContents(document.getElementById('fw-stmt'));
      const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
      copied.textContent = 'Selected — press Ctrl+C to copy.';
    }
    setTimeout(() => { copied.textContent = ''; }, 2600);
  });
})();
