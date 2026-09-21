(() => {
  const header = document.querySelector('.site-header');
  const onScroll = () => header?.classList.toggle('scrolled', window.scrollY > 24);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  const menuToggle = document.querySelector('.menu-toggle');
  menuToggle?.addEventListener('click', () => {
    document.body.classList.toggle('menu-open');
    menuToggle.setAttribute('aria-expanded', document.body.classList.contains('menu-open') ? 'true' : 'false');
  });
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-open')));

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
      const answer = item.querySelector('.faq-a');
      const open = item.classList.toggle('open');
      answer.style.maxHeight = open ? answer.scrollHeight + 'px' : '0px';
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.querySelectorAll('.price-category > button').forEach(button => {
    button.addEventListener('click', () => button.closest('.price-category').classList.toggle('open'));
  });

  const preview = document.querySelector('#servicePreviewImage');
  if (preview) {
    document.querySelectorAll('.service-item[data-preview]').forEach(item => {
      item.addEventListener('mouseenter', () => {
        const next = item.dataset.preview;
        if (!next || preview.getAttribute('src') === next) return;
        preview.style.opacity = '0';
        setTimeout(() => {
          preview.src = next;
          preview.onload = () => preview.style.opacity = '1';
        }, 150);
      });
    });
  }

  // Hide broken videos and leave poster/fallback visible.
  document.querySelectorAll('video').forEach(video => {
    video.addEventListener('error', () => { video.style.display = 'none'; });
  });

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
