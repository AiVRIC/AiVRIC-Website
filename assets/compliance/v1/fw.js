/* The compliance pages (/compliance/<framework>/): the film, the walkthrough player and the readiness check.
   Framework-specific data comes from the page: window.FW_STEPS (its screens.js) and window.FW_CHECK (its content.js).
   Classic script, no build step; load after lib.js, shell.js, screens.js and content.js. */
(function () {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: the check still works */ } },
  };

  /* ---- the film: a still until the page says the film is in (data-ready="true") ------------------------- */
  const film = $('.fw-film');
  if (film && film.dataset.ready === 'true' && film.dataset.film) {
    const still = film.querySelector('img');
    const v = document.createElement('video');
    v.muted = true; v.loop = true; v.playsInline = true; v.preload = 'auto';
    v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
    if (still) v.poster = still.getAttribute('src');
    v.setAttribute('aria-label', film.dataset.label || '');
    v.src = film.dataset.film;
    if (film.dataset.captions) {
      const tr = document.createElement('track');
      tr.kind = 'captions'; tr.srclang = 'en'; tr.label = 'English'; tr.default = true; tr.src = film.dataset.captions;
      v.append(tr);
    }
    if (still) still.replaceWith(v); else film.prepend(v);
    const sb = document.createElement('button');
    sb.type = 'button'; sb.className = 'fw-sound';
    sb.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>Watch with sound';
    film.append(sb);
    if (reduce) v.controls = true; else { v.autoplay = true; v.play().catch(() => {}); }
    sb.addEventListener('click', () => { v.muted = false; v.loop = false; v.currentTime = 0; v.controls = true; v.play().catch(() => {}); sb.hidden = true; });
  }

  /* ---- the walkthrough: one step per word, the product screen in its finished state ---------------------- */
  const STEPS = window.FW_STEPS || [];
  const rail = $('#fw-rail'), view = $('#fw-view'), steps = $('.fw-steps');
  if (rail && view && STEPS.length) {
    const word = $('#fw-word'), def = $('#fw-def'), chip = $('#fw-chip');
    const btns = STEPS.map((st, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'tab'); b.id = 'fw-st-' + i; b.setAttribute('aria-controls', 'fw-stage');
      b.innerHTML = `<small>${String(i + 1).padStart(2, '0')}</small><span></span><i class="fw-tick"></i>`;
      b.querySelector('span').textContent = st.w;
      rail.append(b);
      return b;
    });
    STEPS.forEach((st) => {
      const sc = document.createElement('div'); sc.className = 'fw-scene';
      const cam = document.createElement('div'); cam.className = 'fw-cam cvui';
      const win = st.make();
      cam.append(win.el); sc.append(cam); view.append(sc);
      st.sc = sc; st.cam = cam; st.r = win.r;
      if (st.rest) st.rest(win.r);
    });
    const frame = () => {
      const vw = view.clientWidth, vh = view.clientHeight;
      STEPS.forEach((st) => {
        const [x, y, w, h] = st.region, k = Math.min(vw / w, vh / h);
        st.cam.style.transform = `translate(${(vw - w * k) / 2}px,${(vh - h * k) / 2}px) scale(${k}) translate(${-x}px,${-y}px)`;
      });
    };
    if (window.ResizeObserver) new ResizeObserver(frame).observe(view); else { frame(); addEventListener('resize', frame); }
    let cur = -1, t0 = 0, paused = false;
    const DUR = 6500;
    const tick = (i) => btns[i].querySelector('.fw-tick');
    function show(i, user) {
      if (i === cur) return;
      cur = i;
      btns.forEach((b, j) => { b.setAttribute('aria-selected', String(j === i)); b.tabIndex = j === i ? 0 : -1; tick(j).style.width = '0'; });
      const st = STEPS[i];
      word.textContent = st.w + '.'; def.textContent = st.def; chip.textContent = st.chip;
      // "Lives in": where the step's screen sits in the app, when the step says (the hub's eight words do)
      const where = $('#fw-where');
      if (where) { where.hidden = !st.where; where.querySelector('b').textContent = st.where || ''; }
      $('#fw-stage').setAttribute('aria-labelledby', btns[i].id);
      STEPS.forEach((x, j) => x.sc.classList.toggle('on', j === i));
      if (st.play) st.play(st.r);
      if (user) btns[i].scrollIntoView({ block: 'nearest', inline: 'nearest' });
      t0 = performance.now();
    }
    btns.forEach((b, i) => {
      b.addEventListener('click', () => show(i, true));
      b.addEventListener('keydown', (e) => {
        const d = ['ArrowDown', 'ArrowRight'].includes(e.key) ? 1 : ['ArrowUp', 'ArrowLeft'].includes(e.key) ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        const n = (cur + d + STEPS.length) % STEPS.length;
        show(n, true); btns[n].focus();
      });
    });
    steps.addEventListener('pointerenter', () => { paused = true; });
    steps.addEventListener('pointerleave', () => { paused = false; t0 = performance.now(); });
    steps.addEventListener('focusin', () => { paused = true; });
    steps.addEventListener('focusout', () => { paused = false; });
    show(0);
    if (!reduce) {
      let visible = true;
      if ('IntersectionObserver' in window) new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(steps);
      const loop = (now) => {
        if (!paused && visible) {
          const p = Math.min(1, Math.max(0, (now - t0) / DUR));
          tick(cur).style.width = (p * 100) + '%';
          if (p >= 1) show((cur + 1) % STEPS.length);
        } else t0 = now - (parseFloat(tick(cur).style.width) || 0) / 100 * DUR;
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }
  }

  /* ---- the readiness check: answers stay in this browser ------------------------------------------------ */
  // FW_CHECK has either items (one list) or groups ([[heading, items], …]); each item is [id, name, what it means,
  // citation or where it lives, key item, weight]. A weight (CMMC: a family's practice count) makes the score the sum of
  // the ticked weights; without one each item counts 1. percent: true shows the score as a percentage instead of a count;
  // message(got, total, pct, keyMissing) overrides the four fixed messages.
  const C = window.FW_CHECK, list = $('#fw-list');
  if (C && list) {
    const saved = store.get(C.key) || {}, boxes = [];
    const groups = C.groups || [[null, C.items || []]];
    const total = groups.reduce((n, [, items]) => n + items.reduce((m, it) => m + (it[5] || 1), 0), 0);
    const tot = $('#fw-total');
    if (tot) tot.textContent = String(total);
    const item = ([id, name, d, cite, key, weight]) => {
      const lab = document.createElement('label');
      lab.className = 'fw-item' + (key ? ' key' : '');
      lab.htmlFor = 'fw-c-' + id;
      lab.innerHTML = '<input type="checkbox"><div><b></b><span></span><em></em></div>';
      const cb = lab.querySelector('input');
      cb.id = 'fw-c-' + id;
      lab.querySelector('b').textContent = name;
      lab.querySelector('span').textContent = d;
      lab.querySelector('em').textContent = cite;
      cb.checked = !!saved[id];
      cb.addEventListener('change', () => { saved[id] = cb.checked; store.set(C.key, saved); meter(); });
      boxes.push([cb, key, weight || 1]);
      return lab;
    };
    groups.forEach(([heading, items]) => {
      if (!heading) { items.forEach((it) => list.append(item(it))); return; }
      const g = document.createElement('div');
      g.className = 'fw-group';
      const h3 = document.createElement('h3'); h3.textContent = heading;
      g.append(h3);
      items.forEach((it) => g.append(item(it)));
      list.append(g);
    });
    if (C.groups) list.classList.add('grouped');
    function meter() {
      const got = boxes.reduce((n, [cb, , w]) => n + (cb.checked ? w : 0), 0), pct = Math.round(100 * got / total);
      const keyMissing = boxes.some(([cb, key]) => key && !cb.checked);
      $('#fw-score').textContent = C.percent ? pct + '%' : got;
      $('#fw-bar').style.width = pct + '%';
      const m = C.messages || {};
      $('#fw-msg').textContent = typeof C.message === 'function' ? C.message(got, total, pct, keyMissing)
        : got === 0 ? m.none : got === total ? m.all : keyMissing ? m.keyMissing : m.some.replace('{left}', total - got);
    }
    meter();
  }
})();
