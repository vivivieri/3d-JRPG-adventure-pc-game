---
id: gdscript-autoload-signals
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 711
summary: "GDScript, autoload, signals"
---
# Code Style — GDScript, autoload, signals

**Hub:** [`CODE_STYLE.md`](../CODE_STYLE.md)

## 3. GDScript rules (strict)

From `.cursorrules` — **always enforce:**

```gdscript
# Signals — typed connect, never strings
some_signal.connect(_on_some_signal)

# Coroutines
await object.signal_name
# never yield()

# 3D nodes
player.velocity = ...
player.global_position = ...

# Typed GDScript where file already uses types
func get_flag(name: String) -> Variant:
    return _flags.get(name, false)
```

| Do | Don't |
|----|-------|
| `signal_name.connect(_callback)` | `connect("signal", self, "method")` |
| `await get_tree().create_timer(1.0).timeout` | `yield()` |
| `GameManager.load_json(path)` | Duplicate JSON parse in every system |
| `is_instance_valid(node)` before await resume | Hold dangling node refs |
| Extend `PlayerController` / `Combatant` / `Interactable` | New `CharacterBody3D` controller from scratch |

### 3.1 Base classes (extend-only)

All gameplay controllers and interactables **extend** scripts listed in `game/data/code/base_classes.json`. Architect owns the base `.gd` files; Builder composes component `.tscn` scenes.

See `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`. CI enforces via `L0_base_class_compliance`.

### 3.2 GDScript lint (CI)

Changed `.gd` files must pass `gdlint` (gdtoolkit):

```bash
bash tools/check_gdscript_changed.sh   # L1_gdscript_lint
bash tools/install_ci_deps.sh          # installs gdtoolkit
```

---


## 4. Autoload vs scene-local

| Use autoload when | Use scene-local when |
|-------------------|----------------------|
| State survives scene changes (flags, save) | Zone geometry, triggers, spawn markers |
| Multiple systems need same API (audio, locale) | Combat instance UI bound to one battle |
| Single global coordinator (`CombatManager`) | `PlayerController` instanced per zone |

**Do not** autoload UI scenes — instantiate `dialogue_box.tscn` under a `CanvasLayer` manager or use autoload script only.

---


## 5. Signals & EventBus

### Direct connections
Use when producer and consumer are in the same feature area (e.g. `CombatUI` ↔ `CombatManager`).

### EventBus (`scripts/core/event_bus.gd`)
Use for cross-cutting notifications:

```gdscript
# EventBus (declared signals — add as needed Phase 2+)
signal flag_changed(flag_name: String, value: Variant)
signal locale_changed(locale: String)
signal zone_entered(zone_id: String)
signal combat_started(encounter_id: String)
signal combat_ended(victory: bool)
```

**Rule:** `GameManager.set_flag()` emits `EventBus.flag_changed` — quest tracker and achievements listen, don't poll flags every frame.

---
