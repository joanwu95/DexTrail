(async()=>{
const db=await(await fetch('specimens.json')).json();
const hands=[...db.hands,...(db.systems||[])],mode=document.body.dataset.mode;
const routes=[['tendon-driven','腱绳传动'],['linkage-driven','连杆传动'],['hybrid-transmission','混合传动'],['geared-drive','齿轮传动'],['direct-drive','直接驱动'],['unknown','传动待核实']];
const route=h=>h.classification?.transmission||'unknown';
const name=h=>h.display_name||h.name.replace('Shadow Dexterous Hand（Classic 五指版）','Shadow Hand').replace('LEAP Hand v1（Full）','LEAP Hand v1');
const pic=h=>h.media?.poster||(h.media?.kind==='image'?h.media.url:null);
const url=h=>new URL(h.detail_url||`hands/generated/${h.id}/`,'http://127.0.0.1:8000/').href;
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
function image(h){const src=pic(h);if(!src)return el('span','◇','missing-image');const n=el('img');n.src=src;n.alt=name(h);n.addEventListener('error',()=>n.replaceWith(el('span','◇','missing-image')),{once:true});return n;}
let query='',filter=null,scale=1,selected=hands.find(h=>h.id===(mode==='c'?'shadow-hand':'leap-hand'));
const filtered=()=>hands.filter(h=>(!filter||route(h)===filter)&&(!query||(h.name+' '+(h.facts?.company?.value||'')).toLowerCase().includes(query)));
function select(h){selected=h;const a=document.querySelector('.selected-link');a.textContent=name(h)+' · 技术档案 ↗';a.href=url(h);document.querySelectorAll('[data-id]').forEach(n=>n.classList.toggle('selected',n.dataset.id===h.id));}
function tip(h,x,y){select(h);const t=document.querySelector('.tooltip');t.replaceChildren(image(h),el('strong',name(h)),el('p',h.timeline?.label||String(h.coordinates.year)),el('p',h.facts?.company?.value||routes.find(r=>r[0]===route(h))[1]));t.style.left=Math.max(90,Math.min(document.querySelector('.plot').clientWidth-230,x+12))+'px';t.style.top=Math.max(4,y-74)+'px';t.hidden=false;}
function drawMap(){
 const plot=document.querySelector('.plot'),svg=document.querySelector('.axes'),layer=document.querySelector('.points'),W=plot.clientWidth,H=plot.clientHeight,L=88,R=28,T=15,B=49;
 svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.replaceChildren();layer.replaceChildren();
 const NS='http://www.w3.org/2000/svg';const sv=(tag,attrs,text)=>{const n=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;svg.append(n);return n;};
 const min=scale===1?2000:scale===2?2017:2022,max=2027;
 const px=y=>L+(y-min)/(max-min)*(W-L-R),rh=(H-T-B)/6;
 for(let year=Math.ceil(min/(scale===1?5:1))*(scale===1?5:1);year<=max;year+=scale===1?5:1){const x=px(year);sv('line',{x1:x,x2:x,y1:T,y2:H-B,class:'grid'});sv('text',{x,y:H-25,'text-anchor':'middle'},year);}
 routes.forEach(([key,label],i)=>{const y=T+(i+.5)*rh;sv('line',{x1:L,x2:W-R,y1:y,y2:y,class:'grid'});sv('text',{x:L-12,y:y+4,'text-anchor':'end'},label);});
 sv('path',{d:`M${L} ${T}V${H-B}H${W-R}`,fill:'none',class:'axis'});sv('text',{x:(W+L-R)/2,y:H-5,'text-anchor':'middle'},'公开记录年份');
 const records=filtered().filter(h=>h.coordinates.year>=min&&h.coordinates.year<max),rows=new Map();
 for(const h of records){const key=route(h)+'|'+h.coordinates.year;if(!rows.has(key))rows.set(key,[]);rows.get(key).push(h);}
 const priorities=['shadow-hand','leap-hand','wuji-hand-2','dlr-hand-ii','dlr-clash','orca-hand','linker-l20','allegro-v4','pisa-iit-softhand','ruka-v2','unitree-dex5-s','sharpa-w01'];
 const preferred=new Set(priorities);
 const occupied=[];
 records.sort((a,b)=>Number(preferred.has(b.id))-Number(preferred.has(a.id))||(preferred.has(a.id)?priorities.indexOf(a.id)-priorities.indexOf(b.id):a.coordinates.year-b.coordinates.year));
 for(const h of records){const peers=rows.get(route(h)+'|'+h.coordinates.year).sort((a,b)=>a.id.localeCompare(b.id)),i=peers.findIndex(p=>p.id===h.id),row=routes.findIndex(r=>r[0]===route(h));const x=px(h.coordinates.year),y=T+(row+.5)*rh+(i-(peers.length-1)/2)*Math.min(5,rh*.64/Math.max(1,peers.length-1));
   const n=el('button',null,'point');n.dataset.id=h.id;n.style.left=x+'px';n.style.top=y+'px';n.title=name(h);n.setAttribute('aria-label',name(h));n.append(el('i'));
   const photo=mode==='a'&&pic(h)&&(preferred.has(h.id)||scale>1)&&x>L+20&&x<W-R-20&&!occupied.some(p=>Math.abs(p.x-x)<85&&Math.abs(p.y-y)<62);
   if(photo){n.classList.add('photo');n.append(image(h));const caption=el('span',name(h),'caption');if(row===5){caption.style.top='auto';caption.style.bottom='49px';}if(x<L+70){caption.style.left='0';caption.style.transform='none';}if(x>W-R-70){caption.style.left='auto';caption.style.right='0';caption.style.transform='none';}n.append(caption);occupied.push({x,y});}
   if(mode==='c'&&selected?.id===h.id)n.append(el('span',name(h),'caption'));
   n.onmouseenter=()=>tip(h,x,y);n.onmouseleave=()=>document.querySelector('.tooltip').hidden=true;n.onfocus=()=>tip(h,x,y);n.onclick=()=>{select(h);if(mode==='c'){drawMap();drawFilm();}else location.href=url(h);};layer.append(n);
 }
 select(selected);document.querySelector('.count').textContent=`${filtered().length} 个独立档案 · ${min}—2026`;
}
function drawLanes(){
 const host=document.querySelector('.lanes'),matrix=el('div',null,'lane-matrix');host.replaceChildren(matrix);matrix.append(el('div','分类 / 年份','lane-year lane-corner'));for(let year=2000;year<=2026;year++)matrix.append(el('div',String(year),'lane-year'));
 for(const[key,label]of routes){matrix.append(el('div',label,'lane-title'));for(let year=2000;year<=2026;year++){const cell=el('div',null,'lane-cell');const records=filtered().filter(h=>route(h)===key&&h.coordinates.year===year).sort((a,b)=>name(a).localeCompare(name(b)));for(const h of records){const a=el('a',null,'lane-item');a.href=url(h);a.dataset.id=h.id;a.append(image(h),el('strong',name(h)));a.title=(h.timeline?.label||year)+' · '+h.name;cell.append(a);}if(!records.length)cell.append(el('span',null,'lane-blank'));matrix.append(cell);}}
 host.scrollLeft=(scale===1?21:scale===2?23:24)*154;select(selected);document.querySelector('.count').textContent=`${filtered().length} 个独立档案 · 当前浏览近期年份`;
}
function drawFilm(){const film=document.querySelector('.film');film.replaceChildren();const nearby=filtered().filter(h=>h.coordinates.year===selected.coordinates.year&&route(h)===route(selected)).map(h=>h.id);const preferred=[...new Set([selected.id,...nearby,'leap-hand','wuji-hand-2','sharpa-w01','shadow-hand','allegro-v4','orca-hand'])];const list=preferred.map(id=>hands.find(h=>h.id===id)).filter(h=>h&&filtered().includes(h)).slice(0,Math.max(6,nearby.length));for(const h of list){const b=el('button',null,'film-card');b.dataset.id=h.id;b.append(image(h),el('strong',name(h)),el('p',h.timeline?.label||String(h.coordinates.year)));b.onclick=()=>{select(h);drawMap();};film.append(b);}select(selected);}
function render(){document.querySelector('.scale').textContent=scale.toFixed(1)+'×';document.querySelector('.tooltip').hidden=true;if(mode==='b')drawLanes();else drawMap();if(mode==='c')drawFilm();}
document.querySelector('.plot').hidden=mode==='b';document.querySelector('.lanes').hidden=mode!=='b';document.querySelector('.film').hidden=mode!=='c';
document.querySelector('.zoom-in').onclick=()=>{scale=Math.min(3,scale+1);render();};document.querySelector('.zoom-out').onclick=()=>{scale=Math.max(1,scale-1);render();};document.querySelector('.reset').onclick=()=>{scale=1;query='';filter=null;document.querySelector('input').value='';document.querySelectorAll('[data-route]').forEach(n=>n.classList.remove('active'));render();};
document.querySelector('input').oninput=e=>{query=e.target.value.trim().toLowerCase();render();};document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{filter=filter===b.dataset.route?null:b.dataset.route;document.querySelectorAll('[data-route]').forEach(n=>n.classList.toggle('active',n.dataset.route===filter));document.querySelector('.rail-state').textContent=filter?routes.find(r=>r[0]===filter)[1]:'全部档案';render();});
let previousWidth=document.querySelector('.plot').clientWidth;window.addEventListener('resize',()=>{const width=document.querySelector('.plot').clientWidth;if(width!==previousWidth){previousWidth=width;render();}});render();
})();
