(async()=>{
  'use strict';
  const $=selector=>document.querySelector(selector),mode=document.body.dataset.mode;
  const db=await(await fetch('specimens.json')).json(),all=[...db.hands,...(db.systems||[])];
  const plot=$('.plot'),axes=$('.axes'),anchors=$('.anchors'),layer=$('.specimens'),panel=$('.local-panel');
  const names={dof:'自由度分组',transmission:'传动路线',fingers:'手指构型',actuators:'驱动规模',mobility:'主动轴演进'};
  const helper=window.DexTrailTimeline,NS='http://www.w3.org/2000/svg';
  const make=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
  const svg=(tag,attrs,text)=>{const e=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!=null)e.textContent=text;return e;};
  const name=h=>h.display_name||h.name.replace('Shadow Dexterous Hand（Classic 五指版）','Shadow Hand').replace('LEAP Hand v1（Full）','LEAP Hand v1');
  const source=h=>h.media?.poster||(h.media?.kind==='image'?h.media.url:null);
  const url=h=>new URL(h.detail_url||'hands/generated/'+h.id+'/','http://127.0.0.1:8000/').href;
  function image(h){const src=source(h);if(!src)return make('span',name(h).split(' ')[0].slice(0,3),'glyph');const e=make('img');e.src=src;e.alt='';e.decoding='async';e.onerror=()=>e.replaceWith(make('span',name(h).split(' ')[0].slice(0,3),'glyph'));return e;}
  let view='transmission',query='',routeFilter=null,fingerFilter=null,camera={k:1,x:0,y:0};
  let W=0,H=0,L=105,R=32,T=20,B=48,rows=[],records=[],points=[],elements=new Map(),drag=null,moved=false,frame=0;
  let active=all.find(h=>h.id==='wuji-hand-2'),opened=mode!=='images';
  const preferences=['shadow-hand','leap-hand','wuji-hand-2','sharpa-w01','allegro-v4','dlr-clash','orca-hand','linker-l20','unitree-dex5-s','xynova-flex-2','ruka-v2','pisa-iit-softhand'];
  const key=h=>helper.groupKey(h,view);
  const x=year=>L+(year-2000)/27*(W-L-R);
  const screen=p=>({x:L+(p.x-L)*camera.k+camera.x,y:T+(p.y-T)*camera.k+camera.y});
  function selected(h){active=h;const a=$('.selected-link');a.textContent=name(h)+' · 技术档案 ↗';a.href=url(h);}
  function update(){
    records=all.filter(h=>(!routeFilter||helper.groupKey(h,'transmission')===routeFilter)&&(!fingerFilter||h.classification?.fingers===fingerFilter)&&(!query||(h.name+' '+(h.facts?.company?.value||'')+' '+(h.venue||'')).toLowerCase().includes(query)));
    rows=helper.categories(all,view).filter(([k])=>records.some(h=>key(h)===k));
    $('.count').textContent=`85 款手 · 1 个系统${query||routeFilter||fingerFilter?' · 匹配 '+records.length+' 个档案':''}`;
    $('h2').textContent=names[view];$('.empty').hidden=records.length>0;
    if(!records.includes(active)){active=records[0]||active;opened=false;}
    points=[];const rowH=(H-T-B)/Math.max(1,rows.length),occupied=[];
    const ordered=[...records].sort((a,b)=>{const ai=preferences.indexOf(a.id),bi=preferences.indexOf(b.id);return (ai<0?1000:ai)-(bi<0?1000:bi)||a.coordinates.year-b.coordinates.year||a.id.localeCompare(b.id);});
    for(const h of ordered){
      const r=rows.findIndex(([k])=>k===key(h)),peers=records.filter(p=>key(p)===key(h)&&p.coordinates.year===h.coordinates.year).sort((a,b)=>a.id.localeCompare(b.id));
      const index=peers.findIndex(p=>p.id===h.id),center=T+(r+.5)*rowH;
      const anchor={x:x(h.coordinates.year),y:center+(index-(peers.length-1)/2)*Math.min(3,rowH*.4/Math.max(1,peers.length-1))};
      const candidates=[];
      for(let dx=-88;dx<=88;dx+=22)for(let dy=-36;dy<=36;dy+=18){
        const p={x:anchor.x+dx,y:center+dy};
        if(p.x<L+12||p.x>W-R-12||p.y<T+r*rowH+12||p.y>T+(r+1)*rowH-12)continue;
        const overlap=occupied.filter(o=>Math.abs(o.x-p.x)<21&&Math.abs(o.y-p.y)<23).length;
        candidates.push({...p,cost:overlap*10000+Math.abs(dx)+Math.abs(p.y-anchor.y)*.8});
      }
      candidates.sort((a,b)=>a.cost-b.cost);const packed=candidates[0]||anchor;occupied.push(packed);
      points.push({h,anchor,packed});
    }
    layer.replaceChildren();elements=new Map();
    for(const p of points){
      const e=make('a',null,'specimen');e.dataset.id=p.h.id;e.href=url(p.h);e.setAttribute('aria-label','查看 '+p.h.name+' 详情');e.title=p.h.timeline?.label||String(p.h.coordinates.year);e.append(image(p.h),make('span',name(p.h),'name'));
      e.onmouseenter=()=>selected(p.h);e.onfocus=()=>selected(p.h);
      e.onclick=event=>{
        if(moved){event.preventDefault();return;}
        if(mode!=='images'){event.preventDefault();selected(p.h);opened=true;draw();}
      };
      layer.append(e);elements.set(p.h.id,e);
    }
    selected(active);request();
  }
  function drawAxes(){
    axes.setAttribute('viewBox',`0 0 ${W} ${H}`);axes.replaceChildren();anchors.setAttribute('viewBox',`0 0 ${W} ${H}`);anchors.replaceChildren();
    const rowH=(H-T-B)/Math.max(1,rows.length);
    rows.forEach(([k,label],i)=>{const a=screen({x:L,y:T+i*rowH}),b=screen({x:L,y:T+(i+1)*rowH}),py=screen({x:L,y:T+(i+.5)*rowH}).y;
      if(i%2===0)axes.append(svg('rect',{x:L,y:Math.max(T,a.y),width:W-L-R,height:Math.max(0,Math.min(H-B,b.y)-Math.max(T,a.y)),class:'band'}));
      if(py>=T&&py<=H-B)axes.append(svg('text',{x:L-12,y:py+4,'text-anchor':'end'},label));
    });
    const min=2000-camera.x/camera.k/(W-L-R)*27,max=min+27/camera.k,step=camera.k>=1.7?1:5;
    for(let year=Math.ceil(min/step)*step;year<=max;year+=step){const px=screen({x:x(year),y:T}).x;if(px<L||px>W-R)continue;axes.append(svg('line',{x1:px,x2:px,y1:T,y2:H-B,class:'grid'}),svg('text',{x:px,y:H-24,'text-anchor':'middle'},year));}
    axes.append(svg('path',{d:`M${L} ${T}V${H-B}H${W-R}`,fill:'none',class:'axis'}),svg('text',{x:(L+W-R)/2,y:H-5,'text-anchor':'middle'},'公开年份'));
    anchors.style.clipPath=`inset(${T}px ${R}px ${B}px ${L}px)`;
    for(const p of points){const a=screen(p.anchor);anchors.append(svg('circle',{cx:a.x,cy:a.y,r:1.5,fill:p.h.id===active.id?'#aa4d3e':'#92978d'}));}
  }
  function local(){
    panel.hidden=!opened||!records.length;layer.classList.toggle('is-muted',mode==='expand'&&opened);if(panel.hidden)return;
    const host=$('.local-products');host.replaceChildren();
    panel.style.transform=`scale(${Math.min(1,(W-20)/(mode==='expand'?550:390))})`;panel.style.transformOrigin='top left';
    const target=points.find(p=>p.h.id===active.id);if(!target)return;
    const peers=points.filter(p=>p.h.coordinates.year===active.coordinates.year&&key(p.h)===key(active));
    if(mode==='expand'){
      panel.style.left=(W<600?10:Math.max(L,Math.min(W-558,W*.66-275)))+'px';panel.style.top=Math.max(T,Math.min(H-420,100))+'px';
      $('.local-title').textContent=active.coordinates.year+' 年 · '+peers.length+' 款\n'+rows.find(([k])=>k===key(active))?.[1];
      const inner=peers.length>8?Math.min(6,Math.floor(peers.length*.45)):0;
      peers.forEach((p,i)=>{const innerRing=i<inner,index=innerRing?i:i-inner,count=innerRing?inner:peers.length-inner,angle=-Math.PI/2+index/count*Math.PI*2+(innerRing?.3:0);
        const px=275+Math.cos(angle)*(innerRing?122:220),py=197+Math.sin(angle)*(innerRing?82:140);appendLocal(host,p.h,px,py);
      });
      const a=screen(target.anchor);anchors.append(svg('circle',{cx:a.x,cy:a.y,r:4,fill:'#aa4d3e'}));
    }else{
      panel.style.left=(W<600?10:Math.max(L+20,Math.min(W-408,W*.48)))+'px';panel.style.top='40px';$('.local-title').textContent='局部放大 ×5 · '+rows.find(([k])=>k===key(active))?.[1];
      const factor=5,center={x:target.packed.x-8,y:target.packed.y};
      for(const p of points){const px=195+(p.packed.x-center.x)*factor,py=110+(p.packed.y-center.y)*factor;
        if(px>20&&px<370&&py>20&&py<210)appendLocal(host,p.h,px,py);
      }
      const captions=[];
      for(const e of host.children){const px=parseFloat(e.style.left),py=parseFloat(e.style.top)+22;
        const collision=captions.some(c=>Math.abs(c.x-px)<66&&Math.abs(c.y-py)<43);
        e.querySelector('.local-name').hidden=collision;if(!collision)captions.push({x:px,y:py});
      }
      const marks=svg('svg',{width:'100%',height:253,style:'position:absolute;inset:0;pointer-events:none'});
      for(const year of [active.coordinates.year-1,active.coordinates.year,active.coordinates.year+1]){const px=195+(x(year)-center.x)*factor;if(px<5||px>385)continue;marks.append(svg('line',{x1:px,x2:px,y1:226,y2:232,stroke:'#a6aa9f'}),svg('text',{x:px,y:248,'text-anchor':'middle',fill:'#696d67','font-size':10},year));}
      host.append(marks);
      const a=screen({x:center.x-39,y:center.y-22}),b=screen({x:center.x+39,y:center.y+22});
      anchors.append(svg('rect',{x:a.x,y:a.y,width:b.x-a.x,height:b.y-a.y,fill:'#aa4d3e08',stroke:'#aa4d3e','stroke-width':.8}));
    }
  }
  function appendLocal(host,h,x,y){const a=make('a',null,'local-product');a.href=url(h);a.dataset.id=h.id;a.title=h.name;a.style.left=x+'px';a.style.top=y+'px';a.setAttribute('aria-label','打开 '+h.name+' 技术档案');a.append(image(h),make('span',name(h),'local-name'));a.onmouseenter=()=>selected(h);host.append(a);}
  function draw(){
    frame=0;
    if(camera.k>=1){camera.x=Math.max(-(W-L-R)*(camera.k-1),Math.min(0,camera.x));camera.y=Math.max(-(H-T-B)*(camera.k-1),Math.min(0,camera.y));}
    drawAxes();const used=[],size=Math.min(43,20*Math.sqrt(camera.k));
    layer.style.clipPath=`inset(${T}px ${R}px ${B}px ${L}px)`;
    for(const p of points){const e=elements.get(p.h.id),pos=screen(mode==='expand'?p.anchor:p.packed),label=e.querySelector('.name');
      e.style.left=pos.x+'px';e.style.top=pos.y+'px';e.style.setProperty('--size',size+'px');e.style.width=size+'px';e.style.height=size+'px';
      const rect={x:pos.x-45,y:pos.y+size/2+4,w:90,h:28};
      const room=!used.some(o=>rect.x<o.x+o.w&&rect.x+rect.w>o.x&&rect.y<o.y+o.h&&rect.y+rect.h>o.y);
      const should=mode==='images'&&(camera.k>=1.6||preferences.includes(p.h.id))&&room&&pos.x>=L+46&&pos.x<=W-R-46&&rect.y+rect.h<H-B;
      label.hidden=!should;if(should)used.push(rect);
    }
    $('.scale').textContent=camera.k.toFixed(2)+'×';local();
  }
  function request(){if(!frame)frame=requestAnimationFrame(draw);}
  function zoom(factor,cx=W/2,cy=H/2){const next=Math.max(.65,Math.min(12,camera.k*factor)),ratio=next/camera.k;camera.x=cx-L-(cx-L-camera.x)*ratio;camera.y=cy-T-(cy-T-camera.y)*ratio;camera.k=next;request();}
  function reset(){camera={k:1,x:0,y:0};opened=mode!=='images';active=records.find(h=>h.id==='wuji-hand-2')||records[0]||active;selected(active);request();}
  $('.zoom-in').onclick=()=>{const target=points.find(p=>p.h.id===active.id);if(!target){zoom(1.35);return;}const focus=screen(mode==='expand'?target.anchor:target.packed);zoom(1.35,focus.x,focus.y);camera.x+=(W+L-R)/2-focus.x;camera.y+=(H+T-B)/2-focus.y;request();};$('.zoom-out').onclick=()=>zoom(1/1.35);$('.reset').onclick=reset;
  $('.close-local').onclick=()=>{opened=false;request();};
  $('input').oninput=e=>{query=e.target.value.trim().toLowerCase();opened=false;update();reset();};
  document.querySelectorAll('[data-view]').forEach(e=>e.onclick=()=>{view=e.dataset.view;document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b===e));update();reset();});
  document.querySelectorAll('[data-route]').forEach(e=>e.onclick=()=>{routeFilter=routeFilter===e.dataset.route?null:e.dataset.route;document.querySelectorAll('[data-route]').forEach(b=>b.classList.toggle('active',b.dataset.route===routeFilter));update();reset();});
  document.querySelectorAll('[data-fingers]').forEach(e=>e.onclick=()=>{const n=Number(e.dataset.fingers);fingerFilter=fingerFilter===n?null:n;document.querySelectorAll('[data-fingers]').forEach(b=>b.classList.toggle('active',Number(b.dataset.fingers)===fingerFilter));update();reset();});
  plot.addEventListener('wheel',e=>{if(e.target.closest('.local-panel'))return;e.preventDefault();const r=plot.getBoundingClientRect();zoom(Math.exp(-Math.max(-120,Math.min(120,e.deltaY))*.0025),e.clientX-r.left,e.clientY-r.top);},{passive:false});
  plot.onpointerdown=e=>{moved=false;if(e.target.closest('a,button,.local-panel')||e.button>0)return;drag={id:e.pointerId,x:e.clientX,y:e.clientY};plot.setPointerCapture(e.pointerId);};
  plot.onpointermove=e=>{if(!drag||drag.id!==e.pointerId)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;moved=moved||Math.hypot(dx,dy)>3;camera.x+=dx;camera.y+=dy;drag.x=e.clientX;drag.y=e.clientY;request();};
  plot.onpointerup=()=>{drag=null;};plot.onpointercancel=()=>{drag=null;};
  plot.onkeydown=e=>{if(e.target!==plot)return;const keys=['+','=','-','Home','Escape','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'];if(!keys.includes(e.key))return;e.preventDefault();if(e.key==='Home')reset();else if(e.key==='Escape'){opened=false;request();}else if(e.key==='+'||e.key==='=')zoom(1.35);else if(e.key==='-')zoom(1/1.35);else{camera.x+=e.key==='ArrowLeft'?50:e.key==='ArrowRight'?-50:0;camera.y+=e.key==='ArrowUp'?50:e.key==='ArrowDown'?-50:0;request();}};
  let width=0;new ResizeObserver(()=>{if(!plot.clientWidth||plot.clientWidth===width)return;width=plot.clientWidth;W=width;H=plot.clientHeight;L=W<600?82:105;update();reset();}).observe(plot);
})();
