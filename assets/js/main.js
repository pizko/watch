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
  const manuallyPaused = new Set();
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
      // Autoplay may be blocked by the browser. The poster and play button remain.
      video.closest('[data-video-frame]')?.classList.remove('is-playing');
    });
  };
  const syncPlayback = () => videos.forEach(video => {
    if (automaticPlayback() && active.has(video) && !document.hidden && !manuallyPaused.has(video)) playVideo(video);
    else video.pause();
  });

  videos.forEach(video => {
    const frame = video.parentElement;
    frame.dataset.videoFrame = '';
    const control = document.createElement('button');
    control.className = 'video-control';
    control.type = 'button';
    control.textContent = 'Воспроизвести видео';
    control.setAttribute('aria-label', 'Воспроизвести видео');
    control.addEventListener('click', () => {
      if (video.paused) {
        manuallyPaused.delete(video);
        playVideo(video);
      } else {
        manuallyPaused.add(video);
        video.pause();
      }
    });
    frame.append(control);
    video.addEventListener('playing', () => {
      frame.classList.add('is-playing');
      control.textContent = 'Пауза';
      control.setAttribute('aria-label', 'Приостановить видео');
    });
    video.addEventListener('pause', () => {
      frame.classList.remove('is-playing');
      control.textContent = 'Воспроизвести видео';
      control.setAttribute('aria-label', 'Воспроизвести видео');
    });
    const failed = () => {
      // An unloaded video is deliberately dormant, not a failed request.
      if (!video.dataset.loaded) return;
      frame.classList.remove('is-playing');
      if (!frame.querySelector('img') && video.poster) {
        const fallback = document.createElement('img');
        fallback.src = video.poster;
        fallback.alt = '';
        frame.prepend(fallback);
      }
      video.hidden = true;
      control.disabled = true;
      control.textContent = 'Видео недоступно';
      control.setAttribute('aria-label', 'Видео недоступно');
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

  document.querySelectorAll('[data-demo-form]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const toast = document.querySelector('.toast');
      if (toast) {
        toast.textContent = 'Форма готова. Подключите CRM/почту перед публикацией.';
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3800);
      }
    });
  });

  // Update footer year.
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
