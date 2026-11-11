/* Progressive enhancement for public research pages. No remote inference. */
(() => {
  'use strict';
  const nav = document.getElementById('site-nav');
  const toggle = document.querySelector('.menu-toggle');
  if (nav) {
    const items = Array.from(nav.querySelectorAll('a'));
    if (!items.some(a => /(^|\/)lab\.html(?:#|$)/.test(a.getAttribute('href') || ''))) {
      const a = document.createElement('a');
      a.href = 'lab.html';
      a.textContent = 'Interactive Lab';
      if (location.pathname.endsWith('/lab.html')) a.setAttribute('aria-current', 'page');
      nav.appendChild(a);
    }
  }
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open', !expanded);
    });
    nav.addEventListener('click', e => {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
  const search = document.getElementById('agent-search');
  const cards = Array.from(document.querySelectorAll('#agent-grid .agent-card'));
  const count = document.getElementById('agent-count');
  if (search && cards.length) {
    const filters = Array.from(document.querySelectorAll('[data-filter]'));
    let group = 'all';
    function apply() {
      const q = search.value.toLowerCase().trim();
      let visible = 0;
      cards.forEach(card => {
        const text = (card.dataset.agent || card.textContent || '').toLowerCase();
        const groupMatch = group === 'all' || (card.dataset.group || '').toLowerCase() === group;
        card.hidden = !(text.includes(q) && groupMatch);
        if (!card.hidden) visible++;
      });
      if (count) count.textContent = 'Showing ' + visible + ' of ' + cards.length + ' specialist roles.';
    }
    filters.forEach(btn => btn.addEventListener('click', () => {
      group = (btn.dataset.filter || 'all').toLowerCase();
      filters.forEach(x => {
        x.classList.toggle('is-active', x === btn);
        x.setAttribute('aria-pressed', String(x === btn));
      });
      apply();
    }));
    search.addEventListener('input', apply);
    apply();
  }
})();