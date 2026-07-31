---
id: escalation-ci-forbidden
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 509
summary: "Sprint Orchestration — Escalation, CI, forbidden, cross-refs — Stale threshold: `sprint_board.json` → `orchestration.stale_hours` (default 24)."
---
# Sprint Orchestration — Escalation, CI, forbidden, cross-refs

**Hub:** [`SPRINT_ORCHESTRATION.md`](../SPRINT_ORCHESTRATION.md)

## When to read

Use **Sprint Orchestration — Escalation, CI, forbidden, cross-refs** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [6. Escalation ladder](#6-escalation-ladder)
- [7. CI gates](#7-ci-gates)
- [8. Forbidden patterns](#8-forbidden-patterns)
- [9. Cross-refs](#9-cross-refs)


## 6. Escalation ladder

| Level | Action | Tool |
|-------|--------|------|
| 0 | Normal dispatch | orchestrator |
| 1 | Reminder comment on GitHub issue | `pm_emit_escalation.sh <id> remind` |
| 2 | `severity/S2` label | PM |
| 3 | `severity/S1` — blocks sprint close | PM |
| 4 | `severity/S0` — blocks phase promotion | PM |
| 5 | `human` — notify project owner | PM |

Stale threshold: `sprint_board.json` → `orchestration.stale_hours` (default 24).

---


## 7. CI gates

| Gate ID | Command | Branch |
|---------|---------|--------|
| `L0_sprint_board` | `python3 tools/validate_sprint_board.py --strict` | `main` |
| `L0_sprint_phases` | `python3 tools/validate_sprint_phases.py` | `main` |

Game branch PRs: PM should verify orchestrator PASS on latest `sprint_board.json` in PR description.

---


## 8. Forbidden patterns

Listed in `acceptance_criteria.json` → `invalid_pass_patterns`:

- PM session without `run_pm_orchestrator.sh` PASS
- Agent work without `run_agent_session_gate.sh` PASS
- Issue closed in GitHub but `sprint_board` status not `done`
- Sprint pack / board ID mismatch
- Cross-cutting factory feature without `workflow_integration_registry.json` entry (`docs/ops/qa/WORKFLOW_INTEGRATION.md`)

---


## 9. Cross-refs

- `docs/ops/agents/PM_AGENT_RUNBOOK.md` — step-by-step PM commands
- `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — CI enforcement
- `docs/ops/agents/PROJECT_MANAGEMENT.md` — GitHub labels
- `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` — auto token/duration logging + workflow cooperation §9
