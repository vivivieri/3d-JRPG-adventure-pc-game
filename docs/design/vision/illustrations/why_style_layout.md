---
id: why-style-layout
type: how-to
phase: [1, 6]
audience: [visual, narrative, pm]
status: active
authority: vision
tokens_est: 574
summary: "Why, visual style, file layout"
---
# Storyboard Illustrations — Why, visual style, file layout

**Hub:** [`STORYBOARD_ILLUSTRATIONS.md`](../STORYBOARD_ILLUSTRATIONS.md)

## 1. Why illustrations with the storyboard?

| Use | Benefit |
|-----|---------|
| **Pitch to collaborators** | Show mood before M6 3D rebuild |
| **Steam / social** | Capsule-adjacent key art |
| **Writer / composer brief** | One image per emotional beat |
| **Playtest recruitment** | Faster read than 39 design docs |

**Rule:** Illustrations follow the same hex palettes and silhouettes as `ART_DIRECTION.md`. When 3D models ship, replace pitch art in marketing only — in-game uses GLB assets.

---


## 2. Visual style (all illustrations)

| Attribute | Spec |
|-----------|------|
| Style | High-detail **stylized Japanese** — automated stylized NPR look, not photoreal |
| Reference tone | *Ni no Kuni* richness, *Eastward* clarity, Japanese coastal motifs |
| Mood | Melancholy, muted, beauty with decay |
| Proportions | Adult 1:5 head-to-body — **no chibi** |
| Palette | Zone hex from `ART_DIRECTION.md` §1 |
| Text | No embedded text in image (add titles in slide deck) |
| Aspect | 16:9 for scenes; 1:1 for character portraits |

### Global negative prompts (AI or brief to artist)

- Chibi, bright candy colors, European medieval castle
- Over-sexualized characters, modern streetwear
- Photoreal skin, HDR reflections, anime sparkle eyes

---


## 3. File layout

```
docs/archive/pitch/illustrations/
  README.md
  characters/
    urashima_portrait.png
    yuzu_portrait.png
    roku_portrait.png
    party_lineup.png
  scenes/
    SC-00_prologue.png
    SC-01_shore_arrival.png
    SC-02_ruined_village.png
    SC-03_cracked_torii.png
    SC-06_cave_entrance.png
    SC-07_water_puzzle.png      # silent — no dialogue in scene
    SC-09_shore_wraith.png
    SC-11_otohime_flashback.png
    SC-12_palace_gate.png
    SC-16_choice.png
    SC-17a_rewind.png
    SC-17b_anchor.png
    SC-17c_drift.png
  pitch_deck/
  storyboard_contact_sheet.png  # optional 3×3 grid of key beats
```

**Naming:** `<SC-id>_<short_slug>.png` — matches `STORYBOARD.md` scene IDs.

---
