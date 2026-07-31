---
id: refs-commands
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 491
summary: "Related docs + quick commands"
---
# Coding — CI & PR — Related docs + quick commands

**Hub:** [`ci_pr_commands.md`](../ci_pr_commands.md)

## 11. Related authority docs

| Topic | Document |
|-------|----------|
| **Hub (this page)** | [`CODING_STANDARDS_HUB.md`](../../CODING_STANDARDS_HUB.md) |
| Python / PEP 8 | [`PYTHON_STYLE.md`](../../PYTHON_STYLE.md) |
| JSON / data | [`JSON_DATA_STYLE.md`](../../JSON_DATA_STYLE.md) |
| Bash / CI scripts | [`BASH_STYLE.md`](../../BASH_STYLE.md) |
| Runtime architecture | [`TECHNICAL_DESIGN.md`](../../TECHNICAL_DESIGN.md) |
| GDScript detail | [`GDSCRIPT_STYLE.md`](../../GDSCRIPT_STYLE.md) · [`CODE_STYLE.md`](../../CODE_STYLE.md) |
| TypeScript / MCP Pro | [`TYPESCRIPT_STYLE.md`](../../TYPESCRIPT_STYLE.md) |
| Data spine & schemas | [`DATA_ARCHITECTURE.md`](../../DATA_ARCHITECTURE.md) |
| Base classes | [`CODE_BASE_CLASS_RULES.md`](../../CODE_BASE_CLASS_RULES.md) |
| Helper port workflow | [`GDSCRIPT_REGENERATION.md`](../../GDSCRIPT_REGENERATION.md) |
| Spec-first policy | [`SPEC_FIRST_DEVELOPMENT.md`](../../SPEC_FIRST_DEVELOPMENT.md) |
| Quests & flags | [`QUEST_AND_FLAGS.md`](../../../../design/world/QUEST_AND_FLAGS.md) |
| Agent roles | [`RR_CHEATSHEET.md`](../../../../ops/cheat-sheets/RR_CHEATSHEET.md) |
| CI gates | [`CI.md`](../../../../ops/ci-cd/CI.md) |
| QA thresholds | [`ACCEPTANCE_CRITERIA.md`](../../../../ops/qa/ACCEPTANCE_CRITERIA.md) |
| AI dev workflow | [`AI_DEV_WORKFLOW.md`](../../../../ops/workflow/AI_DEV_WORKFLOW.md) |

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
