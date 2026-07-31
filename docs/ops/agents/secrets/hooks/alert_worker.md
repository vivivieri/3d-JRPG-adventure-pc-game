---
id: alert-worker
type: how-to
audience: [pm, builder]
status: active
authority: ops
tokens_est: 616
summary: "Alert + worker webhooks"
---
# Secrets — Webhooks — Alert + worker webhooks

**Hub:** [`webhooks.md`](../webhooks.md)

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
