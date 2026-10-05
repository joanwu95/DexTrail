# DexTrail homepage

Brand: **DexTrail**  
Tagline: **Tracing the paths to robotic dexterity.**

## Interface

The homepage is a full-width coordinate explorer without the MkDocs global header,
sidebar, or footer. Other documentation pages retain their existing navigation.
Deep-space background `#0D0E11`, restrained gold instruments, monospaced labels,
colored halos, and thin relationship lines provide the cartographic visual style.

### Typography revision

Reading text now uses Segoe UI / Noto Sans SC / Microsoft YaHei; only numeric
axes, zoom values, timestamps and small instrument labels retain monospace.
Desktop hierarchy: brand 44px/600, tagline 16px/400, map heading 22px/600,
controls 14–15px, product names and legend 13px, numeric ticks 12px.
Explanatory panels use 14px text and generous line height. Secondary text uses
brighter blue-gray for contrast on the dark background. Narrow screens wrap
transmission axis labels into two lines instead of shrinking them.

The original fingerprint emblem remains on the homepage. An alternate simplified
five-finger hand with joint marks and palm paths is stored as
`website/docs/images/brand/dextrail-hand-concept.svg`. Both marks can be reviewed at
`/visual-lab/dextrail-icon-study.html`; the candidate is not applied to the site.

- Wheel / pinch to zoom, drag to pan, click a cluster to unfold its products.
- Hover or focus a product for its summary; click its image to open the full record.
- Three coordinate views: active DoF vs actuators, transmission vs active DoF,
  and public release year vs active DoF.
- Search filters products; the unpositioned drawer retains access to records
  that lack either coordinate in the selected view.
- Keyboard: focus the map, use arrows to pan, +/- to zoom, Home to reset.
  Slash focuses search. Reduced-motion preference disables inertia.

## Data meaning

The map reads `website/docs/visual-lab/specimens.json`; it does not duplicate
technical parameters in the renderer. At implementation there are 34 records,
19 positionable in the default view and 15 without both required coordinates.
Other views have different evidence coverage.

Spatial clusters summarize nearby products at their mean coordinate. Their area
scales with product count, capped for readability; they are not quality scores.
Colored ring segments show the transmission categories present in a cluster.
Expanded colliding products have dotted leaders back to their true coordinates.
Thin lines indicate shared transmission categories, not technological ancestry.
Unverified transmission remains gray. Background stars are decorative.

## Rendering and maintenance

`website/docs/javascripts/dextrail-map.js` controls the explorer.
`website/docs/stylesheets/dextrail.css` scopes the visual theme to this homepage.
PixiJS 8.22.0 (locally vendored with MIT license) renders the starfield and reused,
pre-baked radial glow texture using WebGL. SVG axes and accessible HTML product
links stay synchronized with the camera. A Canvas fallback handles unavailable
WebGL. Product images remain remote URLs.

At the current data size, aggregation runs in the browser on zoom; there is no
aggregation server. No fabricated product nodes or simulated activity are added.
The log records real loading and explorer actions. A server returning zoom-level
aggregates can be introduced if the dataset grows enough to require it.

Validation: strict MkDocs build, JavaScript syntax check, 10 existing Python tests;
browser checks for WebGL, classification, search, clusters, details navigation,
keyboard controls and 390px responsive layout.
