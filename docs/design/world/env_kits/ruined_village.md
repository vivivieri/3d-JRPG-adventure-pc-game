---
id: ruined-village
type: reference
audience: [builder, builder_zone, visual]
phase: [1]
status: active
authority: world
tokens_est: 737
summary: "Zone ruined_village hub"
---
# Environment Kits — Zone ruined_village hub

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

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
