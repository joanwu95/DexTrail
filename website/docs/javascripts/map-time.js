/* Only curated timeline months determine the time coordinate. An audit date,
   URL or incidental date in prose must never be treated as a release month. */
window.DexTrailMapTime = (() => {
  function point(hand) {
    const year = hand.timeline?.year ?? hand.coordinates?.year;
    if (!Number.isInteger(year)) return null;
    const month = hand.timeline?.month;
    const precise = Number.isInteger(month) && month >= 1 && month <= 12;
    // Month centers share the same scale as the calendar ticks. A year-only
    // record occupies the year's center; that is a display convention, not July.
    return {value: year + (precise ? (month - .5) / 12 : .5), year,
      month: precise ? month : null, precision: precise ? 'month' : 'year',
      upperBound: hand.timeline?.relation === 'by'};
  }
  function ticks(min, max, pixelsPerYear) {
    const step = pixelsPerYear >= 420 ? 1 / 12 : pixelsPerYear >= 150 ? .25 : pixelsPerYear >= 70 ? 1 : 5;
    const divisions = Math.round(1 / step), result = [];
    if (step >= 1) {
      for (let year = Math.ceil(min / step) * step; year <= max; year += step)
        result.push({value:year, label:String(year), major:true});
    } else {
      const perYear = divisions;
      for (let index = Math.ceil(min * perYear); index <= max * perYear; index++) {
        const year = Math.floor(index / perYear), part = index - year * perYear;
        result.push({value:index / perYear, label:part === 0 ? String(year) : String(part * 12 / perYear + 1).padStart(2,'0') + '月', major:part === 0});
      }
    }
    return result;
  }
  return {point, ticks};
})();
