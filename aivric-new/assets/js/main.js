(() => {
  const body = document.body;
  const menuToggle = document.querySelector('[data-menu-toggle]');
  const menuClose = document.querySelector('[data-menu-close]');
  const menuOverlay = document.querySelector('[data-menu-overlay]');
  const mobileMenu = document.querySelector('#mobile-menu');

  const setMenuState = (isOpen) => {
    body.classList.toggle('menu-open', isOpen);
    if (menuToggle) {
      menuToggle.setAttribute('aria-expanded', String(isOpen));
    }
    if (mobileMenu) {
      mobileMenu.setAttribute('aria-hidden', String(!isOpen));
    }
  };

  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      setMenuState(!body.classList.contains('menu-open'));
    });
  }

  if (menuClose) {
    menuClose.addEventListener('click', () => setMenuState(false));
  }

  if (menuOverlay) {
    menuOverlay.addEventListener('click', () => setMenuState(false));
  }

  const accordionButtons = document.querySelectorAll('[data-accordion-toggle]');
  accordionButtons.forEach((button) => {
    const targetId = button.getAttribute('aria-controls');
    const panel = targetId ? document.getElementById(targetId) : null;
    button.addEventListener('click', () => {
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!isExpanded));
      if (panel) {
        panel.hidden = isExpanded;
      }
    });
  });

  const dropdownButtons = document.querySelectorAll('[data-dropdown-toggle]');
  const closeDropdowns = () => {
    dropdownButtons.forEach((button) => {
      button.setAttribute('aria-expanded', 'false');
      const item = button.closest('.nav-item');
      if (item) {
        item.classList.remove('is-open');
      }
    });
  };

  dropdownButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.stopPropagation();
      const item = button.closest('.nav-item');
      const isOpen = item ? item.classList.contains('is-open') : false;
      closeDropdowns();
      if (item && !isOpen) {
        item.classList.add('is-open');
        button.setAttribute('aria-expanded', 'true');
      }
    });
  });

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav-item')) {
      closeDropdowns();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setMenuState(false);
      closeDropdowns();
    }
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 }
    );

    document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
  }
})();
