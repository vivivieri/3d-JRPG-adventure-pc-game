---
id: webhooks
type: how-to
audience: [pm, builder, release]
phase: [0, 1]
status: active
authority: agents
tokens_est: 1067
summary: "PM / alert / worker webhooks"
---
# Cursor Secrets Setup — PM / alert / worker webhooks

**Hub:** [`CURSOR_SECRETS_SETUP.md`](../CURSOR_SECRETS_SETUP.md)

## 2. `CURSOR_PM_CYCLE_WEBHOOK_URL`

**What it is:** The inbound webhook URL for **Automation A — PM cycle dispatch**. Workers and `pm_emit_cycle_event.sh` POST here when a cycle completes; PM wakes in seconds.

### Steps

1. Open [cursor.com/automations](https://cursor.com/automations) → **New automation**
2. **Name:** `PM — cycle dispatch`
3. **Repo:** `3d-JRPG-adventure-pc-game` · **Branch:** `game/development`
4. **Trigger:** **Webhook** only — **no schedule**
5. **Agent instructions:** paste from `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` §4 Automation A (includes watchdog recovery branch)
6. **Tools:** remove Memories; Godot MCPs not needed for PM
7. **Save** → set **Active**
8. **Triggers** → copy the webhook URL (`https://api2.cursor.sh/auto...`)
9. **Triggers** → **Generate auth header** → copy value → Cursor secret `CURSOR_PM_WEBHOOK_AUTH` (format: `Bearer …`)
10. Cursor environment **Secrets** → `CURSOR_PM_CYCLE_WEBHOOK_URL` → paste URL
11. GitHub repo **Secrets** → same names/values for URL + auth

### Test

```bash
bash tools/curl_cursor_webhook.sh pm @artifacts/agent_cycle_event.json
```

Or full cycle:

```bash
# Full enforced cycle (production workers):
bash tools/run_post_agent_cycle.sh --issue P1-00 --agent pm --commit $(git rev-parse HEAD) --note "webhook test"

# Webhook-only smoke test (low-level — skips done criteria / evidence):
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-00 --agent pm --note "webhook test"
```

Expect PM Automation to start within seconds. If HTTP 401, re-copy URL + **Generate auth header** from automation settings.

**Full prompt + watchdog branch:** `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` §4 · `docs/ops/agents/FACTORY_WATCHDOG.md` §5

---


## 3. `CURSOR_FACTORY_ALERT_WEBHOOK_URL`

**What it is:** Separate webhook for **Automation D — Factory human alert**. Fires on `factory_halt`, `mcp_blocked`, recovery exhausted — **not** normal cycle dispatch.

### Steps

1. [cursor.com/automations](https://cursor.com/automations) → **New automation** (second automation — different from PM)
2. **Name:** `Factory — human alert`
3. **Repo / branch:** same as PM automation
4. **Trigger:** **Webhook** only — **no schedule**
5. **Agent instructions:**

```text
You are the Factory Alert agent for Tides of Urashima.

You were triggered because the automated factory STOPPED or recovery was exhausted.
Read artifacts/agent_cycle_event.json and artifacts/factory_health_report.json if present.

YOUR JOB: notify the human product owner — do NOT start worker agents or run PM dispatch.

1. Summarize: event type, halt reason, last issue in progress, factory health status.
2. Link artifacts/factory_health_report.json and sprint_board blockers.
3. Tell the human: fix root cause → bash tools/run_factory_watchdog.sh --clear-halt → restart PM manually.

NEVER: run_pm_orchestrator.sh to dispatch builders or clear halt without human confirmation.
```

6. **Tools:** no MCP required
7. **Save** → **Active**
8. Copy webhook URL → `CURSOR_FACTORY_ALERT_WEBHOOK_URL`
9. **Generate auth header** → `CURSOR_ALERT_WEBHOOK_AUTH`
10. GitHub repo **Secrets** → same URL + auth names

### Test (optional)

```bash
bash tools/run_factory_watchdog.sh --halt "test alert — ignore"
bash tools/run_factory_watchdog.sh --clear-halt
```

**Cross-ref:** `docs/ops/agents/FACTORY_WATCHDOG.md` §5 Automation D

---


## 3b. `CURSOR_WORKER_WEBHOOK_URL` + `CURSOR_WORKER_WEBHOOK_AUTH`

**What it is:** Webhook for **Automation E — Worker**. GitHub Actions `worker-dispatch.yml` POSTs here when issue labeled `dispatch/ready`.

1. Automation E → **Triggers** → copy webhook URL → `CURSOR_WORKER_WEBHOOK_URL`
2. **Generate auth header** → `CURSOR_WORKER_WEBHOOK_AUTH`
3. Mirror both in GitHub Actions secrets (`bash tools/setup_github_actions_secrets.sh`)

Test:

```bash
gh issue edit 129 --add-label dispatch/ready
# or
bash tools/curl_cursor_webhook.sh worker @artifacts/worker_dispatch_event.json
```

---
