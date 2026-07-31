---
id: zones
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 500
summary: "Generation Readiness — Characters & Zones — Zone rows"
---
# Generation Readiness — Characters & Zones — Zone rows

**Hub:** [`characters_zones.md`](../characters_zones.md)

## When to read

Use **Generation Readiness — Characters & Zones — Zone rows** (roles: visual, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Zone rows (`ENVIRONMENT_KITS.md`)](#5-zone-rows-environment_kitsmd)
- [Per-zone composition contract (to add to `ENVIRONMENT_KITS.md` or `game/data/qa/zone_composition.json`)](#per-zone-composition-contract-to-add-to-environment_kitsmd-or-gamedataqazone_compositionjson)


## 5. Zone rows (`ENVIRONMENT_KITS.md`)

| Zone ID | ✅ Specified today | ⚠️ Partial | ❌ Missing (add before ship) | Build phase |
|---------|-------------------|------------|---------------------------|-------------|
| **beach_shore** (SC-01) | Mood, palette, kit table, spawn path, **generation brief** | Water foam polish | Golden screenshot capture | 2 |
| **ruined_village** (SC-02 hub) | Full kit + layout + lighting + **generation brief** | Pier submerge depth | Golden screenshot + `L2_visual_jury` PASS | **1** |
| **tidal_caves** (SC-06–10) | Biolume palette, modular kit, **generation brief** | Face decal polish | Puzzle state screenshots | 5 |
| **dragon_palace_gate** (SC-12+) | Palace void sky, gold trim, **generation brief** | Mirror chamber polish | SC-12 vertigo golden shot | 6 |

### Per-zone composition contract (to add to `ENVIRONMENT_KITS.md` or `game/data/qa/zone_composition.json`)

| Field | Example (`ruined_village`) | Why humans care |
|-------|---------------------------|-----------------|
| `min_path_width_m` | 2.0 | No stuck on geometry |
| `max_props_per_100m2` | 12 | Clutter vs clarity |
| `vista_anchor` | Torii at end of main path | Direction without UI compass |
| `gameplay_cam_height_m` | 1.6 | Validates door/well scale |
| `golden_screenshot` | `artifacts/screenshots/phase1_ruined_village_gameplay.png` | Visual regression |

---
