# Image prompts for the Excalidraw deck

8 illustrations, one per reserved slot in `presentation.excalidraw`. Generate them, save as PNG with the **exact file name** below into `images/`, then re-run `python3 tools/build_deck.py && node tools/export_frames.mjs` (the builder embeds every image it finds and replaces the dashed placeholder; images are scaled to fit the slot, so the aspect ratio only has to be roughly right).

## Shared style (paste this at the start of EVERY prompt)

> Flat vector cartoon illustration, hand-drawn marker feel: thick dark charcoal outlines (about #1e1e1e), slightly wobbly lines, simple shapes, flat pastel fills with no gradients and no shading, small cute dot eyes, friendly and funny, big readable silhouettes. Palette: sky blue (#339af0 / #d0ebff), violet (#7048e8 / #e5dbff), warm yellow (#fab005 / #fff3bf), mint green (#2f9e44 / #d3f9d8), coral red (#e03131 / #ffe3e3), orange accents. Plain white or transparent background, no scenery, no text, no letters, no logos, no watermark. Original characters only.

## Recurring characters (keep them identical across images)

- **Zap** = the fast "gut-feeling" hero: small, round head, sky-blue cape and mask, yellow lightning-bolt emblem on the chest, confident grin, always in motion.
- **Professor Mull** = the slow "careful thinker": tall and a bit round, big round glasses, grey beard, violet robe and mortarboard, holding a huge coffee mug, sleepy-but-wise look.
- **Bolt-bot** = the sorting robot: boxy sky-blue robot, square head with an antenna with a red ball, two round eyes, smiling mouth line, yellow lightning bolt on its chest.

## The prompts

| File | Slot size (px) | Aspect |
|---|---|---|
| `duo.png` | 620 x 720 (slides 1 and 17) | portrait ~ 4:5 |
| `wizard_essay.png` | 680 x 740 (slide 2) | portrait ~ 9:10 |
| `hero_fast.png` | 640 x 520 (slide 3) | landscape ~ 5:4 |
| `prof_slow.png` | 640 x 520 (slide 3) | landscape ~ 5:4 |
| `sorting_robot.png` | 700 x 680 (slide 10) | square |
| `bouncer.png` | 700 x 680 (slide 11) | square |
| `detective.png` | 700 x 680 (slide 12) | square |
| `relay.png` | 450 x 400 (slide 13) | ~ 9:8 |

### 1. `duo.png`: Zap and Professor Mull together (title + closing)
[Shared style] Two characters standing side by side, full body: on the left Zap (small, sky-blue cape, yellow lightning emblem) mid-jump with a fist pump; on the right Professor Mull (tall, violet robe, big glasses, grey beard) calmly holding a huge coffee mug. They look at each other with friendly smiles; a few small yellow stars and tiny lightning sparks around Zap. Cheerful team-up poster feeling. Portrait composition, plenty of empty margin.

### 2. `wizard_essay.png`: the overkill (hook)
[Shared style] A comically overworked wizard (long violet robe, pointy hat with stars, round glasses, long grey beard) sitting at a small desk, sweating, frantically writing on an enormous paper scroll that unrolls across the floor and piles up behind him in loops; the scroll has only wavy scribble lines, no readable text. Next to the desk, a small speech bubble containing just a big question mark. Funny "way too much effort for a tiny question" mood. Portrait composition.

### 3. `hero_fast.png`: System 1, the fast gut-feeling hero
[Shared style] Zap the hero dashing forward with a motion trail of speed lines and yellow lightning sparks, pointing confidently with one finger at a glowing green check mark on a floating card. Sky-blue background shapes behind him (soft circles only), expression: "I just KNOW!". Landscape composition.

### 4. `prof_slow.png`: System 2, the slow careful thinker
[Shared style] Professor Mull sitting in an armchair next to a chalkboard filled with tangled arrows, boxes and scribbles (no readable text), one hand on his chin, a giant coffee mug steaming, a small sleepy snail on the floor at his feet, a thought cloud with a tiny maze inside. Violet background shapes behind him (soft circles only). Expression: "Hmm, let me think about that…". Landscape composition.

### 5. `sorting_robot.png`: ticket routing
[Shared style] Bolt-bot (boxy sky-blue robot with antenna, yellow lightning bolt on chest) at a conveyor belt, each of its two arms tossing an envelope toward one of three colored bins in front of it: a mint-green bin with a dollar-coin symbol, a sky-blue bin with a wrench symbol, an orange bin with a shopping-bag symbol. A few envelopes flying in the air with motion arcs. Fun, busy but tidy. Square composition.

### 6. `bouncer.png`: moderation
[Shared style] A big, friendly-but-stern bouncer (broad shoulders, sunglasses, black t-shirt, arms crossed, small earpiece) standing at a velvet-rope entrance of a club; one hand holds a clipboard with a green check and a red cross. A tiny grumpy speech-bubble character with an angry zig-zag scribble above its head is being turned away, while a smiling little character with a heart is waved in. No readable text. Square composition.

### 7. `detective.png`: fraud triage
[Shared style] A cute detective (trench coat, flat cap, big magnifying glass) leaning forward to inspect three floating credit-card shapes in a row; two cards have green check marks, the middle one is highlighted with a red flag and a tiny glowing exclamation mark, and the detective's magnifier is aimed right at it with an enlarged eye in the lens. Small yellow sparks of "aha!". No readable numbers or text on the cards. Square composition.

### 8. `relay.png`: fast first, then the big brain
[Shared style] A relay-race handoff: Zap (sky-blue cape, yellow lightning emblem) running in from the left and passing a baton to Professor Mull (violet robe, glasses, coffee mug in the other hand), who takes it with a surprised "oh, my turn" expression. Motion lines behind Zap, a tiny stopwatch icon floating above. Compact composition.

## After generating

1. Save the PNGs as `presentation/images/<file name>.png` (transparent background preferred; white is fine).
2. Tell the agent to continue: it re-runs the build and export, checks the PNGs for overlap and clutter, updates the contact sheet and the PDF, and pushes.
