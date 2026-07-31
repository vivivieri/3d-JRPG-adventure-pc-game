---
id: global-rules
type: reference
audience: [builder, builder_zone, architect]
phase: [1]
status: active
authority: world
tokens_est: 529
summary: "Global level rules"
---
# Level Design — Global level rules

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## 1. Global level rules

| Rule | Value |
|------|-------|
| World structure | Linear hub + dungeon + palace — **no world map screen** |
| Backtracking | Allowed until ending choice |
| Fast travel | None v1 |
| Lost time target | Player not lost >2 min without hint (`WORLD_MAP_AND_FLOW.md` §8) |
| Save points | Village well, palace gate exterior |
| Autosave | Zone transition, quest stage, pre-boss |
| Greybox | Godot primitive meshes only, editor/dev builds Phase 1–6 — replaced by M5 art; never shipped (`.cursorrules` §0 forbids Kenney packs in player-facing builds) |

### Standard node names (all zones)

| Node type | Naming | Script |
|-----------|--------|--------|
| Player spawn | `SpawnMarker_{id}` | `Marker3D` |
| Zone exit | `ZoneTransition_{to_zone}` | `ZoneTransition.gd` |
| Inspectable | `Interactable_{id}` | `Interactable.gd` |
| NPC / dialogue | `Interactable_{scene_id}` | `Interactable.gd` |
| Combat trigger | `EncounterTrigger_{encounter_id}` | `EncounterTrigger.gd` |
| Save | `SavePoint_{name}` | `save_point.gd` (extends `Interactable`) |
| Cinematic | `CinematicTrigger_{hook_id}` | calls `CinematicDirector` |

### 1b. Reusable component scenes (GDAI Builder catalog)

**Policy:** Instance these `.tscn` components in zones — do not rebuild trigger logic per zone.
**Authority:** `game/data/code/base_classes.json` → `component_scenes` · `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`

| Component scene | Path | Script base | Phase |
|-----------------|------|-------------|-------|
| Inspectable | `res://scenes/components/interactable_inspect.tscn` | `Interactable` | 3 |
| Zone exit | `res://scenes/components/zone_transition.tscn` | `ZoneTransition` | 3 |
| Battle trigger | `res://scenes/components/encounter_trigger.tscn` | `EncounterTrigger` | 4 |
| Save point | `res://scenes/components/save_point.tscn` | `SavePoint` | 3 |
| Lantern fill | `res://scenes/components/lantern_fill.tscn` | *(light only)* | 1 |

**Builder handoff:** duplicate component into zone → set export vars (`scene_id`, `encounter_id`, `target_zone`) in GDAI inspector — no new root types.

---
