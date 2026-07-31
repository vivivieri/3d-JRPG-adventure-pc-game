---
id: shots-briefs
type: how-to
phase: [1, 6]
audience: [visual, narrative, pm]
status: active
authority: vision
tokens_est: 1134
summary: "Priority shot list + per-scene briefs"
---
# Storyboard Illustrations — Priority shot list + per-scene briefs

**Hub:** [`STORYBOARD_ILLUSTRATIONS.md`](../STORYBOARD_ILLUSTRATIONS.md)

## 4. Priority shot list (generate in this order)

### Tier P0 — Minimum viable pitch (5 images)

| ID | Scene | Shot | File |
|----|-------|------|------|
| P0-1 | — | Party lineup (Urashima, Yuzu, Roku) | `characters/party_lineup.png` |
| P0-2 | SC-02 | Ruined village hub + cracked torii | `scenes/SC-02_ruined_village.png` |
| P0-3 | SC-09 | Shore Wraith boss arena | `scenes/SC-09_shore_wraith.png` |
| P0-4 | SC-12 | Dragon Palace Gate vertigo | `scenes/SC-12_palace_gate.png` |
| P0-5 | SC-16 | Choice moment — box glow, three paths implied | `scenes/SC-16_choice.png` |

### Tier P1 — Full storyboard pass (14 scene images)

| ID | Scene | Key visual |
|----|-------|------------|
| SC-00 | Prologue | Spirit-turtle rescue, palace silhouette, lacquer box |
| SC-01 | Shore arrival | Urashima on grey beach, box, ruined gate distant |
| SC-03 | Cracked torii | Low angle torii, spirit particles, no Yuzu body |
| SC-04 | Roku shack | Interior two-shot, map handoff |
| SC-05 | Salt Crab | Tutorial fight wide — optional |
| SC-06 | Cave entrance | Biolume algae, cave mouth |
| SC-07 | Water puzzle | **Silent** — flooded chamber, switch, no speech bubbles |
| SC-08 | Deep pool | Faces under black water |
| SC-10 | Yuzu join | Materialize from torii shards |
| SC-11 | Flashback | Otohime silhouette, letterbox 2.39:1 crop |
| SC-13 | Mirror | Young + old Urashima reflection |
| SC-14 | Sentinel | Ryūgū armor, gold slit eye |
| SC-15 | Tide Keeper | Humanoid tide, clock motifs in water cloak |
| SC-17a/b/c | Endings | One image per ending |

### Tier P2 — Portraits (UI-adjacent)

| Character | Framing | File |
|-----------|---------|------|
| Urashima | Chest up, box edge visible | `characters/urashima_portrait.png` |
| Yuzu | Chest up, fox bell | `characters/yuzu_portrait.png` |
| Roku | Chest up, harpoon strap | `characters/roku_portrait.png` |
| Otohime | Half-face shadowed | `characters/otohime_portrait.png` |

---


## 5. Per-scene illustration briefs

Briefs align with `STORYBOARD.md`. Use as ComfyUI/GameLab prompt body.

### SC-00 — Prologue
- **Mood:** Mythic, fateful
- **Elements:** Wounded spirit-turtle in nets, Urashima cutting free, distant Dragon Palace gold under waves, red lacquer box
- **Palette:** Deep sea teal, gold flash, black vignette

### SC-01 — Arrival
- **Mood:** Lonely, grey sky
- **Elements:** Urashima kneeling on pale sand `#C9B89A`, clutching box `#6B1A1A`, driftwood, distant collapsed torii fragment, fog `#8B9DAF`
- **Camera:** Wide establishing

### SC-02 — Empty Village
- **Mood:** Dread, silence
- **Elements:** Submerged houses, rotting festival banner `#8B3A2A`, child sandal in puddle, moss `#3D5C4A`, no living people
- **Camera:** Slow pan feel — wide hub shot

### SC-03 — Cracked Torii
- **Mood:** Accusatory, spiritual
- **Elements:** Broken torii hero prop, cyan spirit motes `#4AE8D8`, low angle up, Yuzu as voice only (particles, not full body)

### SC-07 — Water Puzzle (**no dialogue**)
- **Mood:** Quiet problem-solving
- **Elements:** Flooded chamber, stone switch, water at HIGH state, ancient latch platform — **no text, no speech bubbles**
- **Note:** Illustration matches intentional silence (`NARRATIVE_WRITING_GUIDE.md` §4)

### SC-09 — Shore Wraith
- **Mood:** Confrontational, tragic
- **Elements:** Colossal draped wraith ~4m, villager faces in cloth folds, Urashima small in foreground, cave pool, teal drip highlights

### SC-11 — Otohime Flashback
- **Mood:** Seductive, too perfect
- **Elements:** Porcelain court dress, coral gold trim `#D4A55A`, cave wall overlay, letterbox crop

### SC-12 — Palace Gate
- **Mood:** Awe, scale
- **Elements:** Ryūgū-jō gate floating over void sea, lacquer pillars `#8B2A3A`, vertigo tilt, pearl glow

### SC-16 — Choice
- **Mood:** Stillness
- **Elements:** Urashima close-up, box full bloom `#8B2A3A` glow, three abstract light paths (rewind / anchor / drift) — no UI chrome required

### SC-17a / b / c — Endings
| Ending | Key visual |
|--------|------------|
| Rewind | Restored festival, lanterns, Urashima dissolving at crowd edge |
| Anchor | Dawn shore, sapling, three rebuilders, older Urashima on driftwood |
| Drift | Lone boat, open sea, palace glimmer underwater |

---
