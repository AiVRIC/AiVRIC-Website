/* AiVRIC Visual Enhancement — video reveal v4
 * Videos start at opacity:0 (set in CSS).
 * This script fades each video to opacity:1 once it begins playing.
 * CSS handles all placeholder aesthetics — no fallback images needed.
 * Remove this file once brand videos are in assets/videos/.
 */
(function () {
  function init() {
    [].forEach.call(
      document.querySelectorAll('.ve-vid-frame video, .ve-threat-bg video, .ve-ba-vid-bg video'),
      function (vid) {
        vid.addEventListener('playing', function () {
          vid.style.opacity = '1';
        });
      }
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
