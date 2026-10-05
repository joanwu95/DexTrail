/* The tag ID fixes its colour across pages; neighbouring tags span the spectrum. */
window.DexTrailTags = (() => {
  // Append new IDs to preserve existing colours across both page types.
  const order = ["transmission:tendon-driven", "fingers:5", "actuation:electric-actuation", "configuration:underactuated", "sensing:position-sensing", "sensing:force-sensing", "sensing:tactile-sensing", "control:pid", "control:force-control", "simulation:gazebo", "control:reinforcement-learning", "software:interface-docs", "software:urdf", "software:mjcf", "transmission:unknown", "fingers:4", "control:teleoperation", "simulation:isaac-gym", "transmission:linkage-driven", "fingers:3", "actuation:pneumatic", "software:cad", "transmission:hybrid-transmission", "fingers:unknown", "actuation:hydraulic", "transmission:geared-drive", "actuation:pneumatic-electric"];
  order.push('sensing:current-sensing');
  function paint(element, id) {
    let hash = 2166136261;
    for (const char of id) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0;
    const index = order.indexOf(id);
    const hue = index >= 0 ? (index * 137.50776405 + 12) % 360 : (hash * 137.50776405) % 360;
    element.style.setProperty('--tag-color', `hsl(${hue.toFixed(3)} 72% 76%)`);
  }
  document.querySelectorAll('.dex-tag[data-tag]').forEach(tag => paint(tag, tag.dataset.tag));
  return {paint};
})();
