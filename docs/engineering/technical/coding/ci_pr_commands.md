---
id: ci-pr-commands
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 1417
summary: "CI matrix, PR checklist, related, commands"
---
# Coding Standards Hub — CI matrix, PR checklist, related, commands

**Hub:** [`CODING_STANDARDS_HUB.md`](../CODING_STANDARDS_HUB.md)

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
| Error / exception style | [`ERROR_HANDLING.md`](../ERROR_HANDLING.md) | `L1_error_handling` — all languages |
| GitHub Actions YAML | `L1_workflow_yaml` | both |
| Python reference libs | `L1_mypy_libs` | both |
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
- [ ] `bash tools/check_error_handling.sh` when error paths change
- [ ] `python3 tools/test_reference_libs.py` if `*_lib.py` changed
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Documentation PR (`main`)

- [ ] [MARKDOWN_STYLE.md](../MARKDOWN_STYLE.md) — ATX headings, no tabs in prose, trailing newline
- [ ] `python3 tools/check_markdown_style.py` (`L1_markdown_style`)
- [ ] Relative links resolve from file location
- [ ] `bash tools/run_docs_ci_checks.sh` green

### Data-only PR (`main`)

- [ ] [JSON_DATA_STYLE.md](../JSON_DATA_STYLE.md) — 2-space indent, `snake_case`, RFC 8259 valid
- [ ] Edited upstream files before downstream references (§5.5)
- [ ] IDs are `snake_case`; scene IDs match `SC-*` pattern
- [ ] i18n objects include `en`, `ja`, `zh`, `zh-Hant` where user-facing
- [ ] `python3 tools/validate_story_data.py` (and domain validator if applicable)
- [ ] `bash tools/run_docs_ci_checks.sh` green
- [ ] Updated authority doc if schema version bumped

### GDScript PR (`game/development`)

- [ ] [GDSCRIPT_STYLE.md](../GDSCRIPT_STYLE.md) — typed GDScript, declaration order, base classes
- [ ] No hardcoded story numbers or dialogue strings
- [ ] Typed signals; no `yield()` or string connects
- [ ] `bash tools/run_unit_tests.sh`
- [ ] `bash tools/check_gdscript_changed.sh` + `bash tools/check_gdscript_all.sh`
- [ ] Scenes built via GDAI MCP (not hand-edited `.tscn`)

### TypeScript / MCP PR (`game/development`)

- [ ] [TYPESCRIPT_STYLE.md](../TYPESCRIPT_STYLE.md) — strict TS, `--minimal` preserved
- [ ] `npm run build` in `tools/godot-mcp-pro-server/`
- [ ] No new scene-editing MCP tools
- [ ] `bash tools/check_mcp_ready.sh` passes

### New factory / QA feature

- [ ] Entry in `game/data/qa/workflow_integration_registry.json` if cross-cutting
- [ ] Validator + CI gate wired
- [ ] [`WORKFLOW_INTEGRATION.md`](../../../ops/qa/WORKFLOW_INTEGRATION.md) updated

---


## 11. Related authority docs

| Topic | Document |
|-------|----------|
| **Hub (this page)** | [`CODING_STANDARDS_HUB.md`](../CODING_STANDARDS_HUB.md) |
| Python / PEP 8 | [`PYTHON_STYLE.md`](../PYTHON_STYLE.md) |
| JSON / data | [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md) |
| Bash / CI scripts | [`BASH_STYLE.md`](../BASH_STYLE.md) |
| Runtime architecture | [`TECHNICAL_DESIGN.md`](../TECHNICAL_DESIGN.md) |
| GDScript detail | [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](../CODE_STYLE.md) |
| TypeScript / MCP Pro | [`TYPESCRIPT_STYLE.md`](../TYPESCRIPT_STYLE.md) |
| Data spine & schemas | [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md) |
| Base classes | [`CODE_BASE_CLASS_RULES.md`](../CODE_BASE_CLASS_RULES.md) |
| Helper port workflow | [`GDSCRIPT_REGENERATION.md`](../GDSCRIPT_REGENERATION.md) |
| Spec-first policy | [`SPEC_FIRST_DEVELOPMENT.md`](../SPEC_FIRST_DEVELOPMENT.md) |
| Quests & flags | [`QUEST_AND_FLAGS.md`](../../../design/world/QUEST_AND_FLAGS.md) |
| Agent roles | [`RR_CHEATSHEET.md`](../../../ops/cheat-sheets/RR_CHEATSHEET.md) |
| CI gates | [`CI.md`](../../../ops/ci-cd/CI.md) |
| QA thresholds | [`ACCEPTANCE_CRITERIA.md`](../../../ops/qa/ACCEPTANCE_CRITERIA.md) |
| AI dev workflow | [`AI_DEV_WORKFLOW.md`](../../../ops/workflow/AI_DEV_WORKFLOW.md) |

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
