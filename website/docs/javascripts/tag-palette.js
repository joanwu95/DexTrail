/* All tags share the site's accent; preserve the paint API for dynamic filters. */
window.DexTrailTags = (() => {
  function paint(element) {
    element.style.setProperty('--tag-color', 'var(--dex-accent)');
  }
  document.querySelectorAll('.dex-tag[data-tag]').forEach(tag => paint(tag, tag.dataset.tag));
  return {paint};
})();
