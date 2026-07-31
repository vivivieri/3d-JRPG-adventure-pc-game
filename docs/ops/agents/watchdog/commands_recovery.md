---
id: commands-recovery
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 431
summary: "Commands + recovery behavior"
---
# Factory Watchdog — Commands + recovery behavior

**Hub:** [`FACTORY_WATCHDOG.md`](../FACTORY_WATCHDOG.md)

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

On every run, the watchdog also calls `pm_refresh_agent_telemetry.sh` (non-blocking) to backfill token usage when the Cursor API lagged. See `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` §9.

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
