/* A single category navigator enhances the complete, server-rendered record below. */
// Compact only citation-only columns. Preserve every source node and URL inside
// a native disclosure; mixed resource/status columns remain fully visible.
function compactHandSources(container) {
  for (const table of container.querySelectorAll('table')) {
    const headers = [...table.querySelectorAll('thead th')];
    headers.forEach((header, index) => {
      if (!/^(依据|出处|来源)$/.test(header.textContent.trim())) return;
      for (const row of table.querySelectorAll('tbody tr')) {
        const cell = row.cells[index];
        if (!cell || cell.querySelector('.hand-source-details')) continue;
        const links = [...cell.querySelectorAll('a')];
        if (!links.length) continue;
        cell.classList.add('hand-source-cell');
        const title = links[0].textContent.trim();
        // A short single reference needs no extra interaction.
        if (links.length === 1 && cell.textContent.trim().length <= 30) continue;
        const disclosure = document.createElement('details');
        disclosure.className = 'hand-source-details';
        const summary = document.createElement('summary');
        summary.textContent = (title.length > 24 ? title.slice(0,24) + '…' : title) + (links.length > 1 ? ` 等 ${links.length} 条` : '');
        summary.setAttribute('aria-label', `展开完整来源：${title}${links.length > 1 ? `，共 ${links.length} 条` : ''}`);
        const body = document.createElement('div');
        body.append(...cell.childNodes);
        disclosure.append(summary, body);
        cell.append(disclosure);
      }
    });
  }
}
for (const page of document.querySelectorAll('.dex-hand-page')) compactHandSources(page);
for (const root of document.querySelectorAll('[data-hand-explorer]')) {
  const data=JSON.parse(root.dataset.handExplorer);
  const menu=root.querySelector('.hand-dimensions'),panel=root.querySelector('.hand-dimension-detail');
  const make=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n;};
  let selected=null, fixed=false;
  const snapshots=new Map();
  const label=root.querySelector('.hand-browser-label');
  const hint=label?.querySelector('span');
  if(hint){hint.textContent='悬停预览 · 点击固定';hint.setAttribute('aria-live','polite');}
  const release=make('button','恢复悬停浏览');release.type='button';release.className='hand-preview-release';release.hidden=true;
  release.setAttribute('aria-label','取消固定技术维度，恢复悬停预览');
  label?.append(release);
  release.addEventListener('click',()=>{fixed=false;release.hidden=true;if(hint)hint.textContent='悬停预览 · 点击固定';menu.querySelector('[aria-pressed="true"]')?.focus();});
  function show(entry,button){
    // Re-entering the active dimension must not discard reading position or
    // expanded citations. Other dimensions retain their own state as well.
    if(selected===entry.id)return;
    if(selected)snapshots.set(selected,{nodes:[...panel.childNodes],scrollTop:panel.scrollTop});
    selected=entry.id;
    menu.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    panel.setAttribute('aria-label',entry.title+' · 详细说明');
    const cached=snapshots.get(entry.id);
    if(cached){panel.replaceChildren(...cached.nodes);panel.scrollTop=cached.scrollTop;return;}
    const heading=make('h3',entry.title);heading.className='hand-panel-title';
    const anchor=make('a','阅读全文 ↓');anchor.href=entry.id==='overview'?'#complete-metrics':'#record-'+entry.id;
    heading.append(anchor);
    const content=make('div','');content.className='hand-note-content';content.innerHTML=entry.content_html;
    // Keep the inspector heading hierarchy distinct from subsection headings.
    for(const old of content.querySelectorAll('h3')){const h=make('h4',old.textContent);old.replaceWith(h);}
    compactHandSources(content);
    panel.replaceChildren(heading,content);panel.scrollTop=0;
    panel.setAttribute('aria-label',entry.title+' · 详细说明');
  }
  for(const entry of data.entries){
    const button=make('button',entry.title);button.type='button';button.dataset.dimension=entry.id;
    button.addEventListener('mouseenter',()=>{if(!fixed)show(entry,button);});
    button.addEventListener('focus',()=>{if(!fixed)show(entry,button);});
    button.addEventListener('click',()=>{
      show(entry,button);fixed=true;release.hidden=false;
      if(hint)hint.textContent='已固定：'+entry.title;
    });menu.append(button);
  }
  // Begin with the mechanism; basic fields already have a dedicated section.
  const initial=data.entries.find(e=>e.id==='mechanics'&&e.available)||data.entries[0];
  show(initial,menu.querySelector(`[data-dimension="${initial.id}"]`));
  for (const gallery of root.querySelectorAll('[data-hand-gallery]')) {
    const slides=[...gallery.querySelectorAll('[data-slide]')];
    for (const button of gallery.querySelectorAll('[data-gallery-index]')) {
      button.addEventListener('click',()=>{
        const index=Number(button.dataset.galleryIndex);
        slides.forEach((slide,i)=>{
          slide.hidden=i!==index;
          if(i!==index)slide.querySelectorAll('video').forEach(video=>video.pause());
        });
        gallery.querySelectorAll('[data-gallery-index]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
      });
    }
  }
  for(const media of root.querySelectorAll('img,video')){
    const unavailable=()=>{
      if(media.classList.contains('hand-gallery-thumbnail')){media.hidden=true;return;}
      const p=make('p','远程媒体暂不可用，请通过画面来源查看原图或演示。');
      p.className='hand-media-unavailable';p.setAttribute('role','status');media.replaceWith(p);
    };
    media.addEventListener('error',unavailable);if(media.tagName==='IMG'&&media.complete&&!media.naturalWidth)unavailable();
  }
}
