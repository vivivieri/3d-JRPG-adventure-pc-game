# Sprint Orchestration — Enforced Multi-Agent Workflow

**Version:** 1.0  
**Authority:** Replaces honor-system sprint planning. If orchestrator FAILs, **no agent may proceed**.  
**Cross-refs:** `docs/PM_AGENT_RUNBOOK.md`, `docs/MULTI_AGENT_TEAM.md`, `docs/AGILE_WITHIN_PHASES.md`, `game/data/qa/sprint_board.json`, `game/data/qa/pm_orchestrator_steps.json`

---

## 1. Problem this solves

| Honor system (rejected) | Enforced orchestration |
|-------------------------|-------------------------|
| PM “should” file issues with gate IDs | `validate_sprint_board.py` **FAIL** CI if board invalid |
| Agents “should” wait for handoff | `run_agent_session_gate.sh` **FAIL** if not dispatched |
| PM “should” run planning each session | `run_pm_orchestrator.sh` **FAIL** if any step skipped |
| Stale work ignored | Stale `in_progress` **FAIL** orchestrator |
| Carry-over verbal | `pm_close_sprint.py` + `carry_over_queue` **FAIL** until resolved |

---

## 2. Machine-readable sources of truth

| File | Role |
|------|------|
| `game/data/qa/sprint_phases.json` | Active phase, exit gates, sprint cadence |
| `game/data/qa/sprint_board.json` | **Active sprint issues**, status, deps, dispatch state |
| `game/data/qa/pm_orchestrator_steps.json` | **Mandatory PM session steps** (ordered) |
| `docs/sprints/Phase{N}-Sprint{K}-issues.md` | Human-readable issue bodies (must match board IDs) |
| `artifacts/pm_orchestrator_report.json` | Latest dispatch output (written each PM run) |

---

## 3. Roles

| Role | Orchestration duty |
|------|-------------------|
| **PM Agent** (Sprint Master) | Runs `run_pm_orchestrator.sh` every session; updates board; escalates stale agents |
| **Architect / Builder / QA / …** | Runs `run_agent_session_gate.sh` before work; never self-assign |
| **QA Agent** | Sprint review evidence; does not close issues without gate report |
| **Human** | L6 + escalation level `human` only |

---

## 4. Session flow (event-driven — not cron)

```
PM: bash tools/run_pm_orchestrator.sh          → PASS required
PM: assign next_dispatch[0] to agent
Agent: bash tools/run_agent_session_gate.sh <role> <issue_id>  → PASS required
Agent: execute work + PR + gates
PM or Agent: python3 tools/pm_update_issue.py <id> --status done --commit <sha>
Agent or PM: bash tools/pm_emit_cycle_event.sh agent_cycle_complete ...  → triggers PM webhook
PM: (new Automation run) run_pm_orchestrator.sh → next dispatch or sprint close
```

**No hourly/daily PM schedule.** Next PM run is triggered only by `agent_cycle_complete`, `sprint_cycle_complete`, `watchdog_recovery`, or guarded CI events. See `docs/CLOUD_AGENT_SETUP_RUNBOOK.md` and `docs/FACTORY_WATCHDOG.md` (stall exception layer).

---

## 5. Carry-over and new sprints

When a sprint batch ends with incomplete issues:

```bash
python3 tools/pm_close_sprint.py --next-sprint-number 2
```

PM **must** then:

1. Copy carry-over issues into `docs/sprints/Phase{N}-Sprint{K+1}-issues.md`
2. Add full rows to `sprint_board.json` (or reset carried issues to `pending`)
3. Clear `carry_over_queue`
4. File GitHub issues for carry-over + any new pack items
5. Re-run `bash tools/run_pm_orchestrator.sh` until PASS

`pm_sync_sprint_pack.py` **FAIL** if pack IDs ⊄ board IDs.

---

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

---

## 9. Cross-refs

- `docs/PM_AGENT_RUNBOOK.md` — step-by-step PM commands
- `docs/CONTROLS_CHEATSHEET.md` — CI enforcement
- `docs/PROJECT_MANAGEMENT.md` — GitHub labels
