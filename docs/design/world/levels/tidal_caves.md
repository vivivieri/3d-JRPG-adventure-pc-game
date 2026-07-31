---
id: tidal-caves
type: reference
audience: [builder, builder_zone, architect]
phase: [1, 5]
status: active
authority: world
tokens_est: 720
summary: "Level Design — Zone tidal_caves — covers 4. Zone: `tidal_caves` (SC-06–11); Blockout; Layout; Interactables & triggers"
---
# Level Design — Zone tidal_caves

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## When to read

Use **Level Design — Zone tidal_caves** (roles: builder, builder_zone, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [4. Zone: `tidal_caves` (SC-06–11)](#4-zone-tidal_caves-sc-0611)
- [Blockout](#blockout)
- [Layout](#layout)
- [Interactables & triggers](#interactables-triggers)
- [Encounters](#encounters)
- [Puzzle SC-07](#puzzle-sc-07)


## 4. Zone: `tidal_caves` (SC-06–11)

**Scene:** `res://scenes/world/tidal_caves.tscn`
**Act:** II · **BGM:** `bgm_caves` · **Fog:** distance fog per `RENDERING_GUIDE.md` §6 (density 0.028); **no volumetric fog** (interior)

### Blockout

| Metric | Target |
|--------|--------|
| Structure | Linear main path + one optional chest branch |
| Puzzle room | SC-07 flooded chamber ~40m × 30m |
| Boss arena | SC-09 circular ~25m diameter |

### Layout

```
[Entrance SC-06]
      ↓
[Flooded chamber SC-07] ← PUZZLE_DESIGN.md
      ↓ (requires water_puzzle_solved)
[Deep pool SC-08] + vignette hook
      ↓
[Boss arena SC-09 Shore Wraith]
      ↓
[Shrine alcove SC-10 Yuzu join]
      ↓
[Flashback wall SC-11]
      ↓
[Exit → dragon_palace_gate SC-12]
```

### Interactables & triggers

| Node | Scene ID / hook | Sets flag | Requirement |
|------|-----------------|-----------|-------------|
| `EncounterTrigger_enc_sc06_cave_crab` | SC-06 | — | Optional trash mob |
| `PuzzleRoom_sc07` | SC-07 | `water_puzzle_solved` | Silent — no dialogue |
| `EncounterTrigger_enc_sc07_optional_crabs` | SC-07 | — | Optional trash mob (puzzle zone) |
| `EncounterTrigger_enc_sc08_deep_pool` | SC-08 | `deep_pool_seen` | `water_puzzle_solved`, `deep_pool_dialogue_done` (vignette → dialogue → combat) |
| `CinematicTrigger_sc08_deep_pool_vignette` | hook | `deep_pool_vignette_seen` | After pool enter |
| `EncounterTrigger_enc_sc09_shore_wraith` | SC-09 | `shore_wraith_defeated` | Boss |
| `Interactable_SC-10` | SC-10 | `yuzu_joined` | Post-boss |
| `EncounterTrigger_enc_sc10_optional_wraith` | SC-10 | — | Optional trash mob; requires `yuzu_joined` |
| `CinematicTrigger_sc11_palace_flashback` | hook `sc11_palace_flashback` | `saw_palace_vision` (dialogue) | Letterbox flashback; requires `yuzu_joined` |
| `ZoneTransition_dragon_palace_gate` | SC-12 | `gate_reached` | `yuzu_joined`, `wraith_pearl` |

### Encounters

| ID | Scene | Type |
|----|-------|------|
| `enc_sc06_cave_crab` | SC-06 | Trash |
| `enc_sc07_optional_crabs` | SC-07 | Optional trash (puzzle zone) |
| `enc_sc08_deep_pool` | SC-08 | Mob |
| `enc_sc09_shore_wraith` | SC-09 | Boss |
| `enc_sc10_optional_wraith` | SC-10 | Optional trash |

### Puzzle SC-07

Full spec: [PUZZLE_DESIGN.md](../PUZZLE_DESIGN.md). Water plane Y toggles LOW/HIGH; latch reachable only HIGH.

---
