---
id: global-shared
type: reference
audience: [builder, builder_zone, visual]
phase: [1, 5]
status: active
authority: world
tokens_est: 528
summary: "Environment Kits — Global rules & shared kit — game/assets/models/environment/"
---
# Environment Kits — Global rules & shared kit

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

## When to read

Use **Environment Kits — Global rules & shared kit** (roles: builder, builder_zone, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [1. Global environment rules](#1-global-environment-rules)
- [Folder layout](#folder-layout)
- [2. Shared kit (cross-zone)](#2-shared-kit-cross-zone)


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
