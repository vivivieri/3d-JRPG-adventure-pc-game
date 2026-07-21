# Generation brief — `ruined_village`

**Status:** P0 · Phase 1 vertical slice (SC-02 hub gate)
**Authority:** `docs/world/ENVIRONMENT_KITS.md` §4, `docs/world/LEVEL_DESIGN.md` §3, `docs/art/RENDERING_GUIDE.md`
**Cross-refs:** `docs/art/GENERATION_READINESS.md`, `docs/art/ART_AUTOMATION_PIPELINE.md` §4–5

---

## Intent (one sentence)

Muted overcast **submerged Edo fishing hamlet** hub (~120×120 m) — dread and decay, torii silhouette at vista anchor, **well save visible from main path without compass**, ≤8 hero props in any 20×20 m gameplay view.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Dread, decay, submerged grief |
| Secondary mood | Faint warmth at lantern/shack — not comfort |
| Audience read | Men 20–30 — beauty with decay; not sunny slice-of-life |
| Static read (screenshot) | Overcast fog, weathered wood, torii vista — oppressive but readable |
| Motion feel (human L6) | Slow exploration weight; pier/submerge feels unsafe |
| Must avoid | Sunny anime village, tropical resort, European medieval town |
| Story anchor | SC-02 hub arrival — festival ended, village drowned in time |

---

## Tool chain

| Step | Tool | Output |
|------|------|--------|
| 1 | **ComfyUI** or **Material Maker** | Tileable NPR albedos: wood, plaster, moss, stone, roof tile |
| 2 | `palette_remap.py --zone ruined_village` | Palette-locked texture sheets |
| 3 | **Meshy** / Blender (modular) | Kit meshes per `ENVIRONMENT_KITS.md` §4 tables |
| 4 | **Meshy** (set-pieces) | `village_torii_damaged`, `village_shack_roku`, `village_well_stone` |
| 5 | `install_glb_import_pipeline.sh` | NPR post-import on environment GLBs |
| 6 | **GDAI MCP** | Assemble `ruined_village.tscn`, lights, fog, markers |
| 7 | **GodotPrompter** | `zone_visuals.gd` preset — do not hand-tune fog in inspector without doc values |

**Scene path:** `res://scenes/world/ruined_village.tscn`
**Texture path:** `game/assets/textures/environment/ruined_village/`

---

## Positive prompt anchors

### Mood & style
- Dread, decay, submerged coastal hamlet — **muted**, not sunny anime village
- Stylized Japanese coastal NPR; weathered post-and-beam, rotting pier, moss on wood
- Reference mood: overcast grief — beauty with decay; men 20–30 audience (no candy colors)

### Palette (hard hex)

| Role | Hex | Usage |
|------|-----|-------|
| Weathered wood | `#5C4A3A` | Buildings, pier, stairs |
| Moss / seaweed | `#3D5C4A` | Roof edges, ground creep |
| Rust accent | `#8B3A2A` | Banner, warning trim |
| Fog grey | `#8B9DAF` | Sky, distance, fog color |
| Pale sand / path | `#C9B89A` | Ground, worn paths |
| Cool overcast light | `#B8C8D8` | Directional key |
| Warm lantern fill | `#D4A880` | Ishidōrō, shack interior |

### Sky & atmosphere
- **ProceduralSkyMaterial** — grey overcast coast; **no** sunny PhysicalSky HDRI
- Fog **always on**: color `#8B9DAF`, density **0.008**, aerial perspective **0.72**
- Fog start ~**20 m** — masks draw distance without white clip
- Subtle volumetric fog in village only (optional M5 polish)

### Lighting (`RENDERING_GUIDE.md` §5)

| Light | Color | Notes |
|-------|-------|-------|
| Directional | `#B8C8D8` | 35° angle; shadows **on**, soft filter |
| Fill (lantern + shack) | `#D4A880` | Omni/spot — **never pure white** |
| Glow | Off or minimal | Reserve bloom for lacquer box / lanterns only |

---

## Negative prompt (required)

```
sunny bright sky, tropical resort, European medieval town, Kenney assets,
low-poly greybox, neon colors, candy anime palette, photoreal PBR ORM,
chibi props, fantasy castle, clean new wood, snow, desert, palm trees,
generic suburban, blockout cubes visible to player
```

---

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

## Hard metrics

| Constraint | Value |
|------------|-------|
| Materials visible at gameplay cam | ≤ **8** (`RENDERING_GUIDE.md` §11) |
| FPS target | 60 @ 1080p GTX 1060 |
| Toon shader family | Single ramp — no stray PBR glossy |
| Primitive placeholders | **Forbidden** in player-facing view |
| BGM | `bgm_village` |

---

## Camera beats

| Moment | Spec |
|--------|------|
| First enter (SC-02) | 4 s pan to torii silhouette (`CINEMATICS.md`) |
| Gameplay follow | Third-person; path readable; well in peripheral sightline from spawn approach |
| Establishing shot | Wide overcast — pier + submerged roofs in background fog |

---

## Acceptance evidence

- [ ] `WorldEnvironment` — Filmic/ACES tonemap, fog on, procedural overcast sky
- [ ] Directional `#B8C8D8` + warm fill at lantern/shack
- [ ] Main path ≥2 m wide; torii visible as vista from well–shack approach
- [ ] Well save interactable from path without compass
- [ ] Urashima walk cycle through hub — coat hem acceptable clip
- [ ] `artifacts/screenshots/phase1_ruined_village_gameplay.png` captured
- [ ] `artifacts/screenshots/phase1_ruined_village_establishing.png` captured (SC-02 pan)
- [ ] `python3 tools/check_screenshot_palette.py --zone ruined_village --screenshot ...` — PASS
- [ ] `L2_visual_jury` — PASS (2-of-3 when keys set)
- [ ] `L2_visual_palette` — PASS
- [ ] Golden master committed: `artifacts/golden/ruined_village_gameplay.png`
- [ ] No `BoxMesh` / greybox in player camera frustum
- [ ] GDAI `.gdai_built` marker with `verified_f5=true`

---

## Vertical slice minimum (ship Phase 1)

Build **in this order** (per `CHARACTER_BIBLE.md` §11 + `ENVIRONMENT_KITS.md` §4):

1. Ground + main path + fog/sky/lighting preset
2. `village_well_stone` + `VillageWell` marker
3. `village_torii_damaged` + `village_shrine_pad` + `ToriiShrine`
4. `village_shack_roku` + `RokuShack`
5. Urashima placed — walk cycle + interact at well
6. Gameplay + establishing screenshots → visual jury

Defer to M5: full modular kit scatter, banner/sandal inspect props, pier combat arena polish, cave entrance cliff dressing.

---

## Forbidden

- Kenney / European medieval kits
- Sunny gold sky or PhysicalSky HDRI
- Pure white point lights
- Hand-edited `.tscn` without GDAI MCP (R&R policy)
- Ship without golden screenshot when `VISUAL_SMOKE_STRICT=1`
