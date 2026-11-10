/* The integrations directory (integrations.html): the cards sit in groups in the page's HTML; this filters them by group
   (the tabs), by status (the legend, one at a time, pressed again to clear) and by what's typed in the search, and hides
   any group left empty. */
(function () {
  'use strict';
  var dir = document.getElementById('sx-dir'), tabs = document.getElementById('sx-dir-tabs'), q = document.getElementById('sx-dir-q');
  var legend = document.getElementById('sx-dir-legend'), empty = document.getElementById('sx-dir-empty'), count = document.getElementById('sx-dir-count');
  if (!dir || !tabs || !q || !window.SX) return;
  var groups = [].slice.call(dir.querySelectorAll('.sx-int-group'));
  var cards = [].slice.call(dir.querySelectorAll('.sx-int')), keys = legend ? [].slice.call(legend.querySelectorAll('[data-status]')) : [];
  var cat = 'all', status = '';
  function apply() {
    var term = q.value.trim().toLowerCase(), shown = 0;
    cards.forEach(function (c) {
      var on = (cat === 'all' || c.getAttribute('data-cat') === cat) && (!status || c.getAttribute('data-status') === status)
        && (!term || c.textContent.toLowerCase().indexOf(term) !== -1);
      c.hidden = !on; if (on) shown++;
    });
    groups.forEach(function (g) {
      var n = g.querySelectorAll('.sx-int:not([hidden])').length;
      g.hidden = n === 0; g.querySelector('[data-n]').textContent = n;
    });
    empty.hidden = shown > 0;
    count.textContent = shown === cards.length ? 'All ' + cards.length + ' integrations' : shown + ' of ' + cards.length + ' integrations';
  }
  SX.tabs(tabs, function (key) { cat = key; apply(); });
  keys.forEach(function (k) {
    k.addEventListener('click', function () {
      var s = k.getAttribute('data-status');
      status = status === s ? '' : s;
      keys.forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-status') === status)); });
      apply();
    });
  });
  q.addEventListener('input', apply);
  apply();
})();
