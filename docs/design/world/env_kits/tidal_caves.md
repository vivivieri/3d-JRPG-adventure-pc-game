---
id: tidal-caves
type: reference
audience: [builder, builder_zone, visual]
phase: [1, 5]
status: active
authority: world
tokens_est: 537
summary: "Wonder + wrongness; bioluminescent guilt"
---
# Environment Kits — Zone tidal_caves

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

## When to read

Use **Environment Kits — Zone tidal_caves** (roles: builder, builder_zone, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [5. Zone: Tidal Caves (`tidal_caves`)](#5-zone-tidal-caves-tidal_caves)
- [Modular kit](#modular-kit)
- [Hero set-pieces](#hero-set-pieces)
- [Water puzzle (SC-07)](#water-puzzle-sc-07)
- [Lighting](#lighting)


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
