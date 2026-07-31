---
id: dragon-palace
type: reference
audience: [builder, builder_zone, visual]
phase: [5, 6]
status: active
authority: world
tokens_est: 657
summary: "Palace + endings"
---
# Environment Kits — Palace + endings

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

## 6. Zone: Dragon Palace Gate (`dragon_palace_gate`)

**Storyboard:** SC-12 – SC-16
**Mood:** Awe, scale, sterile perfection vs living world
**Palette:** Coral gold `#D4A55A`, crimson `#8B2A3A`, void `#1A1A3A`

**Critical:** Replace all European castle geometry with **ryūgū-jō** language.

### Modular kit — palace

| Asset ID | Description | Tris |
|----------|-------------|------|
| `palace_pillar_lacquer` | Crimson lacquer column | 1.2k |
| `palace_rail_carved` | Dragon-wave rail | 600 |
| `palace_floor_marble` | Pale tile | 500 |
| `palace_roof_eave_curved` | Karahafu-inspired eave | 1.5k |
| `palace_wall_panel_gold` | Gold inlay panel | 800 |
| `palace_banner_crimson` | Hanging banner | 400 |
| `palace_bridge_segment` | Floating walkway | 1k |
| `palace_lantern_hanging` | Paper + gold frame | 500 |

### Hero set-pieces

| Asset ID | Description | Tris | Storyboard |
|----------|-------------|------|------------|
| `palace_gate_main` | **Impossible floating gate** | 18k | SC-12 vertigo shot |
| `palace_mirror_chamber` | Reflective floor + frame | 8k | SC-13 |
| `palace_sentinel_hall` | Long hall + statues | 12k | SC-14 |
| `palace_throne_tides` | Tide Keeper arena | 10k | SC-15–16 |
| `palace_void_sea` | Below-architecture drop | — | Void blue plane |

### Scope note: reverse gravity

**Cut from v1.** GDD §6.3 reverse-gravity rooms removed; palace uses **floating walkways** and vertical scale instead. Revisit post-launch if needed.

### Lighting

- Directional: warm gold `#FFD890` from above
- Void gaps: no geometry; skybox `#1A1A3A`
- Mirror chamber: dual rim lights (young/old Urashima)

---


## 7. Ending environments (`endings/`)

### SC-17a — Rewind (`ending_rewind`)

| Asset ID | Description |
|----------|-------------|
| `village_restored_kit` | Warm lantern variants, intact roofs |
| `village_festival_lantern_row` | Lit chochin strings |
| `village_crowd_silhouettes` | 8–12 low NPC meshes |
| `village_festival_banner_intact` | Red + white nobori |

**Lighting:** Sunset warm; fog cleared; crane-up camera path documented in `CINEMATICS.md`

### SC-17b — Anchor (`ending_anchor`)

| Asset ID | Description |
|----------|-------------|
| `shore_dawn_skybox` | Pink-gold horizon |
| `prop_sapling_new` | Planted tree Roku |
| `rebuilder_figures` | 3 silhouettes with tools |
| `spirit_dissolve_vfx` | Yuzu + spirits fade into ground |

### SC-17c — Drift (`ending_drift`)

| Asset ID | Description |
|----------|-------------|
| `boat_urashima` | Small fishing boat | 2k |
| `sea_endless_plane` | Open ocean |
| `palace_underwater_glimpse` | Sunken gate silhouette below surface |

---
