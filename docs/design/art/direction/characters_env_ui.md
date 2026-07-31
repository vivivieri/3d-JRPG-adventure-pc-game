---
id: characters-env-ui
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 605
summary: "Art Direction — Silhouettes, environment, UI style — Readable at gameplay camera distance. Exaggerate head-to-body ratio slightly (1:5, not chibi 1:3). Full mod"
---
# Art Direction — Silhouettes, environment, UI style

**Hub:** [`ART_DIRECTION.md`](../ART_DIRECTION.md)

## When to read

Use **Art Direction — Silhouettes, environment, UI style** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [2. Character silhouettes](#2-character-silhouettes)
- [Urashima](#urashima)
- [Yuzu](#yuzu)
- [Roku](#roku)
- [Enemies](#enemies)
- [3. Environment style rules](#3-environment-style-rules)
- [4. UI style](#4-ui-style)


## 2. Character silhouettes

Readable at gameplay camera distance. Exaggerate head-to-body ratio slightly (1:5, not chibi 1:3). Full model sheets: `docs/design/art/CHARACTER_BIBLE.md`.

### Urashima
- Long coat over traditional fisherman's tunic
- Lacquer box on hip (glowing faintly in palace zones)
- Slouched posture → straightens through story

### Yuzu
- Shrine maiden hakama, torn hem
- Semi-transparent lower body (spirit)
- Twin braids, fox-bell accessory

### Roku
- Bulky dive suit, patched
- Harpoon on back
- Wide stance (tank read)

### Enemies
- **Salt Crab:** Low wide silhouette
- **Tide Wraith:** Tall, dripping, no legs
- **Shore Wraith:** Massive draped form
- **Palace Sentinel:** Angular armor, single eye slit
- **Tide Keeper:** Humanoid tide, flowing water cloak

---


## 3. Environment style rules

1. **Modular kits first** — 80% reused pieces (walls, floors, rocks, props); see `docs/design/world/ENVIRONMENT_KITS.md`
2. **Poly budget** — Modules 500–3k tris; hero set-pieces (torii, palace gate) 8k–20k
3. **Automated stylized albedo** (ComfyUI/Material Maker + `palette_remap.py`) + light normal maps OK; single toon ramp across scene
4. **No PBR realism** — avoid glossy skin, HDR reflections
5. **Fog always on** in hub (draw distance mask)
6. **Water** is stylized (sculpted basins + foam decals, not simulation)
7. **Lighting:** One dominant directional + colored fill per zone
8. **Japanese coastal / ryūgū motifs only** — no European castle or medieval fantasy props

---


## 4. UI style

- **Font:** Noto Serif JP (headings) + Noto Sans (body) — OFL license
- **Menu frames:** Ink-wash border texture (subtle)
- **HP bars:** Horizontal, deep red fill, dark frame
- **Combat intent icons:** Simple pictograms (sword, skull, shield, sparkles)
- **Dialogue box:** Lower third, semi-transparent `#1A1A2ECC`, white text

---
