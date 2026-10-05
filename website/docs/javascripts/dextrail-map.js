/* DexTrail: name-only nodes on a continuously zoomable calendar map. */
(async () => {
  'use strict';
  const root = document.getElementById('dex-map');
  if (!root) return;
  document.title = 'DexTrail';
  const $ = (s) => root.querySelector(s);
  const stage = $('.dex-stage'), axes = $('.dex-axes'), nodeLayer = $('.dex-nodes');
  const pending = $('.dex-pending'), inspector = $('.dex-inspector');
  const search = $('.dex-search input');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const routes = {
    'direct-drive': ['直接驱动', '#4b7094'],
    'tendon-driven': ['腱绳传动', '#aa4d3e'],
    'linkage-driven': ['连杆传动', '#4d7865'],
    'hybrid-transmission': ['混合传动', '#80618a'],
    'geared-drive': ['齿轮传动', '#94732c'],
    unknown: ['传动待核实', '#747873'],
  };
  const routeKeys = Object.keys(routes);
  const views = {
    dof: {name:'自由度分组', x:'公开年份 · ≤ 表示至迟已有资料', y:'主动轴数量 · 每 5 轴一档', xf:'year', yf:'dof', grouped:true},
    transmission: {name:'传动路线', x:'公开年份 · ≤ 表示至迟已有资料', y:'传动机制 · 类别无高低顺序', xf:'year', yf:'transmission', grouped:true},
    fingers: {name:'手指构型', x:'公开年份 · ≤ 表示至迟已有资料', y:'手指数量 · 分类分区', xf:'year', yf:'fingers', grouped:true},
    actuators: {name:'驱动规模', x:'公开年份 · ≤ 表示至迟已有资料', y:'执行器数量', xf:'year', yf:'actuators'},
    mobility: {name:'主动轴演进', x:'公开年份 · ≤ 表示至迟已有资料', y:'独立受控关节角（主动轴）', xf:'year', yf:'dof'},
  };
  const el = (tag, text, cls) => {
    const n = document.createElement(tag);
    if (text != null) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  };
  const sv = (tag, attrs, text) => {
    const n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v);
    if (text != null) n.textContent = text;
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
  let view = 'transmission', W = 0, H = 0, left = 65, top = 110, right = 145, bottom = 65;
  let camera = {k:1,x:0,y:0}, target = {...camera}, frame = 0;
  let placed = [], missing = [], drag = null, moved = false;
  let rendered = [];
  let dismissedPreviewKey = null;
  let hoverResumeAt = 0;
  const elements = new Map();
  let previewTimer = 0;
  let labelOffsets = new Map();
  let categoryBands = [];
  let categoryHeight = 1;
  let numericHeight = 560;
  let numericPositions = new Map();
  let unknownPositions = new Map();
  const transmission = h => h.classification?.transmission || 'unknown';
  const color = h => routes[transmission(h)]?.[1] || routes.unknown[1];
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
        const index=[...filterList.children].indexOf(b); remove(); updateData(); resize(); reset();
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
      b.addEventListener('click',()=>{if(selectedTags.has(t.id))selectedTags.delete(t.id);else selectedTags.add(t.id);updateData();resize();reset();});
      list.append(b);
    }
    section.append(list); home.querySelector('.dex-filter-groups').append(section);
  }
  home.querySelector('.dex-clear-filters').addEventListener('click',()=>{selectedTags.clear();updateData();resize();reset();});
  $('.dex-clear-all').addEventListener('click',()=>{selectedTags.clear();search.value='';updateData();resize();reset();search.focus();});
  $('.dex-start-over').addEventListener('click',()=>{
    view='transmission';selectedTags.clear();search.value='';pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');
    root.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
    $('.dex-resume-note').hidden=true;updateData();resize();reset();saveExploration();search.focus();
  });
  const numeric = (h, key) => key==='fingers' ? h.classification?.fingers : h.coordinates?.[key];
  function groupKey(h, v=views[view]) {
    if(v.yf==='transmission')return transmission(h);
    const value=numeric(h,v.yf);
    if(v.grouped && v.yf==='dof' && Number.isFinite(value))return String(Math.ceil(value/5));
    return Number.isFinite(value)?String(value):'unknown';
  }
  function categories(v=views[view]) {
    if(v.yf==='transmission')return routeKeys.map(k=>[k,routes[k][0]]);
    const values = new Map();
    for(const h of entries){const key=groupKey(h,v);if(key!=='unknown')values.set(key,v.yf==='fingers'?`${key} 指`:Number(key)===0?'0 主动轴':`${(Number(key)-1)*5+1}–${Number(key)*5} 轴`);}
    return [...values].sort((a,b)=>a[0].localeCompare(b[0],undefined,{numeric:true})).concat([['unknown',v.yf==='fingers'?'指数量待核实':'主动轴待核实']]);
  }
  function configureAxes() {
    for(const v of Object.values(views)) {
      const xs=entries.map(h=>numeric(h,v.xf)).filter(Number.isFinite);
      const ys=entries.map(h=>numeric(h,v.yf)).filter(Number.isFinite);
      // Leave room for complete thumbnails at the first and last known dates.
      v.min=Math.min(...xs)-.5;
      v.max=Math.max(...xs)+1.5;
      v.ymax=v.grouped?categories(v).length:Math.max(8,Math.ceil(Math.max(0,...ys)/8)*8+8);
    }
  }
  configureAxes();syncFilters();
  const collectionLabel = `${data.hands.length} 款手 · ${(data.systems || []).length} 个系统`;
  const link = h => new URL(h.detail_url || 'hands/generated/'+h.id+'/', document.baseURI).href;
  const short = h => h.name.replace('Shadow Dexterous Hand','Shadow Hand').replace(/[（(].*?[）)]/g,'').replace(/\s+/g,' ').trim();
  const labelWidth = h => Math.min(210,Math.max(65,Array.from(short(h)).reduce((w,c)=>w+(c.charCodeAt(0)>255?12:6.8),14)));
  const gap = (h,k) => h.coordinates.gaps?.[k] || ({dof:'主动轴口径尚未核实',actuators:'执行器总数尚未核实',year:'公开时间依据尚未核实',fingers:'手指数尚无结构化记录',transmission:'传动分类尚未核实'}[k]);
  function image(h) { return el('span', short(h)); }
  function coordinates(h) {
    const v=views[view], time=window.DexTrailMapTime.point(h);
    const value=numeric(h,v.yf);
    return [time?.value, v.grouped?categories().findIndex(([key])=>key===groupKey(h))+.5:
      Number.isFinite(value)?value:-1];
  }
  function screen(x,y) {
    const v = views[view];
    return {x:left + ((x-v.min)/(v.max-v.min)*(W-left-right))*camera.k+camera.x,
            y:H-bottom-(y/v.ymax*(H-top-bottom))*camera.k+camera.y};
  }
  function updateData() {
    syncFilters();
    root.dataset.view = view;
    placed = []; missing = [];
    for (const h of entries) {
      if (!matchesTags(h)) continue;
      const searchable = [h.name, h.venue, h.facts?.company?.value].filter(Boolean).join(' ').toLowerCase().replace(/-/g, '');
      if (!searchable.includes(search.value.trim().toLowerCase().replace(/-/g, ''))) continue;
      const [x,y] = coordinates(h);
      if (Number.isFinite(x) && Number.isFinite(y) && x >= 0) placed.push({h,x,y});
      else missing.push(h);
    }
    $('.dex-pending-toggle span').textContent = missing.length;
    $('.dex-pending-list').replaceChildren();
    $('.dex-unplaced-list').replaceChildren();
    $('.dex-unplaced').hidden = !missing.length;
    $('.dex-unplaced-count').textContent = missing.length;
    for (const h of missing) {
      const a = el('a'); a.href = link(h); const [x,y] = coordinates(h), reasons = [], fields = [];
      const fieldLabels = {dof:'主动自由度', actuators:'执行器数量', year:'公开时间', transmission:'传动类别',fingers:'手指数'};
      const addGap = key => {reasons.push(gap(h,key)); fields.push(fieldLabels[key]);};
      if (!Number.isFinite(x) || x < 0) addGap(views[view].xf);
      if (!Number.isFinite(y)) addGap(views[view].yf);
      a.append(image(h),el('strong',h.name + (h.kind === 'system' ? ' · 系统' : '')),el('small',reasons.join('；')));
      $('.dex-pending-list').append(a);
      const card = el('article', null, 'dex-unplaced-card');
      const title = el('a', h.name + (h.kind === 'system' ? ' · 系统' : ''), 'dex-unplaced-title'); title.href = link(h); card.append(title);
      const known = [h.facts?.dof?.value && `自由度记录：${h.facts.dof.value}`, Number.isFinite(h.coordinates.actuators) && `执行器：${h.coordinates.actuators}`].filter(Boolean);
      card.append(el('small', '待核：' + fields.join(' / ')));
      const detail = el('details', null, 'dex-card-details');
      detail.append(el('summary', '参数与核验说明'));
      if (known.length) detail.append(el('p', known.join('；')));
      detail.append(el('p', reasons.join('；')));
      card.append(detail);
      $('.dex-unplaced-list').append(card);
    }
    if (!missing.length) $('.dex-pending-list').append(el('p','本视图没有未定位的匹配产品。'));
    $('.dex-empty').hidden = placed.length > 0;
    $('.dex-empty').textContent = missing.length ? `已收录 ${missing.length} 个匹配档案，当前轴所需参数尚待核实。请查看地图下方档案。` : '没有匹配档案。可移除上方筛选条件，或清除全部筛选。';
    $('.dex-coverage').replaceChildren(el('span', '已收录 ' + collectionLabel, 'dex-collection-total'), el('span', `${search.value.trim() || selectedTags.size ? '筛选结果' : '当前坐标'}：${placed.length} 可定位 · ${missing.length} 待核`, 'dex-view-coverage'));
    const v=views[view];
    $('.dex-coordinate-note').textContent = '';
    root.dataset.monthRecords = placed.filter(p=>window.DexTrailMapTime.point(p.h)?.precision==='month').length;
    $('.dex-view-title').textContent = v.name;
    inspector.hidden = true;
    if(W && H)updateLabelOffsets();
  }
  function closePreview(restoreFocus=false) {
    clearTimeout(previewTimer);
    dismissedPreviewKey=inspector.dataset.groupKey;
    // Hiding the panel can expose a different node beneath the pointer.
    // Ignore that synthetic entry so Escape/Close actually dismisses it.
    hoverResumeAt=performance.now()+300;
    inspector.hidden=true;
    if(restoreFocus)stage.focus();
  }
  function describe(group) {
    if(drag || performance.now()<hoverResumeAt || dismissedPreviewKey===group.key)return;
    inspector.dataset.kind='product';
    inspector.dataset.groupKey=group.key;
    inspector.setAttribute('aria-label','当前产品');
    inspector.dataset.side = group.x > W/2 ? 'left' : 'right';
    inspector.dataset.vertical=stage.getBoundingClientRect().top+group.y>window.innerHeight/2?'top':'bottom';
    const box = $('.dex-inspector-content'); box.replaceChildren(); inspector.hidden = false;
      const h = group.members[0].h;
      box.append(el('small',route(h)),el('h3',h.name));
      const time=window.DexTrailMapTime.point(h);
      box.append(el('small',time?.precision==='month'?'月份已核实':'仅有年份 · 月份未核实','dex-time-precision'));
      box.append(el('p',h.kind === 'system' ? '已收录 · 机器人系统；手部参数另行核实。' : `自由度：${h.facts?.dof?.value ?? h.coordinates.dof ?? gap(h,'dof')} · 执行器：${h.facts?.actuators?.value ?? h.coordinates.actuators ?? gap(h,'actuators')}`));
      box.append(el('p',h.coordinates.scope));
      if (h.timeline) {
        box.append(el('p',h.timeline.label,'dex-year-label'),el('p',h.timeline.detail));
        const source=el('a','时间依据：'+h.timeline.source.title+' ↗');
        source.href=h.timeline.source.url;source.target='_blank';source.rel='noopener';box.append(source);
      }
      const a = el('a','查看技术档案 ↗','dex-read-more'); a.href=link(h);box.append(a);
      if (h.kind !== 'system') {const compare = el('a','与其他灵巧手对比 ↗','dex-read-more');compare.href='compare/?add='+encodeURIComponent(h.id);box.append(compare);}
      requestDraw();
  }
  function updateLabelOffsets() {
    const v=views[view],baseWidth=W-left-right;
    if(v.grouped) {
      const keys=categories().map(([key])=>key);
      const all=placed.map(({h})=>({
        id:h.id,key:groupKey(h),width:labelWidth(h),
        x:left+(window.DexTrailMapTime.point(h).value-v.min)/(v.max-v.min)*baseWidth,
      }));
      const layout=window.DexTrailNameLayout.pack(all,keys,{left,right:W-right});
      categoryBands=layout.bands;categoryHeight=layout.height;
      labelOffsets=layout.positions;
    } else {
      const all=placed.map(({h,y})=>{
        const x=left+(window.DexTrailMapTime.point(h).value-v.min)/(v.max-v.min)*baseWidth;
        const width=labelWidth(h), side=x+width>W-right?'left':'right';
        return {id:h.id,key:'unknown',x,start:side==='left'?x-width:x,width,value:y,max:v.ymax-8};
      });
      const known=window.DexTrailNameLayout.numeric(all.filter(p=>p.value>=0));
      const unknown=window.DexTrailNameLayout.pack(all.filter(p=>p.value<0),['unknown'],{left,right:W-right});
      numericPositions=known.positions;numericHeight=known.positions.size?known.height:0;
      unknownPositions=unknown.positions;categoryHeight=numericHeight+unknown.height;
    }
  }
  function numericY(value) {
    return (24+value/(views[view].ymax-8)*(numericHeight-48))/categoryHeight*views[view].ymax;
  }
  function groups() {
    return placed.map(p=>{
      const display=labelOffsets.get(p.h.id);
      const known=numericPositions.get(p.h.id), unknown=unknownPositions.get(p.h.id);
      const normalizedY=views[view].grouped?(1-display.center/categoryHeight)*views[view].ymax:
        p.y>=0?numericY(p.y):(numericHeight+unknown.center)/categoryHeight*views[view].ymax;
      const anchor=screen(p.x,normalizedY);
      const offset=(views[view].grouped?display.offset/categoryHeight*(H-top-bottom):
        -(p.y>=0?known.center-known.anchor:unknown.offset)/categoryHeight*(H-top-bottom))*camera.k;
      return {x:anchor.x,y:anchor.y+offset,ax:anchor.x,ay:anchor.y,
        width:labelWidth(p.h),height:18,key:p.h.id,color:color(p.h),members:[p]};
    });
  }
  function drawAxes(gs) {
    axes.setAttribute('viewBox',`0 0 ${W} ${H}`); axes.replaceChildren();
    const defs=sv('defs',{}),clip=sv('clipPath',{id:'dex-plot-clip'});
    clip.append(sv('rect',{x:left,y:top-20,width:W-left-right,height:H-top-bottom+20}));defs.append(clip);axes.append(defs);
    const grid=sv('g',{'clip-path':'url(#dex-plot-clip)'});axes.append(grid);
    const v=views[view];
    // Compute visible ticks from the camera rather than stretching fixed labels.
    const xmin=v.min-camera.x/camera.k/(W-left-right)*(v.max-v.min);
    const xmax=xmin+(v.max-v.min)/camera.k;
    for(const tick of window.DexTrailMapTime.ticks(xmin,xmax,(W-left-right)*camera.k/(v.max-v.min))) {
      const px=screen(tick.value,0).x;if(px<left-1||px>W-right+1)continue;
      if(tick.major)grid.append(sv('line',{x1:px,x2:px,y1:top-20,y2:H-bottom,class:'grid-line'}));
      axes.append(sv('line',{x1:px,x2:px,y1:H-bottom,y2:H-bottom+(tick.major?6:3),class:'tick-line'}));
      axes.append(sv('text',{x:px,y:H-bottom+24,'text-anchor':'middle',class:tick.major?'year-tick':'month-tick'},tick.label));
    }
    const yExtent=v.ymax, ys=camera.k>2?2:8;
    const ymin=(camera.y/camera.k/(H-top-bottom)*categoryHeight-24)/(numericHeight-48)*(v.ymax-8);
    const ymax=ymin+categoryHeight/camera.k/(numericHeight-48)*(v.ymax-8);
    const ticks=v.grouped?categoryBands.map(b=>({y:(1-b.center/categoryHeight)*v.ymax,label:categories().find(([key])=>key===b.key)[1]})):[];
    if(!v.grouped && numericPositions.size)for(let value=Math.max(0,Math.ceil(ymin/ys)*ys);value<=Math.min(v.ymax-8,ymax+ys);value+=ys)ticks.push({y:numericY(value),label:value});
    if(!v.grouped && unknownPositions.size)ticks.push({y:(numericHeight+(categoryHeight-numericHeight)/2)/categoryHeight*v.ymax,label:'参数待核'});
    for(const {y,label} of ticks){
      const py=screen(v.min,y).y;if(py<top-20||py>H-bottom+1)continue;
      grid.append(sv('line',{x1:left,x2:W-right,y1:py,y2:py,class:'grid-line'}));
      axes.append(sv('text',{x:left-12,y:py+3,'text-anchor':'end'},label));
    }
    if(!v.grouped)for(const g of gs){
      if(g.ax<left||g.ax>W-right||g.ay<top-20||g.ay>H-bottom)continue;
      if(Number.isFinite(numeric(g.members[0].h,v.yf))){
        const selected=!inspector.hidden && inspector.dataset.groupKey===g.key;
        grid.append(sv('circle',{cx:g.ax,cy:g.ay,r:selected?3.5:2,fill:'var(--dex-accent)',class:'dex-coordinate-anchor'}));
        // One temporary guide identifies the exact numeric coordinate of the
        // hovered label; there is no permanent network of connection lines.
        if(selected && Math.abs(g.y-g.ay)>12)grid.append(sv('line',{x1:g.ax,x2:g.x,y1:g.ay,y2:g.y,class:'coordinate-leader'}));
      }
    }
    axes.append(sv('path',{d:`M${left} ${top-20} V${H-bottom} H${W-right}`,class:'axis-line'}));
    const detailedTime=(W-left-right)*camera.k/(v.max-v.min)>=150;
    const period=Math.floor(xmin)===Math.floor(xmax)?String(Math.floor(xmin)):`${Math.floor(xmin)}–${Math.floor(xmax)}`;
    axes.append(sv('text',{x:(W+left-right)/2,y:H-15,'text-anchor':'middle',class:'axis-label'},'公开时间'+(detailedTime?' · '+period:'')));
    if(!v.grouped)axes.append(sv('text',{x:19,y:(H+top-bottom)/2,transform:`rotate(-90 19 ${(H+top-bottom)/2})`,'text-anchor':'middle',class:'axis-label'},v.y));
  }
  function draw() {
    const gs=groups(),active=new Set();drawAxes(gs);root.dataset.detailZoom=camera.k>=2.6?'true':'false';
    root.style.setProperty('--label-detail',Math.max(0,Math.min(1,(camera.k-1)/1.5)));
    // Clip individual labels to the coordinate plane.
    nodeLayer.style.clipPath=`inset(${top-20}px ${right}px ${bottom}px ${left}px)`;
    rendered=gs.filter(g=>g.ax>=left&&g.ax<=W-right&&g.y>=top-12&&g.y<=H-bottom-10);
    for(const g of rendered){
      active.add(g.key);let n=elements.get(g.key);
      if(!n){
        n=el('a',null,'dex-node');
        n.href=link(g.members[0].h);n.setAttribute('aria-label','查看 '+g.members[0].h.name+' 详情');
        const h=g.members[0].h;
        n.append(el('i',null,'dex-node-dot'),el('span',short(h),'dex-node-label'));
        n.dataset.kind=h.kind || 'hand';
        n.dataset.precision=window.DexTrailMapTime.point(h)?.precision;
        n.addEventListener('mouseenter',()=>{clearTimeout(previewTimer);previewTimer=setTimeout(()=>describe(n.group),400);});
        n.addEventListener('mouseleave',()=>{clearTimeout(previewTimer);if(dismissedPreviewKey===n.group.key)dismissedPreviewKey=null;});
        n.addEventListener('focus',()=>{if(n.matches(':focus-visible') && (inspector.hidden || inspector.dataset.groupKey!==n.group.key))describe(n.group);});
        elements.set(g.key,n);nodeLayer.append(n);
      }
      n.dataset.members=g.key;n.group=g;n.style.left=g.x+'px';n.style.top=g.y+'px';n.style.width=g.width+'px';n.style.height=g.height+'px';n.style.setProperty('--node-color',g.color);
      n.dataset.side=g.x+g.width>W-right?'left':'right';
      n.style.width=Math.min(g.width,Math.max(12,n.dataset.side==='left'?g.x-left-4:W-right-g.x-4))+'px';
      n.dataset.coordinate=views[view].grouped?'category':g.members[0].y<0?'unknown':'displaced';
      const h=g.members[0].h,value=views[view].grouped?'':` · ${numeric(h,views[view].yf) ?? '待核实'} ${view==='actuators'?'执行器':'主动轴'}`;
      n.querySelector('.dex-node-label').textContent=short(h);
      n.title=(h.timeline?.label || h.coordinates.year)+' · '+h.name+value;
      n.dataset.year=h.coordinates.year;n.dataset.time=g.members[0].x;n.dataset.anchorY=g.ay;n.dataset.anchorX=g.ax;

    }
    for(const [key,n] of elements)if(!active.has(key)){n.remove();elements.delete(key);}
    $('.dex-zoom-readout').textContent=camera.k.toFixed(2)+'×';
    $('[data-action="out"]').disabled=target.k<=1;
    $('[data-action="in"]').disabled=target.k>=window.DexTrailNameLayout.MAX_ZOOM;
    root.dataset.renderedNodes=rendered.length;root.dataset.positioned=placed.length;
  }
  function animate(){
    frame=0;const delta=Math.abs(target.k-camera.k)+Math.abs(target.x-camera.x)+Math.abs(target.y-camera.y);
    if(reduced||delta<.12)camera={...target};else for(const k of ['k','x','y'])camera[k]+=(target[k]-camera[k])*.2;
    draw();if(!reduced&&delta>=.12)frame=requestAnimationFrame(animate);
  }
  function requestDraw(){
    target=window.DexTrailNameLayout.camera(target,W-left-right,H-top-bottom);
    camera=window.DexTrailNameLayout.camera(camera,W-left-right,H-top-bottom);
    if(!frame)frame=requestAnimationFrame(animate);
  }
  function zoom(factor,x=W/2,y=H/2){
    closePreview();hoverResumeAt=performance.now()+600;
    const k=Math.max(1,Math.min(window.DexTrailNameLayout.MAX_ZOOM,target.k*factor)),r=k/target.k;
    target.x=x-left-(x-left-target.x)*r;target.y=y-(H-bottom)-(y-(H-bottom)-target.y)*r;target.k=k;requestDraw();
  }
  function reset(){target={k:1,x:0,y:0};closePreview();requestDraw();}
  function resize(){
    const oldWidth=W-left-right,oldHeight=H-top-bottom;
    const width=stage.clientWidth,height=stage.clientHeight;
    // Hidden tabs and screenshot/layout transitions can briefly report zero size.
    // Preserve the camera until the actual coordinate plane is measurable again.
    if(!width || !height)return;
    const changed=W>0 && H>0 && (width!==W || height!==H);
    W=width;H=height;left=views[view].grouped?(W<600?86:108):(W<600?62:82);right=W<600?80:145;
    if(changed){
      const sx=Math.max(1,W-left-right)/Math.max(1,oldWidth),sy=Math.max(1,H-top-bottom)/Math.max(1,oldHeight);
      target.x*=sx;target.y*=sy;camera.x*=sx;camera.y*=sy;
    }
    updateLabelOffsets();
    const minimum=top+bottom+categoryHeight;
    stage.style.minHeight=Math.max(360,Math.min(1250,minimum))+'px';
    requestDraw();
  }
  // Keep exploration in this tab, including visits via the explicit return link.
  // Normalized offsets restore the same area when the viewport size changes.
  const stateKey = 'dextrail-map:name-calendar-v1:' + new URL('.', document.baseURI).pathname;
  const allowedState = {views:Object.keys(views),tags:new Set(tagIndex.keys()),hands:new Set(entries.map(h=>h.id))};
  function saveExploration() {
    if (!W || !H) return;
    window.DexTrailMapState.save(stateKey, {
        view, query:search.value, tags:[...selectedTags], k:target.k,
        x:target.x / Math.max(1,W-left-right), y:target.y / Math.max(1,H-top-bottom),
        expanded:[], pending:!pending.hidden, scrollY:window.scrollY,
        listScroll:$('.dex-unplaced-list').scrollTop,
      }, allowedState);
  }
  function restoreExploration() {
    const saved=window.DexTrailMapState.read(stateKey,allowedState);
    if(!saved)return false;
    view=saved.view;search.value=saved.query;
    for(const id of saved.tags || [])if(tagIndex.has(id))selectedTags.add(id);
    configureAxes();
    root.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
    updateData();resize();
    target={k:saved.k,x:saved.x*Math.max(1,W-left-right),y:saved.y*Math.max(1,H-top-bottom)};
    camera={...target};
    pending.hidden=saved.pending!==true;
    $('.dex-pending-toggle').setAttribute('aria-expanded',String(!pending.hidden));
    requestAnimationFrame(()=>{
      if (Number.isFinite(saved.listScroll)) $('.dex-unplaced-list').scrollTop=saved.listScroll;
      if (Number.isFinite(saved.scrollY)) window.scrollTo(0,Math.max(0,saved.scrollY));
    });
    root.dataset.restored='true';
    $('.dex-resume-note').hidden=!(saved.view!=='transmission'||saved.query.trim()||saved.tags.length||saved.k!==1||saved.x||saved.y||saved.expanded.length||saved.pending);
    requestDraw();return true;
  }
  document.addEventListener('click',e=>{if(e.target.closest('a[href]'))saveExploration();},true);
  window.addEventListener('pagehide',saveExploration);
  root.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{
    view=b.dataset.view;root.querySelectorAll('[data-view]').forEach(n=>n.setAttribute('aria-pressed',n===b));updateData();resize();reset();
  }));
  search.addEventListener('input',()=>{updateData();resize();reset();});
  $('.dex-pending-toggle').onclick=()=>{pending.hidden=!pending.hidden;$('.dex-pending-toggle').setAttribute('aria-expanded',!pending.hidden);};
  $('.dex-drawer-heading button').onclick=()=>{pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');$('.dex-pending-toggle').focus();};
  $('.dex-inspector-close').onclick=()=>closePreview(true);
  inspector.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();closePreview(true);}});
  root.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>{
    const a=b.dataset.action;if(a==='reset'){reset();return;}
    const xs=rendered.map(g=>g.x).sort((a,b)=>a-b),ys=rendered.map(g=>g.y).sort((a,b)=>a-b);
    zoom(a==='in'?1.35:1/1.35,xs.length?xs[Math.floor(xs.length/2)]:W/2,ys.length?ys[Math.floor(ys.length/2)]:H/2);
  });
  const interactive=e=>e.target.closest('.dex-inspector,.dex-pending,.dex-scale');
  stage.addEventListener('wheel',e=>{if(interactive(e))return;e.preventDefault();const r=stage.getBoundingClientRect();zoom(Math.exp(-Math.max(-120,Math.min(120,e.deltaY))*.0028),e.clientX-r.left,e.clientY-r.top);},{passive:false});
  const pointers=new Map();let pinch=null;
  stage.addEventListener('pointerdown',e=>{
    if(interactive(e)||e.target.closest('.dex-node')||e.button>0)return;
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});moved=false;
    if(pointers.size===2){const [a,b]=[...pointers.values()];pinch={distance:Math.hypot(a.x-b.x,a.y-b.y)};drag=null;return;}
    drag={id:e.pointerId,startX:e.clientX,startY:e.clientY,x:e.clientX,y:e.clientY,last:performance.now(),vx:0,vy:0};
  });
  stage.addEventListener('pointermove',e=>{
    if(!pointers.has(e.pointerId))return;
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
    if(pinch&&pointers.size===2){const [a,b]=[...pointers.values()],distance=Math.hypot(a.x-b.x,a.y-b.y),r=stage.getBoundingClientRect();zoom(distance/Math.max(1,pinch.distance),(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top);pinch.distance=distance;moved=true;return;}
    if(!drag||e.pointerId!==drag.id)return;
    if(Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)>5)moved=true;
    if(moved){stage.setPointerCapture(e.pointerId);stage.classList.add('is-dragging');const now=performance.now(),dt=Math.max(8,now-drag.last);drag.vx=(e.clientX-drag.x)/dt;drag.vy=(e.clientY-drag.y)/dt;target.x+=e.clientX-drag.x;target.y+=e.clientY-drag.y;drag.x=e.clientX;drag.y=e.clientY;drag.last=now;camera={...target};if(!inspector.hidden)closePreview();requestDraw();}
  });
  function release(e){
    pointers.delete(e.pointerId);pinch=null;
    if(drag?.id===e.pointerId){if(moved&&!reduced&&performance.now()-drag.last<80){target.x+=Math.max(-180,Math.min(180,drag.vx*90));target.y+=Math.max(-180,Math.min(180,drag.vy*90));requestDraw();}drag=null;}
    stage.classList.remove('is-dragging');
  }
  window.addEventListener('pointerup',release);stage.addEventListener('pointercancel',release);
  stage.addEventListener('keydown',e=>{
    if(e.target!==stage)return;
    const keys=['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','Home','Escape'];if(!keys.includes(e.key))return;e.preventDefault();
    if(e.key==='Home')reset();else if(e.key==='+'||e.key==='=')zoom(1.35);else if(e.key==='-')zoom(1/1.35);else if(e.key==='Escape'){closePreview();pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');}else {target.x+=e.key==='ArrowRight'?-50:e.key==='ArrowLeft'?50:0;target.y+=e.key==='ArrowDown'?-50:e.key==='ArrowUp'?50:0;requestDraw();}
  });
  document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.target.matches('input,textarea')){e.preventDefault();search.focus();}});
  new ResizeObserver(resize).observe(stage);
  if (!restoreExploration()) {updateData();resize();}

  root.dataset.renderer='html';
  requestDraw();
})();
