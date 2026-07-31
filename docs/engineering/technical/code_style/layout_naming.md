---
id: layout-naming
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 602
summary: "Code Style — Folder layout + naming — core/           GameManager, SaveSystem, EventBus, LocalizationManager, boot"
---
# Code Style — Folder layout + naming

**Hub:** [`CODE_STYLE.md`](../CODE_STYLE.md)

## When to read

Use **Code Style — Folder layout + naming** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Folder layout](#1-folder-layout)
- [2. Naming conventions](#2-naming-conventions)


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
