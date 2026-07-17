# Tides of Urashima — Storyboard Illustrations (Pitch Package)

**Version:** 1.0  
**Purpose:** Presentation art for pitches, Steam, social, and team alignment — **not** final in-game assets unless regenerated as 3D via `ART_AUTOMATION_PIPELINE.md`.  
**Cross-refs:** `docs/vision/STORYBOARD.md`, `docs/art/ART_DIRECTION.md`, `docs/art/CHARACTER_BIBLE.md`, `docs/ui/CINEMATICS.md`

---

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
docs/pitch/illustrations/
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
| SC-00 | Prologue | Kappa-turtle rescue, palace silhouette, lacquer box |
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

## 6. AI generation prompt template

```
[Subject from §5], Tides of Urashima stylized Japanese game concept art,
hand-painted illustration style, muted melancholy coastal JRPG mood,
adult proportions head-to-body 1:5, palette [hex list from zone],
high detail environment, readable silhouette, fog and decay,
no chibi, no text, no watermark, 16:9 cinematic composition
```

**Example (SC-02):**
```
Ruined Japanese fishing village overtaken by sea, rotting festival banners,
submerged wooden houses, grey fog sky #8B9AF, moss and rust accents,
lonely fisherman silhouette with red lacquer box on hip, wide establishing shot,
stylized NPR game concept art, melancholy, no people, no text
```

---

## 7. Automated regeneration brief

| Deliverable | Format | Tool |
|-------------|--------|------|
| Key scenes P0 | PNG 1920×1080 | ComfyUI / Cursor image gen |
| Full storyboard P1 | PNG 1920×1080 | ComfyUI batch |
| Character portraits | PNG 1024×1024 | ComfyUI + `palette_remap.py` |
| Contact sheet | PNG 3840×2160 | ComfyUI batch (optional) |

**Rights:** Log AI tool + prompt in `docs/art/LICENSES.md` + `tools/register_asset.py`.

**Pitch art:** Tool-generated illustrations are acceptable for **marketing/pitch** until 3D replaces for ship (`ASSET_COMPLIANCE.md`).

---

## 8. Pitch deck assembly

Suggested slide order for a 10-minute presentation:

1. Title — `party_lineup.png`  
2. Elevator pitch (text)  
3. SC-00 → SC-01 — prologue + arrival  
4. SC-02 hub — exploration loop  
5. SC-05 / SC-09 — combat + boss  
6. SC-12 palace — Act III scale  
7. SC-16 + three ending thumbs  
8. Scope slide (2–3 h, 3 endings, en/ja/zh)  
9. Vertical slice gate — SC-02 3D target  

---

## 9. Relationship to 3D production

| Illustration | 3D target |
|--------------|-----------|
| `SC-02_ruined_village.png` | `ENVIRONMENT_KITS.md` village kit + vertical slice |
| Character portraits | `CHARACTER_BIBLE.md` portrait spec |
| `SC-09_shore_wraith.png` | `shore_wraith.glb` mesh breakdown |
| Box in all shots | `ITEMS_3D_MODEL_GUIDE.md` lacquer box |

Illustrations are **reference** for modelers — not traced 1:1 if composition differs.

---

## 10. QA checklist (pitch package)

- [x] P0 five images exist under `docs/pitch/illustrations/`
- [x] P1 full scene pass (SC-00 through SC-17c)
- [x] P2 character portraits (party + 4 busts)
- [ ] Palettes match zone hex values at a glance
- [ ] No chibi / European castle motifs
- [x] SC-07 image has no dialogue text
- [x] All images logged in `LICENSES.md`
- [x] `README.md` links pitch folder for collaborators
