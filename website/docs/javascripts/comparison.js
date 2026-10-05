/* Same-tab shortlist; explicit URL selections take precedence over stored selections. */
(() => {
  const key = 'dextrail-comparison:v2';
  const views = {
    all: {label: '完整对比', rows: null},
    mechanics: {label: '机械构型', rows: ['version', 'fingers', 'dof', 'actuators', 'mechanics', 'drive', 'weight']},
    sensing: {label: '感知与力控', rows: ['version', 'sensing', 'control', 'capability']},
    software: {label: '仿真与开发', rows: ['version', 'sdk', 'models', 'control']},
  };
  const clean = value => ({
    ids: [...new Set(Array.isArray(value?.ids) ? value.ids.filter(id => typeof id === 'string' && /^[a-z0-9-]+$/.test(id)) : [])].slice(0, 3),
    view: Object.hasOwn(views, value?.view) ? value.view : 'all',
    differences: value?.differences === true,
  });
  function read() {try {return clean(JSON.parse(sessionStorage.getItem(key)));} catch {return clean(null);}}
  function save(value) {const next = clean(value); try {sessionStorage.setItem(key, JSON.stringify(next));} catch {} return next;}
  function add(value, id) {
    const next = clean(value);
    if (typeof id !== 'string' || !/^[a-z0-9-]+$/.test(id)) return {state: next, result: 'invalid'};
    if (next.ids.includes(id)) return {state: next, result: 'present'};
    if (next.ids.length === 3) return {state: next, result: 'full'};
    next.ids.push(id); return {state: clean(next), result: 'added'};
  }
  window.DexTrailCompare = {read, save, add};
  for (const link of document.querySelectorAll('[data-compare-hand]')) {
    const current = read(), id = link.dataset.compareHand;
    if (current.ids.includes(id)) link.textContent = '返回当前技术对比 ↗';
    else if (current.ids.length === 3) link.textContent = '查看已选对比 · 已满 3 款 ↗';
    else if (current.ids.length) link.textContent = '加入当前对比 ↗';
  }
  const root = document.querySelector('#dex-comparison');
  if (!root) return;
  const status = root.querySelector('.compare-status'), picker = root.querySelector('#compare-product');
  const search = root.querySelector('#compare-search'), selected = root.querySelector('.compare-selected');
  const output = root.querySelector('.compare-table-scroll'), modes = root.querySelector('.compare-modes');
  const differences = root.querySelector('#compare-differences'), explanation = root.querySelector('.compare-view-note');
  const node = (tag, text, cls) => {const e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e;};
  const safeURL = value => {try {const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.href : null;} catch {return null;}};
  fetch(root.dataset.source).then(response => {if (!response.ok) throw new Error('data'); return response.json();}).then(data => {
    const hands = new Map(data.hands.map(h => [h.id, h]));
    let state = read(), notice = '';
    function fromURL() {
      const params = new URL(location.href).searchParams; state = read();
      if (params.has('hands')) state.ids = params.get('hands').split(',');
      if (params.has('view')) state.view = params.get('view');
      if (params.has('differences')) state.differences = params.get('differences') === '1';
      state = clean(state); state.ids = state.ids.filter(id => hands.has(id)); notice = '';
      if (params.has('add') && hands.has(params.get('add'))) {
        const result = add(state, params.get('add')); state = result.state;
        if (result.result === 'full') notice = '已有三款；请先移除一款，再添加新产品。';
      }
    }
    function options() {
      const previous = picker.value, term = search.value.trim().toLocaleLowerCase(); picker.replaceChildren();
      for (const h of data.hands.filter(h => !state.ids.includes(h.id) && h.name.toLocaleLowerCase().includes(term))) {
        const option = node('option', h.name); option.value = h.id; picker.append(option);
      }
      if (!picker.options.length) {const option = node('option', '没有匹配的可选产品'); option.value = ''; picker.append(option);}
      if ([...picker.options].some(option => option.value === previous)) picker.value = previous;
      root.querySelector('[type="submit"]').disabled = !picker.value || state.ids.length >= 3;
    }
    // Flags describe textual records and review needs, not performance or equivalence.
    function flags(row) {
      const cells = state.ids.map(id => hands.get(id).cells[row.id]);
      const incomplete = cells.some(c => !c.sources.length || c.value === '尚未核实' || /待核实$/.test(c.value));
      const different = new Set(cells.map(c => JSON.stringify([c.value, c.scope]))).size > 1;
      return {incomplete, different, boundary: ['dof', 'actuators', 'weight'].includes(row.id) && different};
    }
    function addCell(td, cell, row) {
      const paragraphs = cell.value.split(/\n\s*\n/), first = paragraphs[0];
      let short = first;
      if (first.length > 150) {const end = first.indexOf('。'); short = end > 0 && end < 150 ? first.slice(0, end + 1) : first.slice(0, 150) + '…';}
      if (row.id === 'sdk') short = paragraphs.slice(0, 3).join('\n');
      if (row.id === 'models') short = paragraphs.map(p => p.split('：')[0]).join('\n');
      if (['sensing', 'control'].includes(row.id)) short = cell.value;
      td.append(node('p', short, cell.value === '尚未核实' ? 'compare-unknown' : 'compare-primary'));
      if (cell.scope) td.append(node('p', cell.scope, 'compare-scope'));
      if (paragraphs.length > 1 || short !== cell.value || cell.explanations?.length) {
        const detail = node('details'); detail.append(node('summary', '完整记录与技术解释'), node('p', cell.value));
        for (const e of cell.explanations || []) detail.append(node('strong', (e.kind === 'interpretation' ? '工程解读 · ' : '资料说明 · ') + e.title), node('p', e.text));
        td.append(detail);
      }
      const refs = [...new Map(cell.sources.filter(s => safeURL(s.url)).map(s => [s.url, s])).values()];
      if (refs.length) {
        const detail = node('details'); detail.append(node('summary', '依据与版本'));
        for (const s of refs) {const p = node('p'), a = node('a', s.title || '原始资料'); a.href = safeURL(s.url); a.target = '_blank'; a.rel = 'noopener'; p.append(a); if (s.version) p.append(node('small', s.version)); if (s.verified_on) p.append(node('small', '来源核查：' + s.verified_on)); detail.append(p);}
        td.append(detail);
      }
    }
    function render(updateURL = true) {
      state = save(state);
      if (updateURL) {
        const url = new URL(location.href); url.searchParams.delete('add');
        url.searchParams.set('hands', state.ids.join(',')); url.searchParams.set('view', state.view);
        url.searchParams.set('differences', state.differences ? '1' : '0'); history.replaceState(null, '', url);
      }
      selected.replaceChildren();
      state.ids.forEach(id => {const button = node('button', hands.get(id).name + ' ×', 'compare-chip'); button.type = 'button'; button.setAttribute('aria-label', '移除 ' + hands.get(id).name); button.onclick = () => {state.ids = state.ids.filter(x => x !== id); notice = ''; render(); search.focus();}; selected.append(button);});
      for (const button of modes.querySelectorAll('button')) button.setAttribute('aria-pressed', String(button.dataset.compareView === state.view));
      const topicRail = document.querySelector('.knowledge-tag-rail');
      if (topicRail) {
        for (const button of topicRail.querySelectorAll('[data-compare-topic]')) button.setAttribute('aria-pressed', String(button.dataset.compareTopic === state.view));
        topicRail.querySelector('.dex-filter-result').textContent = views[state.view].label;
        topicRail.querySelector('[data-topic-clear]').disabled = state.view === 'all';
      }
      differences.checked = state.differences; differences.disabled = state.ids.length < 2;
      options(); output.replaceChildren();
      const analysis = root.querySelector('.compare-analysis'); analysis.replaceChildren();
      for (const article of data.articles || []) {
        if (!article.hand_ids.every(id => state.ids.includes(id))) continue;
        const box = node('div', null, 'dex-analysis-link'); box.append(node('small', article.status));
        const link = node('a', article.title + ' ↗'); link.href = '../' + article.page.replace(/\.md$/, '/');
        box.append(link, node('span', article.summary)); analysis.append(box);
      }
      status.textContent = notice || (state.ids.length ? `已选 ${state.ids.length} / 3 款。${state.ids.length === 1 ? '再加入一款，开始比较。' : '选择会保留在本标签页；当前链接包含产品与视图。'}` : '尚未选择产品。可搜索添加，或打开下方对比示例。');
      const scope = views[state.view]; let rows = data.rows.filter(row => !scope.rows || scope.rows.includes(row.id));
      const total = rows.length;
      if (state.differences && state.ids.length >= 2) rows = rows.filter(row => {const f = flags(row); return f.different || f.incomplete;});
      explanation.textContent = `${scope.label} · ${rows.length} / ${total} 项。标记反映记录差异及核查需要，不表示优劣；“只看差异与缺项”保留资料不足的维度。`;
      if (!state.ids.length) return;
      if (!rows.length) {output.append(node('p', '当前记录没有可显示的差异或缺项。可关闭“只看差异与缺项”查看全部。', 'compare-no-rows')); return;}
      const table = node('table'); table.append(node('caption', scope.label + ' · 技术记录对照'));
      const head = node('thead'), header = node('tr'), corner = node('th', '维度 / 阅读口径'); corner.scope = 'col'; header.append(corner);
      state.ids.forEach(id => {const th = node('th'); th.scope = 'col'; const link = node('a', hands.get(id).name + ' ↗'); link.href = '../hands/generated/' + encodeURIComponent(id) + '/'; th.append(link); header.append(th);});
      head.append(header); table.append(head); const body = node('tbody');
      for (const row of rows) {
        const tr = node('tr'), heading = node('th'); heading.scope = 'row'; heading.append(node('strong', row.label), node('small', row.help));
        if (state.ids.length >= 2) {
          const f = flags(row), badges = node('div', null, 'compare-row-flags');
          if (f.incomplete) badges.append(node('span', '资料未核全', 'compare-flag is-unknown'));
          if (f.boundary) badges.append(node('span', '范围需核对', 'compare-flag is-boundary'));
          if (f.different) badges.append(node('span', '记录不同', 'compare-flag is-different'));
          heading.append(badges);
        }
        tr.append(heading);
        for (const id of state.ids) {const td = node('td'); addCell(td, hands.get(id).cells[row.id], row); tr.append(td);}
        body.append(tr);
      }
      table.append(body); output.append(table);
    }
    for (const [id, view] of Object.entries(views)) {const button = node('button', view.label); button.type = 'button'; button.dataset.compareView = id; button.onclick = () => {state.view = id; render();}; modes.append(button);}
    for (const button of document.querySelectorAll('[data-compare-topic]')) button.addEventListener('click', () => {state.view = state.view === button.dataset.compareTopic ? 'all' : button.dataset.compareTopic; render();});
    const topicClear = document.querySelector('.knowledge-tag-rail [data-topic-clear]');
    if (topicClear) topicClear.addEventListener('click', () => {state.view = 'all'; render();});
    differences.onchange = () => {state.differences = differences.checked; render();};
    root.querySelector('form').onsubmit = event => {event.preventDefault(); if (hands.has(picker.value)) {state = add(state, picker.value).state; notice = ''; render();}};
    search.oninput = options;
    root.querySelector('[data-compare-clear]').onclick = () => {state.ids = []; state.differences = false; notice = ''; search.value = ''; render(); search.focus();};
    window.addEventListener('popstate', () => {fromURL(); render(false);});
    fromURL(); render();
  }).catch(() => {status.textContent = '资料读取失败，请刷新重试，或返回产品地图查看档案。'; root.querySelector('[type="submit"]').disabled = true;});
})();
