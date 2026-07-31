---
id: refinement-refs
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, pm]
status: active
authority: engineering
tokens_est: 941
summary: "Spec refinement mode + cross-refs"
---
# Spec-First Development — Spec refinement mode + cross-refs

**Hub:** [`SPEC_FIRST_DEVELOPMENT.md`](../SPEC_FIRST_DEVELOPMENT.md)

## 10. Spec refinement mode — prevent ad-hoc implementation

**When:** Revising design, registries, narrative data, or helper **contracts** — before or between sprint dispatches.

### Allowed on `main` (spec refinement)

| Layer | Paths | Owner |
|-------|-------|-------|
| Design prose | `docs/` | PM / Architect |
| Machine data | `game/data/` | Architect |
| i18n strings | `game/locale/` | Architect |
| Validators + reference behavior | `tools/*.py`, `tools/*_lib.py` | Architect |
| Spec registries | `game/data/code/*.json` | Architect |

**Reference libs are not ship code.** They express behavior for later GDScript ports (`docs/engineering/technical/GDSCRIPT_REGENERATION.md`).

### Forbidden during spec refinement

| Action | Why blocked | Enforcement |
|--------|-------------|-------------|
| `.gd` / `.tscn` / `project.godot` on `main` | Ship implementation | `L0_main_no_ship_code`, `L0_spec_refinement_scope` |
| Hand-edit ship `.tscn` anywhere | Builder R&R | `L0_rr_compliance` |
| `.gd` on `game/development` without PM dispatch | Ad-hoc bypass | `run_agent_session_gate.sh` + PR template |
| Scene work with GDAI down | Silent fallback | `check_mcp_ready.sh` → **STOP** |
| Invent behavior not in spec | Spec drift | `L0_spec_registry`, registry-first PR review |

### Decision flow

```text
Changing behavior or APIs?
  ├─ YES, not yet in game/data/ or registries
  │    → PR to main (docs + JSON + tools/*_lib.py if needed)
  │    → validate_spec_registry.py PASS
  │    → merge main → game/development
  └─ NO, spec already on main
       → PM: run_pm_orchestrator.sh
       → Worker: run_agent_session_gate.sh <role> <issue_id>
       → Architect: .gd / tests OR Builder: GDAI scenes
       → Phase 1 visuals: docs/engineering/technical/GDSCRIPT_REGENERATION.md §10
       → QA: gate report on PR
```

### Session rules (agents)

| Role | During spec refinement | When implementation is allowed |
|------|------------------------|--------------------------------|
| **PM** | `run_docs_ci_checks.sh`; update registries | Dispatch via orchestrator only |
| **Architect** | `docs/`, `game/data/`, `tools/*_lib.py` on `main` | After session gate + linked issue on `game/development` |
| **Builder** | **No scene/code work** | After Architect handoff + `ensure_mcp_stack.sh` |
| **QA** | Validate L0 data gates | After Builder/Architect PR — cite gate IDs |

```bash
# Spec refinement PR (main)
bash tools/run_docs_ci_checks.sh    # includes L0_spec_refinement_scope

# Implementation session (game/development) — both required
bash tools/run_pm_orchestrator.sh
bash tools/run_agent_session_gate.sh architect P1-01
bash tools/ensure_mcp_stack.sh      # Builder scene work only
```

### CI gates

```bash
bash tools/check_spec_refinement_scope.sh   # L0_spec_refinement_scope (main)
bash tools/check_main_no_ship_code.sh       # L0_main_no_ship_code (main)
bash tools/run_agent_session_gate.sh ...    # dispatch (game/development workers)
```

---


## 11. Cross-refs

- `docs/ops/workflow/BRANCHING.md` — branch merge policy
- `docs/engineering/technical/GDSCRIPT_REGENERATION.md` — rebuild core helpers + Phase 1 visuals on `game/development`
- `docs/engineering/technical/TECHNICAL_DESIGN.md` — runtime architecture (prose + diagrams)
- `docs/engineering/technical/CODE_BASE_CLASS_RULES.md` — who writes bases vs instances
- `docs/ops/workflow/IMPLEMENTATION_PLAN.md` — phase task list (execution on `game/development`)
