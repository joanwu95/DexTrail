/* Coordinates are sourced separately; missing values never become zero. */
(async () => {
 const root=document.getElementById('hand-coordinate-map'); if(!root)return;
 const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;};
 let data;try{const r=await fetch(new URL(root.dataset.source,document.baseURI));if(!r.ok)throw Error();data=await r.json();}catch{root.append(node('p','地图数据未加载，请使用下方数据库入口。'));return;}
 root.replaceChildren();const toolbar=node('div',null,'coord-toolbar'),select=node('select'),label=node('label','分类方式 ');
 const views={dof:['自由度与驱动','主动自由度 / 受控关节角','执行器数量',[0,40],[0,40]],transmission:['传动方案','传动机制（类别无高低顺序）','主动自由度 / 受控关节角',[0,5],[0,40]],year:['发展时间','首次公开年份（已有记录）','主动自由度 / 受控关节角',[1990,2030],[0,40]]};
 for(const [key,v]of Object.entries(views)){const o=node('option',v[0]);o.value=key;select.append(o);}label.append(select);toolbar.append(label);
 const search=node('input');search.placeholder='查找产品名称';search.setAttribute('aria-label','查找产品名称');toolbar.append(search);
 const zoomOut=node('button','−'),zoomIn=node('button','＋'),reset=node('button','重置视图');zoomOut.setAttribute('aria-label','缩小地图');zoomIn.setAttribute('aria-label','放大地图');toolbar.append(zoomOut,zoomIn,reset);root.append(toolbar,node('p','滚轮缩放 · 拖动平移 · 悬停或聚焦查看名称 · 点击查看技术档案','coord-help'));
 const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 1000 520');svg.setAttribute('aria-label','灵巧手参数坐标地图');svg.classList.add('coord-canvas');root.append(svg);
 const coverage=node('p',null,'coord-coverage');coverage.setAttribute('aria-live','polite');root.insertBefore(coverage,svg);
 const summary=node('div',null,'coord-summary'),pending=node('div',null,'coord-pending');summary.setAttribute('aria-live','polite');const workspace=node('div',null,'coord-workspace');svg.before(workspace);workspace.append(svg,pending);root.append(summary);
 const categories=['直接驱动','腱绳传动','连杆传动','混合传动','气动软体'],ids=['direct-drive','tendon-driven','linkage-driven','hybrid-transmission','pneumatic-soft'];
 let view='dof',scale=1,dx=0,dy=0,drag=null,moved=false;
 const make=(tag,attrs,text)=>{const n=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text)n.textContent=text;return n;};
 const pos=(x,y)=>[82+((x-views[view][3][0])/(views[view][3][1]-views[view][3][0])*850)*scale+dx,445-(y/40*385)*scale+dy];
 const gap=(c,key)=>c.gaps?.[key]||({dof:'主动轴口径尚未核实',actuators:'执行器总数尚未核实',year:'首次公开年份尚未核实',transmission:'传动分类尚未核实'}[key]);
 function describe(h){const c=h.coordinates;summary.replaceChildren(node('strong',h.name),node('p',`自由度记录：${h.facts?.dof?.value ?? c.dof ?? gap(c,'dof')} · 执行器：${h.facts?.actuators?.value ?? c.actuators ?? gap(c,'actuators')}`),node('p',c.scope));for(const id of c.sources){const s=data.sources.find(s=>s.id===id);if(s){const a=node('a',s.title+' ↗');a.href=s.url;summary.append(a);}}const a=node('a','进入技术档案 →');a.href='hands/generated/'+h.id+'/';summary.append(a);}
 function render(){svg.setAttribute('viewBox','0 0 1000 520');svg.setAttribute('aria-label','灵巧手参数坐标地图');pending.hidden=false;svg.replaceChildren();const defs=make('defs',{}),clip=make('clipPath',{id:'coord-clip'});clip.append(make('rect',{x:82,y:25,width:850,height:420}));defs.append(clip);svg.append(defs);
 const plot=make('g',{'clip-path':'url(#coord-clip)'});svg.append(plot);
 const [,,yl,xrange]=views[view];
 const xstep=view==='year'?5:view==='transmission'?1:4;
 for(let x=xrange[0];x<=xrange[1];x+=xstep){const px=pos(x,0)[0];if(px<82||px>932)continue;plot.append(make('line',{x1:px,x2:px,y1:25,y2:445,class:'coord-grid'}));svg.append(make('text',{x:px,y:469,'text-anchor':'middle',class:'coord-tick'},view==='transmission'?categories[x]||'':String(x)));}
 for(let y=0;y<=40;y+=4){const py=pos(0,y)[1];if(py<25||py>445)continue;plot.append(make('line',{x1:82,x2:932,y1:py,y2:py,class:'coord-grid'}));svg.append(make('text',{x:65,y:py+4,'text-anchor':'end',class:'coord-tick'},String(y)));}
 svg.append(make('path',{d:'M82 25 V445 H932',class:'coord-axis'}),make('text',{x:500,y:508,'text-anchor':'middle',class:'coord-label'},views[view][1]),make('text',{x:20,y:235,transform:'rotate(-90 20 235)','text-anchor':'middle',class:'coord-label'},yl));
 pending.replaceChildren(node('strong','暂未定位'),node('p','已知参数保留；计数口径不同或数值待查时，逐项说明原因。','coord-pending-explanation'));let missing=0,shown=0;const placed=[];
 for(const h of data.hands){if(!h.name.toLowerCase().includes(search.value.toLowerCase()))continue;const c=h.coordinates;let x=view==='dof'?c.dof:view==='year'?c.year:ids.indexOf(c.transmission);const y=view==='dof'?c.actuators:c.dof;
 if(!Number.isFinite(x)||x<0||!Number.isFinite(y)){missing++;const b=node('a',null,'coord-pending-card');b.href='hands/generated/'+h.id+'/';if(h.media?.kind==='image'||h.media?.poster){const im=node('img');im.src=h.media.poster||h.media.url;im.alt=h.name;im.loading='lazy';b.append(im);}else b.append(node('span','图片待补','coord-media-missing'));b.append(node('strong',h.name));const reasons=[];if(!Number.isFinite(x)||x<0)reasons.push(gap(c,view==='dof'?'dof':view==='year'?'year':'transmission'));if(!Number.isFinite(y))reasons.push(gap(c,view==='dof'?'actuators':'dof'));b.append(node('small',reasons.join('；')));b.onmouseenter=()=>describe(h);b.onfocus=()=>describe(h);pending.append(b);continue;}shown++;const [ax,ay]=pos(x,y);let px=ax,py=ay;
 // Keep displaced thumbnails inside the plot while their coordinate anchor is visible.
 if(ax>=82&&ax<=932&&ay>=25&&ay<=445){let best=Infinity;for(let i=0;i<180;i++){const angle=i*2.4,r=22*Math.sqrt(i),cx=Math.max(123,Math.min(891,ax+Math.cos(angle)*r)),cy=Math.max(77,Math.min(389,ay+Math.sin(angle)*r));const overlap=placed.reduce((sum,p)=>sum+Math.max(0,94-Math.hypot(p[0]-cx,p[1]-cy)),0);const score=overlap*100+Math.hypot(cx-ax,cy-ay);if(score<best){best=score;px=cx;py=cy;}if(!overlap)break;}}
 placed.push([px,py]);if(Math.hypot(px-ax,py-ay)>1)plot.append(make('line',{x1:ax,y1:ay,x2:px,y2:py,stroke:'#899b9b','stroke-dasharray':'3 3'}));plot.append(make('circle',{cx:ax,cy:ay,r:3,fill:'#426c68'}));const g=make('a',{href:'hands/generated/'+h.id+'/',tabindex:0,'aria-label':h.name});g.append(make('title',{},h.name),make('rect',{x:px-37,y:py-48,width:74,height:78,rx:10,class:'coord-marker'}));
 if(h.media?.kind==='image'||h.media?.poster)g.append(make('image',{href:h.media.poster||h.media.url,x:px-29,y:py-43,width:58,height:66,preserveAspectRatio:'xMidYMid meet'}));else if(h.media?.kind==='video'){const foreign=make('foreignObject',{x:px-32,y:py-43,width:64,height:66});const video=node('video');video.src=h.media.url;video.muted=true;video.preload='metadata';video.playsInline=true;video.style.cssText='width:100%;height:100%;object-fit:contain;pointer-events:none';foreign.append(video);g.append(foreign);}
 if(!h.media)g.append(make('text',{x:px,y:py-4,'text-anchor':'middle',class:'coord-tick'},'图片待补'));g.append(make('text',{x:px,y:py+48,'text-anchor':'middle',class:'coord-product'},h.short.length>18?h.short.slice(0,17)+'…':h.short));g.addEventListener('mouseenter',()=>describe(h));g.addEventListener('focus',()=>describe(h));g.addEventListener('click',e=>{if(moved)e.preventDefault();});plot.append(g);}
 coverage.textContent=`已收录 ${data.hands.length} 款 · 本次匹配 ${shown+missing} 款 · 可按当前参数定位 ${shown} 款 · 暂未定位 ${missing} 款（见旁侧）。`;
 if(!missing)pending.append(node('span','无；本视图全部产品已有坐标。'));if(!shown)plot.append(make('text',{x:500,y:220,'text-anchor':'middle',class:'coord-label'},'没有匹配的已定位产品'));
 }
 function zoom(factor,x=507,y=235){const next=Math.max(.7,Math.min(5,scale*factor)),ratio=next/scale;dx=x-82-(x-82-dx)*ratio;dy=y-445-(y-445-dy)*ratio;scale=next;render();}
 zoomIn.onclick=()=>zoom(1.25);zoomOut.onclick=()=>zoom(.8);reset.onclick=()=>{scale=1;dx=dy=0;render();};select.onchange=()=>{view=select.value;reset.onclick();summary.textContent='选择产品查看参数口径与来源。';};search.oninput=render;
 const point=e=>{const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());};
 svg.addEventListener('wheel',e=>{e.preventDefault();const p=point(e);zoom(e.deltaY<0?1.12:1/1.12,p.x,p.y);},{passive:false});
 svg.addEventListener('pointerdown',e=>{const p=point(e);drag={x:p.x,y:p.y,dx,dy};moved=false;});svg.addEventListener('pointermove',e=>{if(!drag)return;const p=point(e);if(Math.hypot(p.x-drag.x,p.y-drag.y)>5)moved=true;if(moved){dx=drag.dx+p.x-drag.x;dy=drag.dy+p.y-drag.y;render();}});window.addEventListener('pointerup',()=>{drag=null;});svg.addEventListener('pointerleave',()=>{drag=null;});
 summary.textContent='悬停或选择产品，查看坐标数值、版本口径和来源。';render();
})();
