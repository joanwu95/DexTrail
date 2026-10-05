/* Stable display lanes keep every product independent, including identical dates.
   X coordinates are never shifted. Numeric Y anchors remain separate from labels. */
window.DexTrailMapLayout = (() => {
  const MAX_ZOOM = 40;
  function offsets(points, {grouped, rowHeight}) {
    const rows = new Map(), result = new Map();
    for (const point of points) {
      if (!rows.has(point.y)) rows.set(point.y, []);
      rows.get(point.y).push(point);
    }
    for (const members of rows.values()) {
      const lanes = [], assigned = [];
      // 54 base pixels become 162 pixels at 3x, enough for a full-size label.
      // Same-date records always occupy different lanes; IDs keep order stable.
      for (const p of [...members].sort((a,b)=>a.x-b.x || a.id.localeCompare(b.id))) {
        let lane = lanes.findIndex(lastX=>p.x-lastX>=54);
        if (lane<0) lane=lanes.length;
        lanes[lane]=p.x; assigned.push({p,lane});
      }
      const step = grouped ? Math.min(9, rowHeight*.76/Math.max(1,lanes.length-1)) : 9;
      for (const {p,lane} of assigned) result.set(p.id,(lane-(lanes.length-1)/2)*step);
    }
    return result;
  }
  function size(zoom) {
    const detail=Math.max(0,Math.min(1,(zoom-1)/1.5));
    return {width:104+44*detail,height:34+14*detail};
  }
  return {offsets,size,MAX_ZOOM};
})();
