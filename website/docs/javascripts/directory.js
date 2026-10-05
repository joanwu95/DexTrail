/* Filter the complete, server-rendered directory without duplicating its data. */
for (const page of document.querySelectorAll('.dex-report-page')) {
  const input = page.querySelector('[data-directory-search]');
  const items = [...page.querySelectorAll('.hand-directory > ul > li')];
  const status = page.querySelector('.hand-directory-count');
  if (!input || !status) continue;
  const entries = items.map(item => ({item, text: item.textContent.toLocaleLowerCase()}));
  function filter() {
    const query = input.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const entry of entries) {
      entry.item.hidden = !entry.text.includes(query);
      if (!entry.item.hidden) visible++;
    }
    status.textContent = visible ? `显示 ${visible} / ${items.length} 项` : '没有匹配项，请调整关键词';
  }
  input.addEventListener('input', filter);
  filter();
}
