# DexTrail hand figure and motion visual edition

Created: 2026-10-04.

## Deliverables

- [Joint and segment diagram PNG](../../website/docs/images/knowledge/five-finger-hand-anatomy-dextrail.png)
- [Motion overview GIF](../../website/docs/images/knowledge/hand-motions-dextrail/hand-motions-overview.gif)
- [Motion overview PNG](../../website/docs/images/knowledge/hand-motions-dextrail/hand-motions-overview.png)
- [Reproducible motion renderer](../../scripts/render-hand-motions-dextrail.py)

Individual motion GIFs and their static frames are in website/docs/images/knowledge/hand-motions-dextrail, ready to embed in other pages. The standalone preview page was removed at the user's request. The overview is 1840 × 1220 pixels; individual animations are 800 × 680 pixels. Each loop is 7.68 seconds.

## Design direction

Applied the user-requested frontend-design-pro skill from C:/Users/17267/.agents/skills/frontend-design-pro/SKILL.md.

The website's own theme.css and dextrail.css were the source of truth:

| Role | Website token |
| --- | --- |
| Paper | #f4f1ea |
| Ink | #292b29 |
| Accent | #aa4d3e |
| Muted | #696d67 |
| Rules | #d8d8ce |

The animation renderer reads the tokens from website/docs/stylesheets/theme.css. Its GIF palette reserves the exact base colors and uses lighter mixtures for link surfaces and reference geometry. No additional saturated hue is used. The raster diagram was edited with built-in image_gen using the same color specification; as a generated raster its pixel shades are not a deterministic token export.

Typography follows the website's Segoe UI / Microsoft YaHei families, with restrained section identifiers in Consolas. Link geometry was redrawn with tapered rounded contours and pale fills. Small brick pivots, charcoal link contours, grey reference guides and fine directional arrows provide separate roles. Motion-direction labels use an underline in addition to color.

The motion definitions remain anatomical schematics, not robot-specific joint ranges. Four original motion trajectories are reused. Palmar abduction and circumduction now use a complete hand with orthographically projected spatial geometry. The illustrations have flat contours, no lighting, shadows, gradients or depth shading.

- **Palmar abduction/adduction:** the palm and four fingers stay fixed. The thumb's schematic first-metacarpal chain lifts out of the palm plane and returns. A dashed palm-plane outline, resting thumb reference and synchronized side-view inset distinguish out-of-plane movement from radial abduction in the plane. The illustrated 78-degree sweep is an explanatory drawing parameter, not a measured anatomical range. The joints within the simplified thumb chain stay straight; this does not model the full coupled CMC anatomy.
- **Circumduction:** the index MCP location stays fixed, with the interphalangeal joints held straight. A combination of flexion/extension and abduction/adduction makes the fingertip trace a spatial circle, projected as an ellipse. Other fingers and the palm stay fixed. This demonstrates circumduction rather than axial twisting. The conical path and its angular values are idealized schematic parameters.

