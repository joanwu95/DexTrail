/* Pack independent labels into stable world-space lanes. This does not change
   time coordinates or aggregate products. Zoom scales their separation. */
window.DexTrailNameLayout = (() => {
  function pack(points, keys, {left, right}) {
    const positions=new Map(), bands=[];
    let height=0;
    for(const key of keys) {
      const row=points.filter(p=>p.key===key).map(p=>{
        const side=p.x+p.width>right?'left':'right';
        const start=side==='left'?p.x-p.width:p.x;
        return {...p,side,start};
      }).sort((a,b)=>a.start-b.start || a.id.localeCompare(b.id));
      if(!row.length)continue;
      const ends=[], assigned=[];
      for(const p of row) {
        let lane=ends.findIndex(end=>p.start>=end+8);
        if(lane<0)lane=ends.length;
        ends[lane]=p.start+p.width;assigned.push({...p,lane});
      }
      const bandHeight=Math.max(52,ends.length*19+24);
      const center=height+bandHeight/2;
      bands.push({key,center,height:bandHeight});
      for(const p of assigned)positions.set(p.id,{side:p.side,
        offset:(p.lane-(ends.length-1)/2)*19,center});
      height+=bandHeight;
    }
    return {positions,bands,height};
  }
  function numeric(points) {
    const edges=points.flatMap(p=>[{x:p.start,delta:1},{x:p.start+p.width+8,delta:-1}]).sort((a,b)=>a.x-b.x || b.delta-a.delta);
    let depth=0,maxDepth=0;
    for(const edge of edges){depth+=edge.delta;maxDepth=Math.max(maxDepth,depth);}
    const height=Math.max(300,maxDepth*22+48), positions=new Map(), occupied=[];
    for(const p of [...points].sort((a,b)=>a.value-b.value || a.id.localeCompare(b.id))) {
      const anchor=24+p.value/p.max*(height-48);
      let center=anchor;
      for(let step=0;step<=Math.ceil(height/19);step++) {
        const choices=step?[anchor+step*19,anchor-step*19]:[anchor];
        const free=choices.find(y=>y>=12 && y<=height-12 && !occupied.some(o=>
          p.start<o.end+8 && p.start+p.width+8>o.start && Math.abs(y-o.y)<18));
        if(free!==undefined){center=free;break;}
      }
      occupied.push({start:p.start,end:p.start+p.width,y:center});
      positions.set(p.id,{center,anchor});
    }
    return {positions,height};
  }
  function camera(state,width,height) {
    const k=Math.max(1,Math.min(40,state.k));
    return {k,x:Math.max((1-k)*Math.max(1,width),Math.min(0,state.x)),
      y:Math.max(0,Math.min((k-1)*Math.max(1,height),state.y))};
  }
  return {pack,numeric,camera,MAX_ZOOM:40};
})();
