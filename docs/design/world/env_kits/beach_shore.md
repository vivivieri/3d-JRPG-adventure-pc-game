---
id: beach-shore
type: reference
audience: [builder, builder_zone, visual]
phase: [1]
status: active
authority: world
tokens_est: 350
summary: "Zone beach_shore"
---
# Environment Kits — Zone beach_shore

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

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
