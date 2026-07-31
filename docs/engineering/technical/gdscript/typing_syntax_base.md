---
id: typing-syntax-base
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 779
summary: "Typing, Godot 4 syntax, base classes, autoload"
---
# GDScript Style — Typing, Godot 4 syntax, base classes, autoload

**Hub:** [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md)

## 5. Static typing (required profile)

Use typed GDScript **everywhere in new code** and when touching a file that already uses types.

```gdscript
func get_flag(name: String) -> Variant:
    return _flags.get(name, false)


func load_encounter(encounter_id: String) -> Dictionary:
    var enc: Dictionary = _encounters.get(encounter_id, {})
    return enc


func filter_party(ids: Array[String]) -> Array[String]:
    var out: Array[String] = []
    for id in ids:
        out.append(id)
    return out
```

| Use | Avoid |
|-----|-------|
| `-> void` on procedures | Untyped `func foo():` in new files |
| `Array[String]`, `Dictionary` | Bare `Array` when element type is known |
| Typed signal args `signal x(id: String)` | String-based `connect("sig", ...)` |
| `is` / `as` for nodes | Unchecked casts |

---


## 6. Godot 4 syntax (strict — CI + `.cursorrules`)

```gdscript
# Signals — typed connect only
some_signal.connect(_on_some_signal)

# Coroutines — never yield()
await get_tree().create_timer(1.0).timeout
await object.signal_name

# 3D — use node properties directly
player.velocity = direction * speed
player.global_position = spawn.global_position

# Validity after await
await dialogue_runner.line_finished
if not is_instance_valid(self):
    return
```

| Do | Don't |
|----|-------|
| `signal_name.connect(_callback)` | `connect("signal", self, "method")` |
| `GameManager.load_json(path)` | Copy-paste JSON parse in every system |
| Extend `PlayerController` / `Combatant` / `Interactable` | New `CharacterBody3D` movement stack |
| `push_error()` + early return for missing data | Silent failure in boot path |
| `EventBus` for cross-system events | Poll `GameManager` flags every frame |

---


## 7. Base classes (extend-only)

All gameplay controllers **extend** registered bases in `game/data/code/base_classes.json`.

| Class | Extends | Owner |
|-------|---------|-------|
| `PlayerController` | `CharacterBody3D` | Architect |
| `Combatant` | `Node` | Architect |
| `Interactable` | `Area3D` | Architect |
| `ZoneTransition` | `Area3D` | Architect |
| `EncounterTrigger` | `Area3D` | Architect |

**Builder** instances component `.tscn` scenes — does not add new gameplay scripts on zone roots.

Authority: [`CODE_BASE_CLASS_RULES.md`](../CODE_BASE_CLASS_RULES.md) · CI: `L0_base_class_compliance`.

---


## 8. Autoload vs scene-local

| Autoload | Scene-local |
|----------|-------------|
| `GameManager`, `EventBus`, `SaveSystem` | Zone meshes, triggers, spawn markers |
| `AudioManager`, `DialogueRunner` | Combat HUD bound to one battle |
| `CombatManager` coordinator | `PlayerController` per zone instance |

**Do not** autoload UI scenes — instantiate under a `CanvasLayer` manager.

Registry: `game/data/code/autoload_registry.json`.

---
