---
id: watchdog-refs
type: how-to
audience: [pm]
status: active
authority: ops
tokens_est: 642
summary: "Watchdog + quick ref"
---
# PM Runbook — Planning & Watchdog — Watchdog + quick ref

**Hub:** [`planning_watchdog.md`](../planning_watchdog.md)

## 7. Watchdog recovery (when factory stalls)

Normal handoff uses `pm_emit_cycle_event.sh`. If the factory is **idle too long** while sprint work remains:

```bash
bash tools/run_factory_watchdog.sh          # health check
bash tools/run_factory_watchdog.sh --recover # trigger PM via watchdog_recovery
```

When PM is triggered by `watchdog_recovery`:

1. Read `artifacts/factory_health_report.json`
2. Run `bash tools/run_pm_orchestrator.sh`
3. Diagnose: missing cycle event? stale agent? webhook miss?
4. Re-dispatch or mark `blocked` via `pm_update_issue.py`
5. If unrecoverable: `bash tools/run_factory_watchdog.sh --halt "reason"`

Long worker sessions — emit progress heartbeats:

```bash
bash tools/pm_record_heartbeat.sh --agent builder --issue P1-02 --phase progress
```

See `docs/ops/agents/FACTORY_WATCHDOG.md`.

---



## 8. Quick reference

| Task | Command |
|------|---------|
| PM session start | `bash tools/run_pm_orchestrator.sh` |
| Agent clearance | `bash tools/run_agent_session_gate.sh <role> <issue_id>` |
| Update issue state | `python3 tools/pm_update_issue.py <id> --status done --commit <sha>` |
| Escalate | `bash tools/pm_emit_escalation.sh <id> <level>` |
| **End cycle → trigger PM** | `bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha>` |
| Factory health | `bash tools/run_factory_watchdog.sh` |
| Stall recovery | `bash tools/run_factory_watchdog.sh --recover` |
| **Stakeholder report** | Auto on `pm_emit_cycle_event.sh`; manual: `bash tools/pm_emit_stakeholder_report.sh --trigger phase_exit --telegram` |
| **Alignment audit** | `bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N"` · management: `audit_radar_spec.png` + `audit_radar_build.png` |
| Emergency stop | `bash tools/run_factory_watchdog.sh --halt "reason"` |
| Close sprint | `python3 tools/pm_close_sprint.py --next-sprint-number N` |
| Validate board | `python3 tools/validate_sprint_board.py --strict` |

---



## 9. Cross-refs

- `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — Cloud Agent factory setup
- `docs/ops/agents/FACTORY_WATCHDOG.md` — stall/hang exception handling
- `docs/ops/agents/MULTI_AGENT_TEAM.md` — handoff contracts
- `docs/ops/sprints/Phase1-Sprint1-issues.md` — current issue bodies
- `game/data/qa/sprint_board.json` — live sprint state
