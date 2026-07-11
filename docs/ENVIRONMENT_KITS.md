# Tides of Urashima — Environment Kits

**Version:** 1.0 (Pre-build)  
**Visual target:** High-detail stylized Japanese coastal environments — authored modular kits, no greybox boxes in ship builds.  
**Cross-refs:** `docs/ART_DIRECTION.md`, `docs/STORYBOARD.md`, `docs/CHARACTER_BIBLE.md`, `docs/RENDERING_GUIDE.md`

---

## 1. Global environment rules

| Rule | Detail |
|------|--------|
| Modular first | 80% kit pieces; 20% hero set-pieces |
| Poly per module | 500–3k tris (rocks/walls); hero props 8k–20k |
| Textures | ComfyUI / Material Maker + `palette_remap.py`; light normal maps OK |
| No primitives | No `BoxMesh` / `CylinderMesh` in player-facing scenes |
| Fog | Always on in hub (`#8B9DAF`); zone-specific elsewhere |
| Water | Stylized planes + foam decals; sculpted pool basins in caves |
| Lighting | One dominant directional + one colored fill per zone |
| Cohesion | Japanese coastal / ryūgū motifs only — **no European castle kits** |

### Folder layout

```
game/assets/models/environment/
  shared/           # Rocks, cliffs usable in multiple zones
  beach_shore/
  ruined_village/
  tidal_caves/
  dragon_palace_gate/
  endings/
game/assets/textures/environment/
  <zone>_<surface>.png
```

---

## 2. Shared kit (cross-zone)

| Asset ID | Description | Tris | Notes |
|----------|-------------|------|-------|
| `shared_rock_coast_a` | Barnacled coastal boulder | 800 | Beach, village shore |
| `shared_rock_coast_b` | Flat tide rock | 600 | Stepping, cave mouth |
| `shared_cliff_face_a` | Vertical cliff slice | 2.5k | Cave entrance backdrop |
| `shared_driftwood_a` | Bleached log | 400 | Beach, village |
| `shared_driftwood_b` | Root tangle | 700 | SC-01 shore |
| `shared_seaweed_patch` | Ground decal mesh | 200 | Vertex color green |
| `shared_foam_line` | Shore foam strip decal | 100 | Water edge |
| `shared_fog_volume` | Large transparent box (invisible) | — | Engine fog trigger only |

---

## 3. Zone: Beach Shore (`beach_shore`)

**Storyboard:** SC-01  
**Mood:** Lonely arrival; grey sky; distant thunder  
**Palette:** Pale sand `#C9B89A`, surf teal `#1A6A62`, fog `#8B9DAF`

### Modular kit

| Asset ID | Description | Tris | Placement notes |
|----------|-------------|------|-----------------|
| `beach_terrain_sand` | Sculpted sand mesh (organic) | 4k | Replace flat ground |
| `beach_terrain_dune` | Low dune ridge | 1.5k | Inland edge |
| `beach_path_worn` | Packed sand path | 800 | Spawn → village gate |
| `beach_grass_clump` | Coastal grass | 300 | Sparse on dunes |
| `beach_pebble_scatter` | Small stones | 200 | Near waterline |

### Hero set-pieces

| Asset ID | Description | Tris | Story |
|----------|-------------|------|-------|
| `beach_ruined_gate_silhouette` | Collapsed village entry torii fragment | 3k | SC-01 distant read |
| `beach_lacquer_box_prop` | Ground-placed box (tutorial) | 500 | Optional inspect near spawn |
| `beach_shoreline_water` | Water plane + foam | — | `WaterController` hook |

### Scene composition (SC-01)

```
[Spawn] ──path──► [Ruined gate silhouette] ──transition──► ruined_village
         driftwood clusters          low cliff left
         box prop optional           thunder sky audio
```

### Audio / VFX

- Ambient: surf loop, distant thunder one-shot every 45–90s
- VFX: Light rain particles optional; no combat

---

## 4. Zone: Ruined Fishing Village (`ruined_village`) — HUB

**Storyboard:** SC-02 – SC-05  
**Mood:** Dread, decay, submerged Edo fishing hamlet  
**Palette:** Weathered wood `#5C4A3A`, moss `#3D5C4A`, rust `#8B3A2A`

### Modular kit — architecture

| Asset ID | Description | Tris |
|----------|-------------|------|
| `village_wall_timber_frame` | Exposed post-and-beam section | 1.2k |
| `village_wall_mud_plaster` | Wattle & plaster ruin | 900 |
| `village_roof_tile_a` | Intact tile run | 700 |
| `village_roof_tile_broken` | Collapsed tile pile | 500 |
| `village_floor_wood_rotten` | Pier / floor planks | 600 |
| `village_pier_piling` | Barnacled post | 400 |
| `village_pier_segment` | 2m pier section | 800 |
| `village_stairs_wood` | Short stair to shrine | 500 |

### Modular kit — props

| Asset ID | Description | Tris | Storyboard |
|----------|-------------|------|------------|
| `village_well_stone` | Old well | 1.5k | Save point SC-02 |
| `village_lantern_ishidoro` | Stone lantern, cracked | 800 | Shrine path |
| `village_banner_festival_torn` | Rotting nobori | 400 | Inspect SC-02 |
| `village_sandal_child` | Small zōri | 150 | Inspect SC-02 puddle |
| `village_puddle_shallow` | Mesh depression + water | 300 | Sandal float |
| `village_rope_coil` | Dock rope | 200 | Pier |
| `village_fish_net` | Torn net draped | 350 | Shack exterior |

