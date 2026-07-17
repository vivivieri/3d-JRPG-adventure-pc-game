# Tides of Urashima — Rendering Guide

**Version:** 1.0 (Pre-build)  
**Engine:** Godot 4.7 Forward+  
**Visual target:** High-detail **stylized Japanese 3D** — not photoreal PBR.  
**Cross-refs:** `docs/art/ART_DIRECTION.md`, `docs/world/ENVIRONMENT_KITS.md`, `docs/ui/CINEMATICS.md`, `docs/ui/SETTINGS_ACCESSIBILITY.md`

This document is the single checklist for the M5 art rebuild (Phase 7) and Godot scene polish. It adapts generic “professional 3D” advice to our art bible: automated stylized albedo, toon ramp shaders, muted coastal palette, 60 FPS @ 1080p on GTX 1060.

---

## 1. Summary checklist

| Feature | Default Godot | Our target | Apply? |
|---------|---------------|------------|--------|
| **Tonemap** | Linear (flat / washed out) | **Filmic** or **ACES** | ✅ Yes |
| **Shadows** | Off or low res | **On** — soft directional, zone-tuned | ✅ Yes |
| **Sky** | Clear color | **ProceduralSky** per zone (not sunny HDRI) | ✅ Yes |
| **Fog** | Off | **Distance fog** — hub always on | ✅ Yes |
| **Volumetric fog** | Off | **Subtle** in ruined village only | ⚠️ Optional |
| **Glow (bloom)** | Off | **On** for emissive props (box, algae, palace) | ✅ Yes |
| **SSAO / SSIL** | Off | **Skip** (or very subtle SSIL in caves only) | ❌ No (v1) |
| **PBR materials** | StandardMaterial3D | **Toon ramp** + automated stylized albedo + light normals | ✅ Adapted |
| **SDFGI / VoxelGI** | Off | **Skip** — authored fill lights instead | ❌ No (v1) |
| **LightmapGI** | Off | **Defer** — consider for static village later | ⏳ Later |

---

## 2. Renderer & project defaults

| Setting | Value | Notes |
|---------|-------|-------|
| Renderer | **Forward+** | Already set on Godot branches (`config/features=Forward Plus`) |
| MSAA | **2×** default, **4×** on High | Quality preset |
| VSync | User setting | `docs/ui/SETTINGS_ACCESSIBILITY.md` |
| Exposure | Authored per zone | Prevent fog `#8B9DAF` and biolume `#4AE8D8` clipping to white |
| Max materials per view | **≤ 8** per zone | `docs/world/ENVIRONMENT_KITS.md` §9 |

**Performance gate:** 60 FPS @ 1080p on GTX 1060 — test SC-02 Ruined Village vertical slice before full production. **Hardware + environment spec:** `docs/qa/PERFORMANCE_BASELINE.md` · `game/data/qa/perf_baseline.json`.

---

## 3. WorldEnvironment (per zone)

Every world scene needs a `WorldEnvironment` node. Apply via `game/scripts/exploration/zone_visuals.gd` or a saved `.tres` preset per zone.

### 3.1 Global defaults

| Property | Value |
|----------|-------|
| `background_mode` | `BG_SKY` |
| `tonemap_mode` | `TONE_MAPPER_FILMIC` (or `TONE_MAPPER_ACES` — pick one and keep consistent) |
| `ambient_light_source` | `AMBIENT_SOURCE_COLOR` |
| `fog_enabled` | `true` |
| `fog_sky_affect` | `0.85` |
| `fog_light_color` | Zone palette fog hex (see §5) |

### 3.2 Post-processing

| Effect | When | Settings |
|--------|------|----------|
| **Glow** | Palace, caves, any emissive interactable | `glow_enabled = true`; intensity ~0.3–0.4; bloom ~0.15–0.2; mode Softlight |
| **SSAO** | — | **Off** — fights toon ramp |
| **SSIL** | — | **Off** in v1; if caves feel flat, try very low intensity in `tidal_caves` only |
| **Volumetric fog** | Ruined village hub | Light density; do not use in caves or palace void |
| **Adjustments** | Combat defeat only | Desaturate via `CINEMATICS.md` §4 — not a permanent env setting |

### 3.3 What to avoid

- Mixing StandardMaterial3D PBR and toon shaders in the same scene (`ART_DIRECTION.md` §9)
- Pure white directional lights — always tint warm or cool
- HDR reflections, glossy skin, lens flare (`CINEMATICS.md` §9)
- SDFGI (open-world GI — wrong scale and aesthetic for this game)

---

## 4. Sky

Use **ProceduralSkyMaterial**, not PhysicalSky + HDRI. Our mood is grey overcast coast, biolume caves, and void palace — not sunny photoreal outdoors.

