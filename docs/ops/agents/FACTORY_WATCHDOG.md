---
id: factory-watchdog
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 236
summary: "Stall recovery — load layers, commands, or playbook"
---
# Factory Watchdog

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`layers_monitor.md`](watchdog/layers_monitor.md) | Two layers + what is monitored |
| [`commands_recovery.md`](watchdog/commands_recovery.md) | Commands + recovery behavior |
| [`automations_playbook.md`](watchdog/automations_playbook.md) | Automations, events, playbook, refs |
**Version:** 1.0
**Authority:** Exception layer on top of event-driven PM dispatch.
**Cross-refs:** `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md`, `docs/ops/agents/SPRINT_ORCHESTRATION.md`, `game/data/qa/factory_watchdog.json`

---

## Factory hooks (registry keywords)

- Cycle close: `bash tools/run_post_agent_cycle.sh`
- Telemetry refresh: `pm_refresh_agent_telemetry`

