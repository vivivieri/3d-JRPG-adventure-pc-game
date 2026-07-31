---
id: orchestrator-dispatch
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 518
summary: "Sprint Master, orchestrator, dispatch"
---
# PM Agent Runbook — Sprint Master, orchestrator, dispatch

**Hub:** [`PM_AGENT_RUNBOOK.md`](../PM_AGENT_RUNBOOK.md)

## 0. You are the Sprint Master

You **create** sprint items, **dispatch** other agents in sequence, **verify** gates, **escalate** delays, and **carry forward** incomplete work. You do **not** write `.gd`, `.tscn`, or shaders.

---


## 1. Every PM session — run orchestrator first

```bash
bash tools/run_pm_orchestrator.sh
```

This runs all steps in `game/data/qa/pm_orchestrator_steps.json`:

| Step | What it enforces |
|------|------------------|
| 0–5 | Idempotency, sprint board, GitHub/Linear sync, preflight |
| 6 | `run_sprint_preflight.sh` — snapshot boot + MCP gates |
| 7 | `run_docs_ci_checks.sh` — docs/data baseline |
| 8 | `pm_orchestrator_lib.py --dispatch` — next agent + stale/WIP checks |
| 9 | `dispatch_workers` — `pm_dispatch_workers.py` labels GitHub → Worker automation |
| 10–13 | Event handled, stakeholder report, telemetry, alignment audit |

**If exit ≠ 0:** STOP. Fix failures. Do not assign agents.

**On PASS:** read `artifacts/pm_orchestrator_report.json` → `next_dispatch`.

**Telemetry:** Step 11 auto-refreshes `artifacts/agent_session_reports/` — see `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` §9.

---


## 2. Dispatch the next agent

From orchestrator output:

```bash
# Example — use actual issue_id and agent from next_dispatch[0]
bash tools/run_agent_session_gate.sh architect P1-01
```

Tell the assigned agent (new Cursor session):

- Issue ID + link to `docs/ops/sprints/Phase1-Sprint1-issues.md` section
- Acceptance gate IDs (from board)
- Handoff section (Architect → Builder when applicable)
- **They must pass session gate before coding**

Set GitHub issue: `status/in-progress`, `agent/<role>`.

Optional board update before dispatch:

```bash
python3 tools/pm_update_issue.py P1-01 --status in_progress --agent architect
```

---
