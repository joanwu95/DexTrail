# Hand motion animation diagrams

Created: 2026-10-04.

## Deliverables

- [Animated overview](../../website/docs/images/knowledge/hand-motions/hand-motions-overview.gif)
- [Static overview](../../website/docs/images/knowledge/hand-motions/hand-motions-overview.png)
- [Reproducible renderer](../../scripts/render-hand-motions.py)

All GIFs loop indefinitely. Each cycle lasts 7.68 seconds; frames use 80 ms increments. Repeated held frames may be merged in GIF encoding. Original diagrams use two ink families (navy and teal) on white, with lighter tints and differing line widths. Teal indicates the moving links; thin navy indicates reference structures; pale dashed lines indicate reference poses or paths. English motion names and Chinese explanations are included.

| Diagram | Motion explained | View |
| --- | --- | --- |
| [Abduction / Adduction](../../website/docs/images/knowledge/hand-motions/finger-abduction-adduction.gif) | Fingers spread away from, or return toward, the middle-finger axis | Palmar view |
| [Flexion / Extension](../../website/docs/images/knowledge/hand-motions/finger-flexion-extension.gif) | A finger bends toward the palm, or straightens | Single-finger side view |
| [Opposition / Reposition](../../website/docs/images/knowledge/hand-motions/thumb-opposition-reposition.gif) | Thumb pad approaches and turns toward the index pad, then returns | Palmar projection with an axial-rotation inset |
| [Palmar abduction / Adduction](../../website/docs/images/knowledge/hand-motions/thumb-palmar-abduction-adduction.gif) | Thumb lifts out of the palm plane, then returns | Edge-on palm view |
| [Radial abduction / Adduction](../../website/docs/images/knowledge/hand-motions/thumb-radial-abduction-adduction.gif) | Thumb opens away from the index in the palm plane, then returns | Palmar view |
| [Circumduction](../../website/docs/images/knowledge/hand-motions/finger-circumduction.gif) | Relatively fixed finger base and a fingertip tracing a circular path | Flat projection of a spatial cone; circular path appears elliptical |

## Evidence and diagram interpretation

The motion definitions are based on:

1. [OpenStax, Anatomy and Physiology 2e, Types of Body Movements](https://openstax.org/books/anatomy-and-physiology-2e/pages/9-5-types-of-body-movements): finger abduction/adduction; flexion/extension; opposition/reposition; circumduction. Circumduction combines flexion, abduction, extension and adduction, rather than simply twisting a finger about its own long axis.
2. [In Vivo 3-Dimensional Kinematics of Thumb Carpometacarpal Joint During Thumb Opposition](https://pubmed.ncbi.nlm.nih.gov/28888568/): radial and palmar abduction as distinct thumb positions; opposition includes flexion and internal rotation.
3. [Restoration of opposition](https://pubmed.ncbi.nlm.nih.gov/22117922/): opposition involves abduction, flexion and pronation.

The following are illustration choices, not measured anatomical or product facts:

- Link shapes, example angles, proportions, rates, and axis placement are simplified to communicate motion. They do not specify range of motion, actuation, or degrees of freedom of a particular robotic hand.
- Thumb opposition is shown using a planar approach trajectory and a separate axial-rotation inset. The main drawing alone is not a complete three-dimensional thumb kinematic model.
- The circumduction ellipse is a projection of a fingertip circle; the guide rays show a schematic cone.
- The reference index finger is already bent in the opposition panel so that pad contact is possible.

## Regeneration

Run the renderer with a Python environment containing Pillow. It uses Arial and Microsoft YaHei font files from C:/Windows/Fonts. The renderer constructs all geometry directly and does not edit the earlier generated hand raster.

Contact sheets ending in -review.png are retained for visual review of initial, intermediate, terminal, and return poses.

