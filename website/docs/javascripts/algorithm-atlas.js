/* Shared cases: one choice per dimension, intersection across dimensions. */
(() => {
  'use strict';
  function matches(item, selection) {
    return ['problems', 'methods'].every(group => !selection[group] || item[group].includes(selection[group]));
  }

  function init() {
    const root = document.querySelector('[data-algorithm-atlas]');
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = 'true';
    const page = root.closest('.algo-reader');
    const views = [...root.querySelectorAll('[data-algo-view]')];
    const panels = [...root.querySelectorAll('[data-algo-panel]')];
    const filters = [...page.querySelectorAll('[data-algo-filter]')];
    const items = [...root.querySelectorAll('[data-algo-case]')];
    const params = new URLSearchParams(location.search);
    const selection = {problems: '', methods: ''};
    for (const group of ['problems', 'methods']) {
      const value = params.get(group) || '';
      if (filters.some(button => button.dataset.algoGroup === group && button.dataset.algoFilter === value)) selection[group] = value;
    }
    const hashView = location.hash.slice(1);
    const requestedView = ['problems', 'methods', 'cases'].includes(hashView) ? hashView : params.get('view');
    let view = ['problems', 'methods', 'cases'].includes(requestedView) ? requestedView : 'problems';
    function save() {
      const url = new URL(location.href);
      url.searchParams.set('view', view);
      for (const group of ['problems', 'methods']) {
        if (selection[group]) url.searchParams.set(group, selection[group]);
        else url.searchParams.delete(group);
      }
      if (['#problems', '#methods', '#cases'].includes(url.hash)) url.hash = '';
      history.replaceState(null, '', url);
    }
    function render() {
      views.forEach(anchor => {
        if (anchor.dataset.algoView === view) anchor.setAttribute('aria-current', 'true');
        else anchor.removeAttribute('aria-current');
      });
      panels.forEach(panel => { panel.hidden = panel.dataset.algoPanel !== view; });
      filters.forEach(button => button.setAttribute('aria-pressed', String(selection[button.dataset.algoGroup] === button.dataset.algoFilter)));
      let count = 0;
      items.forEach(item => {
        const metadata = {problems: item.dataset.problems.split(' '), methods: item.dataset.methods.split(' ')};
        item.hidden = !matches(metadata, selection);
        if (!item.hidden) count++;
      });
      const filtered = Boolean(selection.problems || selection.methods);
      page.querySelector('[data-algo-result]').textContent = filtered ? `${count} 个匹配案例` : `${count} 个研究案例`;
      page.querySelector('[data-algo-reset]').disabled = !filtered;
      root.querySelector('[data-algo-empty]').hidden = count !== 0;
    }
    views.forEach(anchor => anchor.addEventListener('click', event => {
      event.preventDefault();
      view = anchor.dataset.algoView;
      render(); save();
    }));
    filters.forEach(button => button.addEventListener('click', () => {
      const group = button.dataset.algoGroup;
      selection[group] = selection[group] === button.dataset.algoFilter ? '' : button.dataset.algoFilter;
      view = 'cases';
      render(); save();
      const toggle = page.querySelector('.dex-rail-toggle');
      if (toggle && toggle.getAttribute('aria-expanded') === 'true') toggle.click();
    }));
    page.querySelector('[data-algo-reset]').addEventListener('click', () => {
      selection.problems = ''; selection.methods = '';
      render(); save();
    });
    page.querySelector('[data-algo-controls]').hidden = false;
    render();
  }
  window.DexTrailAlgorithms = {matches, init};
  init();
  if (typeof document$ !== 'undefined') document$.subscribe(init);
})();
