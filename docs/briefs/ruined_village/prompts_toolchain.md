---
id: prompts-toolchain
type: reference
audience: [visual, builder]
phase: [1]
status: active
authority: briefs
tokens_est: 633
summary: "Toolchain + prompts"
---
# ruined_village brief — Toolchain + prompts

**Hub:** [`ruined_village.md`](../ruined_village.md)

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
