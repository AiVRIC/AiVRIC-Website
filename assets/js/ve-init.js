/* AiVRIC Visual Enhancement — asset fallback loader
 * Swaps missing brand images for existing site screenshots until
 * the generated assets are dropped into assets/images/brand/.
 * Safe to remove once all brand assets + video files are in place.
 */
(function () {
  /* brand filename → relative path within assets/ */
  var FALLBACK = {
    'Main-Screen-Promo.png':             'images/app/Threat-Score.jpg',
    'CS-Montage-1.png':                  'images/app/Findings-AllFindings.jpg',
    'CS-Montage-2.png':                  'images/app/Findings-dashboard-RiskPipeline.jpg',
    'Threat-Signals-1.png':              'images/app/Attack-Surface-Chart.jpg',
    'RiskOps-Dashboard.png':             'images/app/Findings-dashboard-RiskPipeline.jpg',
  };

  /* Infer the assets/ prefix from the img src so sub-directory pages work */
  function assetBase(src) {
    var m = src.match(/^((?:\.\.\/)+)assets\//);
    return m ? m[1] + 'assets/' : 'assets/';
  }

  function wire(img) {
    var src  = img.getAttribute('src') || '';
    var name = src.split('/').pop().split('?')[0];
    var rel  = FALLBACK[name];
    if (!rel) return;

    var base = assetBase(src);

    function tryFallback() {
      img.onerror = null;
      img.src = base + rel;
      img.style.display = 'block';
    }

    img.onerror = tryFallback;

    /* Already broken (cached 404 before JS ran) */
    if (img.complete && img.naturalWidth === 0 && src) {
      tryFallback();
    }
  }

  function init() {
    var sel = '.ve-vid-frame img, .ve-threat-bg img, .ve-ba-vid-bg img';
    [].forEach.call(document.querySelectorAll(sel), wire);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
