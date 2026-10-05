# Five-finger hand anatomy figure

- Created: 2026-10-04
- Asset: ../../website/docs/images/knowledge/five-finger-hand-anatomy.png
- Method: built-in image_gen tool
- Scope: generic robotic hand illustrating human anatomical terminology, not a specific product or its actual joint layout.
- Visual review: five digits; all four fingers have three correctly named phalangeal segments and MCP/PIP/DIP labels; thumb has two phalangeal segments, a metacarpal link, and CMC/MCP/IP labels.

## Terminology sources

- American Society for Surgery of the Hand, [Finger Joints](https://assh.my.site.com/handcare/blog/anatomy-101-finger-joints): MCP, PIP and DIP.
- American Society for Surgery of the Hand, [Upper Extremity Joints](https://assh.my.site.com/handcare/safety/joints): thumb CMC, MCP and IP.
- [Collagen organisation in the fibrous joint capsules in the digits of the human hand](https://pmc.ncbi.nlm.nih.gov/articles/PMC13140493/): proximal, middle and distal phalanges, and their joint relationships.

Phalanx is singular; phalanges is plural. In robotic diagrams these anatomical names are used as a mapping to finger links and joints; individual robot mechanisms may differ.

## Generation prompt

Use case: scientific-educational.
Create a precise, polished English-only technical reference infographic for a robotics atlas. Landscape composition, generous white background, dark navy clean sans-serif text. Title "Dexterous Hand — Finger Segments & Joints". Subtitle "Human anatomical terminology applied to a generic robotic hand".
Main illustration: exactly ONE generic biomimetic FIVE-digit robotic RIGHT HAND, PALMAR front view, wrist at bottom, all digits extended and gently splayed, thumb on viewer's LEFT, mechanically believable but diagrammatic. Four long fingers in correct order from left to right: index, middle (longest), ring, little (shortest). Thumb extends diagonally toward upper left. Precisely THREE phalangeal link segments on each of the four fingers, and precisely TWO phalangeal link segments on thumb. Grey metal palm, subtle mechanical fasteners, muted teal finger link bodies, small warm orange joint pivots. Do not make an organic flesh hand or a bone skeleton. Keep hand large, occupying roughly left two thirds, wide finger links and enough spaces to fit labels without collision.
Label every digit clearly with leader lines from names above the respective fingertip: "Thumb", "Index finger", "Middle finger", "Ring finger", "Little finger". For EACH of index, middle, ring, little, print these labels INSIDE the respective link surfaces: distal/top "Distal phalanx", middle "Middle phalanx", proximal/bottom "Proximal phalanx", using two-line words and clear legible type. Label joints with small orange badges directly adjacent to EACH respective pivot: "DIP" at distal-middle boundary, "PIP" at middle-proximal boundary, "MCP" at proximal-palm boundary. Thus each of these four fingers has exactly DIP, PIP, MCP correctly located, and all 12 segments named. Joint badges must not sit inside a segment.
Thumb: leader labels "Distal phalanx" to its tip link and "Proximal phalanx" to its next link; orange "IP" at boundary between those two phalanges, orange "MCP" where proximal phalanx meets the thumb metacarpal, orange "CMC" where thumb metacarpal meets carpal/base region near wrist. Draw thumb metacarpal as a separate visible grey link running from MCP to CMC in the palm. Label it "Thumb metacarpal". NO middle phalanx, PIP, or DIP on thumb. Label palm "Palm" and wrist "Wrist".
Right-hand margin has an orderly readable terminology key with these exact entries, sufficiently wide for long words:
"JOINT NAMES"
"MCP — Metacarpophalangeal joint"
"PIP — Proximal interphalangeal joint"
"DIP — Distal interphalangeal joint"
"IP — Interphalangeal joint (thumb)"
"CMC — Carpometacarpal joint (thumb)"
"SEGMENT NAMES"
"Proximal phalanx — nearest the palm"
"Middle phalanx — middle segment"
"Distal phalanx — nearest the fingertip"
"Thumb: proximal + distal phalanges"
Small bottom caption "Schematic anatomy mapping; robot joint layouts may vary."
Small source footer "Terminology: American Society for Surgery of the Hand (ASSH)".
Prioritize anatomical mapping accuracy, readable English, separated leader lines, clean technical documentation style, no decorative clutter, no brand-specific product claims, no extra hand or fingers, no arrows suggesting motion.

