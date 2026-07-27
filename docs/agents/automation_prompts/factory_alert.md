# Automation D — Factory human alert

You were triggered because the automated factory **STOPPED** or recovery was exhausted.

Read `artifacts/agent_cycle_event.json` and `artifacts/factory_health_report.json` if present.

## Your job

Notify the human product owner — **do NOT** start worker agents or run PM dispatch.

1. Summarize: event type, halt reason, last issue in progress, factory health status.
2. Link `artifacts/factory_health_report.json` and sprint board blockers.
3. Tell the human: fix root cause → `bash tools/run_factory_watchdog.sh --clear-halt` → restart PM manually.

**Never** run `run_pm_orchestrator.sh` to dispatch builders without human confirmation.

Authority: `docs/agents/FACTORY_WATCHDOG.md` §5
