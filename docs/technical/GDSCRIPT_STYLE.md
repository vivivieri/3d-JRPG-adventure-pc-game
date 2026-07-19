# GDScript 2.0 Style Guide — Tides of Urashima

**Version:** 1.0  
**Scope:** `game/scripts/**/*.gd`, `game/tests/**/*.gd`, editor tools on `game/development`  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)  
**Engine:** Godot **4.7** · Forward+

---

## 1. Industry standards (authoritative externals)

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **GDScript style** | [Godot GDScript style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html) | Naming, layout, order of declarations |
| **Static typing** | [Godot static typing](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html) | Types on vars, params, returns |
| **Signals** | [Godot signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) | Typed signals, `.connect()` |
| **Lint** | [gdtoolkit / gdlint](https://github.com/Scony/godot-gdscript-toolkit) | CI `L1_gdscript_lint` on changed files |
| **Shaders** | [Godot shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/index.html) | `.gdshader` in `game/shaders/` |

**Project architecture:** scene tree + autoload singletons — **not** ECS. See [`TECHNICAL_DESIGN.md`](TECHNICAL_DESIGN.md).

---

## 2. File & folder layout

```
game/scripts/
  core/           GameManager, SaveSystem, EventBus, boot
  audio/          AudioManager, VoiceLinePlayer
  narrative/      DialogueRunner, QuestTracker
  combat/         CombatManager, TurnManager, SkillResolver, Combatant
  exploration/    PlayerController, Interactable, ZoneTransition, EncounterTrigger
  story/          CinematicDirector, StoryData helpers
  ui/             Menu controllers, HUD glue

game/scenes/      .tscn — built via GDAI MCP, not hand-edited in Cursor
game/shaders/     .gdshader — toon family only
game/data/        JSON — never hardcode story content in .gd
game/tests/unit/  Headless unit tests
```

**Rule:** Gameplay **content** (dialogue, stats, flags) lives in `game/data/*.json`. `.gd` files implement **engines**.

---

## 3. Naming (Godot style guide + project)

| Kind | Convention | Example |
|------|------------|---------|
| Files | `snake_case.gd` | `combat_manager.gd` |
| `class_name` | `PascalCase` | `class_name CombatManager` |
| Autoload | `PascalCase` | `GameManager` |
| Functions / variables | `snake_case` | `get_flag()`, `_flags` |
| Signals | `snake_case` past tense or noun | `flag_changed`, `combat_ended` |
| Private | `_leading_underscore` | `_load_hooks()` |
| Constants | `UPPER_SNAKE` or grouped `const` block | `HOOKS_PATH` |
| Enums | `PascalCase` type, `UPPER_SNAKE` members | `enum State { IDLE, WALK }` |
| `@export` vars | `snake_case` | `@export var scene_id: String` |
| Scene files | `snake_case.tscn` | `ruined_village.tscn` |

---

## 4. Script structure (declaration order)

Follow [Godot style guide — script structure](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html#code-order):

```gdscript
class_name Interactable
extends Area3D
## Base interactable — inspectables, NPC hooks (LEVEL_DESIGN.md §1b).

signal interacted(player: PlayerController)

enum PromptMode { AUTO, HIDDEN }

const PROMPT_OFFSET := Vector3(0, 1.2, 0)

@export var scene_id: String = ""
@export var interaction_prompt: String = "Interact"

var _cooldown: float = 0.0

@onready var _prompt: Label3D = $PromptLabel


func _ready() -> void:
    body_entered.connect(_on_body_entered)


func interact(player: PlayerController) -> void:
    if not can_interact():
        return
    interacted.emit(player)


func can_interact() -> bool:
    return _cooldown <= 0.0


func _on_body_entered(body: Node3D) -> void:
    if body is PlayerController:
        pass
```

| Section | Contents |
|---------|----------|
| 1 | `class_name` (optional) |
| 2 | `extends` |
| 3 | `##` class docstring |
| 4 | `signal` declarations |
| 5 | `enum` |
| 6 | `const` |
| 7 | `@export` |
| 8 | Member `var` |
| 9 | `@onready var` |
| 10 | `@onready` `%UniqueNode` if used |
| 11 | `_init`, `_ready`, `_process`, … |
| 12 | Public methods |
| 13 | Private `_methods` |

---

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

Authority: [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md) · CI: `L0_base_class_compliance`.

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

## 9. Data access

```gdscript
# Load once, cache on manager
var _skills: Dictionary = GameManager.load_json("res://data/skills/skills.json")

# Story filter — data-driven
var lines: Array = StoryData.filter_dialogue_lines(
    chapter["lines"],
    GameManager.get_all_flags()
)
```

**Never** embed dialogue strings, skill numbers, or flag names as magic literals without a JSON source — except dev-only debug guarded by `OS.is_debug_build()`.

---

## 10. Signals & EventBus

### Same feature area — direct connect

```gdscript
func _ready() -> void:
    combat_ui.skill_selected.connect(_on_skill_selected)
```

### Cross-system — EventBus autoload

```gdscript
# event_bus.gd
signal flag_changed(flag_name: String, value: Variant)
signal combat_ended(victory: bool)

# game_manager.gd
func set_flag(name: String, value: Variant = true) -> void:
    _flags[name] = value
    EventBus.flag_changed.emit(name, value)
```

Disconnect when nodes are freed if connections span scenes (`Callable` + `is_connected` checks).

---

## 11. Shaders (`.gdshader`)

One **toon ramp family** project-wide. See [`CODE_STYLE.md`](CODE_STYLE.md) §8 · [`RENDERING_GUIDE.md`](../art/RENDERING_GUIDE.md).

```gdshader
shader_type spatial;
render_mode diffuse_toon, specular_toon;

uniform vec4 base_color : source_color;
uniform sampler2D albedo_texture : source_color, filter_linear_mipmap;

void fragment() {
    vec4 tex = texture(albedo_texture, UV);
    ALBEDO = tex.rgb * base_color.rgb;
    ROUGHNESS = 1.0;
    METALLIC = 0.0;
}
```

| Rule | Detail |
|------|--------|
| File naming | `snake_case.gdshader` |
| Zone variants | Duplicate material + uniform tweaks |
| Water only | `water_stylized.gdshader` on water meshes |
| No full PBR | Avoid `StandardMaterial3D` in ship scenes |

---

## 12. Error handling

| Situation | Pattern |
|-----------|---------|
| Missing JSON at boot | `push_error()` + return; fail loud in dev |
| Missing asset (ship) | Assert + `check_asset_compliance.sh` |
| Unknown flag | Return default `false` |
| After `await` | `is_instance_valid(self)` / `is_instance_valid(node)` |

Keep handling minimal — linear single-player game, not a live service.

---

## 13. Comments & documentation

```gdscript
## Applies zone palette from zone_palettes.json (RENDERING_GUIDE.md §13).
func apply_zone(zone_id: String) -> void:
    # SC-07 silent puzzle — no dialogue block by design (PUZZLE_DESIGN.md)
    ...
```

- Prefer **self-documenting names** over comments for obvious logic
- Use `##` doc comments above classes and public methods (shows in editor help)
- Comment **why** for boss phases, audio duck exceptions, flag timing

---

## 14. Lint & tests (CI)

```bash
bash tools/check_gdscript_changed.sh   # gdlint on changed .gd — L1_gdscript_lint
bash tools/run_unit_tests.sh           # L1_unit_tests
bash tools/check_base_class_compliance.sh
```

### gdlint (gdtoolkit)

Install: `bash tools/install_ci_deps.sh` or `pip install gdtoolkit`

Common gdlint rules aligned with [Godot style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html):

| Rule area | Expectation |
|-----------|-------------|
| Line length | 100 chars (gdlint default configurable) |
| Trailing whitespace | None |
| Mixed tabs/spaces | Spaces only (4 per indent) |
| Unused arguments | Prefix with `_` — `_delta` |
| Class name vs file | `class_name` matches file purpose |

---

## 15. Scene authoring (R&R)

| Rule | Detail |
|------|--------|
| `.tscn` mutations | **GDAI MCP only** when stack is up |
| Component scenes | Catalog in `LEVEL_DESIGN.md` §1b |
| Groups | `player`, `interactable`, `encounter_trigger` |
| No ship placeholders | Replace `BoxMesh` greybox before M5 sign-off |

---

## 16. Anti-patterns

| Don't | Why |
|-------|-----|
| `yield()` | Removed in Godot 4 — use `await` |
| String signal connections | Untyped, breaks refactor |
| `_process` polling for flags | Use signals / EventBus |
| New `CharacterBody3D` player | Violates base class policy |
| Hardcoded story text in `.gd` | Belongs in `game/data/` |
| `get_node("../..")` fragile paths | `@export` NodePaths or `%UniqueName` |
| Heavy logic in `.tscn` embedded scripts | Move to named `.gd` file |

---

## 17. PR checklist (GDScript)

- [ ] Extends registered base class (`base_classes.json`)
- [ ] Typed GDScript; no `yield()` or string connects
- [ ] No hardcoded story numbers or dialogue
- [ ] `bash tools/check_gdscript_changed.sh` — gdlint clean
- [ ] `bash tools/run_unit_tests.sh` if logic changed
- [ ] `bash tools/check_base_class_compliance.sh`
- [ ] `.tscn` via GDAI MCP (not hand-edited)
- [ ] `python3 tools/validate_story_data.py` if flags/data references changed

---

## 18. Quick reference links

- [Godot GDScript style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html)
- [Godot static typing](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html)
- [gdtoolkit / gdlint](https://github.com/Scony/godot-gdscript-toolkit)
- Project: [`CODE_STYLE.md`](CODE_STYLE.md) · [`TECHNICAL_DESIGN.md`](TECHNICAL_DESIGN.md) · [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md)
