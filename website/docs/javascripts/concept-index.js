/* Search and tags share URL state. Every opened GIF starts and loops itself. */
(() => {
  const init = () => {
    const root = document.querySelector('[data-concept-index]');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = 'true';
    const page = root.closest('.concept-page');
    const links = [...root.querySelectorAll('[data-concept-link]')];
    const entries = [...root.querySelectorAll('.concept-entry')];
    const search = root.querySelector('#concept-search');
    const groups = [...page.querySelectorAll('[data-concept-group]')];
    const formats = [...page.querySelectorAll('[data-concept-format]')];
    const reset = page.querySelector('[data-concept-reset]');
    const empty = root.querySelector('.concept-empty');
    const pagination = root.querySelector('.concept-pagination');
    const previous = root.querySelector('[data-concept-prev]');
    const next = root.querySelector('[data-concept-next]');
    let category = 'all', format = 'all', selected = '', visible = links;
    const normalize = value => value.normalize('NFKC').toLocaleLowerCase().trim();
    const playback = (entry, running) => {
      const image = entry.querySelector('[data-animation]');
      if (!image) return;
      const source = running ? image.dataset.animation : image.dataset.poster;
      if (image.getAttribute('src') !== source) image.src = source;
      const button = entry.querySelector('.concept-play');
      button.setAttribute('aria-pressed', String(running));
      button.textContent = running ? '暂停动图' : '继续播放';
    };
    const persist = (push = false) => {
      const url = new URL(location.href);
      for (const [key, value] of [['q', search.value.trim()], ['group', category === 'all' ? '' : category], ['format', format === 'all' ? '' : format]]) {
        value ? url.searchParams.set(key, value) : url.searchParams.delete(key);
      }
      url.hash = selected;
      if (url.href !== location.href) history[push ? 'pushState' : 'replaceState'](null, '', url);
    };
    const select = (id, focus = false) => {
      const changed = selected !== id;
      selected = id;
      entries.forEach(entry => {
        const active = entry.id === id;
        entry.hidden = !active;
        if (!active) playback(entry, false);
        else {
          entry.querySelector('img').loading = 'eager';
          if (changed) playback(entry, true);
        }
      });
      links.forEach(link => {
        if (link.dataset.conceptLink === id) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
      empty.hidden = Boolean(id);
      pagination.hidden = !id;
      const index = visible.findIndex(link => link.dataset.conceptLink === id);
      previous.disabled = index <= 0;
      next.disabled = index < 0 || index >= visible.length - 1;
      root.querySelector('[data-concept-position]').textContent = (index + 1) + ' / ' + visible.length;
      const activeLink = links.find(link => link.dataset.conceptLink === id);
      if (activeLink) {
        const nav = activeLink.parentElement, item = activeLink.getBoundingClientRect(), box = nav.getBoundingClientRect();
        if (item.top < box.top) nav.scrollTop += item.top - box.top;
        else if (item.bottom > box.bottom) nav.scrollTop += item.bottom - box.bottom;
      }
      if (focus && id) document.getElementById(id).querySelector('h2').focus({preventScroll: true});
    };
    const matches = link => {
      const terms = normalize(search.value).split(/\s+/).filter(Boolean);
      return (category === 'all' || link.dataset.group === category) &&
        (format === 'all' || link.dataset.format === format) &&
        terms.every(term => normalize(link.dataset.search).includes(term));
    };
    const filter = (preferred = selected) => {
      visible = links.filter(link => { link.hidden = !matches(link); return !link.hidden; });
      groups.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.conceptGroup === category)));
      formats.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.conceptFormat === format)));
      root.querySelector('[data-concept-count]').textContent = visible.length + ' 个';
      page.querySelector('[data-concept-result]').textContent = visible.length + ' / ' + links.length + ' 个概念';
      reset.disabled = category === 'all' && format === 'all' && !search.value;
      select(visible.some(link => link.dataset.conceptLink === preferred) ? preferred : visible[0]?.dataset.conceptLink || '');
    };
    const clear = () => { category = format = 'all'; search.value = ''; };
    const navigate = (id, focus = false) => {
      if (!links.some(link => link.dataset.conceptLink === id)) return;
      if (!visible.some(link => link.dataset.conceptLink === id)) { clear(); filter(id); }
      else select(id, focus);
      if (focus) document.getElementById(id).querySelector('h2').focus({preventScroll: true});
      persist(true);
      if (matchMedia('(max-width:760px)').matches) root.querySelector('.concept-directory').open = false;
    };
    const restore = () => {
      const url = new URL(location.href);
      search.value = url.searchParams.get('q') || '';
      const savedGroup = url.searchParams.get('group'), savedFormat = url.searchParams.get('format');
      category = groups.some(button => button.dataset.conceptGroup === savedGroup) ? savedGroup : 'all';
      format = formats.some(button => button.dataset.conceptFormat === savedFormat) ? savedFormat : 'all';
      let id;
      try { id = decodeURIComponent(url.hash.slice(1)); } catch { id = ''; }
      const known = links.find(link => link.dataset.conceptLink === id);
      if (known && !matches(known)) clear();
      filter(id || 'force-closure');
    };
    root.querySelector('.concept-tools').hidden = false;
    root.classList.add('is-enhanced');
    if (matchMedia('(max-width:760px)').matches) root.querySelector('.concept-directory').open = false;
    root.querySelectorAll('.concept-play').forEach(button => {
      button.hidden = false;
      const entry = button.closest('.concept-entry'), image = entry.querySelector('img');
      button.addEventListener('click', () => playback(entry, button.getAttribute('aria-pressed') !== 'true'));
      image.addEventListener('error', () => {
        if (image.getAttribute('src') !== image.dataset.animation) return;
        playback(entry, false);
        button.textContent = '加载失败，重试';
      });
    });
    search.addEventListener('input', () => { filter(); persist(); });
    root.querySelector('[data-concept-clear]').addEventListener('click', () => { search.value = ''; filter(); persist(); search.focus(); });
    reset.addEventListener('click', () => { clear(); filter(); persist(); });
    groups.forEach(button => button.addEventListener('click', () => {
      category = category === button.dataset.conceptGroup ? 'all' : button.dataset.conceptGroup;
      filter(); persist();
    }));
    formats.forEach(button => button.addEventListener('click', () => {
      format = format === button.dataset.conceptFormat ? 'all' : button.dataset.conceptFormat;
      filter(); persist();
    }));
    root.addEventListener('click', event => {
      const anchor = event.target.closest('[data-concept-link], [data-concept-related]');
      if (!anchor || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      navigate(anchor.dataset.conceptLink || anchor.dataset.conceptRelated, Boolean(anchor.dataset.conceptRelated));
    });
    previous.addEventListener('click', () => {
      const index = visible.findIndex(link => link.dataset.conceptLink === selected);
      if (index > 0) navigate(visible[index - 1].dataset.conceptLink);
    });
    next.addEventListener('click', () => {
      const index = visible.findIndex(link => link.dataset.conceptLink === selected);
      if (index + 1 < visible.length) navigate(visible[index + 1].dataset.conceptLink);
    });
    window.addEventListener('popstate', restore);
    window.addEventListener('hashchange', restore);
    restore();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  if (typeof document$ !== 'undefined') document$.subscribe(init);
})();
