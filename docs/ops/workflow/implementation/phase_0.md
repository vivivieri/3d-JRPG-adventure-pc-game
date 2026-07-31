---
id: implementation-phase-0
type: how-to
audience: [pm, architect, builder]
phase: [0]
status: active
authority: workflow
tokens_est: 522
---
# Implementation Plan — Phase 0

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## Phase 0 — Dev environment ✅ (current)

| Task | Status |
|------|--------|
| Folder structure (`tools/setup_dev_environment.sh`) | Done |
| `tools/check_dev_environment.sh` | Done |
| `.cursor/mcp.json.example` (GDAI MCP) | Done |
| `game/addons/README.md` | Done |
| Story data validator (`tools/validate_story_data.py`) | Done |
| GDAI MCP workflow rules (`.cursorrules`, `tools/ensure_gdai_mcp.sh`) | Done |
| Fresh-rebuild smoke (`tools/run_playtest_smoke.sh`) | Done |
| QA acceptance catalog (`game/data/qa/acceptance_criteria.json`, `docs/ops/qa/ACCEPTANCE_CRITERIA.md`) | Done |
| QA remediation + domain gates (MODEL/VISUAL/AUDIO/FLOW QA docs) | Done |
| AI dev workflow doc (`docs/ops/workflow/AI_DEV_WORKFLOW.md`) | Done |
| AI testing spec (`docs/ops/qa/AI_TESTING_SPEC.md`) | Done |
| Code base class registry (`docs/engineering/technical/CODE_BASE_CLASS_RULES.md`, `game/data/code/base_classes.json`) | Done |
| Base-class + animation + gdlint CI gates (`acceptance_criteria.json`, `run_ci_checks.sh`) | Done |
| Cloud install (`tools/install_cloud_dev.sh`, `.cursor/environment.json`) | Done |
| Spec-first registries (`helpers_registry.json`, `spec_registry.json`, Python reference libs) | Done |
| **`game/project.godot` on `game/development`** | **P1-00** — `bash tools/bootstrap_game_development.sh` (not on `main`) |
| Boot / data validation (`GameBootstrap` autoload) | **Specified** on `main` — **built** Phase 2 on `game/development` |
| Unit tests (`tools/run_unit_tests.sh`, `game/tests/unit/`) | **P1-00** shell on `game/development`; expand per phase |

**Verify (main — docs/data only):**

```bash
bash tools/setup_dev_environment.sh
python3 tools/validate_acceptance_criteria.py
python3 tools/validate_story_data.py
bash tools/run_docs_ci_checks.sh
bash tools/run_playtest_smoke.sh
```

**Verify (game/development — after P1-00 bootstrap):**

```bash
bash tools/bootstrap_game_development.sh
bash tools/ensure_gdai_mcp.sh
bash tools/run_ci_checks.sh
bash tools/run_unit_tests.sh
# Open game/project.godot in Godot 4.7 → F5 when main_scene is set
```

---

