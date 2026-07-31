---
id: scene-data-save
type: reference
audience: [architect, builder]
phase: [1, 2]
status: active
authority: engineering
tokens_est: 862
summary: "Scene flow, data loading, save/load"
---
# Technical Design — Scene flow, data loading, save/load

**Hub:** [`TECHNICAL_DESIGN.md`](../TECHNICAL_DESIGN.md)

## 3. Scene flow

```mermaid
stateDiagram-v2
    [*] --> Boot
    Boot --> MainMenu
    MainMenu --> Prologue: New Game
    MainMenu --> Field: Continue
    Prologue --> BeachShore: SC-00 done
    BeachShore --> RuinedVillage
    RuinedVillage --> TidalCaves: cave_entrance_unlocked
    TidalCaves --> PalaceGate: wraith_pearl + yuzu_joined (SC-10); SC-11 flashback optional before SC-12
    PalaceGate --> EndingZone: SC-16 choice
    EndingZone --> Credits
    Credits --> MainMenu
```

| Transition | Owner | Mechanism |
|--------------|-------|-----------|
| Boot → menu | `boot_scene.gd` | Scene change after data OK |
| Menu → game | `GameManager` | New Game loads `beach_shore.tscn` + SC-00 hook |
| Zone → zone | `ZoneTransition` Area3D | `GameManager.change_zone(zone_id, spawn_marker)` |
| Field → combat | `EncounterTrigger` | `CombatManager.start_encounter(encounter_id)` |
| Combat → field | `CombatManager` | Victory/defeat signal → restore field scene state |
| Field → dialogue | `Interactable` | `DialogueRunner.start(scene_id)` |
| Cinematic | `CinematicDirector` | `play_hook(hook_id)` → camera markers → `then` steps |

**Scene paths (canonical):** see `game/data/code/scene_registry.json` + `docs/design/world/LEVEL_DESIGN.md`.

---


## 4. Data loading

### API (Phase 2)

```gdscript
# GameManager — single entry for JSON
static func load_json(path: String) -> Variant:
    # Delegates to StoryData.load_json today; merge into GameManager
    ...

func get_flag(name: String) -> Variant:
    return _flags.get(name, false)

func set_flag(name: String, value: Variant) -> void:
    _flags[name] = value
    EventBus.flag_changed.emit(name, value)
```

### Load order at New Game

1. `starting/new_game.json` — party, inventory, default flags
2. `story/scenes.json` — validate spine (dev/QA)
3. `story/flags.json` — registry (validation only at runtime)
4. Zone scene + `ZoneVisuals.apply(zone_id)`

### Content resolution

| Player action | Lookup |
|---------------|--------|
| Talk to NPC | `dialogue/chapter_01.json` key = `scene_id` |
| Start fight | `encounters/story_encounters.json` by `encounter_id` |
| Use skill | `skills/skills.json` by `skill_id` |
| Shop buy | `shop/roku_shop.json` |
| Quest update | `quests/main_quests.json` stages vs `GameManager` flags |

**Validation:** `python3 tools/validate_story_data.py` before every commit touching `game/data/`.

---


## 5. Save / load pipeline

```
[Gameplay mutation]
    → GameManager flags / party / inventory
    → SaveSystem.mark_dirty()
    → (autosave trigger: zone transition | quest stage | manual well)
    → SaveSystem.write_slot(0)
    → user://save_slot_0.json
```

| Event | Autosave? |
|-------|-----------|
| Zone transition | Yes |
| Quest stage complete | Yes |
| Manual well | Yes + full heal (first visit) |
| Mid-combat | **No** |
| Before boss (SC-09, SC-14, SC-15) | Yes (pre-fight) |

**Continue:** `SaveSystem.read_slot(0)` → restore scene path + `spawn_marker` + all persisted fields (`SAVE_AND_FAIL_STATES.md` §2).

**Steam cloud (Phase 8):** Same JSON blob via GodotSteam `fileWrite` — path abstraction in `SaveSystem` only.

---
