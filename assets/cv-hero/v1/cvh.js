/* Vision edition kit — the shared engine for /providers and /enterprise (content lives in each page's content.js)
   Classic script, one global (window.CVH), no modules and no build step, matching the rest of
   the site. Everything it touches is inside .cvh-page. */
(function () {
  'use strict';

  var page = document.querySelector('.cvh-page');
  if (!page) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Content and media root come from the page's content.js (window.CVH_CONTENT); the engine is shared.
  var C = window.CVH_CONTENT || {};
  var MEDIA = C.media || 'assets/cv-hero/v1/media/';
  var RAIL = C.RAIL || [], STANDARDS = C.STANDARDS || [], SPINE = C.SPINE || [];
  var ACC_START = C.ACC_START || { items: [] }, ACC_MOM = C.ACC_MOM || { items: [] };

  /* ======================================================================
     CONTENT
     ====================================================================== */


  var SPINE_MEDIA = MEDIA + 'spine/';


  /* ======================================================================
     SMALL HELPERS
     ====================================================================== */

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* ======================================================================
     NAV
     The bar floats on the hero — transparent, light ink — and returns to its
     solid state once the hero has scrolled past it. --cvh-nav carries the
     measured height, for the hero's top padding and for anchored scrolling.
     Note this writes --cvh-nav and never --cvh-header: an inline style would
     beat nav.css, which is what zeroes --cvh-header for a floating bar.
     ====================================================================== */

  var header = document.querySelector('.site-header');
  var hero = page.querySelector('.cvh-hero');

  function measureNav() {
    var h = header ? Math.round(header.getBoundingClientRect().height) : 0;
    if (h > 0) page.style.setProperty('--cvh-nav', h + 'px');
  }
  measureNav();
  if (header && window.ResizeObserver) new ResizeObserver(measureNav).observe(header);
  addEventListener('resize', measureNav);

  if (header && hero && document.body.getAttribute('data-nav') === 'over') {
    var navQueued = false;
    function readNavState() {
      navQueued = false;
      var h = header.getBoundingClientRect().height;
      // During the flight the bar floats in light ink until the footage under it turns bright —
      // cvh-scrub.js flags that frame from the pixels (hero-flight.json · navSolidFrom). On the
      // white page the solid bar then reads as the same floating bar with dark ink.
      if (page.classList.contains('cvh-scrub-ready')) {
        document.body.classList.toggle('is-nav-solid', hero.getAttribute('data-cvh-nav-solid') === '1');
        return;
      }
      document.body.classList.toggle('is-nav-solid', hero.getBoundingClientRect().bottom <= h);
    }
    function onNavScroll() {
      if (navQueued) return;
      navQueued = true;
      requestAnimationFrame(readNavState);
    }
    readNavState();
    addEventListener('scroll', onNavScroll, { passive: true });
    addEventListener('resize', onNavScroll);
    addEventListener('cvh:nav', onNavScroll);
  }

  /* ======================================================================
     CHAPTERS — pure white → faint blue → deep navy
     The background eases across; the ink crosses over in a short window centred on
     the moment the background passes the midpoint of the two luminances, so text is
     never left dark-on-dark the way an instant swap leaves it.
     ====================================================================== */

  // AiVRIC provider edition: light where the flight lands, then AiVRIC navy ("paper" is the product player's chapter)
  var CHAPTERS = {
    paper: { bg: '#ffffff', surface: '#f5f9fc', ink: '#0b1220', ink2: '#475569', line: '#dde8f1', accent: '#0077b6', accentInk: '#ffffff' },
    day:   { bg: '#ffffff', surface: '#f5f9fc', ink: '#0b1220', ink2: '#475569', line: '#dde8f1', accent: '#0077b6', accentInk: '#ffffff' },
    warm:  { bg: '#eef7fc', surface: '#fbfdff', ink: '#050c18', ink2: '#43607a', line: '#d2e6f1', accent: '#0077b6', accentInk: '#ffffff' },
    night: { bg: '#080f1c', surface: '#0d1829', ink: '#f0f8ff', ink2: '#9fb0c6', line: '#1b2a3f', accent: '#00d1ff', accentInk: '#050c18' }
  };
  var BG_KEYS = ['bg', 'surface'];          // ease smoothly
  var INK_KEYS = ['ink', 'ink2', 'line', 'accent', 'accentInk']; // cross at the midpoint

  function hex2rgb(h) {
    return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  }
  function rgb2css(c) {
    return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')';
  }
  function mix(a, b, p) { return [a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p, a[2] + (b[2] - a[2]) * p]; }
  function lum(c) {
    var f = c.map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2];
  }
  // A balanced wash avoids lingering on the light chapter before accelerating into navy.
  function ease(t) {
    return smoothstep(t);
  }
  function smoothstep(p) { p = Math.min(1, Math.max(0, p)); return p * p * (3 - 2 * p); }

  var THEME_MS = 1400, INK_MS = 0;   // smooth wash; ink changes at the contrast-safe crossing
  var current = 'day', anim = null;

  function paint(set) {
    for (var k in set) page.style.setProperty('--cvh-' + (k === 'ink2' ? 'ink-2' : k === 'accentInk' ? 'accent-ink' : k), set[k]);
  }
  paint(CHAPTERS[current]);

  // Where should the ink change hands? Not at the background's halfway point — at the moment
  // the outgoing and incoming ink have the SAME contrast against it. That is the instant the
  // swap is invisible, and it is the best worst-case contrast any crossing can have.
  //   (Lbg + .05)^2 = (Lfrom + .05)(Lto + .05)
  function crossPoint(fromBg, toBg, fromInk, toInk) {
    var target = Math.sqrt((lum(fromInk) + 0.05) * (lum(toInk) + 0.05)) - 0.05;
    var l0 = lum(fromBg), l1 = lum(toBg);
    if ((target - l0) * (target - l1) > 0) return 0.5;        // never reached: fall back to halfway
    for (var i = 0; i <= 120; i++) {
      var t = i / 120;
      var L = lum(mix(fromBg, toBg, ease(t)));
      if ((l1 >= l0 && L >= target) || (l1 < l0 && L <= target)) return t;
    }
    return 0.5;
  }

  function setChapter(name) {
    if (name === current || !CHAPTERS[name]) return;
    var from = CHAPTERS[current], to = CHAPTERS[name];
    current = name;
    page.setAttribute('data-cvh-chapter', name);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', to.bg);

    if (reduce) { paint(to); return; }

    var fromC = {}, toC = {};
    BG_KEYS.concat(INK_KEYS).forEach(function (k) { fromC[k] = hex2rgb(from[k]); toC[k] = hex2rgb(to[k]); });

    var tCross = crossPoint(fromC.bg, toC.bg, fromC.ink, toC.ink);
    var inkHalf = INK_MS / THEME_MS / 2;

    if (anim) cancelAnimationFrame(anim);
    var t0 = performance.now();
    (function step(now) {
      var p = Math.min(1, (now - t0) / THEME_MS);
      var e = ease(p);
      var out = {};
      BG_KEYS.forEach(function (k) { out[k] = rgb2css(mix(fromC[k], toC[k], e)); });
      var ip = inkHalf > 0 ? smoothstep((p - (tCross - inkHalf)) / (inkHalf * 2)) : (p >= tCross ? 1 : 0);
      INK_KEYS.forEach(function (k) { out[k] = rgb2css(mix(fromC[k], toC[k], ip)); });
      paint(out);
      if (p < 1) anim = requestAnimationFrame(step); else anim = null;
    })(t0);
  }

  // the section whose band crosses the middle of the screen owns the colour
  var sections = [].slice.call(page.querySelectorAll('[data-cvh-chapter]'));
  if ('IntersectionObserver' in window) {
    var chapterObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) setChapter(en.target.getAttribute('data-cvh-chapter'));
      });
    }, { rootMargin: '-44% 0px -56% 0px', threshold: 0 });
    sections.forEach(function (s) { chapterObs.observe(s); });
  }

  /* ======================================================================
     2 · THE PRODUCT PLAYER
     The pattern (docs/design-notes.md):
     - the active item's clip autoplays muted, plays once, holds a beat and replays;
       it never advances on its own — you click the next item to see the next clip;
     - clicking swaps clips with a 400ms opacity + 8px blur cross-fade, in place
       (the CSS does the fade; the outgoing clip keeps playing until it's gone);
     - a frosted pause control sits on the window, shown on hover or focus.
     The clips are framed by clips/geometry.json; the numbers below mirror it.
     ====================================================================== */

  var CLIP = { w: 2560, h: 1440, panel: { x: 0.176, y: 0.14, w: 0.648, h: 0.72 } };
  var LOOP_HOLD = 400;

  var list = document.getElementById('cvh-rail');
  var stage = document.getElementById('cvh-stage');
  var stageTrack = document.getElementById('cvh-stage-track');
  var pin = document.querySelector('.cvh-product-pin');
  var col = document.querySelector('.cvh-product-col');
  var phaseEl = document.querySelector('[data-cvh-phase]');
  var desktop = window.matchMedia('(min-width: 1024px)');
  var items = [], slides = [], active = -1, userPaused = reduce, visible = false, loopTimer = 0;

  var ICONS = '<svg class="cvh-i-pause" viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="2.5" width="3" height="11" rx="1"/><rect x="9.5" y="2.5" width="3" height="11" rx="1"/></svg>' +
    '<svg class="cvh-i-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 2.9v10.2c0 .6.6.9 1.1.6l7.4-5.1a.7.7 0 0 0 0-1.2L6.1 2.3C5.6 2 5 2.3 5 2.9z"/></svg>';

  function play(v) {
    if (!visible || userPaused) return;
    var p = v.play();
    if (p && typeof p.catch === 'function') p.catch(function () {});
  }

  function syncPause() {
    slides.forEach(function (s, j) {
      var paused = j === active && userPaused;
      s.pb.classList.toggle('is-paused', paused);
      s.pb.setAttribute('aria-label', paused ? 'Play' : 'Pause');
    });
  }

  // A clip upgrades from metadata to a full preload the moment someone shows interest. Only a
  // clip that has fetched nothing yet is (re)loaded — resetting one mid-fetch is what makes a
  // swap stall on the empty window.
  function warm(i) {
    var v = slides[i] && slides[i].v;
    if (!v || v.preload === 'auto') return;
    v.preload = 'auto';
    if (v.readyState === 0 && v.networkState !== 2) v.load();
  }

  // Once the clip on screen can play through, fetch the others quietly, one at a time, so a
  // click never waits on the network. Only for people who actually reach this section.
  var prefetchStarted = false;
  function prefetchRest() {
    if (prefetchStarted) return;
    prefetchStarted = true;
    var queue = slides.map(function (s, j) { return j; }).filter(function (j) { return j !== active; });
    (function next() {
      var j = queue.shift();
      if (j === undefined) return;
      var v = slides[j].v;
      warm(j);
      if (v.readyState >= 4) next();
      else v.addEventListener('canplaythrough', next, { once: true });
    })();
  }

  function select(i, user) {
    if (i === active || i < 0 || i >= slides.length) return;
    var prev = active;
    active = i;
    if (user && !reduce) userPaused = false;
    clearTimeout(loopTimer);
    items.forEach(function (x, j) {
      x.btn.setAttribute('aria-expanded', String(j === i));
      x.btn.tabIndex = j === i ? 0 : -1;
      x.item.classList.toggle('is-open', j === i);
    });
    slides.forEach(function (s, j) {
      if (j === i) {
        s.slide.dataset.active = 'true';
        warm(j);
        try { s.v.currentTime = 0; } catch (err) {}
        play(s.v);
      } else {
        s.slide.dataset.active = 'false';
        // the outgoing clip keeps playing under the fade, then stops once it's gone
        if (j === prev) setTimeout(function () { if (active !== j) s.v.pause(); }, 420);
        else s.v.pause();
      }
    });
    syncPause();
    placeStage();
  }

  RAIL.forEach(function (it, i) {
    var item = el('div', 'cvh-pl-item');
    var btn = el('button', 'cvh-pl-btn');
    btn.type = 'button';
    btn.id = 'cvh-pl-btn-' + i;
    btn.tabIndex = -1;
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'cvh-pl-panel-' + i);
    btn.innerHTML = '<span class="cvh-pl-mark" aria-hidden="true"></span><span class="cvh-pl-title">' + esc(it.t) + '</span>';
    var panel = el('div', 'cvh-pl-panel');
    panel.id = 'cvh-pl-panel-' + i;
    panel.setAttribute('role', 'region');
    panel.setAttribute('aria-labelledby', btn.id);
    panel.innerHTML = '<div><p>' + esc(it.d) + '</p><div class="cvh-pl-slot"></div></div>';
    item.appendChild(btn);
    item.appendChild(panel);
    list.appendChild(item);
    btn.addEventListener('click', function () { select(i, true); });
    btn.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
      if (e.key === 'Home') d = -i; else if (e.key === 'End') d = RAIL.length - 1 - i;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + RAIL.length) % RAIL.length;
      select(n, true);
      items[n].btn.focus();
    });
    btn.addEventListener('pointerenter', function () { warm(i); });
    btn.addEventListener('focus', function () { warm(i); });
    items.push({ item: item, btn: btn, slot: panel.querySelector('.cvh-pl-slot') });

    var slide = el('div', 'cvh-slide');
    slide.dataset.active = 'false';
    var v = document.createElement('video');
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.setAttribute('muted', '');
    v.setAttribute('playsinline', '');
    v.preload = i === 0 ? 'auto' : 'metadata';
    v.poster = MEDIA + 'clip-' + it.clip + '.jpg';
    v.setAttribute('aria-label', it.cap);
    [['mp4', 'video/mp4']].forEach(function (f) {
      var src = document.createElement('source');
      src.src = MEDIA + 'clip-' + it.clip + '.' + f[0];
      src.type = f[1];
      v.appendChild(src);
    });
    var controls = el('div', 'cvh-slide-controls');
    var pb = el('button', 'cvh-pause', ICONS);
    pb.type = 'button';
    pb.setAttribute('aria-label', 'Pause');
    controls.appendChild(pb);
    slide.appendChild(v);
    slide.appendChild(controls);
    stageTrack.appendChild(slide);

    // play once, hold a beat, then on to the next item; after the last, back to the top of the list
    v.addEventListener('ended', function () {
      if (active !== i) return;
      clearTimeout(loopTimer);
      loopTimer = setTimeout(function () {
        if (active !== i) return;
        select((i + 1) % slides.length);
      }, LOOP_HOLD);
    });
    pb.addEventListener('click', function () {
      userPaused = !userPaused;
      if (userPaused) { clearTimeout(loopTimer); v.pause(); }
      else { if (v.ended) try { v.currentTime = 0; } catch (err) {} play(v); }
      syncPause();
    });
    slides.push({ slide: slide, v: v, pb: pb });
  });

  // Where the window lands. The clip is shown object-fit: cover across the whole stage; the
  // window's left edge is carried to just past the copy column, and the rest runs off the edge.
  function layout() {
    if (!stage) return;
    if (!desktop.matches) {
      ['--cvh-stage-x', '--cvh-panel-x', '--cvh-panel-y', '--cvh-panel-w', '--cvh-panel-h', '--cvh-fade-a', '--cvh-fade-b']
        .forEach(function (k) { stage.style.removeProperty(k); });
      return;
    }
    var W = stage.clientWidth, H = stage.clientHeight;
    if (!W || !H) return;
    var s = Math.max(W / CLIP.w, H / CLIP.h), fw = CLIP.w * s, fh = CLIP.h * s;
    var px = (W - fw) / 2 + CLIP.panel.x * fw, py = (H - fh) / 2 + CLIP.panel.y * fh;
    var pw = CLIP.panel.w * fw, ph = CLIP.panel.h * fh;
    var gap = Math.max(56, Math.min(110, W * 0.06));
    var target = col.getBoundingClientRect().right - stage.getBoundingClientRect().left + gap;
    var tx = Math.round(target - px);
    var landed = !phaseEl || phaseEl.getAttribute('data-cvh-phase') !== 'idle';
    stage.style.setProperty('--cvh-stage-x', (landed ? tx : 0) + 'px');
    stage.style.setProperty('--cvh-panel-x', px.toFixed(1) + 'px');
    stage.style.setProperty('--cvh-panel-y', py.toFixed(1) + 'px');
    stage.style.setProperty('--cvh-panel-w', pw.toFixed(1) + 'px');
    stage.style.setProperty('--cvh-panel-h', ph.toFixed(1) + 'px');
    // the window dissolves just before the viewport's right edge (element coordinates)
    var edge = ((W - tx) / W) * 100;
    stage.style.setProperty('--cvh-fade-b', edge.toFixed(2) + '%');
    stage.style.setProperty('--cvh-fade-a', (edge - 6).toFixed(2) + '%');
  }

  // desktop: the stage is the full-bleed layer behind the copy; below that it moves into the
  // open item, as a framed box
  function placeStage() {
    if (!stage) return;
    var home = desktop.matches ? pin : items[active] && items[active].slot;
    if (home && stage.parentNode !== home) home.insertBefore(stage, home.firstChild);
    layout();
  }

  if (stage && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (en) {
      visible = en[0].isIntersecting && en[0].intersectionRatio >= 0.25;
      var s = slides[active];
      if (!s) return;
      if (visible) {
        play(s.v);
        if (s.v.readyState >= 4) prefetchRest();
        else s.v.addEventListener('canplaythrough', prefetchRest, { once: true });
      } else { clearTimeout(loopTimer); s.v.pause(); }
    }, { threshold: [0, 0.25, 0.5] }).observe(stage);
  } else visible = true;

  function onViewport() { placeStage(); }
  if (desktop.addEventListener) desktop.addEventListener('change', onViewport);
  else if (desktop.addListener) desktop.addListener(onViewport);
  addEventListener('resize', layout);
  if (window.ResizeObserver && col) new ResizeObserver(layout).observe(col);

  select(0, false);

  // the hand-off in cvh-scrub.js drives the phase; the player only needs to know it changed
  // At the hand-off the flight's last frame is clip 1's first, so clip 1 starts from zero the
  // moment the glide begins — it is on screen by then, whatever the observer has seen so far.
  function restart() {
    var s = slides[active];
    if (!s) return;
    clearTimeout(loopTimer);
    visible = true;
    try { s.v.currentTime = 0; } catch (err) {}
    play(s.v);
  }

  window.CVH_PLAYER = { select: select, layout: layout, restart: restart, slides: slides, items: items, active: function () { return active; } };

  /* ======================================================================
     3 · STANDARDS MARQUEE
     ====================================================================== */

  var track = document.getElementById('cvh-marquee-track');
  if (track) {
    // two copies so the loop is seamless; the colours alternate across both (an even count, 28), so no
    // two blues ever meet, not even at the seam
    track.innerHTML = STANDARDS.concat(STANDARDS).map(function (s, i) {
      return '<span class="' + (i % 2 === 0 ? 'is-lead' : 'is-alt') + '">' + esc(s) + '</span>';
    }).join('');
    var sr = document.getElementById('cvh-std-list');
    if (sr) sr.textContent = 'Standards and frameworks covered: ' + STANDARDS.join(', ') + '.';
  }

  /* ======================================================================
     6 · THE SPINE
     ====================================================================== */

  var spine = document.getElementById('cvh-spine');
  var spineFrame = document.getElementById('cvh-spine-frame');
  var spineCap = document.getElementById('cvh-spine-cap');
  if (spine) {
    var steps = [], shots = [];
    SPINE.forEach(function (s, i) {
      var li = el('li', 'cvh-step cvh-rise');
      // phones get the screen inline under the step; desktop hides it and uses the sticky stage
      li.innerHTML = '<i>' + (i + 1) + '</i><div><b>' + esc(s.t) + '</b><p>' + s.d + '</p>' +
        '<img class="cvh-step-shot" src="' + SPINE_MEDIA + s.img + '" alt="' + esc(s.cap) + '" width="1280" height="800" loading="lazy" decoding="async" /></div>';
      spine.appendChild(li); steps.push(li);
      if (spineFrame) {
        var im = el('img', 'cvh-spine-shot' + (i === 0 ? ' is-on' : ''));
        im.src = SPINE_MEDIA + s.img; im.alt = ''; im.width = 1280; im.height = 800; im.decoding = 'async';
        if (i > 1) im.loading = 'lazy';
        spineFrame.appendChild(im); shots.push(im);
      }
    });
    var spineActive = -1;
    function spineSelect(i) {
      if (i < 0 || i === spineActive) return; spineActive = i;
      steps.forEach(function (li, k) { li.classList.toggle('is-active', k === i); });
      shots.forEach(function (im, k) { im.classList.toggle('is-on', k === i); });
      if (spineCap) spineCap.textContent = SPINE[i].cap;
    }
    spineSelect(0);
    // the step crossing the middle of the viewport is the active one
    if (shots.length && 'IntersectionObserver' in window) {
      var spineObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) spineSelect(steps.indexOf(en.target)); });
      }, { rootMargin: '-45% 0px -45% 0px' });
      steps.forEach(function (li) { spineObs.observe(li); });
    }
  }

  /* ======================================================================
     8 + 9 · SPLIT ACCORDIONS
     ====================================================================== */

  function buildAcc(accId, mediaId, data) {
    var acc = document.getElementById(accId), media = document.getElementById(mediaId);
    if (!acc || !media) return;
    var btns = [], imgs = [], cur = -1;
    data.items.forEach(function (it, i) {
      var b = el('button', 'cvh-acc-item');
      b.type = 'button';
      b.setAttribute('aria-expanded', 'false');
      b.innerHTML = '<b>' + esc(it.t) + '</b><span>' + esc(it.d) + '</span>';
      b.addEventListener('click', function () { openItem(i); });
      acc.appendChild(b);
      btns.push(b);

      var img = el('img');
      img.src = MEDIA + it.img;
      img.alt = it.t;
      img.loading = 'lazy';
      img.decoding = 'async';
      media.appendChild(img);
      imgs.push(img);
    });
    function openItem(i) {
      cur = i;
      btns.forEach(function (b, j) { b.setAttribute('aria-expanded', String(j === i)); });
      imgs.forEach(function (im, j) { im.classList.toggle('is-in', j === i); });
    }
    openItem(0);
  }
  buildAcc('cvh-acc-start', 'cvh-media-start', ACC_START);
  buildAcc('cvh-acc-mom', 'cvh-media-mom', ACC_MOM);

  /* ======================================================================
     REVEALS
     ====================================================================== */

  [].slice.call(page.querySelectorAll('.cvh-slides, .cvh-turn-pivot, .cvh-turn-cta, .cvh-quote, .cvh-split-grid, .cvh-fits-grid, .cvh-close .cvh-wrap'))
    .forEach(function (n) { n.classList.add('cvh-rise'); });

  requestAnimationFrame(function () { page.classList.add('cvh-ready'); });

  var rises = [].slice.call(page.querySelectorAll('.cvh-rise'));
  if ('IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        ro.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    rises.forEach(function (n) { ro.observe(n); });
  } else {
    rises.forEach(function (n) { n.classList.add('is-in'); });
  }

  window.CVH = { setChapter: setChapter, select: select, chapters: CHAPTERS };
})();
