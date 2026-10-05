/* DexTrail: individual product rows in a year/category timeline. */
(async () => {
  'use strict';
  const root = document.getElementById('dex-map');
  if (!root) return;
  document.title = 'DexTrail';
  const $ = (s) => root.querySelector(s);
  const stage = $('.dex-stage'), lanes = $('.dex-lanes');
  const pending = $('.dex-pending'), inspector = $('.dex-inspector');
  const search = $('.dex-search input');
  const routes = {
    'direct-drive': ['直接驱动', '#4b7094'],
    'tendon-driven': ['腱绳传动', '#aa4d3e'],
    'linkage-driven': ['连杆传动', '#4d7865'],
    'hybrid-transmission': ['混合传动', '#80618a'],
    'geared-drive': ['齿轮传动', '#94732c'],
    unknown: ['传动待核实', '#747873'],
  };
  const views = {
    dof: {name:'自由度分组', x:'公开年份 · ≤ 表示至迟已有资料', y:'主动轴数量 · 每 5 轴一档', xf:'year', yf:'dof', grouped:true},
    transmission: {name:'传动路线', x:'公开年份 · ≤ 表示至迟已有资料', y:'传动机制 · 类别无高低顺序', xf:'year', yf:'transmission', grouped:true},
    fingers: {name:'手指构型', x:'公开年份 · ≤ 表示至迟已有资料', y:'手指数量 · 分类分区', xf:'year', yf:'fingers', grouped:true},
    actuators: {name:'驱动规模', x:'公开年份 · ≤ 表示至迟已有资料', y:'执行器数量 · 按确切数值分行', xf:'year', yf:'actuators'},
    mobility: {name:'主动轴演进', x:'公开年份 · ≤ 表示至迟已有资料', y:'独立受控关节角 · 按确切数值分行', xf:'year', yf:'dof'},
  };
  const el = (tag, text, cls) => {
    const n = document.createElement(tag);
    if (text != null) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  };
  let data;
  try {
    const r = await fetch(new URL(root.dataset.source, document.baseURI));
    if (!r.ok) throw Error('HTTP '+r.status);
    data = await r.json();
  } catch (error) {
    $('.dex-coverage').textContent = '地图数据加载失败';
    const a = el('a','打开产品数据库'); a.href = 'hands/';
    $('.dex-empty').replaceChildren('无法读取地图数据。', a); $('.dex-empty').hidden = false;
     return;
  }
  let view = 'transmission', scale = 1, layout;
  let dismissedPreviewKey = null;
  let hoverTimer = 0;
  const transmission = h => h.classification?.transmission || 'unknown';
  const route = h => routes[transmission(h)]?.[0] || routes.unknown[0];
  const thumb = h => h.media?.poster || (h.media?.kind === 'image' ? h.media.url : null);
  const entries = [...data.hands, ...(data.systems || [])];
  const selectedTags = new Set();
  const home = root.closest('#dextrail-home');
  const filterStrip = $('.dex-active-filters');
  const filterList = $('.dex-active-filter-list');
  const tagGroups = {transmission:'传动机构', fingers:'手指构型', actuation:'驱动源', configuration:'驱动配置', structure:'结构', sensing:'感知', control:'控制证据', simulation:'仿真资料', software:'软件与模型资料'};
  const tagIndex = new Map();
  for (const h of entries) for (const t of h.classification?.tags || []) {
    if (!tagIndex.has(t.id)) tagIndex.set(t.id, {...t, count:0});
    tagIndex.get(t.id).count++;
  }
  function matchesTags(h) {
    const own = new Set((h.classification?.tags || []).map(t=>t.id));
    return Object.keys(tagGroups).every(group=>{
      const selected = [...selectedTags].filter(id=>tagIndex.get(id)?.group===group);
      return !selected.length || selected.some(id=>own.has(id));
    });
  }
  function syncFilters() {
    home.querySelectorAll('[data-filter-tag]').forEach(b=>b.setAttribute('aria-pressed',String(selectedTags.has(b.dataset.filterTag))));
    home.querySelector('.dex-filter-result').textContent = selectedTags.size ? `已选 ${selectedTags.size} 个标签${search.value.trim() ? ' · 含搜索条件' : ''}` : search.value.trim() ? '按搜索条件查看档案' : '未限制标签 · 显示全部档案';
    home.querySelector('.dex-clear-filters').disabled = !selectedTags.size;
    filterStrip.hidden = !selectedTags.size && !search.value.trim();
    filterList.replaceChildren();
    function chip(label, remove, tag) {
      const b = el('button', null, 'dex-active-filter'); b.type = 'button';
      b.append(el('span',label), el('span','×','dex-filter-remove'));
      b.setAttribute('aria-label','移除筛选：'+label);
      if(tag)window.DexTrailTags.paint(b,tag);
      b.addEventListener('click',()=>{
        const index=[...filterList.children].indexOf(b); remove(); updateData(); reset();
        (filterList.children[Math.min(index,filterList.children.length-1)] || search).focus();
      }); filterList.append(b);
    }
    if(search.value.trim())chip('搜索：'+search.value.trim(),()=>{search.value='';});
    for(const id of selectedTags)chip(tagIndex.get(id).label,()=>selectedTags.delete(id),id);
  }
  for (const [group, title] of Object.entries(tagGroups)) {
    const tags = [...tagIndex.values()].filter(t=>t.group===group);
    if (!tags.length) continue;
    const section = el('div',null,'dex-tag-group'); section.dataset.tagGroup=group;
    section.append(el('h3',title)); const list=el('div',null,'dex-tag-list');
    for (const t of tags) {
      const b=el('button',null,'dex-tag'); b.type='button'; b.dataset.filterTag=t.id;
      b.append(el('span',t.label)); b.setAttribute('aria-pressed','false');
      b.title=`筛选 ${t.label}`;
      window.DexTrailTags.paint(b,t.id);
      b.addEventListener('click',()=>{if(selectedTags.has(t.id))selectedTags.delete(t.id);else selectedTags.add(t.id);updateData();reset();});
      list.append(b);
    }
    section.append(list); home.querySelector('.dex-filter-groups').append(section);
  }
  home.querySelector('.dex-clear-filters').addEventListener('click',()=>{selectedTags.clear();updateData();reset();});
  $('.dex-clear-all').addEventListener('click',()=>{selectedTags.clear();search.value='';updateData();reset();search.focus();});
  $('.dex-start-over').addEventListener('click',()=>{
    view='transmission';selectedTags.clear();search.value='';pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');
    root.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
    $('.dex-resume-note').hidden=true;updateData();reset();saveExploration();search.focus();
  });
  const timeline = window.DexTrailTimeline;
  const allowedState = {views:Object.keys(views), tags:new Set(tagIndex.keys()), hands:new Set(entries.map(h=>h.id))};
  const stateKey = 'dextrail-map:time-lanes-v1:' + new URL('.', document.baseURI).pathname;
  const collectionLabel = `${data.hands.length} 款手 · ${(data.systems || []).length} 个系统`;
  const link = h => new URL(h.detail_url || 'hands/generated/'+h.id+'/', document.baseURI).href;
  const short = h => h.display_name || h.name.replace('Shadow Dexterous Hand（Classic 五指版）','Shadow Hand').replace('LEAP Hand v1（Full）','LEAP Hand v1');
  function image(h, cls) {
    const source = thumb(h);
    if (!source) return el('span',h.kind === 'system' ? 'R1' : '◇','dex-lane-glyph');
    const img = el('img',null,cls); img.src=source; img.alt=''; img.loading='lazy'; img.decoding='async';
    img.addEventListener('error',()=>img.replaceWith(el('span','◇','dex-lane-glyph')),{once:true});
    return img;
  }
  function closePreview(restoreFocus=false) {
    clearTimeout(hoverTimer);
    dismissedPreviewKey=inspector.dataset.product;
    inspector.hidden=true;
    if (restoreFocus) lanes.focus({preventScroll:true});
  }
  function describe(h) {
    if (dismissedPreviewKey===h.id) return;
    inspector.dataset.product=h.id;
    const item=root.querySelector(`.dex-lane-item[data-id="${h.id}"]`);
    const bounds=item?.getBoundingClientRect(),plane=stage.getBoundingClientRect();
    inspector.dataset.side=bounds && bounds.x+bounds.width/2>plane.x+plane.width/2 ? 'left' : 'right';
    const box=$('.dex-inspector-content'); box.replaceChildren();
    box.append(image(h,'dex-preview-img'),el('small',route(h)),el('h3',h.name));
    box.append(el('p',`自由度：${h.facts?.dof?.value ?? h.coordinates.dof ?? '口径待核实'} · 执行器：${h.facts?.actuators?.value ?? h.coordinates.actuators ?? '数量待核实'}`));
    if (h.kind==='system') box.append(el('p','机器人系统档案；手部硬件参数分别核实。'));
    if (h.coordinates.scope) box.append(el('p',h.coordinates.scope));
    if (h.timeline) {
      box.append(el('p',h.timeline.label,'dex-year-label'),el('p',h.timeline.detail));
      if(h.timeline.source) {
        const source=el('a','时间依据：'+h.timeline.source.title+' ↗');
        source.href=h.timeline.source.url;source.target='_blank';source.rel='noopener';box.append(source);
      }
    }
    const a=el('a','查看技术档案 ↗','dex-read-more');a.href=link(h);box.append(a);
    if(h.kind!=='system') {
      const compare=el('a','与其他灵巧手对比 ↗','dex-read-more');
      compare.href='compare/?add='+encodeURIComponent(h.id);box.append(compare);
    }
    inspector.hidden=false;
  }
  function productItem(h) {
    const a=el('a',null,'dex-lane-item');a.href=link(h);a.dataset.id=h.id;a.dataset.year=h.coordinates.year;
    a.setAttribute('aria-label','查看 '+h.name+' 详情');
    const caption=el('span',null,'dex-lane-caption');
    caption.append(el('strong',short(h)));
    // A bound on first known evidence is different from a release date.
    if(h.timeline?.label?.includes('≤')) caption.append(el('small','≤ '+h.coordinates.year));
    if(h.kind==='system') caption.append(el('small','系统档案'));
    a.append(image(h),caption);
    a.title=[h.name,h.timeline?.label || String(h.coordinates.year),h.timeline?.detail].filter(Boolean).join(' · ');
    a.addEventListener('mouseenter',()=>{clearTimeout(hoverTimer);hoverTimer=setTimeout(()=>describe(h),350);});
    a.addEventListener('mouseleave',()=>{clearTimeout(hoverTimer);dismissedPreviewKey=null;});
    a.addEventListener('focus',()=>{clearTimeout(hoverTimer);hoverTimer=setTimeout(()=>describe(h),350);});
    a.addEventListener('blur',()=>clearTimeout(hoverTimer));
    a.addEventListener('click',()=>closePreview());
    return a;
  }
  function renderLanes() {
    const matrix=el('div',null,'dex-lane-matrix');matrix.setAttribute('role','table');matrix.setAttribute('aria-label',views[view].name+'，按公开年份排列');
    matrix.style.setProperty('--lane-years',layout.years.length);
    const header=el('div',null,'dex-lane-row');header.setAttribute('role','row');
    const corner=el('div','分类 / 年份','dex-lane-year dex-lane-corner');corner.setAttribute('role','columnheader');header.append(corner);
    for(const year of layout.years) {const cell=el('div',String(year),'dex-lane-year');cell.setAttribute('role','columnheader');cell.dataset.year=year;header.append(cell);}
    matrix.append(header);
    for(const [key,label] of layout.rows) {
      const row=el('div',null,'dex-lane-row');row.setAttribute('role','row');row.dataset.category=key;
      const title=el('div',label,'dex-lane-title');title.setAttribute('role','rowheader');row.append(title);
      for(const year of layout.years) {
        const cell=el('div',null,'dex-lane-cell');cell.setAttribute('role','cell');cell.dataset.year=year;cell.dataset.category=key;
        for(const h of layout.cells.get(`${key}|${year}`) || []) cell.append(productItem(h));
        row.append(cell);
      }
      matrix.append(row);
    }
    lanes.replaceChildren(matrix);setWidth();
    root.dataset.renderedNodes=layout.cells.size ? [...layout.cells.values()].reduce((sum,cell)=>sum+cell.length,0) : 0;
    root.dataset.positioned=root.dataset.renderedNodes;
    root.dataset.renderer='time-lanes';
  }
  function updateData() {
    closePreview();syncFilters();root.dataset.view=view;
    const query=search.value.trim().toLowerCase().replace(/-/g,'');
    const filtered=entries.filter(h=>matchesTags(h) && [h.name,h.venue,h.facts?.company?.value].filter(Boolean).join(' ').toLowerCase().replace(/-/g,'').includes(query));
    layout=timeline.build(entries,filtered,view);renderLanes();
    const missing=layout.missing;
    $('.dex-pending-toggle span').textContent=missing.length;
    $('.dex-pending-list').replaceChildren();$('.dex-unplaced-list').replaceChildren();
    $('.dex-unplaced').hidden=!missing.length;$('.dex-unplaced-count').textContent=missing.length;
    for(const h of missing) {
      const a=el('a');a.href=link(h);a.append(image(h),el('strong',h.name),el('small','公开年份依据待核实'));$('.dex-pending-list').append(a);
      const card=el('article',null,'dex-unplaced-card'),title=el('a',h.name,'dex-unplaced-title');title.href=link(h);card.append(title,el('small','公开年份依据待核实'));$('.dex-unplaced-list').append(card);
    }
    if(!missing.length) $('.dex-pending-list').append(el('p','所有匹配档案均有公开年份记录。'));
    $('.dex-empty').hidden=Number(root.dataset.renderedNodes)>0;
    $('.dex-empty').textContent=missing.length ? '公开年份尚待核实，请查看下方档案。' : '没有匹配档案。可移除筛选条件，或清除全部筛选。';
    $('.dex-coverage').replaceChildren(el('span','已收录 '+collectionLabel,'dex-collection-total'),el('span',`${query || selectedTags.size ? '筛选结果' : '当前视图'}：${root.dataset.renderedNodes} 个档案`,'dex-view-coverage'));
    $('.dex-coordinate-note').textContent='';
    $('.dex-view-title').textContent=views[view].name;
  }
  function columnWidth(){return Math.round(176*scale);}
  function setWidth(){
    root.style.setProperty('--lane-width',columnWidth()+'px');
    // End the initial viewport on complete years instead of a clipped left column.
    const space=Math.max(0,lanes.clientWidth-108);
    root.style.setProperty('--lane-tail',Math.max(0,space-Math.max(1,Math.floor(space/columnWidth()))*columnWidth())+'px');
    $('.dex-zoom-readout').textContent=scale.toFixed(2)+'×';
  }
  function focusRecent() {
    const records=[...layout.cells.values()].flat(),dates=records.map(h=>h.coordinates.year);
    const latest=dates.length ? Math.max(...dates) : layout.years[layout.years.length-1];
    const columns=Math.max(1,Math.floor((lanes.clientWidth-108)/columnWidth()));
    lanes.scrollLeft=Math.max(0,(latest-layout.years[0]-columns+1)*columnWidth());
    lanes.scrollTop=0;
  }
  function reset(){scale=1;setWidth();focusRecent();closePreview();$('.dex-resume-note').hidden=true;}
  function zoom(factor) {
    closePreview();const old=columnWidth(),anchor=(lanes.scrollLeft+Math.max(0,lanes.clientWidth-108)/2)/old;
    scale=Math.max(.7,Math.min(2.5,scale*factor));setWidth();
    lanes.scrollLeft=anchor*columnWidth()-Math.max(0,lanes.clientWidth-108)/2;
    saveExploration();
  }
  function saveExploration() {
    window.DexTrailMapState.save(stateKey,{
      view,query:search.value,tags:[...selectedTags],k:scale,
      x:lanes.scrollLeft/Math.max(1,lanes.clientWidth),y:lanes.scrollTop/Math.max(1,lanes.clientHeight),
      expanded:[],pending:!pending.hidden,scrollY:window.scrollY,listScroll:$('.dex-unplaced-list').scrollTop,
    },allowedState);
  }
  function restoreExploration() {
    const saved=window.DexTrailMapState.read(stateKey,allowedState);if(!saved)return false;
    view=saved.view;search.value=saved.query;for(const id of saved.tags)selectedTags.add(id);
    scale=Math.max(.7,Math.min(2.5,saved.k));
    root.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
    updateData();lanes.scrollLeft=saved.x*lanes.clientWidth;lanes.scrollTop=saved.y*lanes.clientHeight;
    pending.hidden=!saved.pending;$('.dex-pending-toggle').setAttribute('aria-expanded',String(saved.pending));
    requestAnimationFrame(()=>{window.scrollTo(0,saved.scrollY);$('.dex-unplaced-list').scrollTop=saved.listScroll;});
    root.dataset.restored='true';$('.dex-resume-note').hidden=!(saved.view!=='transmission'||saved.query.trim()||saved.tags.length||saved.k!==1||saved.pending);
    return true;
  }
  root.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{
    const yearOffset=lanes.scrollLeft/columnWidth();view=b.dataset.view;
    root.querySelectorAll('[data-view]').forEach(n=>n.setAttribute('aria-pressed',n===b));
    updateData();lanes.scrollLeft=yearOffset*columnWidth();lanes.scrollTop=0;saveExploration();
  }));
  search.addEventListener('input',()=>{updateData();focusRecent();saveExploration();});
  $('.dex-pending-toggle').onclick=()=>{pending.hidden=!pending.hidden;$('.dex-pending-toggle').setAttribute('aria-expanded',String(!pending.hidden));saveExploration();};
  $('.dex-drawer-heading button').onclick=()=>{pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');$('.dex-pending-toggle').focus();};
  $('.dex-inspector-close').onclick=()=>closePreview(true);
  inspector.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();closePreview(true);}});
  root.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>{if(b.dataset.action==='reset'){reset();saveExploration();}else zoom(b.dataset.action==='in'?1.2:1/1.2);});
  lanes.addEventListener('wheel',e=>{
    if(e.ctrlKey || e.metaKey){e.preventDefault();zoom(Math.exp(-Math.max(-120,Math.min(120,e.deltaY))*.002));}
  },{passive:false});
  lanes.addEventListener('scroll',()=>closePreview());
  lanes.addEventListener('keydown',e=>{
    if(e.target!==lanes)return;
    if(['+','=','-','Home','Escape'].includes(e.key)) {
      e.preventDefault();if(e.key==='Home')reset();else if(e.key==='Escape')closePreview();else zoom(e.key==='-'?1/1.2:1.2);
    }
  });
  document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.target.matches('input,textarea')){e.preventDefault();search.focus();}});
  document.addEventListener('click',e=>{if(e.target.closest('a[href]'))saveExploration();},true);
  window.addEventListener('pagehide',saveExploration);
  let previousWidth=lanes.clientWidth;
  new ResizeObserver(()=>{
    if(!lanes.clientWidth || lanes.clientWidth===previousWidth)return;
    previousWidth=lanes.clientWidth;setWidth();
    lanes.scrollLeft=Math.round(lanes.scrollLeft/columnWidth())*columnWidth();
  }).observe(lanes);
  if(!restoreExploration()){updateData();reset();}
})();
