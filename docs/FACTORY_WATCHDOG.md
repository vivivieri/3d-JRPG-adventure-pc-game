# Factory Watchdog — Stall & Hang Exception Handling

**Version:** 1.0  
**Authority:** Exception layer on top of event-driven PM dispatch.  
**Cross-refs:** `docs/CLOUD_AGENT_SETUP_RUNBOOK.md`, `docs/SPRINT_ORCHESTRATION.md`, `game/data/qa/factory_watchdog.json`

---

## 1. Two layers (do not confuse them)

| Layer | Trigger | Purpose |
|-------|---------|---------|
| **Primary — event-driven PM** | `agent_cycle_complete` webhook | Fast cycle-to-cycle dispatch when work finishes |
| **Exception — factory watchdog** | Stall/hang detected | Recovery when something broke or was forgotten |

**Normal flow:** Worker finishes → `pm_emit_cycle_event.sh` → PM wakes in **seconds**.

**Watchdog flow:** No cycle event for **4+ hours** (configurable) while sprint work remains → `watchdog_recovery` → PM wakes to diagnose and re-dispatch.

The watchdog is **not** a replacement for event-driven PM. It is insurance against:

- Worker forgot `pm_emit_cycle_event.sh`
- Cloud Agent hung mid-session
- Webhook failed but work completed
- PM orchestrator failed and nobody retried

---

## 2. What gets monitored

| Signal | Source | Threshold (default) |
|--------|--------|----------------------|
| Last cycle event | `artifacts/factory_cycle_log.jsonl` | 4h idle → **stalled** |
| Issue `in_progress` | `sprint_board.json` | 24h → **stale_agent** |
| Agent heartbeat | `artifacts/factory_heartbeat.json` | 6h gap → **no_heartbeat** |
| Orchestrator result | `artifacts/factory_state.json` | last run **fail** |
| Factory halt flag | `artifacts/factory_state.json` | `halted: true` → stop all recovery |

Config: `game/data/qa/factory_watchdog.json`

---

## 3. Commands

```bash
# Analyze only (CI + manual health check)
bash tools/run_factory_watchdog.sh

# JSON report
bash tools/run_factory_watchdog.sh --json

# Trigger recovery (posts watchdog_recovery to PM webhook if unhealthy)
bash tools/run_factory_watchdog.sh --recover

# Human emergency stop
bash tools/run_factory_watchdog.sh --halt "reason for stop"

# Resume after human fix
bash tools/run_factory_watchdog.sh --clear-halt
```

Worker agents should emit heartbeats during long sessions:

```bash
bash tools/pm_record_heartbeat.sh --agent builder --issue P1-02 --phase progress --note "GDAI scene pass"
```

Session gate and PM orchestrator record **start** heartbeats automatically.

---

## 4. Recovery behavior

When `--recover` runs and health is not OK:

1. Check `factory_halt` — if set, **STOP** (human only)
2. Check recovery cooldown (default 2h since last recovery)
3. Check per-issue attempt cap (default 3) and per-sprint cap (12)
4. Escalate stale issues (`pm_emit_escalation.sh … S2`)
5. Emit `watchdog_recovery` via `pm_emit_cycle_event.sh` → **same PM webhook** as normal cycles
6. PM Automation runs `run_pm_orchestrator.sh` and re-dispatches

If recovery attempts are exhausted → **factory_halt** + optional `CURSOR_FACTORY_ALERT_WEBHOOK_URL` alert.

---

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
5. On fix: bash tools/pm_emit_cycle_event.sh agent_cycle_complete ...
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

- `docs/CLOUD_AGENT_SETUP_RUNBOOK.md` — full Cloud Agent setup
- `docs/PM_AGENT_RUNBOOK.md` — PM session steps
- `docs/SPRINT_ORCHESTRATION.md` — escalation ladder
