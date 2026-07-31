---
id: problem-sources-roles
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 593
summary: "Problem, sources of truth, roles"
---
# Sprint Orchestration — Problem, sources of truth, roles

**Hub:** [`SPRINT_ORCHESTRATION.md`](../SPRINT_ORCHESTRATION.md)

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
| `docs/ops/sprints/Phase{N}-Sprint{K}-issues.md` | Human-readable issue bodies (must match board IDs) |
| `artifacts/pm_orchestrator_report.json` | Latest dispatch output (written each PM run) |
| `artifacts/pm_dispatch_packet.json` | Structured worker handoff (gates, refs, branch) |
| `artifacts/agent_session_telemetry/events.jsonl` | **Agent session telemetry** — role, task, duration, tokens (see `docs/ops/qa/AGENT_SESSION_TELEMETRY.md`) |
| `artifacts/linear_sync_manifest.json` | Linear mirror state |
| `game/data/qa/factory_health_snapshot.json` | Remote watchdog cycle signal (committed) |

---


## 3. Roles

| Role | Orchestration duty |
|------|-------------------|
| **PM Agent** (Sprint Master) | Runs `run_pm_orchestrator.sh` every session; updates board; escalates stale agents |
| **Architect / Builder / QA / …** | Runs `run_agent_session_gate.sh` before work; never self-assign |
| **Factory Analyst** | Reviews `artifacts/agent_session_reports/` after sprint cycles; does not block dispatch |
| **QA Agent** | Sprint review evidence; does not close issues without gate report |
| **Human** | L6 + escalation level `human` only |

---
