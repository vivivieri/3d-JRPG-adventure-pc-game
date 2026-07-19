# Coding Standards Hub — Tides of Urashima

**Version:** 1.4  
**Purpose:** Single entry point for languages, naming, best practices, data-structure rules, and CI enforcement.  
**Authority chain:** This hub **indexes** deeper docs — when details conflict, follow the linked authority doc.

| Priority | Document | Scope |
|----------|----------|-------|
| 1 | **This hub** | Where to start; cross-language conventions |
| 2 | Per-language guides (below) | PEP 8, JSON RFC, shell style, GDScript detail |
| 3 | [`CODE_STYLE.md`](CODE_STYLE.md) | GDScript scenes, autoloads, tests |
| 4 | [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) | Story spine, save shape |
| 5 | [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md) | Extend-only architecture |
| 6 | `game/data/*.json` | **Runtime numbers win** over prose in design docs |

### Per-language deep dives

| Language | Detailed guide | External standard |
|----------|----------------|-------------------|
| **Python 3** | [**PYTHON_STYLE.md**](PYTHON_STYLE.md) | [PEP 8](https://peps.python.org/pep-0008/) · [PEP 257](https://peps.python.org/pep-0257/) · [PEP 484](https://peps.python.org/pep-0484/) |
| **JSON** | [**JSON_DATA_STYLE.md**](JSON_DATA_STYLE.md) | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) · [Google JSON Style](https://google.github.io/styleguide/jsoncstyleguide.xml) |
| **Bash** | [**BASH_STYLE.md**](BASH_STYLE.md) | [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) |
| **GDScript 2.0** | [**GDSCRIPT_STYLE.md**](GDSCRIPT_STYLE.md) | [Godot GDScript style](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html) · `gdlint` |
| **TypeScript / Node** | [**TYPESCRIPT_STYLE.md**](TYPESCRIPT_STYLE.md) | [TS Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) · [Google TS style](https://google.github.io/styleguide/tsguide.html) · MCP Pro server |
| **Markdown** | [**MARKDOWN_STYLE.md**](MARKDOWN_STYLE.md) | [CommonMark](https://spec.commonmark.org/) · Google developer docs style |
| **Shaders** | [**SHADER_STYLE.md**](SHADER_STYLE.md) | [Godot shader docs](https://docs.godotengine.org/en/stable/tutorials/shaders/index.html) |
| **Scenes** | [**SCENE_STYLE.md**](SCENE_STYLE.md) | GDAI MCP build policy · [`CODE_STYLE.md`](CODE_STYLE.md) |
| **Errors & messages** | [**ERROR_HANDLING.md**](ERROR_HANDLING.md) | Cross-language patterns · tri-state gate messages |

---

## 1. Language stack

| Language | Role | Location | Authority |
|----------|------|----------|-----------|
| **GDScript 2.0** | Game runtime — combat, narrative, UI, world | `game/scripts/` (`game/development`) | [**GDSCRIPT_STYLE.md**](GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](CODE_STYLE.md) |
| **Godot Shader** (`.gdshader`) | NPR toon, water, emissive VFX | `game/shaders/` | [**SHADER_STYLE.md**](SHADER_STYLE.md) · [`RENDERING_GUIDE.md`](../art/RENDERING_GUIDE.md) |
| **Godot Scene** (`.tscn`) | Zones, UI, components — **GDAI built** | `game/scenes/` | [**SCENE_STYLE.md**](SCENE_STYLE.md) · [`MCP_STACK.md`](../agents/MCP_STACK.md) |
| **Markdown** | Design docs, runbooks, QA policy | `docs/` | [**MARKDOWN_STYLE.md**](MARKDOWN_STYLE.md) |
| **JSON** | Story, combat, registries, QA catalogs | `game/data/` | [**JSON_DATA_STYLE.md**](JSON_DATA_STYLE.md) · [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) |
| **Python 3** | Validators, CI, procedural generators, reference libs | `tools/*.py` | [**PYTHON_STYLE.md**](PYTHON_STYLE.md) · [PEP 8](https://peps.python.org/pep-0008/) |
| **Bash** | CI runners, bootstrap, QA orchestration | `tools/*.sh` | [**BASH_STYLE.md**](BASH_STYLE.md) · [`CI.md`](../ci-cd/CI.md) |
| **HTML** | Generated stakeholder dashboards | `docs/compliance/` | [`ALIGNMENT_AUDIT.md`](../qa/ALIGNMENT_AUDIT.md) |
| **TypeScript** | Godot MCP Pro server (dev tooling — **not shipped**) | `tools/godot-mcp-pro-server/` | [**TYPESCRIPT_STYLE.md**](TYPESCRIPT_STYLE.md) |

**Not shipped in the game:** Godot MCP Pro server + addon, GDAI/Godotiq plugins, GitHub Actions YAML.

**Engine:** Godot **4.7** Forward+ · scene tree + autoload singletons — **not** ECS.

### Branch policy

| Branch | Code you write | CI |
|--------|----------------|-----|
| **`main`** | JSON data, Python validators, docs | `bash tools/run_docs_ci_checks.sh` |
| **`game/development`** | GDScript, shaders, scenes (via GDAI MCP) | `bash tools/run_ci_checks.sh` |

See [`BRANCHING.md`](../workflow/BRANCHING.md) · [`SPEC_FIRST_DEVELOPMENT.md`](SPEC_FIRST_DEVELOPMENT.md).

---

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

## 3. GDScript — industrial rules

**Full guide:** [**GDSCRIPT_STYLE.md**](GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](CODE_STYLE.md) (scenes, autoloads)  
**External:** [Godot GDScript style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html) · [Static typing](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html)

### Must enforce (Godot 4)

```gdscript
# Signals — typed connect only
some_signal.connect(_on_some_signal)

# Coroutines
await object.signal_name

# 3D nodes
player.velocity = ...
player.global_position = ...
```

| Do | Don't |
|----|-------|
| `signal_name.connect(_callback)` | `connect("signal", self, "method")` |
| `await get_tree().create_timer(1.0).timeout` | `yield()` |
| `GameManager.load_json(path)` | Duplicate JSON parse in every system |
| `is_instance_valid(node)` before await resume | Hold dangling node refs |
| Extend `PlayerController` / `Combatant` / `Interactable` | New `CharacterBody3D` controller from scratch |

### Architecture

- **Base classes:** extend only — see [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md) · `game/data/code/base_classes.json`
- **Autoloads:** register per `game/data/code/autoload_registry.json` — Builder wires via GDAI MCP
- **Signals over polling:** `EventBus` for cross-system events
- **Scenes:** GDAI MCP builds `.tscn` — no hand-editing scene trees when MCP is up

### Lint & tests

```bash
bash tools/check_gdscript_changed.sh    # gdlint (gdtoolkit) on changed .gd — L1_gdscript_lint
bash tools/run_unit_tests.sh            # L1_unit_tests
bash tools/check_base_class_compliance.sh
```

| GDScript rule | Standard |
|---------------|----------|
| `snake_case` files, functions, variables | Godot style guide |
| `PascalCase` class names | Godot style guide |
| Type hints where file already uses them | Godot 4 typed GDScript |
| `gdlint` clean on changed files | Project CI (`gdtoolkit`) |

---

## 4. Shaders

- One **toon ramp family** project-wide (`toon_base.gdshader`)
- Zone variants = material + uniform tweaks, not new shader languages
- `render_mode diffuse_toon, specular_toon` — no full PBR in player-facing scenes
- Water: `water_stylized.gdshader` only on water meshes

Spec detail: [`SHADER_SPECS.md`](../art/SHADER_SPECS.md) · [`RENDERING_GUIDE.md`](../art/RENDERING_GUIDE.md).

---

## 5. Data structures — conventions & extensions

**Detailed JSON rules:** [**JSON_DATA_STYLE.md**](JSON_DATA_STYLE.md)  
**Architecture:** [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) · file index: [`game/data/README.md`](../../game/data/README.md)

### 5.1 Story spine (gameplay content)

```
scenes.json → flags.json → quests → encounters / dialogue → items / shop
```

| Rule | Detail |
|------|--------|
| Every flag traces to a `scene_id` | Register in `story/flags.json` before use |
| Every quest stage traces to a flag | `quests/main_quests.json` |
| No orphan references | Encounter `scene_id`, drop `item_id`, skill IDs must resolve |
| i18n inline | `{ "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." }` on display strings |
| Selective VO | `voice_id` on dialogue line → `voice/{locale}/{voice_id}.ogg` |

**Load API (runtime):**

```gdscript
GameManager.load_json("res://data/story/scenes.json")
```

### 5.2 Data file categories

| Category | Path pattern | Examples | Validator |
|----------|--------------|----------|-----------|
| **Story spine** | `story/`, `dialogue/`, `quests/`, `encounters/` | `scenes.json`, `chapter_01.json` | `validate_story_data.py` |
| **Gameplay balance** | `enemies/`, `skills/`, `items/`, `combat/` | `enemies.json`, `difficulty.json` | `validate_story_data.py` |
| **Code registries** | `code/` | `base_classes.json`, `scene_registry.json` | `validate_base_classes.py`, etc. |
| **QA / factory catalogs** | `qa/` | `acceptance_criteria.json`, `sprint_board.json` | matching `validate_*.py` |
| **Audio metadata** | `audio/` | `audio_qa_catalog.json`, `scene_audio_map.json` | `validate_audio_qa_catalog.py` |
| **Art / model QA** | `models/` | `qa_catalog.json` | `validate_qa_catalog.py` |

**Not in JSON:** zone geometry, transforms (except `lore_placements.json`), 3D mesh paths beyond registries.

### 5.3 Schema versioning

Bump version when field names or required shapes change.

| File type | Version key | Current examples |
|-----------|-------------|------------------|
| Gameplay JSON | `schema_version` (int) | `chapter_01.json` = **5**, most others = **1** |
| QA / audio catalogs | `version` (string) | `"1.0"`, `"1.3"` |

**Procedure:**

1. Edit upstream files first (see maintenance order below)
2. Bump `schema_version` or `version` in the changed file
3. Update validator if new fields need cross-ref checks
4. Run the matching `validate_*.py` gate
5. Document breaking changes in [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) §17

### 5.4 How to extend data (checklist)

Use this whenever you add fields, rows, or new JSON files.

#### A. New story flag

1. Add to `game/data/story/flags.json` with `set_by` / description
2. Reference only from `scenes.json`, dialogue, encounters, or quests
3. `python3 tools/validate_story_data.py`

#### B. New scene / dialogue block

1. Add row to `game/data/story/scenes.json`
2. Add dialogue key in `dialogue/chapter_01.json` (unless silent by design)
3. Update `docs/vision/STORYBOARD.md` if narrative beat is new
4. `python3 tools/validate_story_data.py`

#### C. New item, enemy, skill, encounter

1. Register ID in authoritative file (`items.json`, `enemies.json`, `skills.json`)
2. Reference from encounters, shop, or drops — never invent IDs in prose only
3. `python3 tools/validate_story_data.py`

#### D. New QA / factory catalog

1. Add `game/data/qa/<name>.json` with `version` + `authority` doc path
2. Add `tools/validate_<name>.py` (follow existing validators)
3. Register gate in `game/data/qa/acceptance_criteria.json` → `docs_ci_gates` or `ci_gates`
4. Wire `run_gate` in `tools/run_docs_ci_checks.sh` or `tools/run_ci_checks.sh`
5. Link from this hub + `docs/README.md` if new doc is added

#### E. New code registry entry

| Registry | When | Also update |
|----------|------|-------------|
| `base_classes.json` | New extend-only gameplay class | `CODE_BASE_CLASS_RULES.md`, Architect PR |
| `autoload_registry.json` | New singleton API contract | `TECHNICAL_DESIGN.md`, `project.godot` on dev branch |
| `scene_registry.json` | New canonical `.tscn` | `LEVEL_DESIGN.md`, GDAI-built scene |
| `helpers_registry.json` | New core helper | `GDSCRIPT_REGENERATION.md`, `tools/*_lib.py` reference |
| `spec_registry.json` | New blocking spec artifact | `SPEC_FIRST_DEVELOPMENT.md` |

#### F. New zone / audio / model row

- Zones: `game/data/qa/zone_composition.json` + `validate_zone_composition.py`
- Audio: `game/data/audio/scene_audio_map.json` + `validate_scene_audio_map.py`
- Models: `game/data/models/qa_catalog.json` + `validate_qa_catalog.py`

### 5.5 Maintenance order (dependency-safe edits)

Edit in this order to avoid broken cross-refs:

1. `story/scenes.json` + `story/flags.json`
2. `quests/main_quests.json`
3. `items/items.json` + `starting/new_game.json`
4. `encounters/story_encounters.json`
5. `dialogue/chapter_01.json`
6. `shop/roku_shop.json` + `achievements/achievements.json`
7. Re-run validators

### 5.6 Save game shape

Authoritative field list: [`SAVE_AND_FAIL_STATES.md`](SAVE_AND_FAIL_STATES.md) · example in [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) §11.

- Single slot v1: `user://save_slot_0.json`
- Signed fields via `SaveIntegrity` helper — do not add save fields without Architect review

---

## 6. Python 3 — industrial rules

**Full guide:** [**PYTHON_STYLE.md**](PYTHON_STYLE.md)  
**Primary external standard:** [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)

Also apply: [PEP 257](https://peps.python.org/pep-0257/) (docstrings) · [PEP 484](https://peps.python.org/pep-0484/) / [PEP 585](https://peps.python.org/pep-0585/) (type hints) · [PEP 20](https://peps.python.org/pep-0020/) (Zen of Python).

Python on `main` is the **behavior reference** for core helpers ported to GDScript on `game/development`.

### PEP 8 quick reference (project profile)

| Topic | Rule |
|-------|------|
| Indent | 4 spaces, no tabs |
| Line length | 100 chars soft limit |
| Names | `snake_case` functions/vars · `CapWords` classes · `UPPER_SNAKE` constants |
| Imports | stdlib → third-party → local; one per line |
| Files | UTF-8 `encoding="utf-8"` on all text I/O |
| Module header | `from __future__ import annotations` on new files |
| Docstrings | Every module + public function ([PEP 257](https://peps.python.org/pep-0257/)) |
| CLI scripts | `def main() -> int:` + `raise SystemExit(main())` |

### Example (validator pattern)

```python
#!/usr/bin/env python3
"""Validate story-driven game data integrity.

Authority: docs/technical/DATA_ARCHITECTURE.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "game" / "data"


def load_json(rel: str) -> dict[str, Any]:
    return json.loads((DATA / rel).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    # ... collect errors ...
    if errors:
        for msg in errors:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    print("OK — story data valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Project-specific rules

| Rule | Detail |
|------|--------|
| Reference libs | `tools/*_lib.py` — must pass `L0_reference_libs` unit tests |
| Validators | One `validate_*.py` per catalog; exit `0`=PASS, `1`=FAIL, `2`=SKIP |
| Paths | `pathlib.Path`; repo root via `Path(__file__).resolve().parents[1]` |
| No secrets | Never commit API keys — `bash tools/check_no_secrets.sh` |
| Gameplay numbers | Belong in `game/data/*.json`, not Python constants |

**Port workflow:** [`GDSCRIPT_REGENERATION.md`](GDSCRIPT_REGENERATION.md) — Python reference wins until `main` spec is fixed.

```bash
python3 tools/validate_story_data.py      # after any game/data story edit
python3 tools/test_reference_libs.py    # after *_lib.py changes
bash tools/run_docs_ci_checks.sh          # full main-branch gate suite
```

Dependencies: `tools/requirements-ci.txt` (`gdtoolkit`, `matplotlib`, …).

---

## 7. Shell / CI scripts

**Full guide:** [**BASH_STYLE.md**](BASH_STYLE.md)  
**External:** [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)

| Rule | Detail |
|------|--------|
| Shebang | `#!/usr/bin/env bash` |
| Safety | `set -euo pipefail` |
| ROOT | `ROOT="$(cd "$(dirname "$0")/.." && pwd)"` |
| Naming | `run_<domain>_<action>.sh`, `check_<domain>.sh` |
| Quoting | Always `"${var}"` — see BASH_STYLE.md |
| Gate runner | `run_gate "<id>"` in `run_docs_ci_checks.sh` — ids match `acceptance_criteria.json` |
| Exit codes | `0` PASS · `1` FAIL · `2` SKIP (SKIP ≠ PASS on `game/development`) |

Authority: [`CI.md`](../ci-cd/CI.md) · [`ACCEPTANCE_CRITERIA.md`](../qa/ACCEPTANCE_CRITERIA.md).

---

## 8. TypeScript / Node.js — MCP Pro server

**Full guide:** [**TYPESCRIPT_STYLE.md**](TYPESCRIPT_STYLE.md)  
**External:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) · [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)

| Topic | Rule |
|-------|------|
| Location | `tools/godot-mcp-pro-server/` (from commercial zip — gitignored) |
| Node | 18+ · `npm install && npm run build` → `build/index.js` |
| Cursor mode | **`--minimal`** always — L4/L5 test tools only; no scene editing |
| Naming | `camelCase` functions · `PascalCase` types · MCP tools `snake_case` |
| Strict TS | `strict: true` in `tsconfig.json` when patching vendor sources |
| R&R | Scene mutations = **GDAI MCP** — never fork MCP Pro to add editors |

```bash
bash tools/install_godot_mcp_pro.sh
bash tools/check_mcp_ready.sh
```

Not shipped — stripped before Steam export (`ship_security.json`).

---

## 9. CI enforcement matrix

| Change type | Minimum gates | Branch |
|-------------|---------------|--------|
| Story / combat JSON | `L0_story_data`, `L1_json_style` | `main` |
| Python tooling | `L1_python_lint` | both |
| Shell scripts | `L1_shellcheck` | both |
| JSON format / naming | `L1_json_style` | both |
| Documentation (`.md`) | `L1_markdown_style` | `main` |
| Shaders (`.gdshader`) | `L1_gdshader_style` | both (templates on `main`) |
| Scenes (`.tscn`) | `L1_scene_style`, `L2_scene_primitives`, `L3_gdai_built` | `game/development` |
| TypeScript (MCP Pro) | `L1_typescript_lint` | `game/development` (SKIP when vendor not installed) |
| Error / exception style | [`ERROR_HANDLING.md`](ERROR_HANDLING.md) | all — enforced via language linters + `L0_*` validators |
| New QA catalog | matching `L0_*` + `L0_doc_sync` | `main` |
| GDScript logic | `L1_unit_tests`, `L1_gdscript_lint`, `L1_gdscript_lint_all` | `game/development` |
| Base class / extends | `L0_base_class_compliance` | both |
| Scenes / materials | `L2_boot_headless`, `L3_gdai_built`, perf if applicable | `game/development` |
| Phase gate | `L4_integration` (INT-*) | `game/development` |
| Full ship path | `L5_e2e_three_endings` | `game/development` |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS · F5 alone ≠ visual PASS.

```bash
# main — docs + data
bash tools/run_docs_ci_checks.sh

# game/development — full game CI
bash tools/run_ci_checks.sh
```

---

## 10. PR checklist by change type

### Python PR (`main`)

- [ ] [PEP 8](https://peps.python.org/pep-0008/) naming, 4-space indent, quoted UTF-8 I/O
- [ ] Module docstring + `from __future__ import annotations`
- [ ] `main() -> int` with correct exit codes
- [ ] `bash tools/check_python_lint.sh`
- [ ] `python3 tools/test_reference_libs.py` if `*_lib.py` changed
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Documentation PR (`main`)

- [ ] [MARKDOWN_STYLE.md](MARKDOWN_STYLE.md) — ATX headings, no tabs in prose, trailing newline
- [ ] `python3 tools/check_markdown_style.py` (`L1_markdown_style`)
- [ ] Relative links resolve from file location
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Data-only PR (`main`)

- [ ] [JSON_DATA_STYLE.md](JSON_DATA_STYLE.md) — 2-space indent, `snake_case`, RFC 8259 valid
- [ ] Edited upstream files before downstream references (§5.5)
- [ ] IDs are `snake_case`; scene IDs match `SC-*` pattern
- [ ] i18n objects include `en`, `ja`, `zh`, `zh-Hant` where user-facing
- [ ] `python3 tools/validate_story_data.py` (and domain validator if applicable)
- [ ] `bash tools/run_docs_ci_checks.sh` green
- [ ] Updated authority doc if schema version bumped

### GDScript PR (`game/development`)

- [ ] [GDSCRIPT_STYLE.md](GDSCRIPT_STYLE.md) — typed GDScript, declaration order, base classes
- [ ] No hardcoded story numbers or dialogue strings
- [ ] Typed signals; no `yield()` or string connects
- [ ] `bash tools/run_unit_tests.sh`
- [ ] `bash tools/check_gdscript_changed.sh` + `bash tools/check_gdscript_all.sh`
- [ ] Scenes built via GDAI MCP (not hand-edited `.tscn`)

### TypeScript / MCP PR (`game/development`)

- [ ] [TYPESCRIPT_STYLE.md](TYPESCRIPT_STYLE.md) — strict TS, `--minimal` preserved
- [ ] `npm run build` in `tools/godot-mcp-pro-server/`
- [ ] No new scene-editing MCP tools
- [ ] `bash tools/check_mcp_ready.sh` passes

### New factory / QA feature

- [ ] Entry in `game/data/qa/workflow_integration_registry.json` if cross-cutting
- [ ] Validator + CI gate wired
- [ ] [`WORKFLOW_INTEGRATION.md`](../qa/WORKFLOW_INTEGRATION.md) updated

---

## 11. Related authority docs

| Topic | Document |
|-------|----------|
| **Hub (this page)** | [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md) |
| Python / PEP 8 | [`PYTHON_STYLE.md`](PYTHON_STYLE.md) |
| JSON / data | [`JSON_DATA_STYLE.md`](JSON_DATA_STYLE.md) |
| Bash / CI scripts | [`BASH_STYLE.md`](BASH_STYLE.md) |
| Runtime architecture | [`TECHNICAL_DESIGN.md`](TECHNICAL_DESIGN.md) |
| GDScript detail | [`GDSCRIPT_STYLE.md`](GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](CODE_STYLE.md) |
| TypeScript / MCP Pro | [`TYPESCRIPT_STYLE.md`](TYPESCRIPT_STYLE.md) |
| Data spine & schemas | [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) |
| Base classes | [`CODE_BASE_CLASS_RULES.md`](CODE_BASE_CLASS_RULES.md) |
| Helper port workflow | [`GDSCRIPT_REGENERATION.md`](GDSCRIPT_REGENERATION.md) |
| Spec-first policy | [`SPEC_FIRST_DEVELOPMENT.md`](SPEC_FIRST_DEVELOPMENT.md) |
| Quests & flags | [`QUEST_AND_FLAGS.md`](../world/QUEST_AND_FLAGS.md) |
| Agent roles | [`RR_CHEATSHEET.md`](../cheat-sheets/RR_CHEATSHEET.md) |
| CI gates | [`CI.md`](../ci-cd/CI.md) |
| QA thresholds | [`ACCEPTANCE_CRITERIA.md`](../qa/ACCEPTANCE_CRITERIA.md) |
| AI dev workflow | [`AI_DEV_WORKFLOW.md`](../workflow/AI_DEV_WORKFLOW.md) |

---

## 12. Quick commands

```bash
# Validate story data after any game/data edit
python3 tools/validate_story_data.py

# Full main-branch CI
bash tools/run_docs_ci_checks.sh

# GDScript lint (game/development)
bash tools/check_gdscript_changed.sh
bash tools/check_gdscript_all.sh

# Unit tests
bash tools/run_unit_tests.sh

# Doc index sync
python3 tools/check_doc_sync.py
```
