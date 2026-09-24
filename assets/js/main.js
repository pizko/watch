(() => {
  const header = document.querySelector('.site-header');
  const onScroll = () => header?.classList.toggle('scrolled', window.scrollY > 24);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  const menuToggle = document.querySelector('.menu-toggle');
  const closeMenu = () => {
    document.body.classList.remove('menu-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  };
  menuToggle?.addEventListener('click', () => {
    document.body.classList.toggle('menu-open');
    menuToggle.setAttribute('aria-expanded', document.body.classList.contains('menu-open') ? 'true' : 'false');
  });
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', closeMenu));
  addEventListener('keydown', event => {
    if (event.key === 'Escape' && document.body.classList.contains('menu-open')) {
      closeMenu();
      menuToggle?.focus();
    }
  });

  const revealObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: .12 }) : null;
  document.querySelectorAll('.reveal').forEach(el => revealObserver ? revealObserver.observe(el) : el.classList.add('in'));

  document.querySelectorAll('.faq-q').forEach(button => {
    button.addEventListener('click', () => {
      const item = button.closest('.faq-item');
      const open = item.classList.toggle('open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.querySelectorAll('.price-category > button').forEach(button => {
    button.addEventListener('click', () => button.closest('.price-category').classList.toggle('open'));
  });

  // Load media only near the viewport; respect motion and data-saving preferences.
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const videos = [...document.querySelectorAll('video[data-lazy-video]')];
  const active = new Set();
  const automaticPlayback = () => !motion.matches && !connection?.saveData;

  const loadVideo = video => {
    if (video.dataset.loaded) return;
    video.muted = true;
    video.dataset.loaded = 'true';
    video.src = video.dataset.src;
    video.load();
  };
  const playVideo = video => {
    loadVideo(video);
    video.play().catch(() => {
      // Autoplay may be blocked by the browser. The poster remains visible.
    });
  };
  const syncPlayback = () => videos.forEach(video => {
    if (automaticPlayback() && active.has(video) && !document.hidden) playVideo(video);
    else video.pause();
  });

  videos.forEach(video => {
    const frame = video.parentElement;
    const failed = () => {
      // An unloaded video is deliberately dormant, not a failed request.
      if (!video.dataset.loaded) return;
      if (!frame.querySelector('img') && video.poster) {
        const fallback = document.createElement('img');
        fallback.src = video.poster;
        fallback.alt = '';
        frame.prepend(fallback);
      }
      video.hidden = true;
      console.warn('Video unavailable:', video.currentSrc || video.dataset.src);
    };
    video.addEventListener('error', failed);
  });

  if ('IntersectionObserver' in window) {
    const loader = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting && automaticPlayback()) loadVideo(entry.target);
    }), { rootMargin: '240px 0px' });
    const player = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? active.add(entry.target) : active.delete(entry.target));
      syncPlayback();
    }, { threshold: .08 });
    videos.forEach(video => { loader.observe(video); player.observe(video); });
  }
  motion.addEventListener('change', syncPlayback);
  connection?.addEventListener('change', syncPlayback);
  document.addEventListener('visibilitychange', syncPlayback);


  // Update footer year.
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();

/* Плавающая кнопка звонка: прячется, когда на экране контакты или подвал —
   иначе она перекрывает карту и телефон, до которых человек уже долистал. */
const callFab = document.querySelector('.call-fab');

if (callFab && 'IntersectionObserver' in window) {
  const zones = [...document.querySelectorAll('.contact-block, .contact-grid, .site-footer')];
  if (zones.length) {
    const seen = new Set();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? seen.add(entry.target) : seen.delete(entry.target));
      callFab.classList.toggle('is-hidden', seen.size > 0);
    }, { threshold: 0.01 });
    zones.forEach(zone => observer.observe(zone));
  }
}
