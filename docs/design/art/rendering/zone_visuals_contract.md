---
id: zone-visuals-contract
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 891
summary: "`ZoneVisuals.apply_to_scene(root, zone_id)` — static; finds `WorldEnvironment`, `DirectionalLight3D`, and nodes in group `zone_fill_light`, then applies palette"
---
# Rendering — zone_visuals contract & refs

**Hub:** [`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)

## When to read

Use **Rendering — zone_visuals contract & refs** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [13. Reference: `zone_visuals.gd` contract](#13-reference-zone_visualsgd-contract)
- [Canonical entry (zone load)](#canonical-entry-zone-load)
- [Instance node (in-scene)](#instance-node-in-scene)
- [Runtime behavior](#runtime-behavior)
- [14. External advice filter](#14-external-advice-filter)
- [15. Related files](#15-related-files)


## 13. Reference: `zone_visuals.gd` contract

**Authority:** `game/data/code/base_classes.json` (`ZoneVisuals`) · `tools/zone_visuals_lib.py` · `game/data/world/zone_palettes.json`

### Canonical entry (zone load)

`ZoneVisuals.apply_to_scene(root, zone_id)` — static; finds `WorldEnvironment`, `DirectionalLight3D`, and nodes in group `zone_fill_light`, then applies palette data.

### Instance node (in-scene)

`ZoneVisuals` node with `@export zone_id` — on `_ready` calls `apply_zone_visuals()` when `apply_on_ready` is true.

### Runtime behavior

- `WorldEnvironment` with Filmic tonemap (`defaults.tonemap_mode`)
- `ProceduralSkyMaterial` per zone palette row
- Zone fog density + per-zone `aerial_perspective` from palette row (`fog_sky_affect` from defaults)
- Glow per zone `glow_enabled` + `glow_use_case` in `zone_palettes.json` (beach off; village/caves/palace on for emissives)
- Volumetric fog when zone row sets `volumetric_fog_enabled` (village hub)
- Colored `DirectionalLight3D` + `OmniLight3D` fill (`zone_fill_light` group)

Optional editor preset: `game/environments/ruined_village.tres` — see `environment_registry.json` (derived from palette; runtime may build via `build_environment()` instead).

**Gaps to close in M5 (art rebuild):**

1. Extend glow to caves + lacquer box emission states
2. Shadow quality tiers + soft filter
3. Graphics quality presets in settings UI
4. Optional light volumetric fog in village hub
5. Custom water shader polish (foam, displacement)
6. Zone `.tres` environment presets for designer tuning in editor

---


## 14. External advice filter

When evaluating generic “make Godot look professional” tips:

| Tip | Our answer |
|-----|------------|
| “Use full PBR ORM textures” | **No** — automated stylized + toon |
| “Enable SSAO + SSIL” | **No** (v1) — stylized, not realistic |
| “Use SDFGI for open worlds” | **No** — small authored zones |
| “PhysicalSky + HDRI” | **No** — ProceduralSky + palette |
| “ACES / Filmic tonemap” | **Yes** |
| “Soft shadows + colored lights” | **Yes** |
| “WorldEnvironment + glow on emissives” | **Yes** |
| “Custom water / wind shaders” | **Yes** |
| “Day/night cycle” | **No** — fixed zone moods |

---


## 15. Related files

| Path | Role |
|------|------|
| `docs/design/art/ART_DIRECTION.md` | Palette, poly budgets, style rules |
| `docs/design/world/ENVIRONMENT_KITS.md` | Per-zone lighting tables, fog start |
| `docs/design/ui/CINEMATICS.md` | Camera fog overrides, combat FX |
| `docs/design/art/CHARACTER_BIBLE.md` | Box glow states, spirit materials |
| `docs/design/ui/SETTINGS_ACCESSIBILITY.md` | Graphics quality presets (§10) |
| `game/scripts/exploration/zone_visuals.gd` | Runtime zone environment (Godot branches) |
| `game/assets/shaders/toon_base.gdshader` | NPR ramp family (GLB post-import + zones) |
| `game/shaders/water_stylized.gdshader` | Stylized water (foam + displacement) |
