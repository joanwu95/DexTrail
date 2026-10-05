const themePicker=document.querySelector('[aria-label="预览配色"]');
const palette=new URLSearchParams(location.search).get('theme');
if(['paper','slate','white','plum'].includes(palette))document.body.dataset.theme=palette;
themePicker.value=document.body.dataset.theme;
themePicker.onchange=()=>document.body.dataset.theme=themePicker.value;
const escapeHtml=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const detailUrl=h=>'http://127.0.0.1:8000/'+(h.kind==='system'?'systems/sudo-r1/':'hands/generated/'+h.id+'/');
const picture=h=>h.media?.kind==='video'?h.media.poster:h.media?.url;
const names=h=>h.id==='shadow-hand'?'Shadow Hand':h.name.replace(/（.*?）/g,'').replace('Shadow Dexterous Hand','Shadow Hand');
const routes={'tendon-driven':['腱绳传动','#b48a73'],'direct-drive':['直接驱动','#7891ab'],'linkage-driven':['连杆传动','#7d9e91'],'hybrid-transmission':['混合传动','#a191b2'],'geared-drive':['齿轮传动','#9e9976'],'unknown':['待核实','#909aa6']};
if(document.querySelector('.plot'))initMap();
if(document.querySelector('.dimensions'))initDetail();
async function initDetail(){
 const data=await (await fetch('detail-data.json')).json(),menu=document.querySelector('.dimensions'),panel=document.querySelector('.content'),title=document.querySelector('.note-title');
 const show=e=>{title.textContent=e.title;panel.innerHTML=e.content_html;menu.querySelectorAll('button').forEach(b=>b.classList.toggle('active',b.dataset.id===e.id));};
 for(const e of data){const b=document.createElement('button');b.type='button';b.textContent=e.title;b.dataset.id=e.id;b.onmouseenter=()=>show(e);b.onfocus=()=>show(e);b.onclick=()=>show(e);menu.append(b);}
 show(data.find(e=>e.id==='mechanics')||data[0]);
 document.querySelectorAll('[data-picture]').forEach(b=>b.onclick=()=>{document.querySelector('.product-profile .hero').src=b.dataset.picture;document.querySelector('.product-profile .hero').alt=b.getAttribute('aria-label');});
}
async function initMap(){
 const database=await(await fetch('specimens.json')).json(),hands=[...database.hands,...(database.systems||[])],plot=document.querySelector('.plot'),svg=document.querySelector('.grid'),layer=document.querySelector('.node-layer'),mode=document.body.dataset.study;
 let selected=hands.find(h=>h.id==='shadow-hand'),view=mode==='lanes'?'route':'dof',scale=1,filter='',routeFilter=null;
 const NS='http://www.w3.org/2000/svg';
 function sv(t,a,text){const n=document.createElementNS(NS,t);for(const [k,v]of Object.entries(a))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;svg.append(n);return n;}
 function route(h){const v=h.classification?.transmission||h.coordinates?.transmission;return routes[v]?v:'unknown';}
 function cat(h){if(view==='route')return route(h);if(view==='fingers'){const f=parseInt(h.facts?.fingers?.value);return f>=2&&f<=5?String(f):'unknown';}const n=h.coordinates?.dof;return typeof n==='number'&&n>0?String(Math.ceil(n/5)*5):'unknown';}
 function categories(){if(view==='route')return Object.entries(routes).map(([k,[v]])=>[k,v]);if(view==='fingers')return [['5','5 指'],['4','4 指'],['3','3 指'],['2','2 指'],['unknown','待核实']];const max=Math.max(25,...hands.map(h=>Math.ceil((h.coordinates?.dof||0)/5)*5));const rows=[];for(let i=max;i>=5;i-=5)rows.push([String(i),`${i-4}–${i} 轴`]);return [...rows,['unknown','待核实']];}
 function describe(h,group){selected=h;document.querySelector('.selection').textContent=names(h)+' · 查看技术档案 ↗';document.querySelector('.selection').href=detailUrl(h);const dock=document.querySelector('.dock');if(dock){const pic=picture(h);dock.innerHTML='<small>PRODUCT / '+(h.coordinates?.year??'未知年份')+'</small>'+(pic?'<img src="'+escapeHtml(pic)+'" alt="'+escapeHtml(h.name)+'">':'<p>此型号暂无可核实的产品图片</p>')+'<h3>'+escapeHtml(names(h))+'</h3><p>'+escapeHtml(h.facts?.company?.value??'机构待核实')+'</p><p>'+escapeHtml(h.coordinates?.scope??'技术范围待核实')+'</p><a href="'+detailUrl(h)+'">进入技术档案 ↗</a>'+(group?.length>1?'<p>同一坐标分组另有 '+(group.length-1)+' 款；放大可进一步展开。</p>':'');}layer.querySelectorAll('.point').forEach(n=>n.classList.toggle('selected',n.dataset.ids.split('|').includes(h.id)));}
 function draw(){
  const W=plot.clientWidth,H=plot.clientHeight,L=88,R=22,T=24,B=49,cats=categories(),pw=W-L-R,ph=H-T-B,min=scale===1?1998:2027-29/scale,max=2027;
  svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${W} ${H}`);layer.replaceChildren();
  const defs=document.createElementNS(NS,'defs'),clip=document.createElementNS(NS,'clipPath');clip.id='study-plot-clip';const rect=document.createElementNS(NS,'rect');for(const[k,v]of Object.entries({x:L,y:T,width:pw,height:ph}))rect.setAttribute(k,v);clip.append(rect);defs.append(clip);svg.append(defs);
  const px=y=>L+(y-min)/(max-min)*pw,cy=k=>T+(cats.findIndex(c=>c[0]===k)+.5)*ph/cats.length;
  const step=scale>1.4?2:5;for(let year=Math.ceil(min/step)*step;year<=max;year+=step){sv('line',{x1:px(year),x2:px(year),y1:T,y2:H-B,class:'guide'});sv('text',{x:px(year),y:H-24,'text-anchor':'middle'},year);}
  for(const[k,label]of cats){const y=cy(k);sv('line',{x1:L,x2:W-R,y1:y,y2:y,class:'guide'});sv('text',{x:L-12,y:y+4,'text-anchor':'end'},label);}
  sv('path',{d:`M${L} ${T}V${H-B}H${W-R}`,fill:'none',class:'axis'});sv('text',{x:(L+W-R)/2,y:H-5,'text-anchor':'middle'},'公开记录时间 / YEAR');
  const visible=hands.filter(h=>h.coordinates?.year>=min&&h.coordinates.year<=max&&(!routeFilter||route(h)===routeFilter)&&(!filter||(h.name+' '+(h.facts?.company?.value??'')).toLowerCase().includes(filter)));
  const groups=[];
  for(const h of visible){const x=px(h.coordinates.year),y=cy(cat(h)),threshold=mode==='precision'?22:scale>1.5?40:80;let g=groups.find(g=>g.cat===cat(h)&&Math.abs(g.ax-x)<threshold);if(!g){g={cat:cat(h),ax:x,ay:y,members:[]};groups.push(g);}g.members.push(h);g.ax=g.members.reduce((sum,h)=>sum+px(h.coordinates.year),0)/g.members.length;}
  const bw=mode==='precision'?30:mode==='lanes'?118:87,bh=mode==='precision'?30:mode==='lanes'?44:79,occupied=[];
  groups.sort((a,b)=>a.members.some(h=>h.id===selected.id)?-1:b.members.some(h=>h.id===selected.id)?1:a.ax-b.ax);
  for(const g of groups){
   let best=null;for(let i=0;i<700;i++){const r=i?12*Math.sqrt(i):0,a=i*2.399,x=Math.max(L+bw/2+4,Math.min(W-R-bw/2-4,g.ax+Math.cos(a)*r)),y=Math.max(T+bh/2+3,Math.min(H-B-bh/2-3,g.ay+Math.sin(a)*r));const penalty=occupied.reduce((s,p)=>s+(Math.abs(p.x-x)<bw+8&&Math.abs(p.y-y)<bh+7?10000:0),0)+Math.abs(y-g.ay)*1.7+Math.abs(x-g.ax);if(!best||penalty<best.penalty)best={x,y,penalty};if(penalty<5)break;}g.x=best.x;g.y=best.y;occupied.push(g);
   if(best.penalty>=10000){for(let x=L+bw/2+4;x<=W-R-bw/2-4;x+=12)for(let y=T+bh/2+3;y<=H-B-bh/2-3;y+=12){if(occupied.slice(0,-1).some(p=>Math.abs(p.x-x)<bw+8&&Math.abs(p.y-y)<bh+7))continue;const penalty=Math.abs(y-g.ay)*1.7+Math.abs(x-g.ax);if(penalty<best.penalty)best={x,y,penalty};}g.x=best.x;g.y=best.y;}
   if(Math.hypot(g.x-g.ax,g.y-g.ay)>7)sv('line',{x1:g.ax,y1:g.ay,x2:g.x,y2:g.y,class:'leader','clip-path':'url(#study-plot-clip)'});
   const h=g.members.find(h=>h.id===selected.id)||g.members[0],n=document.createElement('a');n.href=detailUrl(h);n.className='point';n.dataset.ids=g.members.map(h=>h.id).join('|');n.setAttribute('aria-label',names(h)+(g.members.length>1?`，同组${g.members.length}款`:'')+'，进入技术档案');n.style.left=g.x+'px';n.style.top=g.y+'px';n.style.setProperty('--point-color',routes[route(h)][1]);const pic=picture(h);if(pic){const img=document.createElement('img');img.className='pic';img.src=pic;img.alt=h.name;img.decoding='sync';n.append(img);}else {const empty=document.createElement('span');empty.className='pic';empty.textContent='暂无实物图';n.append(empty);}const d=document.createElement('span');d.className='diamond';n.append(d);const name=document.createElement('span');name.className='name';name.textContent=names(h);n.append(name);if(g.members.length>1){const count=document.createElement('span');count.className='count';count.textContent=mode==='precision'?'×'+g.members.length:'+'+(g.members.length-1);n.append(count);}n.onmouseenter=()=>describe(h,g.members);n.onfocus=()=>describe(h,g.members);layer.append(n);
  }
  document.querySelector('.coverage').textContent=visible.length+' 个档案 · '+groups.length+' 个坐标分组';document.querySelector('.zoom-label').textContent=scale.toFixed(2)+'×';document.querySelector('[data-view-title]').textContent='公开时间 × '+({dof:'主动轴分组',route:'传动路线',fingers:'手指构型'}[view]);document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===view));describe(selected);
 }
 document.querySelector('.legend').innerHTML=Object.values(routes).slice(0,5).map(([name,c])=>'<span><i style="--point-color:'+c+'"></i>'+name+'</span>').join('');
 document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view;draw();});
 document.querySelectorAll('[data-zoom]').forEach(b=>b.onclick=()=>{scale=b.dataset.zoom==='reset'?1:Math.max(1,Math.min(5,scale*(b.dataset.zoom==='in'?1.35:1/1.35)));draw();});
 document.querySelector('[type=search]').oninput=e=>{filter=e.target.value.trim().toLowerCase();draw();};
 document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{routeFilter=routeFilter===b.dataset.route?null:b.dataset.route;b.setAttribute('aria-pressed',String(routeFilter===b.dataset.route));draw();});
 plot.addEventListener('wheel',e=>{e.preventDefault();scale=Math.max(1,Math.min(5,scale*(e.deltaY<0?1.13:1/1.13)));draw();},{passive:false});
 new ResizeObserver(draw).observe(plot);draw();
}
