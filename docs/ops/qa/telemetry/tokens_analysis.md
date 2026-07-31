---
id: tokens-analysis
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 929
summary: "Token reporting, analysis, categories"
---
# Agent Session Telemetry — Token reporting, analysis, categories

**Hub:** [`AGENT_SESSION_TELEMETRY.md`](../AGENT_SESSION_TELEMETRY.md)

## 4. Token reporting (automatic)

When `CURSOR_API_KEY` is set in Cursor Secrets (one-time setup — `docs/ops/agents/CURSOR_SECRETS_SETUP.md` §8), tokens are fetched **automatically** from the Cursor Cloud Agents API:

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
- `docs/ops/agents/MULTI_AGENT_TEAM.md` handoff contracts
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
