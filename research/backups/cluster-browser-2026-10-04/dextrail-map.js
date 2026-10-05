/* DexTrail: coordinate map, proximity groups and accessible specimen entries. */
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
  for (const [label, color] of Object.values(routes)) {
    const item = el('span'), dot = el('i'); dot.style.setProperty('--route-color',color);
    item.append(dot, document.createTextNode(label)); $('.dex-legend').append(item);
  }
  let view = 'transmission', W = 0, H = 0, left = 65, top = 132, right = 65, bottom = 80;
  let camera = {k:1,x:0,y:0}, target = {...camera}, frame = 0;
  let placed = [], missing = [], expanded = new Set(), drag = null, moved = false;
  let rendered = [], pinned = false;
  const elements = new Map();
  const mapThumbnails = new Map();
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
  const numeric = (h, key) => key==='fingers' ? h.classification?.fingers : h.coordinates[key];
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
      v.min=Math.floor((Math.min(...xs)-3)/5)*5;
      v.max=Math.ceil((Math.max(...xs)+5)/5)*5;
      v.ymax=v.grouped?categories(v).length:Math.max(8,Math.ceil(Math.max(0,...ys)/8)*8+4);
    }
  }
  configureAxes();syncFilters();
  const collectionLabel = `${data.hands.length} 款手 · ${(data.systems || []).length} 个系统`;
  const link = h => new URL(h.detail_url || 'hands/generated/'+h.id+'/', document.baseURI).href;
  const short = h => h.name.replace('Shadow Dexterous Hand（Classic 五指版）','Shadow Hand').replace('LEAP Hand v1（Full）','LEAP Hand v1');
  const gap = (h,k) => h.coordinates.gaps?.[k] || ({dof:'主动轴口径尚未核实',actuators:'执行器总数尚未核实',year:'公开时间依据尚未核实',fingers:'手指数尚无结构化记录',transmission:'传动分类尚未核实'}[k]);
  function image(h, cls) {
    const url = thumb(h);
    if (!url) return el('span',h.kind === 'system' ? 'R1' : '◇','dex-node-glyph');
    const img = el('img',null,cls); img.src = url; img.alt = h.name; img.loading = 'lazy'; img.decoding = 'async';
    img.addEventListener('error', () => {img.replaceWith(el('span','◇','dex-node-glyph'));}, {once:true});
    return img;
  }
  function coordinates(h) {
    const v=views[view];
    return [numeric(h,'year'), v.grouped?categories().findIndex(([key])=>key===groupKey(h))+.5:numeric(h,v.yf)];
  }
  function screen(x,y) {
    const v = views[view];
    return {x:left + ((x-v.min)/(v.max-v.min)*(W-left-right))*camera.k+camera.x,
            y:H-bottom-(y/v.ymax*(H-top-bottom))*camera.k+camera.y};
  }
  function updateData() {
    syncFilters();
    root.dataset.view = view;
    placed = []; missing = []; expanded.clear();
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
    $('.dex-coordinate-note').textContent = `横轴：${v.x}；纵轴：${v.y}。` + (v.grouped?'未知信息保留独立分区。':'缺少数值坐标的档案保留在下方；执行器数不等于独立输入数。');
    $('.dex-view-title').textContent = v.name;
    inspector.hidden = true; pinned = false;
  }
  function describe(group, pin = false) {
    if (drag || (pinned && !pin)) return;
    pinned = pin;
    inspector.dataset.side = group.x > W/2 ? 'left' : 'right';
    const box = $('.dex-inspector-content'); box.replaceChildren(); inspector.hidden = false;
    if (group.members.length > 1) {
      box.append(el('small','相近坐标'),el('h3',group.members.length+' 款产品'),el('p','图片直接打开对应产品，下方可选择同组其他产品。放大后逐步分开；坐标重合的产品保留在同组，避免错置年份或类别。'));
      const links = el('div',null,'dex-cluster-links');
      for (const p of group.members) {const a = el('a',(p.h.timeline?.label ? p.h.timeline.label+' · ' : '')+p.h.name+' ↗'); a.href=link(p.h);links.append(a);}
      box.append(links);
      const expand=el('button','放大这一组','dex-expand-group');expand.type='button';
      expand.onclick=()=>{group.members.forEach(p=>expanded.add(p.h.id));zoom(1.65,group.ax,group.ay);target.x+=(W+left-right)/2-group.ax;target.y+=(H+top-bottom)/2-group.ay;inspector.hidden=true;pinned=false;};box.append(expand);
    } else {
      const h = group.members[0].h;
      box.append(image(h,'dex-preview-img'),el('small',route(h)),el('h3',h.name));
      box.append(el('p',h.kind === 'system' ? '已收录 · 机器人系统；手部参数另行核实。' : `自由度：${h.facts?.dof?.value ?? h.coordinates.dof ?? gap(h,'dof')} · 执行器：${h.facts?.actuators?.value ?? h.coordinates.actuators ?? gap(h,'actuators')}`));
      box.append(el('p',h.coordinates.scope));
      if (h.timeline) {
        box.append(el('p',h.timeline.label,'dex-year-label'),el('p',h.timeline.detail));
        const source=el('a','时间依据：'+h.timeline.source.title+' ↗');
        source.href=h.timeline.source.url;source.target='_blank';source.rel='noopener';box.append(source);
      }
      const a = el('a','查看技术档案 ↗','dex-read-more'); a.href=link(h);box.append(a);
      if (h.kind !== 'system') {const compare = el('a','与其他灵巧手对比 ↗','dex-read-more');compare.href='compare/?add='+encodeURIComponent(h.id);box.append(compare);}
    }
  }
  // Cluster close points at low magnification. No synthetic product nodes are added.
  function groups() {
    const points = placed.map(p => ({...p,...screen(p.x,p.y)}));
    const result = [];
    for (const p of points) {
      const threshold = expanded.has(p.h.id) ? 134 : 148;
      let g = result.find(g => (!views[view].grouped || groupKey(g.members[0].h) === groupKey(p.h)) && Math.abs(g.x-p.x)<threshold && Math.abs(g.y-p.y)<48);
      if (!g) {g={x:p.x,y:p.y,members:[],expanded:expanded.has(p.h.id)};result.push(g);}
      g.members.push(p);g.x=g.members.reduce((s,p)=>s+p.x,0)/g.members.length;g.y=g.members.reduce((s,p)=>s+p.y,0)/g.members.length;
    }
    // Updating a group's centroid can bring two previously separate groups
    // together. Merge again so specimen rectangles never cover each other.
    let merged=true;
    while(merged){
      merged=false;
      for(let i=0;i<result.length&&!merged;i++)for(let j=i+1;j<result.length;j++){
        const a=result[i],b=result[j];
        if(views[view].grouped && groupKey(a.members[0].h)!==groupKey(b.members[0].h))continue;
        if(Math.abs(a.x-b.x)>=156 || Math.abs(a.y-b.y)>=48)continue;
        a.members.push(...b.members);a.expanded=a.expanded||b.expanded;
        a.x=a.members.reduce((sum,p)=>sum+p.x,0)/a.members.length;
        a.y=a.members.reduce((sum,p)=>sum+p.y,0)/a.members.length;
        result.splice(j,1);merged=true;break;
      }
    }
    // Keep real coordinates at every zoom. Identical coordinates remain selectable
    // through the group list rather than being scattered into another category.
    for (const g of result) {
      g.ax=g.x;g.ay=g.y;g.width=g.members.length>1?148:132;g.height=44;
      g.key=g.members.map(p=>p.h.id).sort().join('|');
      g.colors=[...new Set(g.members.map(p=>color(p.h)))];g.color=g.colors.length===1?g.colors[0]:'#747873';
    }
    return result;
  }
  function drawAxes(gs) {
    axes.setAttribute('viewBox',`0 0 ${W} ${H}`); axes.replaceChildren();
    const defs=sv('defs',{}),clip=sv('clipPath',{id:'dex-plot-clip'});
    clip.append(sv('rect',{x:left,y:top-20,width:W-left-right,height:H-top-bottom+20}));defs.append(clip);axes.append(defs);
    const grid=sv('g',{'clip-path':'url(#dex-plot-clip)'});axes.append(grid);
    const v=views[view], step=camera.k>2?1:5;
    // Compute visible ticks from the camera rather than stretching fixed labels.
    const xmin=v.min-camera.x/camera.k/(W-left-right)*(v.max-v.min);
    const xmax=xmin+(v.max-v.min)/camera.k;
    for(let x=Math.ceil(xmin/step)*step;x<=xmax+step;x+=step) {
      const px=screen(x,0).x;if(px<left-1||px>W-right+1)continue;
      grid.append(sv('line',{x1:px,x2:px,y1:top-20,y2:H-bottom,class:'grid-line'}));
      axes.append(sv('line',{x1:px,x2:px,y1:H-bottom,y2:H-bottom+5,class:'tick-line'}));
      const label = String(x);
      const tick = sv('text',{x:px,y:H-bottom+24,'text-anchor':'middle'});
      tick.textContent=label;
      axes.append(tick);
    }
    const yExtent=v.ymax, ys=camera.k>2?2:8;
    const ymin=camera.y/camera.k/(H-top-bottom)*yExtent, ymax=ymin+yExtent/camera.k;
    const ticks=v.grouped?categories().map(([k,label],i)=>({y:i+.5,label})):[];
    if(!v.grouped)for(let y=Math.ceil(ymin/ys)*ys;y<=ymax+ys;y+=ys)ticks.push({y,label:y});
    for(const {y,label} of ticks){
      const py=screen(v.min,y).y;if(py<top-20||py>H-bottom+1)continue;
      grid.append(sv('line',{x1:left,x2:W-right,y1:py,y2:py,class:'grid-line'}));
      axes.append(sv('text',{x:left-12,y:py+3,'text-anchor':'end'},label));
    }
    axes.append(sv('path',{d:`M${left} ${top-20} V${H-bottom} H${W-right}`,class:'axis-line'}));
    axes.append(sv('text',{x:(W+left-right)/2,y:H-15,'text-anchor':'middle',class:'axis-label'},v.x));
    if(!v.grouped)axes.append(sv('text',{x:19,y:(H+top-bottom)/2,transform:`rotate(-90 19 ${(H+top-bottom)/2})`,'text-anchor':'middle',class:'axis-label'},v.y));
  }
  function draw() {
    const gs=groups(),active=new Set();drawAxes(gs);root.dataset.detailZoom=camera.k>=2.6?'true':'false';
    // Clip whole entries to the coordinate plane, including labels and group buttons.
    nodeLayer.style.clipPath=`inset(${top-20}px ${right}px ${bottom}px ${left}px)`;
    rendered=gs.filter(g=>g.x+g.width/2>left&&g.x-g.width/2<W-right&&g.y+g.height/2>top-20&&g.y-g.height/2<H-bottom);
    for(const g of rendered){
      active.add(g.key);let n=elements.get(g.key);
      if(!n){
        const cluster=g.members.length>1;n=el(cluster?'div':'a',null,'dex-node'+(cluster?' is-cluster':''));
        const product=cluster?el('a',null,'dex-cluster-product'):n;
        product.href=link(g.members[0].h);product.setAttribute('aria-label','查看 '+g.members[0].h.name+' 详情');
        const h=g.members[0].h;
        let thumbnail=mapThumbnails.get(h.id);
        if(!thumbnail){
          thumbnail=image(h);
          if(thumbnail.tagName==='IMG'){
            thumbnail.loading='eager';
            thumbnail.addEventListener('error',()=>mapThumbnails.set(h.id,el('span','◇','dex-node-glyph')),{once:true});
          }
          mapThumbnails.set(h.id,thumbnail);
        }
        product.append(thumbnail,el('span',short(g.members[0].h),'dex-node-label'));
        product.title=g.members.map(p=>(p.h.timeline?.label || p.h.coordinates.year)+' · '+p.h.name).join('\n');
        if(cluster){
          n.append(product);
          const expand=el('button',null,'dex-node-count');expand.type='button';expand.append(el('span',g.members.length));
          expand.title=`选择同组 ${g.members.length} 款产品`;
          expand.setAttribute('aria-label',`选择这组 ${g.members.length} 款产品`);
          expand.addEventListener('click',e=>{e.stopPropagation();describe(n.group,true);});
          n.append(expand);
        }
        n.addEventListener('mouseenter',()=>describe(n.group));product.addEventListener('focus',()=>describe(n.group));
        elements.set(g.key,n);nodeLayer.append(n);
      }
      n.dataset.members=g.key;n.group=g;n.style.left=g.x+'px';n.style.top=g.y+'px';n.style.width=g.width+'px';n.style.height=g.height+'px';n.style.setProperty('--node-color',g.color);
      n.style.setProperty('--cluster-stops',g.members.map((p,i)=>`${color(p.h)} ${i/g.members.length*100}% ${(i+1)/g.members.length*100}%`).join(','));
    }
    for(const [key,n] of elements)if(!active.has(key)){n.remove();elements.delete(key);}
    $('.dex-zoom-readout').textContent=camera.k.toFixed(2)+'×';
    root.dataset.renderedNodes=rendered.length;root.dataset.positioned=placed.length;
  }
  function animate(){
    frame=0;const delta=Math.abs(target.k-camera.k)+Math.abs(target.x-camera.x)+Math.abs(target.y-camera.y);
    if(reduced||delta<.12)camera={...target};else for(const k of ['k','x','y'])camera[k]+=(target[k]-camera[k])*.2;
    draw();if(!reduced&&delta>=.12)frame=requestAnimationFrame(animate);
  }
  function requestDraw(){if(!frame)frame=requestAnimationFrame(animate);}
  function zoom(factor,x=W/2,y=H/2){
    const k=Math.max(.65,Math.min(6,target.k*factor)),r=k/target.k;
    target.x=x-left-(x-left-target.x)*r;target.y=y-(H-bottom)-(y-(H-bottom)-target.y)*r;target.k=k;requestDraw();
  }
  function reset(){target={k:1,x:0,y:0};expanded.clear();requestDraw();}
  function resize(){
    stage.style.minHeight=views[view].grouped?`${top+bottom+categories().length*68}px`:'540px';
    const oldWidth=W-left-right,oldHeight=H-top-bottom;
    const width=stage.clientWidth,height=stage.clientHeight;
    const changed=W>0 && H>0 && (width!==W || height!==H);
    W=width;H=height;left=views[view].grouped?(W<600?92:112):(W<600?47:65);right=W<600?40:65;
    if(changed){
      const sx=Math.max(1,W-left-right)/Math.max(1,oldWidth),sy=Math.max(1,H-top-bottom)/Math.max(1,oldHeight);
      target.x*=sx;target.y*=sy;camera.x*=sx;camera.y*=sy;
    }
    requestDraw();
  }
  // Keep exploration in this tab, including visits via the explicit return link.
  // Normalized offsets restore the same area when the viewport size changes.
  const stateKey = 'dextrail-map:time-x-v2:' + new URL('.', document.baseURI).pathname;
  const allowedState = {views:Object.keys(views),tags:new Set(tagIndex.keys()),hands:new Set(entries.map(h=>h.id))};
  function saveExploration() {
    if (!W || !H) return;
    window.DexTrailMapState.save(stateKey, {
        view, query:search.value, tags:[...selectedTags], k:target.k,
        x:target.x / Math.max(1,W-left-right), y:target.y / Math.max(1,H-top-bottom),
        expanded:[...expanded], pending:!pending.hidden, scrollY:window.scrollY,
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
    const ids=new Set(entries.map(h=>h.id));
    expanded=new Set(Array.isArray(saved.expanded)?saved.expanded.filter(id=>ids.has(id)):[]);
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
  search.addEventListener('input',()=>{updateData();reset();});
  $('.dex-pending-toggle').onclick=()=>{pending.hidden=!pending.hidden;$('.dex-pending-toggle').setAttribute('aria-expanded',!pending.hidden);};
  $('.dex-drawer-heading button').onclick=()=>{pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');$('.dex-pending-toggle').focus();};
  $('.dex-inspector-close').onclick=()=>{inspector.hidden=true;pinned=false;stage.focus();};
  root.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>{const a=b.dataset.action;if(a==='reset')reset();else zoom(a==='in'?1.35:1/1.35);});
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
    if(moved){stage.setPointerCapture(e.pointerId);stage.classList.add('is-dragging');const now=performance.now(),dt=Math.max(8,now-drag.last);drag.vx=(e.clientX-drag.x)/dt;drag.vy=(e.clientY-drag.y)/dt;target.x+=e.clientX-drag.x;target.y+=e.clientY-drag.y;drag.x=e.clientX;drag.y=e.clientY;drag.last=now;camera={...target};inspector.hidden=true;requestDraw();}
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
    if(e.key==='Home')reset();else if(e.key==='+'||e.key==='=')zoom(1.35);else if(e.key==='-')zoom(1/1.35);else if(e.key==='Escape'){inspector.hidden=true;pending.hidden=true;$('.dex-pending-toggle').setAttribute('aria-expanded','false');}else {target.x+=e.key==='ArrowRight'?-50:e.key==='ArrowLeft'?50:0;target.y+=e.key==='ArrowDown'?-50:e.key==='ArrowUp'?50:0;requestDraw();}
  });
  document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.target.matches('input,textarea')){e.preventDefault();search.focus();}});
  new ResizeObserver(resize).observe(stage);
  if (!restoreExploration()) {updateData();resize();}

  root.dataset.renderer='html';
  requestDraw();
})();
