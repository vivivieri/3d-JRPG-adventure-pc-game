---
id: beach-shore
type: reference
audience: [builder, builder_zone, architect]
phase: [1]
status: active
authority: world
tokens_est: 406
summary: "Level Design — Zone beach_shore — Scene: `res://scenes/world/beach_shore.tscn"
---
# Level Design — Zone beach_shore

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## When to read

Use **Level Design — Zone beach_shore** (roles: builder, builder_zone, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [2. Zone: `beach_shore` (SC-01)](#2-zone-beach_shore-sc-01)
- [Blockout](#blockout)
- [Layout (top-down)](#layout-top-down)
- [Interactables & triggers](#interactables-triggers)
- [Encounters](#encounters)
- [Camera](#camera)


## 2. Zone: `beach_shore` (SC-01)

**Scene:** `res://scenes/world/beach_shore.tscn`
**Act:** I · **BGM:** `bgm_village` · **Fog:** light coastal

### Blockout

| Metric | Target |
|--------|--------|
| Playable area | ~80m × 40m strip |
| Path | Linear shore → village gate visible ahead |
| Duration | 2–4 min first visit |

### Layout (top-down)

```
[Ocean]  ~~~~~  [Driftwood scatter]
                    |
              [Player spawn SC-01]
                    |
              [Path to gate]
                    |
         [ZoneTransition → ruined_village]
```

### Interactables & triggers

| Node | Scene ID | Sets flag | Notes |
|------|----------|-----------|-------|
| `SpawnMarker_SC-01` | — | — | New game / prologue exit spawn (`starting/new_game.json`) |
| `ZoneTransition_ruined_village` | — | `tutorial_movement_done` | After SC-01 dialogue |
| `Interactable_SC-01` | SC-01 | `tutorial_movement_done`, `game_started` | Optional auto on enter |

### Encounters

None.

### Camera

Wide establishing → follow cam (`CINEMATICS.md` SC-01). No authored pan v1.

---
