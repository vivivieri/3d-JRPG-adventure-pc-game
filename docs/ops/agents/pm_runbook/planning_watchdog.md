---
id: planning-watchdog
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 995
summary: "Planning, close, watchdog, never-do, refs"
---
# PM Agent Runbook — Planning, close, watchdog, never-do, refs

**Hub:** [`PM_AGENT_RUNBOOK.md`](../PM_AGENT_RUNBOOK.md)

## 5. Sprint planning — create / sync issues

### New sprint batch

1. Read `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase N + `sprint_phases.json` exit gates.
2. Write `docs/ops/sprints/Phase{N}-Sprint{K}-issues.md` (copy Phase1 template).
3. Add all issues to `game/data/qa/sprint_board.json`:
   - `id`, `sequence`, `depends_on`, `agent_owner`, `acceptance_gate_ids`, `implementation_plan_tasks`
4. Set `active_sprint.id` = `Phase{N}-Sprint{K}`.
5. Run `bash tools/run_pm_orchestrator.sh` — must PASS before filing GitHub issues.
6. File GitHub issues from pack; set `github_issue` on board rows.

### Missing issue detection

`pm_sync_sprint_pack.py` compares pack markdown `## P1-XX` headers to board — **FAIL** if mismatch.

### Carry-over from previous sprint

```bash
python3 tools/pm_close_sprint.py --next-sprint-number 2 --dry-run   # preview
python3 tools/pm_close_sprint.py --next-sprint-number 2
```

Then update issue pack + board rows; clear `carry_over_queue`; re-run orchestrator.

---


## 6. Sprint close checklist

- [ ] All board issues `status: done` OR explicitly `carry_over` with next sprint filed
- [ ] `bash tools/run_pm_orchestrator.sh` → `sprint_complete: true`
- [ ] QA gate report archived in P1-06 / sprint review issue
- [ ] `carry_over_queue` empty
- [ ] Optional: `git tag v0.1.0-rc1` per `sprint_phases.json` uat_tag_pattern

---


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
