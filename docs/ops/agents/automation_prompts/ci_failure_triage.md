# Automation B — CI failure triage

Game CI failed on `game/development`.

1. Read `artifacts/agent_cycle_event.json` and the failed CI run logs.
2. Run `bash tools/qa_emit_remediation.sh` for the failing domain.
3. Re-dispatch the **same issue** — do not mark `done`.
4. Emit `agent_cycle_failed` if remediation needs a new worker cycle.

Do **not** skip orchestrator or mark gates PASS without evidence.

Authority: `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` §4 Automation B
