---
id: development-lifecycle
type: explanation
phase: [0, 1, 8]
audience: [pm, architect, release]
status: active
authority: workflow
tokens_est: 406
summary: "Macro lifecycle, branching, gates, promotion"
---
# Development Lifecycle

**Hub** — load one pack below.

| Pack | Topic |
|------|-------|
| [`overview_time.md`](lifecycle/overview_time.md) | Doc map, overview, time model |
| [`branching_agents.md`](lifecycle/branching_agents.md) | Branching, agent envs, issue lifecycle |
| [`gates_trackers.md`](lifecycle/gates_trackers.md) | Quality ladder, trackers, promotion |
| [`enhancements_commands.md`](lifecycle/enhancements_commands.md) | Enhancements, commands, cross-refs |

## Factory surfaces (always on this hub)

Keep these strings discoverable for `L0_workflow_integration`:

| Surface | Command / doc |
|---------|----------------|
| End-of-cycle | `bash tools/run_post_agent_cycle.sh` |
| Session telemetry | `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` |
| Stall recovery | `bash tools/run_factory_watchdog.sh` |
| Worker dispatch | `python3 tools/pm_dispatch_workers.py` |
| Stakeholder report | `bash tools/pm_emit_stakeholder_report.sh` |
| Alignment audit | `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png` |
| Candidate tournament | `bash tools/run_candidate_tournament.sh` |

# Development Lifecycle — End-to-End

**Version:** 1.0
**Authority:** Single hub for how work flows from spec → ship.
**Machine-readable:** `game/data/qa/environments.json`, `game/data/qa/sprint_phases.json`, `game/data/qa/sprint_board.json`
**Branching ADR:** `docs/ops/workflow/BRANCHING_DECISION_RECORD.md`

---
