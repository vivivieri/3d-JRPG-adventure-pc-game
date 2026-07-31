---
id: standards-layout
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 878
summary: "Project architecture: scene tree + autoload singletons — not ECS. See `TECHNICAL_DESIGN.md`."
---
# GDScript Style — Standards, layout, naming, structure

**Hub:** [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md)

## When to read

Use **GDScript Style — Standards, layout, naming, structure** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. Industry standards (authoritative externals)](#1-industry-standards-authoritative-externals)
- [2. File & folder layout](#2-file-folder-layout)
- [3. Naming (Godot style guide + project)](#3-naming-godot-style-guide-project)
- [4. Script structure (declaration order)](#4-script-structure-declaration-order)


## 1. Industry standards (authoritative externals)

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **GDScript style** | [Godot GDScript style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html) | Naming, layout, order of declarations |
| **Static typing** | [Godot static typing](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html) | Types on vars, params, returns |
| **Signals** | [Godot signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) | Typed signals, `.connect()` |
| **Lint** | [gdtoolkit / gdlint](https://github.com/Scony/godot-gdscript-toolkit) | CI `L1_gdscript_lint` on changed files |
| **Shaders** | [Godot shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/index.html) | `.gdshader` in `game/shaders/` |

**Project architecture:** scene tree + autoload singletons — **not** ECS. See [`TECHNICAL_DESIGN.md`](../TECHNICAL_DESIGN.md).

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
