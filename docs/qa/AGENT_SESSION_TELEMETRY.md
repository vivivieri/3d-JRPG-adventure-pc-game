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

## 4. Token reporting (automatic)

When `CURSOR_API_KEY` is set in Cursor Secrets (one-time setup — `docs/agents/CURSOR_SECRETS_SETUP.md` §8), tokens are fetched **automatically** from the Cursor Cloud Agents API:

```
GET https://api.cursor.com/v1/agents/{bcId}/usage
```

| Step | Auto? | Mechanism |
|------|-------|-----------|
| Detect cloud agent id | Yes | `CURSOR_CONVERSATION_ID` env (injected on every cloud agent) |
| Session start baseline | Yes | API call at `session_start` |
| Session end tokens | Yes | API call with 3 retries at `session_end` |
| Delta per session | Yes | end usage − start baseline |
| Backfill if API lags | Yes | `pm_refresh_agent_telemetry.sh` on cycle complete, orchestrator, watchdog |

### One-time setup (you)

Add **one** secret in Cursor Cloud Agents → Environment → Secrets:

| Secret | Where to get it | Scope |
|--------|-----------------|-------|
| `CURSOR_API_KEY` | [cursor.com/dashboard](https://cursor.com/dashboard) → Settings → API Keys | Personal + Runtime Secret |

Everything else is automatic — `CURSOR_CONVERSATION_ID` is injected on every cloud agent; no per-session config.

Verify setup:

```bash
bash tools/check_agent_telemetry_ready.sh
bash tools/check_day_one_secrets.sh   # includes CURSOR_API_KEY
```

### Manual fallback (only if API unavailable)

```bash
export AGENT_TOKENS_TOTAL=225000 AGENT_TOKENS_SOURCE=manual
```

Or write `artifacts/agent_session_telemetry/session_enrichment.json` before session end.

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
| `factory_analytics` | analyst | Token/duration rollups, efficiency studies |
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

**Drift prevention:** Feature is registered in `game/data/qa/workflow_integration_registry.json` — CI gate `L0_workflow_integration` fails if hooks or doc cross-refs drift. See `docs/qa/WORKFLOW_INTEGRATION.md`.
