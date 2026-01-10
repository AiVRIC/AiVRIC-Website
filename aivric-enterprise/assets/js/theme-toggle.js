(function(){
  var root = document.documentElement;
  var toggles = document.querySelectorAll('[data-theme-toggle]');

  function setTheme(mode){
    root.setAttribute('data-theme', mode);
    try { localStorage.setItem('aivric-theme', mode); } catch (e) {}
    toggles.forEach(function(btn){
      btn.textContent = mode === 'dark' ? 'Light mode' : 'Dark mode';
    });
  }

  var saved = null;
  try { saved = localStorage.getItem('aivric-theme'); } catch (e) {}
  setTheme(saved || 'light');

  toggles.forEach(function(btn){
    btn.addEventListener('click', function(){
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      setTheme(next);
    });
  });
})();
