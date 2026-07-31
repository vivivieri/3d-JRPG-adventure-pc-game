---
id: what-storage-hooks
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 901
summary: "What logs, storage, hooks"
---
# Agent Session Telemetry — What logs, storage, hooks

**Hub:** [`AGENT_SESSION_TELEMETRY.md`](../AGENT_SESSION_TELEMETRY.md)

## 1. What gets logged

Every agent session produces **append-only JSONL** events:

| Event | When | Purpose |
|-------|------|---------|
| `session_start` | `run_agent_session_gate.sh` PASS (or PM orchestrator) | Open session, capture dispatch context |
| `session_progress` | `pm_record_heartbeat.sh` | Heartbeats + optional notes |
| `session_end` | `run_post_agent_cycle.sh` → `pm_emit_cycle_event.sh` | Success rollup |
| `session_failed` | `pm_emit_cycle_event.sh agent_cycle_failed` | Failure rollup |

### Captured attributes (raw data)

| Group | Fields |
|-------|--------|
| **Identity** | `session_id`, `issue_id`, `agent_role`, `sprint_id`, `phase` |
| **Task taxonomy** | `task_category`, `task_tags` (for pivots) |
| **Dispatch** | `acceptance_gate_ids`, `done_requires`, `branch_name`, `handoff_refs`, `implementation_plan_tasks` |
| **Cursor / model** | `cursor_bc_id`, `cursor_agent_url`, `model_name`, `model_provider` |
| **Git** | `commit_sha_start`, `commit_sha_end`, `git_branch`, `files_changed`, `lines_added`, `lines_removed` |
| **PR** | `pr_url`, `pr_number` |
| **Gates** | `gates_passed`, `gates_failed`, `ci_pass_count`, `ci_fail_count`, `failed_check` |
| **Timing** | `ts`, `t`, `duration_seconds`, `heartbeat_count` |
| **Tokens** | `tokens_input`, `tokens_output`, `tokens_total`, `tokens_cache_read`, `tokens_cache_write`, `tokens_source` |
| **Outcome** | `outcome` (`complete` / `failed` / `aborted`), `error_message`, `note` |

Token fields are **nullable** until reported — see section 4 below.

---


## 2. Storage layout (analysis-friendly)

```
artifacts/agent_session_telemetry/
  events.jsonl              # PRIMARY — append-only, one event per line (gitignored)
  active_sessions.json      # In-flight sessions (gitignored)

artifacts/sprint_evidence/<issue_id>/
  session_<uuid>.json       # Per-issue rollup with full event chain (gitignored)

artifacts/agent_session_reports/
  latest.json               # Analyzer output — rollups by role/category/issue
  sessions.csv              # Flat table — import to Excel/pandas/BI
  latest.md                 # Human summary
```

**Why JSONL + CSV:**
- JSONL = lossless raw stream; easy to `cat`, `jq`, DuckDB, BigQuery load
- CSV = flat session table for spreadsheets and pandas
- Optional Parquet: `analyze_agent_session_telemetry.py --parquet out.parquet`

Committed schema + sample only (no raw telemetry in git):

- `game/data/qa/agent_session_telemetry_schema.json`
- `game/data/qa/examples/agent_session_telemetry_sample.jsonl`

---


## 3. Automatic hooks

| Script | Telemetry action |
|--------|------------------|
| `run_agent_session_gate.sh` | `session_start` |
| `pm_record_heartbeat.sh` | `session_progress` |
| `pm_emit_cycle_event.sh` (complete/fail) | `session_end` / `session_failed` |
| `run_pm_orchestrator.sh` | PM `session_start` + end refresh |
| `pm_refresh_agent_telemetry.sh` | Token backfill + CSV/JSON/Markdown reports |
| `run_factory_watchdog.sh` | Non-blocking telemetry refresh on every run |

Manual CLI:

```bash
bash tools/pm_record_agent_session.sh start --agent builder --issue P1-02
bash tools/pm_record_agent_session.sh progress --agent builder --issue P1-02 --note "GDAI fog tuned"
bash tools/pm_record_agent_session.sh end --agent builder --issue P1-02 --outcome complete
```

---
