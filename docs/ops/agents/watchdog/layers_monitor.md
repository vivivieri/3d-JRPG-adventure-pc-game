---
id: layers-monitor
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 444
summary: "Two layers + what is monitored"
---
# Factory Watchdog — Two layers + what is monitored

**Hub:** [`FACTORY_WATCHDOG.md`](../FACTORY_WATCHDOG.md)

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
| Token backfill | `artifacts/agent_session_telemetry/events.jsonl` | Sessions missing `tokens_total` → refreshed by watchdog |

Config: `game/data/qa/factory_watchdog.json`

---
