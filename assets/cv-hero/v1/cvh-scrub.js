/* Desktop hero flight — scroll-scrubbed into the laptop, then handed off to the product player.
   Mercury's pattern, measured on mercury.com:
   - scroll maps linearly to video time, smoothed by a spring (about 130ms of lag);
   - the footage ends with the screen flattening off the laptop and the room dissolving to the
     page, and its last frame is the product player's first frame;
   - at that last frame, in one task before paint, the hero's runway collapses to one screen and
     scroll is compensated so the product section sits exactly where the pinned hero was — the
     same picture, so the swap is invisible — then the clip layer glides into its column;
   - one-way for the page load: scroll back up and the hero is a still screen.
   Frame counts and the nav switch come from hero-flight.json, written by tools/build-hero-flight.mjs. */
(function () {
  'use strict';

  var page = document.querySelector('.cvh-page');
  var hero = page && page.querySelector('.cvh-hero');
  var pin = hero && hero.querySelector('[data-cvh-hero-pin]');
  var video = hero && hero.querySelector('.cvh-hero-video');
  var copy = hero && hero.querySelector('.cvh-hero-content');
  var product = page && page.querySelector('.cvh-product');
  var phaseEl = product && product.querySelector('[data-cvh-phase]');
  var still = document.getElementById('cvh-stage-still');
  if (!page || !hero || !pin || !video || !product) return;

  var MEDIA = (window.CVH_CONTENT && window.CVH_CONTENT.media) || 'assets/cv-hero/v1/media/';
  var KEY = 'cvh.hero.flight';
  var SPRING = { k: 200, c: 30, m: 0.5 };      // framer-motion useSpring, as Mercury configures it
  var GLIDE_MS = 600;
  var desktop = matchMedia('(min-width: 1024px)');
  var motion = matchMedia('(prefers-reduced-motion: reduce)');

  var M = null;                 // the manifest
  var state = 'off';            // off · pending · flying · done
  var target = 0, pos = 0, vel = 0, lastT = 0, raf = 0, frame = -1, restore = null, seekWait = 0;

  function eligible() { return desktop.matches && !motion.matches; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function smooth(p) { p = clamp(p, 0, 1); return p * p * (3 - 2 * p); }
  function docTop(n) { return n.getBoundingClientRect().top + window.scrollY; }
  // The section is taller than the flight needs: after the mapped runway there is a buffer
  // (BUFFER of a screen) where the hero stays pinned at its last frame while the spring catches
  // up. Without it a quick wheel outruns the spring and the pin starts scrolling away before the
  // swap — a double image for a frame or two.
  var BUFFER = 0.4;
  function runway() { return Math.max(1, hero.offsetHeight - pin.offsetHeight); }
  function mapRunway() { return Math.max(1, runway() - pin.offsetHeight * BUFFER); }
  // scroll lands on whole pixels but the runway rarely does — the last pixel and a half is the end
  function scrollProgress() {
    var into = window.scrollY - docTop(hero), r = mapRunway();
    return r - into < 1.5 ? 1 : clamp(into / r, 0, 1);
  }
  function navChanged() { window.dispatchEvent(new Event('cvh:nav')); }
  function setPhase(p) {
    if (phaseEl) phaseEl.setAttribute('data-cvh-phase', p);
    if (window.CVH_PLAYER) window.CVH_PLAYER.layout();
  }
  function jump(y) {
    try { window.scrollTo({ top: y, left: 0, behavior: 'instant' }); } catch (e) { window.scrollTo(0, y); }
  }

  try {
    var nav = performance.getEntriesByType('navigation')[0];
    var saved = sessionStorage.getItem(KEY);
    if (nav && nav.type === 'reload' && saved !== null) {
      var n = Number(saved);
      if (isFinite(n) && n >= 0 && n < 1) restore = n;
    }
  } catch (e) { /* storage can be disabled; the flight still works without restore */ }

  // --- the look at a given frame ----------------------------------------------------------
  function paint(p) {
    var last = M.frames - 1;
    var fr = Math.round(p * last);
    var tail = clamp((fr - M.tailStart) / (last - M.tailStart), 0, 1);
    var clarity = smooth((p - 0.5) / 0.38);
    page.style.setProperty('--cvh-video-opacity', smooth(p / 0.018).toFixed(3));
    page.style.setProperty('--cvh-copy-opacity', (1 - smooth(p / 0.16)).toFixed(3));
    page.style.setProperty('--cvh-vignette-clear', (34 + 46 * clarity).toFixed(1) + '%');
    page.style.setProperty('--cvh-vignette-blur', (9 - 7.8 * clarity).toFixed(1) + 'px');
    page.style.setProperty('--cvh-vignette-wash', (0.07 - 0.045 * clarity).toFixed(3));
    // the room is dissolving in the footage, so the vignette has to leave with it
    page.style.setProperty('--cvh-vignette-opacity', (1 - smooth(tail / 0.55)).toFixed(3));
    hero.setAttribute('data-cvh-scrub-progress', p.toFixed(3));
    var solid = fr >= M.navSolidFrom ? '1' : '0';
    if (hero.getAttribute('data-cvh-nav-solid') !== solid) { hero.setAttribute('data-cvh-nav-solid', solid); navChanged(); }
    if (copy) copy.inert = p >= 0.2;
    if (fr !== frame && video.readyState >= 2) {
      frame = fr;
      try { video.currentTime = fr / M.fps + 0.01; } catch (e) { /* keep the last decoded frame */ }
    }
    try { sessionStorage.setItem(KEY, String(p)); } catch (e) {}
  }

  // --- the spring --------------------------------------------------------------------------
  function tick(now) {
    raf = 0;
    if (state !== 'flying') return;
    var dt = Math.min(0.05, lastT ? (now - lastT) / 1000 : 1 / 60);
    lastT = now;
    for (var steps = Math.ceil(dt / 0.004), h = dt / steps, i = 0; i < steps; i++) {
      var a = (-SPRING.k * (pos - target) - SPRING.c * vel) / SPRING.m;
      vel += a * h;
      pos += vel * h;
    }
    pos = clamp(pos, 0, 1);
    var resting = Math.abs(pos - target) < 1e-4 && Math.abs(vel) < 1e-3;
    if (resting) { pos = target; vel = 0; }
    paint(pos);
    if (pos >= 0.9995 && target >= 1) { handoff(true); return; }
    if (!resting) raf = requestAnimationFrame(tick);
    else lastT = 0;
  }
  function wake() { if (!raf && state === 'flying') raf = requestAnimationFrame(tick); }

  // --- the hand-off ------------------------------------------------------------------------
  function glideIn() {
    setPhase('transitioning');
    setTimeout(function () { setPhase('complete'); }, GLIDE_MS + 50);
  }

  function handoff(glide) {
    if (state === 'done') return;
    var wasFlying = state === 'flying' || state === 'pending';
    // The hero is still pinned at its last frame here (the buffer and the fling guard see to
    // that), so the product section always lands exactly at the top — nothing carries over.
    state = 'done';
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    if (seekWait) { clearTimeout(seekWait); seekWait = 0; }

    // collapse: the hero becomes one still screen at its opening frame, copy restored
    page.classList.remove('cvh-scrub-ready', 'cvh-scrub-pending');
    page.classList.add('cvh-flight-done');
    ['--cvh-video-opacity', '--cvh-copy-opacity', '--cvh-vignette-clear', '--cvh-vignette-blur', '--cvh-vignette-wash', '--cvh-vignette-opacity']
      .forEach(function (k) { page.style.removeProperty(k); });
    hero.removeAttribute('data-cvh-nav-solid');
    if (copy) copy.inert = false;
    try { video.pause(); } catch (e) {}
    try { sessionStorage.removeItem(KEY); } catch (e) {}

    // compensate: the product section lands exactly where the pinned hero was
    if (wasFlying) jump(docTop(product));
    navChanged();

    if (glide) {
      // the idle layout is the flight's last frame; the glide starts on the next frame.
      // (check-scrub.mjs holds it with __cvhHoldGlide to photograph the swap itself.)
      if (window.CVH_PLAYER) window.CVH_PLAYER.restart();
      requestAnimationFrame(function () { if (!window.__cvhHoldGlide) glideIn(); });
    } else {
      setPhase('complete');
    }
    window.dispatchEvent(new Event('scroll'));
  }

  // --- start -------------------------------------------------------------------------------
  // A host that ignores HTTP Range requests (python -m http.server, some preview hosts) delivers the
  // whole file, but Chromium and Edge then leave the seekable range empty and every seek snaps back
  // to 0: the runway would be a frozen first frame. GitHub Pages serves ranges; the dev server in
  // tools/serve.mjs does too. If the range has not appeared shortly after the data has, skip the flight.
  function canSeek() {
    try { var s = video.seekable; return s.length > 0 && s.end(s.length - 1) > 0.5; } catch (e) { return false; }
  }
  function ready() {
    if (state !== 'pending') return;
    if (!canSeek()) {
      if (!seekWait) seekWait = setTimeout(function () {
        seekWait = 0;
        if (state !== 'pending') return;
        if (canSeek()) { ready(); return; }
        try { console.warn('cvh-scrub: hero flight skipped; the host does not serve byte ranges, so the video cannot seek.'); } catch (e) {}
        handoff(false);
      }, 1500);
      return;
    }
    state = 'flying';
    page.classList.remove('cvh-scrub-pending');
    page.classList.add('cvh-scrub-ready');
    if (restore !== null) { jump(docTop(hero) + restore * mapRunway()); pos = restore; restore = null; }
    else pos = 0;
    vel = 0;
    target = scrollProgress();
    // someone who scrolled on while the video loaded gets the flight from where they are
    paint(pos);
    wake();
  }

  function start() {
    if (state !== 'off' || !eligible()) return;
    // arriving part-way down the page (a hash, or scroll restored without a saved flight) skips
    // the flight entirely
    // (the anchor may not have scrolled yet when this runs, so a fragment counts on its own)
    if (restore === null && (window.scrollY > 4 || location.hash.length > 1)) { state = 'pending'; handoff(false); return; }
    state = 'pending';
    page.classList.add('cvh-scrub-pending');
    setPhase('idle');
    var w = window.innerWidth >= 1440 ? 1920 : 1280;
    if (still) still.src = MEDIA + 'hero-end-' + w + '.jpg';
    fetch(MEDIA + 'hero-flight.json', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (m) {
      M = m;
      video.preload = 'auto';
      video.src = MEDIA + 'hero-flight-' + w + '.mp4';
      video.load();
      if (video.readyState >= 2) ready();
    }).catch(function () { handoff(false); });
  }

  video.addEventListener('loadeddata', ready);
  video.addEventListener('canplay', ready);
  video.addEventListener('progress', ready);
  video.addEventListener('canplaythrough', ready);
  video.addEventListener('error', function () { if (state !== 'done' && state !== 'off') handoff(false); });

  window.addEventListener('scroll', function () {
    if (state === 'pending') {
      // still loading and already past the hero: skip the flight rather than show a half state
      if (scrollProgress() >= 1) handoff(false);
      return;
    }
    if (state !== 'flying') return;
    target = scrollProgress();
    // a fling that reaches the end of the buffer swaps now, before the pin can release
    if (window.scrollY - docTop(hero) >= runway() - 2) { pos = 1; vel = 0; paint(1); handoff(true); return; }
    wake();
  }, { passive: true });

  function leave() { if (state === 'flying' || state === 'pending') handoff(false); }
  window.addEventListener('resize', function () { if (!eligible()) leave(); else if (state === 'flying') { target = scrollProgress(); wake(); } }, { passive: true });
  var onChange = function () { if (!eligible()) leave(); else start(); };
  if (desktop.addEventListener) { desktop.addEventListener('change', onChange); motion.addEventListener('change', onChange); }
  else { desktop.addListener(onChange); motion.addListener(onChange); }

  if (eligible()) start();
  else setPhase('complete');

  window.CVH_FLIGHT = { state: function () { return state; }, progress: function () { return pos; }, manifest: function () { return M; }, runway: mapRunway, glideIn: glideIn };
})();
