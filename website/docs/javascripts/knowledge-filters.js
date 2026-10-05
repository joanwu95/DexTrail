/* OR within a topic group, AND across groups, matching the product map. */
(() => {
  function matches(own, selected, groups) {
    const available = new Set(own), grouped = new Map();
    for (const tag of selected) {
      if (!Object.hasOwn(groups, tag)) return false;
      const group = groups[tag];
      if (!grouped.has(group)) grouped.set(group, []);
      grouped.get(group).push(tag);
    }
    return [...grouped.values()].every(tags => tags.some(tag => available.has(tag)));
  }
  window.DexTrailTopics = {matches};
  const rail = document.querySelector('.knowledge-tag-rail');
  if (!rail || !['filter', 'history'].includes(rail.dataset.topicMode)) return;
  const page = rail.closest('.has-dex-rail');
  const items = [...page.querySelectorAll('[data-topic-item]')];
  const controls = [...page.querySelectorAll('[data-topic-tag]')];
  const groups = Object.fromEntries([...rail.querySelectorAll('[data-topic-group]')].map(button => [button.dataset.topicTag, button.dataset.topicGroup]));
  const selected = new Set(new URLSearchParams(location.search).getAll('tag').filter(tag => Object.hasOwn(groups, tag)));
  const summary = rail.querySelector('.dex-filter-result'), clear = rail.querySelector('[data-topic-clear]');
  const yearNav = rail.querySelector('.history-year-nav');
  const years = [...page.querySelectorAll('[data-history-year]')];
  const yearLinks = yearNav ? [...yearNav.querySelectorAll('[data-history-link]')] : [];
  let scheduled = false;
  function syncYears() {
    scheduled = false;
    const visible = years.filter(row => !row.hidden);
    let current = visible[0];
    for (const row of visible) {
      if (row.getBoundingClientRect().top <= 110) current = row;
    }
    const visibleYears = new Set(visible.map(row => row.dataset.historyYear));
    for (const link of yearLinks) {
      link.hidden = !visibleYears.has(link.dataset.historyLink);
      const active = current && current.dataset.historyYear === link.dataset.historyLink;
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
      // Scroll just the directory, without moving the timeline or keyboard focus.
      if (active) {
        const rect = link.getBoundingClientRect(), container = yearNav.getBoundingClientRect();
        if (rect.top < container.top) yearNav.scrollTop += rect.top - container.top;
        else if (rect.bottom > container.bottom) yearNav.scrollTop += rect.bottom - container.bottom;
      }
    }
    const emptyYears = rail.querySelector('.history-year-empty');
    if (emptyYears) emptyYears.hidden = visible.length !== 0;
    if (yearNav) yearNav.hidden = !visible.length;
  }
  function scheduleYears() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(syncYears); }
  }
  if (yearNav) {
    window.addEventListener('scroll', scheduleYears, {passive: true});
    window.addEventListener('resize', scheduleYears);
    window.addEventListener('hashchange', scheduleYears);
    new ResizeObserver(scheduleYears).observe(page);
  }
  function apply() {
    let count = 0;
    for (const item of items) {
      const visible = matches(item.dataset.topicTags.split(' '), selected, groups);
      item.hidden = !visible;
      if (visible) count++;
    }
    for (const row of page.querySelectorAll('.history-year')) row.hidden = ![...row.querySelectorAll('[data-topic-item]')].some(item => !item.hidden);
    const timeline = page.querySelector('.history-scroll');
    if (timeline) timeline.hidden = !count;
    for (const control of controls) control.setAttribute('aria-pressed', String(selected.has(control.dataset.topicTag)));
    summary.textContent = `${count} / ${items.length} ${rail.dataset.topicUnit}${selected.size ? ` · 已选 ${selected.size} 个标签` : ''}`;
    clear.disabled = !selected.size;
    const empty = page.querySelector('.knowledge-filter-empty');
    if (empty) empty.hidden = count !== 0;
    const spread = page.querySelector('.route-spread');
    if (spread) spread.classList.toggle('is-filtered', count === 1);
    if (yearNav) scheduleYears();
  }
  for (const button of controls) button.addEventListener('click', () => {
    const tag = button.dataset.topicTag;
    if (selected.has(tag)) selected.delete(tag); else selected.add(tag);
    apply();
  });
  clear.addEventListener('click', () => {selected.clear(); apply();});
  apply();
})();
