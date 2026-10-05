/* Static content stays searchable; enhance layer/question selection and case tags. */
(() => {
  const reader = document.querySelector('.tech-explorer');
  if (!reader) return;
  const page = reader.closest('.dex-technologies'), rail = page.querySelector('.tech-rail');
  const panels = [...reader.querySelectorAll('[data-tech-panel]')];
  const layers = [...reader.querySelectorAll('[data-tech-layer]')];
  const groups = Object.fromEntries([...rail.querySelectorAll('[data-tech-group]')].map(b => [b.dataset.techTag, b.dataset.techGroup]));
  const selected = new Set();
  let active, activeQuestion;
  const tagsFor = panel => new Set([...panel.querySelectorAll('[data-tech-case]')].flatMap(item => item.dataset.techTags.split(' ')));
  const availablePanels = new Map(panels.map(panel => [panel.dataset.techPanel, tagsFor(panel)]));

  function writeURL(hash = location.hash) {
    const url = new URL(location.href);
    url.hash = hash;
    url.searchParams.delete('tag');
    selected.forEach(tag => url.searchParams.append('tag', tag));
    history.replaceState(null, '', url);
  }

  function filterCases() {
    const items = [...active.querySelectorAll('[data-tech-case]')];
    let count = 0;
    for (const item of items) {
      const match = window.DexTrailTopics.matches(item.dataset.techTags.split(' '), selected, groups);
      item.hidden = !match;
      if (match) count++;
    }
    for (const control of page.querySelectorAll('[data-tech-tag]')) control.setAttribute('aria-pressed', String(selected.has(control.dataset.techTag)));
    rail.querySelector('.dex-filter-result').textContent = `${count} / ${items.length} 个关联案例${selected.size ? ` · 已选 ${selected.size} 个标签` : ''}`;
    page.querySelectorAll('[data-tech-clear]').forEach(button => {button.disabled = selected.size === 0;});
    active.querySelector('.tech-empty').hidden = count !== 0;
  }

  function selectQuestion(index) {
    const views = [...active.querySelectorAll('[data-tech-view]')];
    activeQuestion = views.some(view => Number(view.dataset.techView) === index) ? index : Number(active.dataset.defaultQuestion);
    views.forEach(view => {view.hidden = Number(view.dataset.techView) !== activeQuestion;});
    active.querySelectorAll('[data-tech-question]').forEach(tab => {
      const current = Number(tab.dataset.techQuestion) === activeQuestion;
      tab.setAttribute('aria-selected', String(current));
      tab.tabIndex = current ? 0 : -1;
    });
  }

  function selectPanel(key, question) {
    const previous = active, previousQuestion = activeQuestion;
    active = panels.find(panel => panel.dataset.techPanel === key) || panels.find(panel => panel.dataset.techPanel === reader.dataset.defaultChapter);
    const id = active.dataset.techPanel, available = availablePanels.get(id);
    panels.forEach(panel => {panel.hidden = panel !== active;});
    layers.forEach(tab => {
      const current = tab.dataset.techLayer === id;
      tab.setAttribute('aria-selected', String(current));
      tab.tabIndex = current ? 0 : -1;
    });
    for (const tag of selected) if (!available.has(tag)) selected.delete(tag);
    for (const button of rail.querySelectorAll('[data-tech-tag]')) button.hidden = !available.has(button.dataset.techTag);
    for (const group of rail.querySelectorAll('[data-tech-tag-group]')) group.hidden = ![...group.querySelectorAll('[data-tech-tag]')].some(b => !b.hidden);
    for (const link of rail.querySelectorAll('[data-tech-anchor]')) link.href = `#route-${id}-${link.dataset.techAnchor}`;
    selectQuestion(question ?? (active === previous ? previousQuestion : Number(active.dataset.defaultQuestion)));
    filterCases();
  }

  function readURL() {
    const url = new URL(location.href), initialTags = url.searchParams.getAll('tag').filter(tag => Object.hasOwn(groups, tag));
    const hash = url.hash.slice(1), match = /^route-([a-z]+)(?:-question-(\d+))?/.exec(hash);
    let key = match && panels.some(p => p.dataset.techPanel === match[1]) ? match[1] : reader.dataset.defaultChapter;
    if (!match && initialTags.length && !initialTags.some(tag => availablePanels.get(key).has(tag))) key = panels.find(p => initialTags.some(tag => availablePanels.get(p.dataset.techPanel).has(tag)))?.dataset.techPanel || key;
    selected.clear();
    initialTags.forEach(tag => selected.add(tag));
    selectPanel(key, match?.[2] !== undefined ? Number(match[2]) : undefined);
    const destination = document.getElementById(hash);
    if (destination && hash) requestAnimationFrame(() => destination.scrollIntoView({block:'start'}));
  }

  reader.classList.add('is-enhanced');
  reader.querySelector('.tech-layers').setAttribute('role', 'tablist');
  layers.forEach(tab => {tab.setAttribute('role', 'tab'); tab.setAttribute('aria-controls', 'route-' + tab.dataset.techLayer);});
  panels.forEach(panel => {
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', 'tech-tab-' + panel.dataset.techPanel);
    panel.querySelector('.tech-questions').setAttribute('role', 'tablist');
    panel.querySelectorAll('[data-tech-question]').forEach(tab => {
      tab.setAttribute('role', 'tab');
      tab.id = `${panel.id}-question-tab-${tab.dataset.techQuestion}`;
      tab.setAttribute('aria-controls', `${panel.id}-question-${tab.dataset.techQuestion}`);
    });
    panel.querySelectorAll('[data-tech-view]').forEach(view => {
      view.setAttribute('role', 'tabpanel');
      view.setAttribute('aria-labelledby', `${panel.id}-question-tab-${view.dataset.techView}`);
    });
  });
  page.querySelectorAll('[data-tech-tag]').forEach(button => {button.disabled = false;});
  readURL();

  page.addEventListener('click', event => {
    const layer = event.target.closest('[data-tech-layer]'), question = event.target.closest('[data-tech-question]');
    const tag = event.target.closest('[data-tech-tag]'), clear = event.target.closest('[data-tech-clear]');
    if (layer || question) {
      event.preventDefault();
      if (layer) {selected.clear(); selectPanel(layer.dataset.techLayer);} else selectQuestion(Number(question.dataset.techQuestion));
      writeURL(layer ? '#route-' + active.dataset.techPanel : `#route-${active.dataset.techPanel}-question-${activeQuestion}`);
    }
    if (tag) {
      const value = tag.dataset.techTag;
      selected.has(value) ? selected.delete(value) : selected.add(value);
      filterCases(); writeURL();
    }
    if (clear) {selected.clear(); filterCases(); writeURL();}
    if (event.target.closest('[data-tech-anchor]') && rail.classList.contains('is-open')) rail.querySelector('.dex-rail-close').click();
  });
  reader.addEventListener('keydown', event => {
    const tab = event.target.closest('[role="tab"]');
    if (!tab) return;
    if (event.key === ' ') {event.preventDefault(); tab.click(); return;}
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    const tabs = [...tab.parentElement.querySelectorAll('[role="tab"]')], index = tabs.indexOf(tab);
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    tabs[next].click(); tabs[next].focus();
  });
  window.addEventListener('hashchange', readURL);
  window.addEventListener('popstate', readURL);
})();
