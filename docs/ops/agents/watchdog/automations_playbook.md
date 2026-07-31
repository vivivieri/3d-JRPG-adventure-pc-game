---
id: automations-playbook
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 616
summary: "Automations, events, playbook, refs"
---
# Factory Watchdog — Automations, events, playbook, refs

**Hub:** [`FACTORY_WATCHDOG.md`](../FACTORY_WATCHDOG.md)

## 5. Cursor Automations

### Automation A — PM cycle dispatch (primary)

Unchanged — webhook on `agent_cycle_complete`, `sprint_cycle_complete`, `watchdog_recovery`.

When PM receives `watchdog_recovery`, prompt addition:

```text
WATCHDOG RECOVERY — factory was stalled or hung.
Read artifacts/factory_health_report.json for findings.
1. bash tools/run_pm_orchestrator.sh
2. Diagnose: missing cycle event? stale agent? webhook failure?
3. Re-dispatch or mark issue blocked with pm_update_issue.py
4. If unrecoverable: bash tools/run_factory_watchdog.sh --halt "reason"
5. On fix: bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha>
```

### Automation D — Factory alert (optional)

| Field | Value |
|-------|--------|
| **Name** | `Factory — human alert` |
| **Trigger** | Webhook → `CURSOR_FACTORY_ALERT_WEBHOOK_URL` |
| **Events** | `factory_halt`, recovery exhausted |
| **Prompt** | Notify human; do not start workers |

### GitHub Actions — scheduled watchdog

`.github/workflows/factory-watchdog.yml` runs **every 2 hours**:

- Validates watchdog config
- Runs health analysis
- Calls `--recover` **only if unhealthy** and webhook secret set

This is **exception monitoring**, not PM planning on a timer.

---


## 6. Event types (watchdog-related)

| Event | When |
|-------|------|
| `watchdog_recovery` | Watchdog detected stall/hang; PM must diagnose |
| `factory_halt` | Human or exhausted recovery; factory stopped |

Machine-readable: `game/data/qa/agent_cycle_events.json`

---


## 7. Operator playbook

| Symptom | Action |
|---------|--------|
| Factory idle after merge | `bash tools/run_factory_watchdog.sh --recover` |
| Agent hung 24h+ | Watchdog escalates; PM re-dispatch or `--halt` |
| Runaway recovery loop | Auto-halt at max attempts; `--clear-halt` after fix |
| Intentional pause | `bash tools/run_factory_watchdog.sh --halt "vacation"` |
| Resume | `--clear-halt` then manual `pm_emit_cycle_event.sh` |

---


## 8. Cross-refs

- `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — full Cloud Agent setup
- `docs/ops/agents/PM_AGENT_RUNBOOK.md` — PM session steps
- `docs/ops/agents/SPRINT_ORCHESTRATION.md` — escalation ladder
