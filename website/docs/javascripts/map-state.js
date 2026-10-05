/* Validate saved exploration against the current collection, not stale product IDs. */
window.DexTrailMapState = (() => {
  function clean(value, allowed) {
    if (!value || typeof value !== 'object' || !allowed.views.includes(value.view) ||
        typeof value.query !== 'string' || ![value.k, value.x, value.y].every(Number.isFinite) ||
        value.k < .65 || value.k > 40) return null;
    const ids = (list, available) => Array.isArray(list) ? [...new Set(list.filter(id => typeof id === 'string' && available.has(id)))] : [];
    const offset = number => Math.max(-100, Math.min(100, number));
    const scroll = number => Number.isFinite(number) ? Math.max(0, number) : 0;
    return {view:value.view, query:value.query, tags:ids(value.tags, allowed.tags),
            k:value.k, x:offset(value.x), y:offset(value.y), expanded:ids(value.expanded, allowed.hands),
            pending:value.pending === true, scrollY:scroll(value.scrollY), listScroll:scroll(value.listScroll)};
  }
  function read(key, allowed) {
    try {return clean(JSON.parse(sessionStorage.getItem(key)), allowed);} catch {return null;}
  }
  function save(key, value, allowed) {
    const state = clean(value, allowed);
    if (state) try {sessionStorage.setItem(key, JSON.stringify(state));} catch {}
    return state;
  }
  return {clean, read, save};
})();
