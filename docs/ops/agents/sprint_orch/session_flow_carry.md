---
id: session-flow-carry
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 571
summary: "Session flow + carry-over"
---
# Sprint Orchestration — Session flow + carry-over

**Hub:** [`SPRINT_ORCHESTRATION.md`](../SPRINT_ORCHESTRATION.md)

## 4. Session flow (event-driven — not cron)

```
PM: bash tools/run_pm_orchestrator.sh          → PASS required
PM: python3 tools/pm_dispatch_workers.py        → labels dispatch/ready (Automation E)
Agent: bash tools/run_agent_session_gate.sh <role> <issue_id>  → PASS required
Agent: execute work + PR + gates
Optional (M5 / tournament policy): bash tools/run_candidate_tournament.sh  → L2.5 champion/challenger (docs/ops/qa/CANDIDATE_TOURNAMENT.md)
PM or Agent: bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha>  → enforced close + stakeholder report + PM webhook
PM: (new Automation run) run_pm_orchestrator.sh → next dispatch or sprint close
```

**Telemetry:** Session gate opens logging; `run_post_agent_cycle.sh` closes session and auto-fetches tokens. Stakeholder status reports emit on every cycle event. See `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` §9 and `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md`.

**Alignment audit:** PM or agent may run `bash tools/run_alignment_audit.sh --trigger post_merge` after registry or spec changes — `docs/ops/qa/ALIGNMENT_AUDIT.md`. **Management visuals:** `audit_radar_spec.png` + `audit_radar_build.png` only.

**No hourly/daily PM schedule.** Next PM run is triggered only by `agent_cycle_complete`, `sprint_cycle_complete`, `watchdog_recovery`, or guarded CI events. See `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` and `docs/ops/agents/FACTORY_WATCHDOG.md` (stall exception layer).

---


## 5. Carry-over and new sprints

When a sprint batch ends with incomplete issues:

```bash
python3 tools/pm_close_sprint.py --next-sprint-number 2
```

PM **must** then:

1. Copy carry-over issues into `docs/ops/sprints/Phase{N}-Sprint{K+1}-issues.md`
2. Add full rows to `sprint_board.json` (or reset carried issues to `pending`)
3. Clear `carry_over_queue`
4. File GitHub issues for carry-over + any new pack items
5. Re-run `bash tools/run_pm_orchestrator.sh` until PASS

`pm_sync_sprint_pack.py` **FAIL** if pack IDs ⊄ board IDs.

---