| Zone | Sky top | Sky horizon | Ground horizon | Sun |
|------|---------|-------------|----------------|-----|
| `beach_shore` | `#5A98B0` | `#C8E0EC` | `#3A7888` | Low angle, soft (`sun_angle_max` ~32°) |
| `ruined_village` | `#4A7A9A` | `#B8D0E0` | `#6A8A9A` | Overcast (`sun_angle_max` ~28°) |
| `tidal_caves` | `#060C14` | `#1A3048` | `#142838` | No visible sun — emissive fill |
| `dragon_palace_gate` | `#080818` | `#3A2868` | `#1A2858` | Void sky; warm gold light from above |
| Endings | Per ending doc | `ENVIRONMENT_KITS.md` §7 | — | Sunset / cleared fog for Rewind |

**Do not** use a generic sunny PhysicalSky HDRI — it breaks the muted emotional palette.

---

## 5. Lighting & shadows

### 5.1 Rule

**One dominant DirectionalLight3D + one colored fill per zone** (`ART_DIRECTION.md` §3.7).

| Zone | Directional color | Angle | Fill |
|------|-------------------|-------|------|
| `beach_shore` | Warm `#F0E8D0` | ~−48° / −35° | Ambient × 0.4 |
| `ruined_village` | Cool overcast `#B8C8D8` | 35° | Warm `#D4A880` at lantern + shack |
| `tidal_caves` | Cyan `#6EC8C0` (low) | N/A (no sky) | Emissive algae `#4AE8D8` |
| `dragon_palace_gate` | Gold `#FFD890` | ~−62° / 22° | Ambient × 0.55; glow on trim |

### 5.2 Shadows

| Property | Target |
|----------|--------|
| `shadow_enabled` | `true` on all zone directionals |
| Filter | Soft shadow filter (quality preset) |
| `directional_shadow_mode` | Orthogonal for palace; default elsewhere |
| `shadow_opacity` | ~0.4–0.5 in void palace (softer read) |
| Max distance | Tune so village props stay sharp near camera; fade before horizon |

### 5.3 Point / spot lights

- Caves: cyan pool lights only — **avoid pure white**
- Palace mirror chamber (SC-13): dual rim lights — `CINEMATICS.md`
- Lanterns / shrine glow: warm `#D4A880` omni, low range

---

## 6. Fog

| Zone | Fog color | Density | Aerial perspective | Notes |
|------|-----------|---------|-------------------|-------|
| `beach_shore` | `#9AB8C8` | 0.010 | 0.78 | Light coastal haze |
| `ruined_village` | `#8B9DAF` | 0.008 | 0.72 | **Always on** — draw-distance mask |
| `tidal_caves` | `#0A141C` | 0.028 | 0.48 | Heavier — depth in tunnels |
| `dragon_palace_gate` | `#1A1A3A` | 0.012 | 0.68 | Void atmosphere |

**Hub rule:** Fog always on in ruined village (`ART_DIRECTION.md` §3.5).  
**Fog start:** ~20 m in village per `ENVIRONMENT_KITS.md` §4.

---

## 7. Materials & shaders

### 7.1 Use (stylized stack)

| Map / technique | Usage |
|-----------------|-------|
| **Albedo** | Automated stylized (ComfyUI/Material Maker + palette_remap); 4K heroes, 2K modules, 1K weapons |
| **Normal map** | Light normals OK — brick mortar, wood grain, stone cracks |
| **Emission** | Algae, lacquer box, palace gold, spirit lower body |
| **Toon ramp** | Single shader family across scene |
| **Roughness variation** | Via stylized albedo grunge — not metallic PBR workflow |

### 7.2 Do not use (v1)

| Technique | Why |
|-----------|-----|
| Full PBR ORM packs | Conflicts with toon look; art bible §3.4 |
| Metallic / glossy skin | Wrong tone for muted JRPG |
| HDR environment reflections | Breaks stylized readability |
| Realistic water simulation | Use stylized planes + foam decals + custom shader |

### 7.3 Custom shaders (recommended)

| Shader | Purpose | Reference |
|--------|---------|-----------|
| **Water** | Gentle vertex displacement, foam edge, zone tint | `water_stylized.gdshader` |
| **Spirit alpha** | Additive / alpha on Yuzu lower body | `CHARACTER_BIBLE.md` |
| **Lacquer box glow** | 3 emission states by story flag | `CHARACTER_BIBLE.md` §2 |
| **Mirror chamber** | Mirror shader SC-13 | `STORYBOARD.md` |
| **Wind sway** | Coastal grass / reeds vertex offset | Optional polish |
| **Ink-wash combat** | 2D screen shader on transition | `CINEMATICS.md` §9 |

---

## 8. Global illumination

| System | Verdict | Notes |
|--------|---------|-------|
| **SDFGI** | ❌ Skip | Open-world, realistic bounce — wrong for 2–3 h stylized game |
| **VoxelGI** | ❌ Skip (v1) | Expensive; caves can use emissive + fill lights |
| **LightmapGI** | ⏳ Later | Good for static ruined village on low-end; needs bake pipeline |
| **Authored fill** | ✅ Now | Directional + colored ambient + emissive props |

---

## 9. Glow targets (bloom)

Enable `Environment.glow` wherever emissive content should read on screen:

