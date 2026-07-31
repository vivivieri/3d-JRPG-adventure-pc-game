---
id: spatial-kit
type: reference
audience: [visual, builder]
phase: [1]
status: active
authority: briefs
tokens_est: 796
summary: "Spatial composition + kit build order"
---
# ruined_village brief — Spatial composition + kit build order

**Hub:** [`ruined_village.md`](../ruined_village.md)

## Spatial composition contract

| Field | Target | Why humans care |
|-------|--------|-----------------|
| `min_path_width_m` | **2.0** | Player never stuck on geometry |
| `max_props_per_100m2` | **12** | Clutter vs readability |
| `max_hero_props_per_20x20m` | **8** | No visual noise at gameplay cam |
| `hub_size_m` | 120 × 120 | `LEVEL_DESIGN.md` §3 |
| `vista_anchor` | **Damaged torii** at north end of main path | Direction without UI compass |
| `gameplay_cam_height_m` | **1.6** | Validates door / well / torii scale |
| `pier_drop_m` | −2.0 to water | Pier submerge read |
| `torii_arch_height_m` | ≥ **4.0** (≥2.3× Urashima 1.7 m) | Silhouette dominance at vista |
| `well_visible_from_path` | Yes — no compass needed | Save point discoverability |
| `golden_screenshot` | `artifacts/screenshots/phase1_ruined_village_gameplay.png` | L2 visual regression |
| `golden_establishing` | `artifacts/golden/ruined_village_establishing.png` | SC-02 first-enter pan |

### Scene layout (do not move gameplay markers)

```
                    [SEA -Z]
    ═══════════════════════════════════
         pier          submerged roofs
              \
    [well]──[shack]──[path]──[torii/shrine]
              |                    |
         [banner inspect]    [sandal puddle]
              |
         [tutorial path]──[cave entrance cliff]
```

**Marker nodes (GDAI):** `ToriiShrine`, `RokuShack`, `VillageWell`, `InspectBanner`, `InspectSandal`, `TutorialEncounter`, `CaveEntrance` — see `LEVEL_DESIGN.md` §3.

---


## Modular kit priorities (build order)

### Architecture (ComfyUI / Material Maker + modular mesh)

| Asset ID | Description | Tris budget |
|----------|-------------|-------------|
| `village_wall_timber_frame` | Exposed post-and-beam | ~1.2k |
| `village_wall_mud_plaster` | Wattle ruin section | ~900 |
| `village_roof_tile_a` | Intact tile run | ~700 |
| `village_roof_tile_broken` | Collapsed pile | ~500 |
| `village_floor_wood_rotten` | Pier / floor planks | ~600 |
| `village_pier_piling` | Barnacled post | ~400 |
| `village_pier_segment` | 2 m pier section | ~800 |
| `village_stairs_wood` | Short stair to shrine | ~500 |

### Props (Phase 1 minimum)

| Asset ID | Storyboard | Notes |
|----------|------------|-------|
| `village_well_stone` | SC-02 save | 1.5k tris; interact highlight read |
| `village_lantern_ishidoro` | Shrine path | Warm `#D4A880` emissive cap |
| `village_banner_festival_torn` | SC-02 inspect | Rust `#8B3A2A` accent |
| `village_sandal_child` | SC-02 puddle | Small zōri in shallow water |
| `village_puddle_shallow` | Sandal float | Water shader hook |
| `village_rope_coil` | Pier | Dock dressing |
| `village_fish_net` | Shack exterior | Torn net drape |

### Hero set-pieces (vertical slice gate)

| Asset ID | Tris | Brief notes |
|----------|------|-------------|
| `village_torii_damaged` | 4k–25k | **Cracked torii** — splinter pattern, moss on base; spirit particles at SC-03; height ≥4 m arch |
| `village_shack_roku` | 3k–15k | Half-collapsed diver shack; door ~2.0 m; **3 porch steps**; interior lantern glow visible from doorway at gameplay cam |
| `village_shrine_pad` | ~2k | Stone platform under torii |

---
