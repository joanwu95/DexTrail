/* Each record belongs to one year column and one category row. */
window.DexTrailTimeline = (() => {
  const routes = [
    ['tendon-driven', '腱绳传动'], ['linkage-driven', '连杆传动'],
    ['hybrid-transmission', '混合传动'], ['geared-drive', '齿轮传动'],
    ['direct-drive', '直接驱动'], ['unknown', '传动待核实'],
  ];
  function value(hand, field) {
    return field === 'fingers' ? hand.classification?.fingers : hand.coordinates?.[field];
  }
  function groupKey(hand, view) {
    if (view === 'transmission') {
      const key = hand.classification?.transmission;
      return routes.some(row => row[0] === key) ? key : 'unknown';
    }
    const number = value(hand, view === 'actuators' ? 'actuators' : view === 'fingers' ? 'fingers' : 'dof');
    if (!Number.isFinite(number) || number < 0) return 'unknown';
    return String(view === 'dof' ? Math.ceil(number / 5) : number);
  }
  function categories(hands, view) {
    if (view === 'transmission') return routes;
    const keys = [...new Set(hands.map(hand => groupKey(hand, view)))].filter(key => key !== 'unknown');
    const rows = keys.sort((a, b) => Number(a) - Number(b)).map(key => {
      const number = Number(key);
      const label = view === 'fingers' ? `${key} 指` : view === 'actuators' ? `${key} 执行器` :
        view === 'mobility' ? `${key} 主动轴` : number === 0 ? '0 主动轴' : `${(number - 1) * 5 + 1}–${number * 5} 轴`;
      return [key, label];
    });
    const unknown = view === 'fingers' ? '手指数待核实' : view === 'actuators' ? '执行器待核实' : '主动轴待核实';
    return rows.concat([['unknown', unknown]]);
  }
  function build(allHands, filteredHands, view) {
    const dates = allHands.map(hand => hand.coordinates?.year).filter(Number.isInteger);
    const first = dates.length ? Math.min(...dates) : new Date().getFullYear();
    const last = dates.length ? Math.max(...dates) : first;
    const years = Array.from({length:last - first + 1}, (_, index) => first + index);
    const cells = new Map(), missing = [];
    for (const hand of filteredHands) {
      const year = hand.coordinates?.year;
      if (!Number.isInteger(year)) { missing.push(hand); continue; }
      const key = `${groupKey(hand, view)}|${year}`;
      if (!cells.has(key)) cells.set(key, []);
      cells.get(key).push(hand);
    }
    for (const cell of cells.values()) cell.sort((a, b) => a.name.localeCompare(b.name) || a.id.localeCompare(b.id));
    const rows = categories(allHands, view).filter(([key]) => years.some(year => cells.has(`${key}|${year}`)));
    return {years, rows, cells, missing};
  }
  return {groupKey, categories, build};
})();
