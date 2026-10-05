/* Native controls expose the same reviewed channels used by product pages. */
(() => {
  const root = document.querySelector('#dex-sensing-map');
  if (!root) return;
  const picker = root.querySelector('#sensing-hand'), status = root.querySelector('.sensing-status');
  const stages = root.querySelector('.sensing-stages'), evidence = root.querySelector('.sensing-evidence');
  const node = (tag, text, cls) => {const e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e;};
  const safeURL = value => {try {const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : null;} catch {return null;}};
  fetch(root.dataset.source).then(r => {if (!r.ok) throw new Error('data'); return r.json();}).then(data => {
    let selectedStage = 'transmission';
    for (const hand of data.hands) {const option = node('option', hand.name); option.value = hand.id; picker.append(option);}
    const params = new URL(location.href).searchParams;
    if (data.hands.some(h => h.id === params.get('hand'))) picker.value = params.get('hand');
    if (data.stages.some(s => s.id === params.get('stage'))) selectedStage = params.get('stage');
    function render() {
      const hand = data.hands.find(h => h.id === picker.value), stage = data.stages.find(s => s.id === selectedStage);
      root.querySelector('.sensing-version').textContent = hand.version + ' · 复核 ' + hand.checked_on;
      for (const b of stages.querySelectorAll('button')) b.setAttribute('aria-pressed', String(b.dataset.stage === selectedStage));
      for (const g of root.querySelectorAll('[data-sensing-visual]')) g.classList.toggle('is-active', g.dataset.sensingVisual === selectedStage);
      root.querySelector('.sensing-stage-description').textContent = '位置说明 · 工程解读：' + stage.description;
      const channels = hand.channels.filter(c => c.stage === selectedStage);
      status.textContent = channels.length ? `${hand.name} · ${stage.label} · ${channels.length} 项核查记录` : `${hand.name} · ${stage.label} · 没有独立通道记录`;
      evidence.replaceChildren();
      if (!channels.length) {
        const blank = node('div', null, 'sensing-empty');
        blank.append(node('strong', '此位置尚无独立通道记录'), node('p', '该型号的已核查通道位于其他位置。没有记录不代表不支持；也不能把别处的反馈自动搬到这里。'));
        evidence.append(blank);
      }
      for (const channel of channels) {
        const card = node('article', null, 'sensing-channel');
        const header = node('header'); header.append(node('h3', channel.label));
        const badge = node('span', data.statuses[channel.status], 'sensing-badge'); badge.dataset.status = channel.status; header.append(badge); card.append(header);
        card.append(node('p', channel.quantity, 'sensing-quantity'));
        const list = node('dl');
        for (const [key, label] of data.fields.filter(([key]) => key !== 'quantity' && key !== 'boundary')) list.append(node('dt', label), node('dd', channel[key]));
        card.append(list);
        const boundary = node('div', null, 'sensing-boundary'); boundary.append(node('strong', '证据边界'), node('p', channel.boundary)); card.append(boundary);
        if (channel.interpretation) {const p = node('p', '工程解读 · ' + channel.interpretation, 'sensing-interpretation'); card.append(p);}
        const refs = node('div', null, 'sensing-sources');
        for (const key of channel.sources) {const source = hand.sources[key], url = safeURL(source.url); if (!url) continue; const a = node('a', source.title + ' · ' + source.locator + ' ↗'); a.href = url; a.target = '_blank'; a.rel = 'noopener'; refs.append(a);}
        card.append(refs); evidence.append(card);
      }
      const links = root.querySelector('.sensing-links'); links.replaceChildren();
      const profile = node('a', '查看这款手的完整感知记录 ↗'); profile.href = `../../hands/generated/${hand.id}/#record-sensing`;
      const compare = node('a', '打开三款手的感知对比 ↗'); compare.href = '../../compare/?hands=shadow-hand,leap-hand,wuji-hand-2&view=sensing'; links.append(profile, compare);
      const url = new URL(location.href); url.searchParams.set('hand', hand.id); url.searchParams.set('stage', selectedStage); history.replaceState(null, '', url);
    }
    data.stages.forEach((stage, index) => {
      const b = node('button'); b.type = 'button'; b.dataset.stage = stage.id; b.setAttribute('aria-pressed', 'false');
      b.append(node('strong', stage.label), node('small', stage.quantity));
      b.addEventListener('click', () => {selectedStage = stage.id; render();}); stages.append(b);
    });
    // Larger transparent hit areas make the line drawing itself clickable.
    for (const g of root.querySelectorAll('[data-sensing-visual]')) {
      const bounds = g.getBBox(), hit = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      hit.setAttribute('x', bounds.x - 12); hit.setAttribute('y', bounds.y - 12);
      hit.setAttribute('width', bounds.width + 24); hit.setAttribute('height', bounds.height + 24);
      hit.setAttribute('fill', 'transparent'); hit.setAttribute('stroke', 'none');
      g.append(hit); g.style.cursor = 'pointer';
      g.addEventListener('click', () => {selectedStage = g.dataset.sensingVisual; render();});
    }
    picker.addEventListener('change', render); render();
  }).catch(() => {status.textContent = '感知资料未能加载。请从下方产品链接阅读完整记录。'; const a = node('a', '打开产品数据库 ↗'); a.href = '../../hands/'; root.querySelector('.sensing-links').append(a);});
})();
