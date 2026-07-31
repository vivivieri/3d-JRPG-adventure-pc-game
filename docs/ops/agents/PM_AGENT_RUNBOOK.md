---
id: pm-agent-runbook
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 365
summary: "Sprint Master runbook — load dispatch, close-loop, or watchdog"
---
# PM Agent Runbook

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`orchestrator_dispatch.md`](pm_runbook/orchestrator_dispatch.md) | Sprint Master, orchestrator, dispatch |
| [`close_loop_features.md`](pm_runbook/close_loop_features.md) | Close loop, factory features, stale agents |
| [`planning_watchdog.md`](pm_runbook/planning_watchdog.md) | Planning, close, watchdog, never-do, refs |
**Version:** 1.0
**Role:** PM Agent / Sprint Master (same role — `sprint_phases.json` → `sprint_master.role = "pm"`)
**Rule:** Execute **every step below in order**. Skip = orchestrator FAIL = project blocked.
**Authority:** `docs/ops/agents/SPRINT_ORCHESTRATION.md`

---

## Factory hooks (registry keywords)

Keep these strings on the hub for `L0_workflow_integration`:

- Cycle close: `bash tools/run_post_agent_cycle.sh` (writes session **telemetry**)
- Dispatch: `python3 tools/pm_dispatch_workers.py` · orchestrator step `dispatch_workers`
- Watchdog: `bash tools/run_factory_watchdog.sh`
- Stakeholder: `bash tools/pm_emit_stakeholder_report.sh`
- Alignment: `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png` + `audit_radar_build.png`
- Tournament gate: `L2_candidate_select` · `docs/ops/qa/CANDIDATE_TOURNAMENT.md`

