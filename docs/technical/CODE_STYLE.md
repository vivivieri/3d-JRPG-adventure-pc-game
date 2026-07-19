# Tides of Urashima — Code Style Guide

**Version:** 1.1  
**Language:** GDScript 2.0 (Godot 4.7)  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md) · **Deep dive:** [`GDSCRIPT_STYLE.md`](GDSCRIPT_STYLE.md)  
**Architecture:** Scene-tree + autoload singletons — **not** Entity-Component-System  
**Cross-refs:** [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md), [CODE_BASE_CLASS_RULES.md](CODE_BASE_CLASS_RULES.md), [`.cursorrules`](../.cursorrules) §5, [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md)

---

## 1. Folder layout

```
game/scripts/
  core/           GameManager, SaveSystem, EventBus, LocalizationManager, boot
  audio/          AudioManager, VoiceLinePlayer (or story/ until split)
  narrative/      DialogueRunner, QuestTracker
  combat/         CombatManager, TurnManager, SkillResolver, Combatant
  player/         PlayerController, OrbitCamera
  world/          ZoneVisuals, Interactable, ZoneTransition, EncounterTrigger
  story/          CinematicDirector, StoryData (helpers), VoiceLinePlayer
  ui/             Menu controllers, HUD glue scripts

game/scenes/
  boot.tscn
  ui/             Menus, dialogue, combat HUD
  world/          One .tscn per zone_id
  combat/         combat_instance.tscn + shared sub-scenes

game/shaders/     .gdshader — toon family only
game/environments/ .tres WorldEnvironment presets per zone
game/data/        JSON — never hardcode story content in .gd
```

**Rule:** Gameplay content in JSON; `.gd` files implement engines, not story text.

---

## 2. Naming conventions

| Thing | Convention | Example |
|-------|------------|---------|
| GDScript files | `snake_case.gd` | `combat_manager.gd` |
| Classes (`class_name`) | `PascalCase` | `class_name CombatManager` |
| Autoload name | `PascalCase` | `GameManager` |
| Signals | `snake_case` past tense or noun | `flag_changed`, `combat_ended` |
| Private members | `_leading_underscore` | `_flags`, `_load_hooks()` |
| Constants | `UPPER_SNAKE` or `const` PascalCase paths | `HOOKS_PATH` |
| Scene files | `snake_case.tscn` | `ruined_village.tscn` |
| Node names (authored) | `PascalCase` or `snake_case` — **match zone docs** | `VillageWell`, `CaveEntrance` |
| JSON IDs | `snake_case` | `shore_wraith_defeated`, `enc_sc09_shore_wraith` |
| Scene IDs (story) | `SC-NN` or `SC-NN-NAME` | `SC-02-WELL` |
| Zone IDs | `snake_case` | `ruined_village`, `dragon_palace_gate` |
| Shaders | `snake_case.gdshader` | `toon_base.gdshader` |
| Audio files | `snake_case.ogg` | `bgm_village.ogg`, `sc03_yuzu_01.ogg` |

---

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

See `docs/technical/CODE_BASE_CLASS_RULES.md`. CI enforces via `L0_base_class_compliance`.

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

## 6. Data access patterns

```gdscript
# Load once, cache on manager
var _skills: Dictionary = GameManager.load_json("res://data/skills/skills.json")

# Story line filter
var lines: Array = StoryData.filter_dialogue_lines(
    chapter["lines"],
    GameManager.get_all_flags()
)

# Encounter by id
var enc: Dictionary = _encounters["encounters"][encounter_id]
```

**Never** embed dialogue strings or skill numbers in `.gd` except dev-only debug.

---

## 7. Scene authoring rules

| Rule | Detail |
|------|--------|
| **GDAI MCP builds `.tscn`** | No hand-editing scene trees in Cursor when GDAI is up |
| **Component scenes** | Use catalog from `LEVEL_DESIGN.md` §1b — wells, doors, triggers |
| **Groups** | `player`, `interactable`, `encounter_trigger` for queries |
| **Markers** | `SpawnMarker_default`, `CameraMarker_sc12_wide` — match `LEVEL_DESIGN.md` |
| **Layers** | Collision layers documented per zone in level design |
| **No primitives in ship** | `BoxMesh` greybox OK until M5; replace with kit meshes |

---

## 8. Shader conventions

- One **toon ramp family** project-wide (`toon_base.gdshader`)
- Zone variants = duplicate material + uniform tweaks, not separate shader languages
- Water: `water_stylized.gdshader` only on water meshes
- Emission for interactables, box, biolume — see `RENDERING_GUIDE.md`

```gdshader
shader_type spatial;
render_mode diffuse_toon, specular_toon;
# uniforms: base_color, albedo_texture, emission_strength
```

---

## 9. Error handling

| Situation | Pattern |
|-----------|---------|
| Missing JSON | `push_error()` + return early; boot fails loud in dev |
| Missing asset | Fallback only for dev placeholders; ship = assert + compliance script |
| Invalid flag access | Return default `false`; log once in debug builds |

Keep error handling minimal — this is a linear game, not a live service.

---

## 10. Comments

- **Self-documenting names** over comments for obvious logic
- Comment **why** for: flag timing, boss phase transitions, audio duck exceptions (SC-16)
- Link to doc sections for complex design: `# SC-07 silent — PUZZLE_DESIGN.md`

---

## 11. Tests

| Location | Style |
|----------|-------|
| `game/tests/unit/` | Extend `test_runner.gd`; no engine restart per assert |
| Python validators | `tools/validate_story_data.py`, `validate_base_classes.py` for data integrity |
| GDScript lint | `tools/check_gdscript_changed.sh` on changed `.gd` (L1 gate) |
| MCP Pro | Scenario names match `AI_TESTING_SPEC.md` |

---

## 12. Copyright & assets

- No web imports without `register_asset.py` + `LICENSES.md`
- Procedural generators OK for dev; ship assets per `ASSET_COMPLIANCE.md`

---

## 13. Quick checklist (PR / commit)

- [ ] Typed GDScript matches surrounding file
- [ ] No string-based signal connections
- [ ] Story changes have `validate_story_data.py` pass
- [ ] New flags in `flags.json` + `scenes.json` setter
- [ ] New JSON IDs snake_case
- [ ] `.tscn` changes via GDAI MCP when available
