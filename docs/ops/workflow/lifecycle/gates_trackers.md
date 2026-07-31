---
id: gates-trackers
type: explanation
phase: [0, 1, 8]
audience: [pm, architect, release]
status: active
authority: workflow
tokens_est: 891
summary: "Development Lifecycle — Quality ladder, trackers, promotion — QA stage = L0–L2 (and L4/L5 when phase requires) automated on trunk."
---
# Development Lifecycle — Quality ladder, trackers, promotion

**Hub:** [`DEVELOPMENT_LIFECYCLE.md`](../DEVELOPMENT_LIFECYCLE.md)

## When to read

Use **Development Lifecycle — Quality ladder, trackers, promotion** (roles: pm, architect, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [7. Quality gate ladder (when each stage runs)](#7-quality-gate-ladder-when-each-stage-runs)
- [8. Tracker roles (GitHub vs Linear)](#8-tracker-roles-github-vs-linear)
- [9. Promotion checklist](#9-promotion-checklist)


## 7. Quality gate ladder (when each stage runs)

| Layer | When | Command / owner | Blocks |
|-------|------|-----------------|--------|
| **L0** | Every commit | `validate_story_data.py`, R&R compliance | Data + policy |
| **L1** | Every commit | `run_unit_tests.sh`, gdlint | Logic regressions |
| **L2** | Every commit / when assets exist | smoke, visual/audio/model jury | Art/audio tech |
| **L3** | Scene change | GDAI F5 + `.gdai_built` | Broken scenes |
| **L4** | Phase 2+ milestones | `run_integration_tests.sh` | Flow scenarios |
| **L5** | Phase 6+ | `run_e2e_playthrough.sh` | Three endings |
| **L6** | UAT only | Human `PLAYTEST_SCRIPT.md` | Ship sign-off |

**QA stage** = L0–L2 (and L4/L5 when phase requires) automated on trunk.
**UAT stage** = tagged RC + human L6 — never before L0–L5 on the same commit.

---


## 8. Tracker roles (GitHub vs Linear)

| Tracker | Stores | Sprint role |
|---------|--------|-------------|
| **GitHub Issues** | Full task spec, gate IDs, evidence, PR links | **Required** — traceability + CI |
| **Linear** | Cycle batching, optional mirror issues | **Optional** — sprint iteration lens |

GitHub = **what + proof** · Linear = **which batch + cycle progress**

**Agent session telemetry** (efficiency studies): `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` — JSONL log of role, task, duration, tokens per issue. Wired into session gate, cycle events, PM orchestrator, watchdog, and stakeholder reports (`tools/analyze_agent_session_telemetry.py`). Requires one-time `CURSOR_API_KEY` secret.

**Workflow integration registry** (drift prevention): `docs/ops/qa/WORKFLOW_INTEGRATION.md` — agents register cross-cutting factory features before merge; `L0_workflow_integration` CI + `bash tools/check_feature_integration.sh --remind`.

**Factory watchdog:** `bash tools/run_factory_watchdog.sh` — stall recovery when PM dispatch stalls (`docs/ops/agents/FACTORY_WATCHDOG.md`).

**Stakeholder reporting:** `bash tools/pm_emit_stakeholder_report.sh` — auto on cycle events; manual at phase exit (`docs/ops/agents/PM_STAKEHOLDER_REPORTING.md`).

**Alignment audit:** `bash tools/run_alignment_audit.sh` — post-merge spec/data parity (`docs/ops/qa/ALIGNMENT_AUDIT.md`). **Management status:** `audit_radar_spec.png` + `audit_radar_build.png` (ignore mega dashboard).

---


## 9. Promotion checklist

| From → To | Criteria | Action |
|-----------|----------|--------|
| Design → Dev | `SPEC_DEV_START` gate PASS | Bootstrap `game/development` |
| Dev → QA | Push/PR to trunk | Game CI green |
| QA → UAT | Phase/milestone gates PASS | Tag `v*-rc*`; run `run_cd_gates.sh --channel rc` |
| UAT → Preprod | L6 ≥80%; S0/S1 = 0; Steamworks ready | Tag `v*-beta*` |
| Preprod → Prod | Beta soak; store live; compliance | Tag `v*.*.*` + `steam-production` approval |
| Prod → Design merge | One-time ship | `game/development` → `main` |

**Never promote with SKIP gates** (`skip_is_not_pass` in `acceptance_criteria.json`).

---
