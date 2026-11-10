/* The two-desk opener: one shared first frame, two flights (docs/build-sheet.md).
   At scroll 0 the hero is the wide room with a label on each desk. The pointer over a desk (or focus on its label)
   lights it: the hero copy and the header actions become that edition's. The first scroll, a click on a label or a
   key that scrolls picks the lit desk: that edition's sections (read from its own page, so the copy lives in one
   place) go in under the hero, its content becomes window.CVH_CONTENT with that desk's flight, and the engine starts.
   The choice is remembered; ?door=enterprise or ?door=clients (the nav links) overrides it. Phones and reduced motion
   have no flight: the remembered door goes in at once, and the other label reloads the page on that door.
   Picking the other desk after the engine has started reloads on that door; the engine runs once per page load. */
(function () {
  'use strict';

  var page = document.querySelector('.cvh-page');
  var hero = page && page.querySelector('.cvh-hero');
  if (!page || !hero) return;

  // every path is absolute, from where this script sits (assets/cv-hero/v1/), so the page works at any depth (the site root)
  var here = document.currentScript && document.currentScript.src;
  var ROOT = here ? new URL('./', here).href : '../assets/cv-hero/v1/';
  var SITE = new URL('../../../', new URL(ROOT, location.href)).href;
  // fx, fy: the desk on the 16:9 frame, where the light centres; zone: the desk and its laptop, where the pointer lights it
  var DOORS = {
    enterprise: { page: SITE + 'enterprise/', flight: ROOT + 'media-enterprise/', mobile: ROOT + 'media-enterprise/poster-mobile.webp',
      fx: 0.308, fy: 0.675, zone: [0.12, 0.47, 0.5, 1] },
    clients: { page: SITE + 'providers/', flight: ROOT + 'flight-clients/', mobile: ROOT + 'flight-clients/poster-mobile.webp',
      fx: 0.695, fy: 0.675, zone: [0.53, 0.875, 0.5, 1] }
  };
  var KEY = 'cvh.door';
  var FRAME = { w: 1920, h: 1080 };

  var pin = hero.querySelector('[data-cvh-hero-pin]');
  var copy = hero.querySelector('.cvh-hero-content');
  var shade = hero.querySelector('.cvh-door-shade');
  var mobileSrc = hero.querySelector('[data-door-mobile]');
  var labels = [].slice.call(hero.querySelectorAll('.cvh-door[data-door]'));
  var actions = document.querySelector('.mnav-actions');
  var sheetCta = document.querySelector('.mnav-sheet-cta');
  var desktop = matchMedia('(min-width: 1024px)');
  var motion = matchMedia('(prefers-reduced-motion: reduce)');

  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}

  function norm(d) { return d === 'clients' || d === 'providers' ? 'clients' : d === 'enterprise' ? 'enterprise' : null; }
  var asked = norm(new URLSearchParams(location.search).get('door'));
  var saved = null;
  try { saved = norm(localStorage.getItem(KEY)); } catch (e) {}
  var lit = asked || saved || 'enterprise';
  var committed = false, started = false;

  document.body.classList.add('cvh-door-waiting');

  /* ---- both editions, read from their own pages --------------------------------------------- */
  function text(url) { return fetch(url, { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw new Error(url + ' ' + r.status); return r.text(); }); }
  // the edition's relative URLs are relative to its own page; make them absolute before they move into this one
  function abs(v, base) { return /^(#|[a-z][a-z0-9+.-]*:|\/\/)/i.test(v) ? v : new URL(v, base).href; }
  function rebase(doc, base) {
    ['src', 'href', 'poster', 'data-film', 'data-captions', 'data-src'].forEach(function (a) {
      [].slice.call(doc.querySelectorAll('[' + a + ']')).forEach(function (e) { var v = e.getAttribute(a); if (v && v.charAt(0) !== '?') e.setAttribute(a, abs(v, base)); });
    });
    [].slice.call(doc.querySelectorAll('[srcset]')).forEach(function (e) {
      e.setAttribute('srcset', e.getAttribute('srcset').split(',').map(function (p) { p = p.trim().split(/\s+/); p[0] = abs(p[0], base); return p.join(' '); }).join(', '));
    });
  }
  function edition(d) {
    var base = DOORS[d].page;
    return Promise.all([text(base), text(base + 'content.js')]).then(function (r) {
      var doc = new DOMParser().parseFromString(r[0], 'text/html');
      rebase(doc, base);
      var shim = {};
      // content.js assigns window.CVH_CONTENT; run it against a stand-in so the two editions never collide
      new Function('window', r[1])(shim);
      if (shim.CVH_CONTENT && shim.CVH_CONTENT.media) shim.CVH_CONTENT.media = abs(shim.CVH_CONTENT.media, base);
      var srcPage = doc.querySelector('.cvh-page'), srcHero = srcPage && srcPage.querySelector('.cvh-hero');
      var sections = [], n = srcHero && srcHero.nextElementSibling;
      for (; n; n = n.nextElementSibling) sections.push(n);
      var q = function (s) { var e = doc.querySelector(s); return e ? e.innerHTML : null; };
      var desc = doc.querySelector('meta[name="description"]');
      return {
        content: shim.CVH_CONTENT || {}, sections: sections, hero: q('.cvh-hero-content'),
        actions: q('.mnav-actions'), sheetCta: q('.mnav-sheet-cta'),
        title: doc.title, desc: desc ? desc.getAttribute('content') : ''
      };
    });
  }
  var data = {};
  var ready = Promise.all([edition('enterprise'), edition('clients')]).then(function (r) {
    data.enterprise = r[0]; data.clients = r[1];
    light(lit, true);
    return data;
  });
  ready.catch(function (e) {
    // without the editions there is nothing to fly into: the labels stay plain links to the two pages
    try { console.warn('door: editions not loaded, the labels link to the pages instead.', e); } catch (x) {}
    document.body.classList.remove('cvh-door-waiting');
    page.classList.add('cvh-door-static');
  });

  /* ---- where things sit on the frame (object-fit: cover) ---------------------------------- */
  function geo() {
    var r = pin.getBoundingClientRect(), W = r.width, H = r.height;
    var s = Math.max(W / FRAME.w, H / FRAME.h), fw = FRAME.w * s, fh = FRAME.h * s;
    return { r: r, x: function (f) { return (W - fw) / 2 + f * fw; }, y: function (f) { return (H - fh) / 2 + f * fh; } };
  }
  // the light follows the lit desk (the switch itself sits centred on the floor, in CSS)
  function place() {
    if (!desktop.matches) return;
    var g = geo();
    if (!g.r.width || !g.r.height) return;     // between layouts (the pin has no box for a moment at the pick)
    var d = DOORS[lit];
    page.style.setProperty('--cvh-door-x', g.x(d.fx).toFixed(1) + 'px');
    page.style.setProperty('--cvh-door-y', g.y(d.fy - 0.08).toFixed(1) + 'px');
  }

  /* ---- lighting a desk ------------------------------------------------------------------- */
  function light(d, force) {
    if (!DOORS[d] || (d === lit && !force)) return;
    lit = d;
    page.setAttribute('data-door', d);
    labels.forEach(function (a) {
      var on = a.getAttribute('data-door') === d;
      a.classList.toggle('is-lit', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    if (mobileSrc) mobileSrc.setAttribute('srcset', DOORS[d].mobile);
    if (!committed) { dress(d); warm(d); }   // only the lit desk's flight is warmed: its manifest and its last frame
    place();
  }
  // the hero copy and the header actions become that edition's
  function dress(d) {
    var ed = data[d];
    if (!ed) return;
    if (ed.hero != null && copy) copy.innerHTML = ed.hero;
    if (ed.actions != null && actions) actions.innerHTML = ed.actions;
    if (ed.sheetCta != null && sheetCta) sheetCta.innerHTML = ed.sheetCta;
  }
  var warmed = {};
  function warm(d) {
    if (warmed[d] || !desktop.matches || motion.matches) return;
    warmed[d] = true;
    var w = window.innerWidth >= 1440 ? 1920 : 1280;
    fetch(DOORS[d].flight + 'hero-flight.json', { cache: 'no-store' }).catch(function () {});
    new Image().src = DOORS[d].flight + 'hero-end-' + w + '.jpg';
  }

  /* ---- picking it -------------------------------------------------------------------------- */
  function go(d) { location.href = location.pathname + '?door=' + d; }
  function load(srcs, done) {
    var left = srcs.length;
    srcs.forEach(function (src) {
      var s = document.createElement('script');
      s.src = src;
      s.async = false;          // in order: the flight, then the engine, as the edition pages load them
      s.onload = s.onerror = function () { if (--left === 0 && done) done(); };
      document.body.appendChild(s);
    });
  }
  function rerun(root) {
    // inline scripts in the sections (the film's caption fallback) do not run when inserted; recreate them
    [].slice.call(root.querySelectorAll ? root.querySelectorAll('script') : []).forEach(function (old) {
      var s = document.createElement('script');
      if (old.src) s.src = old.getAttribute('src'); else s.textContent = old.textContent;
      old.replaceWith(s);
    });
  }
  function commit(d, after) {
    d = DOORS[d] ? d : lit;
    if (committed) { if (d !== lit) go(d); else if (after) after(); return; }
    committed = true;
    light(d);
    ready.then(function () {
      var ed = data[d];
      dress(d);          // a pick made before the editions arrived (phones, a reload mid-flight) still gets its own copy
      window.CVH_CONTENT =Object.assign({}, ed.content, { flight: DOORS[d].flight });
      var at = hero;
      ed.sections.forEach(function (n) {
        var c = document.importNode(n, true);
        at.after(c);
        at = c;
        rerun(c);
      });
      document.title = ed.title;
      var meta = document.querySelector('meta[name="description"]');
      if (meta && ed.desc) meta.setAttribute('content', ed.desc);
      document.body.classList.remove('cvh-door-waiting');
      try { localStorage.setItem(KEY, d); } catch (e) {}
      load([ROOT + 'cvh-scrub.js', ROOT + 'cvh.js'], function () {
        // the flight has put its own hero layout on by now (or skipped to the still); the opener's can go
        page.classList.remove('cvh-door-open');
        started = true;
        place();
        window.dispatchEvent(new Event('cvh:door'));
        if (after) after();
      });
    }, function () { location.href = DOORS[d].page; });
  }

  /* ---- input --------------------------------------------------------------------------------- */
  function zoneAt(cx, cy) {
    var g = geo(), x = cx - g.r.left, y = cy - g.r.top;
    for (var d in DOORS) {
      var z = DOORS[d].zone;
      if (x >= g.x(z[0]) && x <= g.x(z[1]) && y >= g.y(z[2]) && y <= g.y(z[3])) return d;
    }
    return null;
  }
  hero.addEventListener('pointermove', function (e) {
    if (committed || e.pointerType === 'touch') return;
    var d = zoneAt(e.clientX, e.clientY);
    if (d) light(d);
  });
  labels.forEach(function (a) {
    var d = a.getAttribute('data-door');
    a.addEventListener('pointerenter', function () { if (!committed) light(d); });
    a.addEventListener('focus', function () { if (!committed) light(d); });
    a.addEventListener('click', function (e) {
      if (page.classList.contains('cvh-door-static')) return;      // plain link to the page
      e.preventDefault();
      commit(d);
    });
  });
  // the nav's two Vision links
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="?door="]');
    if (a) {
      var d = norm(a.getAttribute('href').slice(6));
      if (!d) return;
      e.preventDefault();
      if (committed) { if (d !== lit) go(d); else window.scrollTo(0, 0); }
      else commit(d);
      return;
    }
    // an in-page link in the hero copy (#two-ways) before the sections are in: put them in, then follow it
    var h = !committed && e.target.closest && e.target.closest('.cvh-hero a[href^="#"]');
    if (h) {
      e.preventDefault();
      var hash = h.getAttribute('href');
      commit(lit, function () { location.hash = hash; });
    }
  });
  // the first scroll picks the lit desk; it is spent on the choice, so the flight starts from its first frame
  var SCROLL_KEYS = { ArrowDown: 1, PageDown: 1, End: 1, ' ': 1, Spacebar: 1 };
  window.addEventListener('wheel', function (e) {
    if (committed || e.deltaY <= 0 || e.ctrlKey) return;
    e.preventDefault();
    commit(lit);
  }, { passive: false });
  window.addEventListener('keydown', function (e) {
    if (committed || !SCROLL_KEYS[e.key] || e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(t.tagName) || (e.key === ' ' && t.tagName === 'A'))) return;
    e.preventDefault();
    commit(lit);
  });
  window.addEventListener('scroll', function () { if (!committed && window.scrollY > 0) commit(lit); }, { passive: true });
  addEventListener('resize', place);
  if (window.ResizeObserver) new ResizeObserver(place).observe(pin);

  // straight in: phones and reduced motion (no flight to choose), or a reload in the middle of a flight
  var midFlight = false;
  try {
    var nav = performance.getEntriesByType('navigation')[0];
    midFlight = nav && nav.type === 'reload' && sessionStorage.getItem('cvh.hero.flight') !== null;
  } catch (e) {}
  light(lit, true);
  if (!desktop.matches || motion.matches || midFlight) commit(lit);
  // a window narrowed to phone width before a pick has no flight to choose either
  var noFlight = function () { if (!committed && (!desktop.matches || motion.matches)) commit(lit); };
  if (desktop.addEventListener) { desktop.addEventListener('change', noFlight); motion.addEventListener('change', noFlight); }

  window.CVH_DOOR = { lit: function () { return lit; }, light: light, commit: commit, committed: function () { return committed; }, started: function () { return started; } };
})();
