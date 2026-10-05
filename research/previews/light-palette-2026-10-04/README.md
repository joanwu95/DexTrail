# DexTrail light-palette design studies

These are isolated previews. Production documentation, datasets, styles and JavaScript were not edited.

## Open

The production MkDocs server must run on http://127.0.0.1:8000/ because the prototypes reuse its styles, source-backed content and assets. A separate Python HTTP server serves this directory on http://127.0.0.1:8768/.

Open http://127.0.0.1:8768/index.html to compare all variants.

## Variants

- A: pale mint (#edf6f0), dark text, muted red (#bc3540). Product title is beside the image.
- B: pale Tiffany blue (#e7f5f5), dark text, red (#c83d49). A short product title row precedes the image and inspector.
- C: stronger seafoam (#cee7e2), dark text, red (#bc263c). Uses A's compact overview layout.

Colors and layouts can be selected independently.

## Prototype changes

- Product images have no circular frames or glow. Text has no glow.
- Labels appear on hover or keyboard focus, reducing clutter.
- Preserve existing coordinate categories, dates, zoom, pan, aggregation and detail links.
- Keep image tiles within the plot and clip the product layer at the axes; displaced tiles retain leaders to their true coordinate anchors.
- Preserve chapter labels at the left, fixed navigation and individual rainbow tags at the right.
- Compact gallery, metadata, technical dimension buttons and preview panel.
- Deep text colors are used on light backgrounds; white is reserved for media and chart surfaces.

## Checks

- Existing map contains 85 hands and one related system; the prototype reads the same 86 entries.
- Initial view: 21 aggregate/singleton nodes, all 21 images loaded, no product image exceeded the plot bounds.
- Transmission view and zoom controls: no product image exceeded the plot bounds in the inspected state.
- Shadow Hand uses the real source-backed picture and content. No speculative hardware facts were added.

This is a design review prototype, not a production-ready clipping patch. Final implementation should test boundary labels, group buttons, pointer interaction, all view modes and responsive layouts.