| Asset / moment | Color | Intensity note |
|----------------|-------|----------------|
| Lacquer box (dormant) | `#8B2A3A` seam | Faint — 15% emission |
| Lacquer box (awakened) | `#8B2A3A` pulse | Looping; SC-02+ |
| Lacquer box (choice) | Strong bloom | SC-16 |
| Cave algae | `#4AE8D8` | Primary cave fill |
| Palace gold trim | `#D4A55A` | Palace zone glow enabled |
| Spirit particles | `#6EC8C0` | Additive |
| Lore interactables | Cyan subtle | `LORE_AND_ENVIRONMENTAL_STORY.md` |
| Puzzle switch (stuck 5 min) | Glow pulse + chime | `PUZZLE_DESIGN.md` |

Tune glow so emissive elements **pop without blowing out** the muted palette.

---

## 10. Graphics quality presets

Add to settings menu (`docs/ui/SETTINGS_ACCESSIBILITY.md`). Store in `user://settings.json`.

| Preset | Shadows | MSAA | Glow | Fog density | Notes |
|--------|---------|------|------|-------------|-------|
| **Low** | Off or hard only | Off | Off | 50% | GTX 1050 / laptop |
| **Medium** | Soft, 1024 | 2× | On | 100% | Default — target GTX 1060 |
| **High** | Soft, 2048 | 4× | On + HQ | 100% | Desktop |

**Storage keys (proposed):** `graphics_quality`, `shadows_enabled`, `msaa`, `glow_enabled`, `fog_density_scale`

Apply at runtime by updating `WorldEnvironment.environment` and `DirectionalLight3D` shadow settings when the player changes preset.

---

## 11. Zone implementation map

| Scene | `zone_id` | WorldEnvironment | Sky | Glow | Special |
|-------|-----------|-------------------|-----|------|---------|
| `beach_shore.tscn` | `beach_shore` | ✅ | ProceduralSky | Off (`glow_enabled: false`) | Coastal haze |
| `ruined_village.tscn` | `ruined_village` | ✅ | Overcast | On emissive (`glow_use_case: emissive_only`) | Vertical slice gate |
| `tidal_caves.tscn` | `tidal_caves` | ✅ | Dark | On (`glow_use_case: emissive_algae`) | No sky; emissive primary |
| `dragon_palace_gate.tscn` | `dragon_palace_gate` | ✅ | Void | On | Gold directional |
| `ending_*.tscn` | per ending | ✅ | Custom | Per scene | Fog cleared on Rewind |

**Code entry point:** `ZoneVisuals.apply_to_scene(root, zone_id)` — Godot feature branches.

---

## 12. M5 art acceptance checklist

Before marking an M5 art-pass zone complete, verify:

- [ ] `WorldEnvironment` present; tonemap Filmic or ACES
- [ ] Directional shadows on; light color matches zone table (§5)
- [ ] Fog color + density match palette (§5–6)
- [ ] Sky matches zone (ProceduralSky — not default clear color)
- [ ] Materials use toon ramp family — no stray PBR glossy materials
- [ ] Emissive glow reads on box / algae / palace trim
- [ ] No `BoxMesh` / primitive placeholders in player-facing view
- [ ] ≤ 8 materials visible per zone at gameplay camera
- [ ] 60 FPS @ 1080p on target hardware
- [ ] Graphics Low/Medium/High presets functional (when implemented)

**Vertical slice gate:** SC-02 Ruined Village first — `docs/art/ART_DIRECTION.md` §10.

---

## 13. Reference: `zone_visuals.gd` contract

**Authority:** `game/data/code/base_classes.json` (`ZoneVisuals`) · `tools/zone_visuals_lib.py` · `game/data/world/zone_palettes.json`

### Canonical entry (zone load)

`ZoneVisuals.apply_to_scene(root, zone_id)` — static; finds `WorldEnvironment`, `DirectionalLight3D`, and nodes in group `zone_fill_light`, then applies palette data.

### Instance node (in-scene)

`ZoneVisuals` node with `@export zone_id` — on `_ready` calls `apply_zone_visuals()` when `apply_on_ready` is true.

### Runtime behavior

- `WorldEnvironment` with Filmic tonemap (`defaults.tonemap_mode`)
- `ProceduralSkyMaterial` per zone palette row
- Zone fog density + aerial perspective (`defaults.fog_sky_affect`)
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
| `docs/art/ART_DIRECTION.md` | Palette, poly budgets, style rules |
| `docs/world/ENVIRONMENT_KITS.md` | Per-zone lighting tables, fog start |
| `docs/ui/CINEMATICS.md` | Camera fog overrides, combat FX |
| `docs/art/CHARACTER_BIBLE.md` | Box glow states, spirit materials |
| `docs/ui/SETTINGS_ACCESSIBILITY.md` | Graphics quality presets (§10) |
| `game/scripts/exploration/zone_visuals.gd` | Runtime zone environment (Godot branches) |
| `game/assets/shaders/toon_base.gdshader` | NPR ramp family (GLB post-import + zones) |
| `game/shaders/water_stylized.gdshader` | Stylized water (foam + displacement) |
