---
id: cursor-api
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 466
summary: "What it is: User API key for the Cursor Cloud Agents API — enables fully automatic token usage logging in agent session telemetry (`docs/ops/qa/AGENT_SESSION_TE"
---
# Secrets — API Keys — CURSOR_API_KEY

**Hub:** [`api_keys.md`](../api_keys.md)

## When to read

Use **Secrets — API Keys — CURSOR_API_KEY** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [8. `CURSOR_API_KEY`](#8-cursor_api_key)
- [Steps (one-time setup)](#steps-one-time-setup)
- [How auto token logging works](#how-auto-token-logging-works)


## 8. `CURSOR_API_KEY`

**What it is:** User API key for the **Cursor Cloud Agents API** — enables **fully automatic** token usage logging in agent session telemetry (`docs/ops/qa/AGENT_SESSION_TELEMETRY.md`). Without this key, sessions log duration/role/task but `tokens_total` stays empty.

### Steps (one-time setup)

1. Open [cursor.com/dashboard](https://cursor.com/dashboard) → **Settings** → **API Keys** (or **Integrations** → API)
2. **Create API key** — user API key or service account key (not Team Admin key)
3. Copy key (`crsr_...` or similar)
4. Cursor **Cloud Agents → Environment → Secrets** → add `CURSOR_API_KEY`
5. Scope: **Personal + Runtime Secret**
6. Verify:

```bash
bash tools/check_agent_telemetry_ready.sh
# Optional live test (on a cloud agent with CURSOR_CONVERSATION_ID set):
python3 tools/collect_cursor_agent_usage.py --retries 3
```

### How auto token logging works

| Step | What happens |
|------|----------------|
| Session start | `run_agent_session_gate.sh` records `CURSOR_CONVERSATION_ID` as `cursor_bc_id` + usage baseline |
| Session end | `pm_emit_cycle_event.sh` calls `GET /v1/agents/{bcId}/usage` with retries |
| Backfill | `pm_sync_agent_session_tokens.py` fills any sessions where usage lagged |

No manual `export AGENT_TOKENS_*` needed when this key is set.

**API docs:** [Cloud Agents API — Get Agent Usage](https://cursor.com/docs/cloud-agent/api/endpoints#get-agent-usage)

---
