/* Fixed chapter navigation; only the active link changes during document scroll. */
for (const rail of document.querySelectorAll('.dex-rail')) {
  const page = rail.closest('.has-dex-rail');
  const toggle = document.createElement('button');
  toggle.type = 'button'; toggle.className = 'dex-rail-toggle';
  toggle.textContent = rail.dataset.topicMode === 'history' ? '年份与标签' : rail.classList.contains('knowledge-tag-rail') ? '标签筛选' : page.classList.contains('dex-knowledge') ? '本页目录' : rail.classList.contains('dex-detail-rail') ? '目录与标签' : '标签筛选';
  rail.id ||= 'dex-reading-rail';
  toggle.setAttribute('aria-controls', rail.id); toggle.setAttribute('aria-expanded', 'false');
  const introduction = rail.classList.contains('knowledge-tag-rail') && page.querySelector('.knowledge-section-purpose,.hand-heading');
  if (introduction) introduction.after(toggle); else page.append(toggle);
  const close = document.createElement('button'); close.type = 'button'; close.className = 'dex-rail-close';
  close.textContent = '×'; close.setAttribute('aria-label', '关闭侧栏'); rail.prepend(close);
  function setOpen(open) { rail.classList.toggle('is-open', open); page.classList.toggle('rail-open', open); toggle.setAttribute('aria-expanded', String(open)); }
  toggle.addEventListener('click', () => setOpen(!rail.classList.contains('is-open')));
  close.addEventListener('click', () => {setOpen(false); toggle.focus();});
  rail.addEventListener('keydown', e => {if (e.key === 'Escape') {setOpen(false); toggle.focus();}});
  rail.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (a && document.getElementById(a.hash.slice(1)) && matchMedia('(max-width:1050px)').matches) setOpen(false);
  });
  const links = [...rail.querySelectorAll('.dex-scroll-nav a')];
  const sections = links.map(a => document.getElementById(a.hash.slice(1)));
  if (!links.length) continue;
  function highlight(index) {
    links.forEach((a, i) => {if (i === index) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');});
  }
  let scheduled = false;
  function sync() {
    scheduled = false;
    let current = 0;
    sections.forEach((section, i) => {if (section && section.getBoundingClientRect().top <= 110) current = i;});
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3) current = links.length - 1;
    highlight(current);
  }
  // A rAF-throttled position check also handles tall sections and fast scrolling.
  window.addEventListener('scroll', () => {if (!scheduled) {scheduled = true; requestAnimationFrame(sync);}}, {passive:true});
  window.addEventListener('resize', sync);
  rail.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || !document.getElementById(a.hash.slice(1))) return;
    if (matchMedia('(max-width:1050px)').matches) setOpen(false);
    // Native anchors retain URL hashes, history, and keyboard navigation.
    requestAnimationFrame(sync);
  });
  new ResizeObserver(sync).observe(page);
  sync();
}
