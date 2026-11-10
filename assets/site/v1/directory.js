/* The integrations directory (integrations.html): filter the cards by category and by what's typed in the search.
   The cards are in the page's HTML; this only shows and hides them. */
(function () {
  'use strict';
  var grid = document.getElementById('sx-dir'), tabs = document.getElementById('sx-dir-tabs'), q = document.getElementById('sx-dir-q');
  var empty = document.getElementById('sx-dir-empty'), count = document.getElementById('sx-dir-count');
  if (!grid || !tabs || !q || !window.SX) return;
  var cards = [].slice.call(grid.querySelectorAll('.sx-int')), cat = 'all';
  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c) {
      var on = (cat === 'all' || c.getAttribute('data-cat') === cat) && (!term || c.textContent.toLowerCase().indexOf(term) !== -1);
      c.hidden = !on; if (on) shown++;
    });
    empty.hidden = shown > 0;
    count.textContent = shown + ' of ' + cards.length + ' integrations';
  }
  SX.tabs(tabs, function (key) { cat = key; apply(); });
  q.addEventListener('input', apply);
  apply();
})();
