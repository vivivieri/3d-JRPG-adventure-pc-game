---
id: privacy-refs
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 779
summary: "Privacy, cross-refs, workflow coop"
---
# Agent Session Telemetry — Privacy, cross-refs, workflow coop

**Hub:** [`AGENT_SESSION_TELEMETRY.md`](../AGENT_SESSION_TELEMETRY.md)

## 7. Privacy

- Raw logs stay **local** under `artifacts/` (gitignored)
- No API keys, emails, or webhook URLs in telemetry
- `cursor_bc_id` is an opaque agent run id — join to Cursor dashboard only with consent
- Do not upload telemetry to third-party analytics without a privacy notice

---


## 8. Cross-refs

- `docs/ops/agents/SPRINT_ORCHESTRATION.md` — dispatch + cycle events
- `docs/ops/agents/FACTORY_WATCHDOG.md` — heartbeat stall detection
- `docs/ops/qa/PLAYTEST_TELEMETRY.md` — in-game playtest analytics (separate)
- `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md` — full factory workflow

---


## 9. Workflow cooperation (how other agents use this)

Agent session telemetry is **wired into the factory** — not a standalone tool. Every workflow below cooperates automatically when `CURSOR_API_KEY` is set.

### Integration map

| Workflow | Cooperates how |
|----------|----------------|
| **`run_agent_session_gate.sh`** | Opens session (`session_start`) + warns if `CURSOR_API_KEY` missing |
| **`pm_record_heartbeat.sh`** | Appends `session_progress` on every heartbeat |
| **`pm_emit_cycle_event.sh`** | Closes session, fetches tokens, enriches webhook payload, refreshes reports |
| **`run_pm_orchestrator.sh`** | PM session telemetry + step 11 `pm_refresh_agent_telemetry.sh` |
| **`run_sprint_preflight.sh`** | Warns if telemetry not ready before worker dispatch |
| **`run_factory_watchdog.sh`** | Non-blocking token backfill on every run |
| **`pm_bundle_evidence.py`** | Auto-links `session_*.json` into sprint evidence bundles |
| **`pm_emit_stakeholder_report.sh`** | Includes duration + tokens in stakeholder dashboard |
| **Factory Analyst** | Runs `analyze_agent_session_telemetry.py` for sprint efficiency studies |

### Mandatory worker contract

Every specialist agent session **must**:

1. **Start:** `bash tools/run_agent_session_gate.sh <role> <issue_id>` (telemetry opens automatically)
2. **During long work:** `bash tools/pm_record_heartbeat.sh --agent <role> --issue <id> --note "..."`
3. **End:** `bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha>`

Skipping step 3 leaves the session open and **no token data** — watchdog may fire `no_heartbeat`.

### PM contract

PM **must not** manually close telemetry. Orchestrator + cycle events handle it. After sprint review, PM or **Factory Analyst** may run:

```bash
python3 tools/analyze_agent_session_telemetry.py
```

### Not a ship gate

`L0_agent_session_telemetry` validates the **schema only** — missing tokens do not block merge. Efficiency data is for post-ship factory tuning.

**Drift prevention:** Feature is registered in `game/data/qa/workflow_integration_registry.json` — CI gate `L0_workflow_integration` fails if hooks or doc cross-refs drift. See `docs/ops/qa/WORKFLOW_INTEGRATION.md`.
