---
id: sprint-orchestration
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 348
summary: "Enforced multi-agent workflow — load roles, flow, or escalation"
---
# Sprint Orchestration

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`problem_sources_roles.md`](sprint_orch/problem_sources_roles.md) | Problem, sources of truth, roles |
| [`session_flow_carry.md`](sprint_orch/session_flow_carry.md) | Session flow + carry-over |
| [`escalation_ci_forbidden.md`](sprint_orch/escalation_ci_forbidden.md) | Escalation, CI, forbidden, cross-refs |
**Version:** 1.0
**Authority:** Replaces honor-system sprint planning. If orchestrator FAILs, **no agent may proceed**.
**Cross-refs:** `docs/ops/agents/PM_AGENT_RUNBOOK.md`, `docs/ops/agents/MULTI_AGENT_TEAM.md`, `docs/ops/workflow/AGILE_WITHIN_PHASES.md`, `game/data/qa/sprint_board.json`, `game/data/qa/pm_orchestrator_steps.json`

---

## Factory hooks (registry keywords)

- Cycle close: `bash tools/run_post_agent_cycle.sh`
- Docs pack adherence: session gate → `log_docs_read.py --from-pack`; cycle → `check_docs_pack_adherence.py --strict`
- Telemetry: `docs/ops/qa/AGENT_SESSION_TELEMETRY.md`
- Watchdog: `docs/ops/agents/FACTORY_WATCHDOG.md`
- Dispatch: `python3 tools/pm_dispatch_workers.py`
- Stakeholder: `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md`
- Alignment: `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png`
- Tournament: `docs/ops/qa/CANDIDATE_TOURNAMENT.md`
- Portable pack: `packages/game-dev-factory/` · `FACTORY_DATA_DIR`

