# DexTrail: second design study

Independent review prototypes. No production website code or data was changed.

Open http://127.0.0.1:8769/index.html while the preview server runs.

## Concepts

- M1: product specimen thumbnails with short names; leaders connect displaced thumbnails back to their coordinate anchors.
- M2: small diamond markers and a separate product preview dock. Hover or focus updates the product preview.
- M3: compact thumbnails and names organized by technical category rows.
- D1: three source-backed product/model pictures before identity and metrics; a vertical technical navigator below the media.
- D2: a narrow sticky product profile beside a larger technical reading workspace.

Four independent palettes: warm paper and brick red; graphite and grey green; cold white and cobalt; dark plum and grey violet. Every prototype has a palette selector.

## Data and boundaries

The map copies the current generated site dataset: 85 hand records and one related robot system. The preview groups nearby records; counts represent additional group members. No synthetic hand records were created. Product images and captions are copied from current source-backed records. Detail explanations come from the current Shadow Hand page, including their source links and version caveats.

This is a concept study. Three classification selectors, search, transmission filters, horizontal time zoom, product links, detail dimensions and gallery controls are implemented. Full group member selection, inertial panning, the other production filters, and production navigation/scroll highlighting are outside this preview's scope. Static tags on the map are explicitly labelled as layout examples.

## Checks

- M1: all 86 records represented by 21 coordinate groups; no overlapping thumbnails or plot-boundary overflow in the reviewed state.
- M1 at 1.35×: no plot-boundary overflow.
- M3: 16 groups, all 16 representative images loaded, no plot-boundary overflow in the reviewed state.
- Detail dimension selection changed to sensing and displayed the four existing sensing tables.

The prototypes are built with native HTML/CSS/JavaScript for actual screenshot review; PNGs are browser captures, not invented interface images.