### Hero set-pieces

| Asset ID | Description | Tris | Storyboard |
|----------|-------------|------|------------|
| `village_torii_damaged` | **Cracked torii** — hero prop | 8k | SC-03; spirit particles |
| `village_shack_roku` | Half-collapsed diver shack | 6k | SC-04 interior/exterior |
| `village_shrine_pad` | Stone platform under torii | 2k | SC-03 |

### Gameplay markers (do not move)

| Marker | Purpose |
|--------|---------|
| `ToriiShrine` | SC-03 dialogue |
| `RokuShack` | SC-04 dialogue + shop |
| `VillageWell` | Save point |
| `InspectBanner` | SC-02 lore |
| `InspectSandal` | SC-02 lore |
| `TutorialEncounter` | SC-05 Salt Crab |
| `CaveEntrance` | → tidal_caves |

### Scene layout (top-down)

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

### Lighting

- Directional: cool `#B8C8D8`, angle 35° (overcast)
- Fill: warm `#D4A880` at lantern + shack interior
- Fog: start 20m, density medium

### Vertical slice scope

**Build this zone first** as art proof: torii + shack + well + Urashima walk cycle.

---

## 5. Zone: Tidal Caves (`tidal_caves`)

**Storyboard:** SC-06 – SC-10  
**Mood:** Wonder + wrongness; bioluminescent guilt  
**Palette:** Deep teal `#1A4A5A`, biolume `#4AE8D8`, wet stone `#3A3A45`

### Modular kit

| Asset ID | Description | Tris |
|----------|-------------|------|
| `cave_wall_segment_a` | Curved tunnel wall | 1.5k |
| `cave_wall_segment_b` | Narrow choke | 1.2k |
| `cave_floor_slick` | Wet floor tile | 800 |
| `cave_stalactite_cluster` | Ceiling drip | 600 |
| `cave_stalagmite_a` | Floor spike | 400 |
| `cave_rock_pile` | Blockage / cover | 1k |
| `cave_algae_emissive` | Glowing algae patch | 300 | Emissive cyan |
| `cave_switch_stone` | Puzzle interactable | 500 | SC-07 |
| `cave_chest_ancient` | Optional antidote | 700 | SC-07 |

### Hero set-pieces

| Asset ID | Description | Tris | Storyboard |
|----------|-------------|------|------------|
| `cave_entrance_arch` | Mouth below cliffs | 4k | SC-06 |
| `cave_flood_basin` | Sculpted pool basin | 3k | Water puzzle |
| `cave_deep_pool` | Guilt pool face surface | 2k | SC-08 |
| `cave_face_decal_set` | Underwater faces (4) | — | Decal on pool |
| `cave_shrine_alcove` | Small stone shrine | 2.5k | SC-10 Yuzu join |
| `cave_boss_arena_ring` | Raised stone circle | 4k | SC-09 |

### Water puzzle (SC-07)

| State | Water Y | Access |
|-------|---------|--------|
| Low | -0.5m | Switch A side, chest dry |
| High | +0.8m | Latch platform reachable |

**Markers:** `WaterPuzzle`, `DeepPoolEncounter`, `ShoreWraithBoss`

### Lighting

- No sky; emissive algae primary fill
- Point lights: cyan pools; avoid pure white

---

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

## 8. Lore collectible placements

Map for environment artists — 8 entries (`game/data/lore/lore_entries.json`).

| ID | Zone | Placement | Asset hook |
|----|------|-----------|------------|
| `fishing_ledger` | ruined_village | Near shack | Lore pickup |
| `festival_banner` | ruined_village | On `InspectBanner` | Banner inspectable |
| `yuzu_prayer` | ruined_village | Torii area | Shrine prop |
| `roku_dive_log` | ruined_village | Shack interior | Scroll prop |
| `cave_inscription` | tidal_caves | Puzzle room wall | Carved kanji |
| `sailor_charm` | tidal_caves | Post-boss alcove | Grants `spirit_bell` on read |
| `palace_seal` | dragon_palace_gate | Sentinel hall | Plaque |
| `otohime_letter` | dragon_palace_gate | Mirror chamber | Reflection trigger |

---

## 9. LOD & performance (PC target)

| Tier | Distance | Action |
|------|----------|--------|
| LOD0 | 0–25m | Full mesh |
| LOD1 | 25–60m | 50% tris |
| LOD2 | 60m+ | Impostor or culled |

**Target:** 60 FPS at 1080p on GTX 1060 / equivalent. Hub + palace are heaviest — batch materials per zone (max 8 draw call materials per view).

---

## 10. Production order

1. **Shared rocks + beach terrain** (SC-01 path)
2. **Village hub kit + torii hero** (vertical slice)
3. **Cave tunnel + algae + puzzle basin**
4. **Palace gate hero + modular trim**
5. **Mirror chamber + throne arena**
6. **Ending variants** (reuse village kit where possible)

---

## 11. Acceptance checklist (per zone)

- [ ] No box/primitive placeholders visible
- [ ] Palette matches `ART_DIRECTION.md` hex values
- [ ] Gameplay markers untouched
- [ ] Fog + water + lighting match mood table
- [ ] Japanese motif read clear at 15m camera distance
- [ ] All props logged in `LICENSES.md` if sourced externally
- [ ] Asset registered in `docs/asset_manifest.license.json` and compliance check passes
