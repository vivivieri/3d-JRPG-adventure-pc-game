# Agent Session Telemetry — AI Factory Efficiency Studies

**Discipline:** Dev-time factory analytics — measure agent performance by role, task category, and issue  
**Status:** Active on `main` + `game/development` — hooks wired into session gate, heartbeat, and cycle events  
**Authority:** `game/data/qa/agent_session_telemetry_schema.json`  
**Analyzer:** `python3 tools/analyze_agent_session_telemetry.py`

This is **not** a ship gate. It exists so you can study which task types cost the most time/tokens and tune dispatch, prompts, and issue sizing after the game ships.

---

## 1. What gets logged

Every agent session produces **append-only JSONL** events:

| Event | When | Purpose |
|-------|------|---------|
| `session_start` | `run_agent_session_gate.sh` PASS (or PM orchestrator) | Open session, capture dispatch context |
| `session_progress` | `pm_record_heartbeat.sh` | Heartbeats + optional notes |
| `session_end` | `pm_emit_cycle_event.sh agent_cycle_complete` | Success rollup |
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
| `run_pm_orchestrator.sh` | PM `session_start` |

Manual CLI:

```bash
bash tools/pm_record_agent_session.sh start --agent builder --issue P1-02
bash tools/pm_record_agent_session.sh progress --agent builder --issue P1-02 --note "GDAI fog tuned"
bash tools/pm_record_agent_session.sh end --agent builder --issue P1-02 --outcome complete
```

---

## 4. Token reporting

Cursor does not yet expose per-session token counts to repo scripts automatically. Three paths:

### A. Environment variables (recommended at session end)

```bash
export AGENT_TOKENS_INPUT=180000
export AGENT_TOKENS_OUTPUT=45000
export AGENT_TOKENS_TOTAL=225000
export AGENT_TOKENS_SOURCE=cursor_dashboard
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-02 --agent builder --commit <sha>
```

### B. Enrichment file

Write `artifacts/agent_session_telemetry/session_enrichment.json` before `session_end`:

```json
{
  "tokens_input": 180000,
  "tokens_output": 45000,
  "tokens_total": 225000,
  "tool_calls_reported": 42
}
```

### C. Cursor dashboard (post-hoc)

Export usage from [cursor.com/agents](https://cursor.com/agents) and join on `cursor_bc_id` + `started_at` in your analysis tool.

---

## 5. Analysis

```bash
# Live log
python3 tools/analyze_agent_session_telemetry.py

# Sample data
python3 tools/analyze_agent_session_telemetry.py game/data/qa/examples/agent_session_telemetry_sample.jsonl

# Export paths
python3 tools/analyze_agent_session_telemetry.py --json /tmp/report.json --csv /tmp/sessions.csv
```

### Study dimensions (from schema)

- `agent_role` — architect vs builder vs qa efficiency
- `task_category` — scene_build vs spec_architecture vs qa_verification
- `task_tags` — shader, zone, gdai, etc.
- `issue_id` — per-task cost
- `model_name` — model A vs B comparisons
- `outcome` — fail rate by category

### Efficiency questions to answer after ship

1. Which `task_category` has the highest median `tokens_total`?
2. Which issues needed more than one session (remediation flags)?
3. Do builder sessions with more heartbeats correlate with fewer CI failures?
4. Can we split large issues (high duration + high tokens) into smaller dispatch packets?

Feed findings back into:
- `sprint_board.json` issue sizing
- `docs/agents/MULTI_AGENT_TEAM.md` handoff contracts
- Prompt templates / MCP usage policy

---

## 6. Task categories

| ID | Typical role | Use for |
|----|--------------|---------|
| `pm_orchestration` | pm | Orchestrator overhead |
| `spec_architecture` | architect | Shaders, GDScript, plans |
| `scene_build` | builder | GDAI `.tscn` work |
| `qa_verification` | qa | Gate runs |
| `flow_integration` | flow | L4/L5 scenarios |
| `visual_jury` | visual | Art/model jury |
| `release_cd` | release | Tags, Steam CD |
| `bootstrap` | pm/architect | P1-00 setup |
| `docs_data` | any | Main-branch docs/data |
| `remediation` | any | QA FAIL retries |
| `other` | fallback | Unclassified |

Categories are inferred from `agent_role`, issue title, and `implementation_plan_tasks`.

---

## 7. Privacy

- Raw logs stay **local** under `artifacts/` (gitignored)
- No API keys, emails, or webhook URLs in telemetry
- `cursor_bc_id` is an opaque agent run id — join to Cursor dashboard only with consent
- Do not upload telemetry to third-party analytics without a privacy notice

---

## 8. Cross-refs

- `docs/agents/SPRINT_ORCHESTRATION.md` — dispatch + cycle events
- `docs/agents/FACTORY_WATCHDOG.md` — heartbeat stall detection
- `docs/qa/PLAYTEST_TELEMETRY.md` — in-game playtest analytics (separate)
- `docs/workflow/DEVELOPMENT_LIFECYCLE.md` — full factory workflow
