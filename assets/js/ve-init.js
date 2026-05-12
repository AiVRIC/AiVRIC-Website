/* AiVRIC Visual Enhancement — asset fallback loader v3
 * Three scenarios handled:
 *   A) Frame has <img> before <video> (old) — now fixed to video-first in HTML
 *   B) Frame has <video> then <img> — img on top as fallback; fade on playing
 *   C) Frame has <video> only — inject proxy img after video; fade on playing
 * Remove this file once assets/images/brand/ + assets/videos/ are populated.
 */
(function () {
  /* brand filename → path relative to assets/ */
  var FALLBACK = {
    'Main-Screen-Promo.png':  'images/app/Threat-Score.jpg',
    'CS-Montage-1.png':       'images/app/Findings-AllFindings.jpg',
    'CS-Montage-2.png':       'images/app/Findings-dashboard-RiskPipeline.jpg',
    'Threat-Signals-1.png':   'images/app/Attack-Surface-Chart.jpg',
    'RiskOps-Dashboard.png':  'images/app/Findings-dashboard-RiskPipeline.jpg',
  };

  /* Detect assets/ prefix from a src string (handles ../../ subdirectory pages) */
  function assetBase(src) {
    var m = (src || '').match(/^((?:\.\.\/)+)assets\//);
    return m ? m[1] + 'assets/' : 'assets/';
  }

  function fname(src) {
    return (src || '').split('/').pop().split('?')[0];
  }

  function fadeOut(el) {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
  }

  /* ── 1. Wire <img> elements — swap to fallback on 404 ────────────────── */
  function wireImg(img) {
    var src = img.getAttribute('src') || '';
    var rel = FALLBACK[fname(src)];
    if (!rel) return;
    var base = assetBase(src);

    function swap() {
      img.onerror = null;
      img.src = base + rel;
    }
    img.onerror = swap;
    /* Already broken (cached 404 before script ran) */
    if (img.complete && img.naturalWidth === 0 && src) swap();
  }

  /* ── 2. For frames with video + img sibling: fade img when video plays ── */
  function wireFadeOnPlay(vid) {
    var frame = vid.closest
      ? vid.closest('.ve-vid-frame, .ve-threat-bg, .ve-ba-vid-bg')
      : null;
    if (!frame) return;
    var img = frame.querySelector('img:not([data-ve-bg])');
    if (!img) return;
    vid.addEventListener('playing', function () { fadeOut(img); });
  }

  /* ── 3. Wire <video>-only frames — inject proxy img after video ───────── */
  function wireVideo(vid) {
    var frame = vid.closest
      ? vid.closest('.ve-vid-frame, .ve-threat-bg, .ve-ba-vid-bg')
      : null;
    if (!frame) return;

    /* Skip frames that already have a non-proxy img — wireFadeOnPlay handles those */
    if (frame.querySelector('img:not([data-ve-bg])')) return;

    /* Determine fallback from poster or source src */
    var poster  = vid.getAttribute('poster') || '';
    var srcEl   = vid.querySelector('source[src]');
    var vidSrc  = srcEl ? (srcEl.getAttribute('src') || '') : (vid.getAttribute('src') || '');
    var rel     = FALLBACK[fname(poster)] || FALLBACK[fname(vidSrc)];
    if (!rel) return;

    var base = assetBase(poster || vidSrc);

    /* Insert proxy img AFTER video so DOM order puts it above video (z-index:auto) */
    var img = document.createElement('img');
    img.setAttribute('data-ve-bg', '1');
    img.alt = '';
    img.src = base + rel;

    if (vid.nextSibling) {
      vid.parentNode.insertBefore(img, vid.nextSibling);
    } else {
      vid.parentNode.appendChild(img);
    }

    vid.addEventListener('playing', function () { fadeOut(img); });
  }

  function init() {
    var sel = '.ve-vid-frame, .ve-threat-bg, .ve-ba-vid-bg';

    /* Wire fallback swap for all brand <img> elements */
    var imgs = document.querySelectorAll(
      '.ve-vid-frame img:not([data-ve-bg]), .ve-threat-bg img:not([data-ve-bg]), .ve-ba-vid-bg img:not([data-ve-bg])'
    );
    [].forEach.call(imgs, wireImg);

    /* Wire all videos */
    var vids = document.querySelectorAll(
      '.ve-vid-frame video, .ve-threat-bg video, .ve-ba-vid-bg video'
    );
    [].forEach.call(vids, function (vid) {
      wireFadeOnPlay(vid);  /* fade existing img sibling when video plays */
      wireVideo(vid);       /* inject proxy img for video-only frames */
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
