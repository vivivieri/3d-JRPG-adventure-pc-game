---
id: branch-purpose
type: reference
audience: [release, qa, pm]
status: active
authority: ci-cd
tokens_est: 401
summary: "Branch split & purpose"
---
# Continuous Integration — Branch split & purpose

**Hub:** [`CI.md`](../CI.md)

## 0. Branch split

| Branch | CI workflows | What runs |
|--------|--------------|-----------|
| **`main`** | `ci.yml` | Docs + design data validation only — **no Godot runtime** |
| **`game/development`** | `ci.yml` **+** `game-ci.yml` | **All** docs/data gates (`run_docs_ci_checks.sh`) **plus** full headless L0–L4 game gates (`run_ci_checks.sh`) — **required green before PR merge** |

Game implementation does **not** merge to `main` until ship-ready (M6). **`game/development` CI is a required merge gate** — it will fail until `game/project.godot` and tests are bootstrapped; that is expected, not a reason to treat CI as optional. See `docs/ops/workflow/BRANCHING.md`.

---


## 1. Purpose

CI enforces **measurable, headless gates** on every push and pull request. It aligns with `.cursorrules` §0 (GDAI R&R), `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`, `docs/ops/workflow/AI_DEV_WORKFLOW.md` §2, and `docs/ops/qa/ACCEPTANCE_CRITERIA.md`.

CI is **not** a substitute for GDAI MCP editor verification (L3 F5) or human QA (L6).

**Tri-state gates:** Gate commands use exit `0`=PASS, `1`=FAIL, `2`=SKIP. On `game/development`, SKIP is treated as FAIL for required gates (`global_rules.skip_is_not_pass`), **except during Phase 1 bootstrap** (P1-00: `project.godot` exists but `run/main_scene` unset — see `issue_bootstrap.P1-00`). On `main`, SKIP is allowed for game-only gates (lint, animation, feel, boot).

**P1-00 bootstrap runner:** `bash tools/run_bootstrap_ci_checks.sh` — sets `PHASE1_BOOTSTRAP_CI=1` and allows documented SKIP for export, GLB, and lint gates until P1-02.

---
