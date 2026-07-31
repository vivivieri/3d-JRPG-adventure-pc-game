---
id: naming
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 414
summary: "Gameplay **content** lives in JSON; `.gd` implements engines, not story text."
---
# Coding Standards Hub — Naming conventions

**Hub:** [`CODING_STANDARDS_HUB.md`](../CODING_STANDARDS_HUB.md)

## When to read

Use **Coding Standards Hub — Naming conventions** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



## 2. Naming conventions (all languages)

| Thing | Convention | Example |
|-------|------------|---------|
| GDScript files | `snake_case.gd` | `combat_manager.gd` |
| GDScript classes (`class_name`) | `PascalCase` | `class_name CombatManager` |
| Autoload singletons | `PascalCase` | `GameManager` |
| Signals | `snake_case` (past tense or noun) | `flag_changed`, `combat_ended` |
| Private members | `_leading_underscore` | `_flags`, `_load_hooks()` |
| Constants | `UPPER_SNAKE` | `HOOKS_PATH` |
| Scene files | `snake_case.tscn` | `ruined_village.tscn` |
| Shader files | `snake_case.gdshader` | `toon_base.gdshader` |
| JSON field keys | `snake_case` | `set_flags`, `requires_flags` |
| Story scene IDs | `SC-NN` or `SC-NN-NAME` | `SC-02-WELL` |
| Zone IDs | `snake_case` | `ruined_village`, `tidal_caves` |
| Flag / item / enemy IDs | `snake_case` | `shore_wraith_defeated`, `sea_salve` |
| Encounter IDs | `enc_<zone>_<name>` | `enc_sc09_shore_wraith` |
| Audio files | `snake_case.ogg` | `bgm_village.ogg`, `sc03_yuzu_01.ogg` |
| Python modules | `snake_case.py` | `validate_story_data.py` |
| Python functions | `snake_case` | `load_catalog()`, `run_gate()` |
| Shell scripts | `snake_case.sh` | `run_docs_ci_checks.sh` |

**Rule:** Gameplay **content** lives in JSON; `.gd` implements engines, not story text.

---
