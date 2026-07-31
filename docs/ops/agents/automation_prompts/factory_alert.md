---
id: automation-d-factory-human-alert
type: reference
status: active
summary: "Automation D — Factory human alert — project reference"
tokens_est: 182
---
# Automation D — Factory human alert

## When to read

Use **Automation D — Factory human alert** when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



## Your job

Notify the human product owner — **do NOT** start worker agents or run PM dispatch.

1. Summarize: event type, halt reason, last issue in progress, factory health status.
2. Link `artifacts/factory_health_report.json` and sprint board blockers.
3. Tell the human: fix root cause → `bash tools/run_factory_watchdog.sh --clear-halt` → restart PM manually.

**Never** run `run_pm_orchestrator.sh` to dispatch builders without human confirmation.

Authority: `docs/ops/agents/FACTORY_WATCHDOG.md` §5