Definitions: [OpenStax: Types of Body Movements](https://openstax.org/books/anatomy-and-physiology-2e/pages/9-5-types-of-body-movements); thumb-specific distinctions and coupled-motion caveats: [thumb kinematics review](https://pubmed.ncbi.nlm.nih.gov/28888568/) and [thumb CMC movement study](https://pubmed.ncbi.nlm.nih.gov/22117922/). Additional references remain in [the motion evidence note](hand-motion-animations.md) and [the anatomy source note](five-finger-hand-anatomy.md).

The skill's bundled design-system search was run. Its generic marketing, pink accent and playful type suggestions did not fit this existing technical atlas, so the closer website conventions took precedence.

## Validation

- Reviewed the anatomy figure for five digits, all finger segment labels, four MCP/PIP/DIP sets, and thumb CMC/MCP/IP.
- Reviewed motion representative frames for typography, diagram separation, shapes and directional labels.
- Decoded every frame in all seven GIFs and verified every loop totals 7680 ms.
- Reviewed the two spatial animations across the full cycle using six-frame contact sheets. Verified their fixed bases and constant geometric link lengths.
- Verified that both updated GIF assets load and display through the local in-app browser. The browser now shows the image file directly instead of the removed standalone page.
- The supplied runtime does not contain MkDocs; no MkDocs production build was claimed. These are embeddable static assets, with no standalone gallery page or new navigation entry.
- Static PNG counterparts are supplied for pages that offer reduced-motion display.

## Anatomy image edit prompt

Edit the supplied flat hand terminology illustration. Keep all of its correct anatomy and English nomenclature, but redesign the entire illustration to fit the existing DexTrail robotics atlas website.
Palette taken from website CSS, mandatory: background warm paper #f4f1ea, primary ink charcoal #292b29, single accent brick red #aa4d3e. Muted text #696d67; pale rules #d8d8ce; light fills only tints of these three color families. Absolutely no blue, teal, orange, black-blue or bright white background. Pure flat 2D vector-style technical schematic; zero texture, no gradients, no photorealism, no shadows, no glossy effects.
Visual direction: restrained editorial engineering plate, precise modern museum technical drawing. Make it much more beautiful through elegant hand proportions, a balanced composition, clear disciplined type hierarchy, thin articulate structural strokes, small brick-red joint rings, subtle warm-grey link fills and generous spacing. NOT a children's drawing, NOT a generic infographic dashboard. No heavy colored panels. No cartoon plastic armor.
Typography: Segoe UI / humanist sans look, regular and semibold, no huge bold headings. Small monospaced section identifiers. Landscape approximately 3:2. At upper-left small brick-red "DEXTRAIL / ANATOMY 01"; below a moderately sized charcoal title "Finger segments & joints". Small muted subtitle "Five-finger hand · anatomical nomenclature". Fine pale horizontal rule below title. No title dominating the hand.
Large primary hand at left, about 68% of width, right terminology key about 27%, fine vertical rule between; generous margins. Exactly ONE RIGHT hand palmar view, thumb on viewer's left, wrist down. Exactly five digits, anatomically ordered index, middle tallest, ring slightly shorter, little shortest. Palm a soft clean single outline with subtle light grey flat fill, faint structural seams only, NO skin wrinkles. Finger links as elegant tapered rounded slender bands in light warm grey fill with precise charcoal contours, not thick capsules stacked like sausages. Each segment contains its small centered readable English label, and there is ample width.
Every finger named with an unobtrusive thin leader above it: "Thumb", "Index finger", "Middle finger", "Ring finger", "Little finger". All four fingers EACH have exactly three labeled segments bottom to top: "Proximal phalanx", "Middle phalanx", "Distal phalanx". Thin small brick-red ring joints at correct boundaries, with readable small brick-red "MCP", "PIP", "DIP" adjacent to EACH corresponding finger joint, on white/paper clear spaces. Keep 12 segment labels and 12 joint labels distinct, no overlaps.
Thumb exactly two phalangeal links with leaders labeled "Proximal phalanx" and "Distal phalanx", separate grey thumb metacarpal inside palm labeled "Thumb metacarpal". Correct thumb rings "CMC" at metacarpal base near wrist, "MCP" between metacarpal and proximal phalanx, "IP" between proximal and distal phalanx. Never add a middle phalanx, PIP, DIP to thumb. Palm labeled "Palm" and wrist "Wrist" in small muted regular type.
Right glossary without box, header "JOINT NOMENCLATURE" in small spaced charcoal type. Five well-spaced entries, acronym brick-red semibold, term charcoal regular on following line:
"MCP" / "Metacarpophalangeal joint"
"PIP" / "Proximal interphalangeal joint"
"DIP" / "Distal interphalangeal joint"
"IP" / "Interphalangeal joint (thumb)"
"CMC" / "Carpometacarpal joint (thumb)"
Below pale separator and three concise lines:
"Proximal — nearest the palm"
"Distal — nearest the fingertip"
"Thumb — two phalanges"
At bottom tiny muted "Schematic anatomy; robot mechanisms may differ." and "Terminology: ASSH".
Ensure anatomy exact, text clean and no misspellings. The image should feel like a refined, authored engineering atlas figure native to a warm-paper and brick-red documentation website.

