---
id: workflow-handoff
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 721
summary: "Workflow, situation→tool, handoffs"
---
# R&R Cheat Sheet — Workflow, situation→tool, handoffs

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## Default workflow (one feature)

```
READ  → zone row in ENVIRONMENT_KITS.md + RENDERING_GUIDE.md
PLAN  → GodotPrompter: shaders, scripts, node tree, gate IDs
BUILD → GDAI MCP: scenes, materials, lights, F5
DEBUG → Godotiq (on failure only)
TEST  → QA L0–L3; Flow L4/L5 if flows/scenes changed
MERGE → PR template checkboxes + CI green (see CONTROLS_CHEATSHEET)
SHIP  → commit; gates PASS; check_asset_compliance.sh
```

---


## Situation → tool (conflict resolver)

| Situation | Use |
|-----------|-----|
| Edit `.tscn` / reparent nodes | **GDAI MCP only** |
| Combat/signal hang | **Godotiq** `signal_map`, `trace_flow` |
| Menu/combat automated test | **MCP Pro** `run_test_scenario` |
| Zone wood/stone texture | ComfyUI/Material Maker → **GDAI** assign |
| UI ink frame / icons | GameLab → **GDAI** assign |
| Balance / dialogue / flags | **`game/data/`** PR to `main` |
| Spec refinement (design time) | **`main` only** — docs + data + `tools/*_lib.py`; **never** `.gd`/`.tscn` (`SPEC_FIRST_DEVELOPMENT.md` §10) |
| Core helper spec / Python ref | **Architect** PR to `main` — `docs/engineering/technical/GDSCRIPT_REGENERATION.md` |
| Phase 1 visuals port (P1-01) | **Architect** on `game/development` — `GDSCRIPT_REGENERATION.md` §10 · `bash tools/regenerate_phase1_visuals.sh` |
| Core helper `.gd` port | **Architect** on `game/development` — PM dispatch by phase |
| EventBus autoload registration | **Builder** (GDAI MCP) — after Architect `event_bus.gd` |
| RC / beta / prod tag | **Release Agent** + `run_cd_gates.sh` |

---


## Handoff minimums

**Architect → Builder:** design doc row, node tree, shader/uniform list, inspector targets, gate IDs, **component scene** to instance (`LEVEL_DESIGN.md` §1b); for art assets, link or attach `docs/briefs/<id>.md` when present (`GENERATION_READINESS.md`). On-direction = bible + brief; feel polish = human L6 feedback loop (`MODEL_QA.md` §9).

**Architect → Builder (core helpers):** `helpers_registry.json` entry + Python reference path; GDScript file at `gdscript_path` committed on `game/development`; for **EventBus** only — Builder registers autoload in `project.godot` via GDAI MCP (`docs/engineering/technical/GDSCRIPT_REGENERATION.md` §2).

**Builder → QA:** commit SHA, `game/scenes/.gdai_built` (`verified_f5=true`), scenes touched, screenshots if visual.

**QA → PM (pass):** gate report in **PR body** (template block) with commit + gate IDs + evidence paths.

**QA → Architect (fail):** `bash tools/qa_emit_remediation.sh <brief-id>` + gate ID in issue.

**PM → all:** ensure linked issue + correct **PR template** before review.

---
