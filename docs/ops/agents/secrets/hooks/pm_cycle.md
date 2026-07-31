---
id: pm-cycle
type: how-to
audience: [pm, builder]
status: active
authority: ops
tokens_est: 531
summary: "The inbound webhook URL for **Automation A — PM cycle dispatch**. Workers and `pm_emit_cycle_event.sh` POST here when a cycle completes; PM wakes in seconds."
---
# Secrets — Webhooks — PM cycle webhook

**Hub:** [`webhooks.md`](../webhooks.md)

## When to read

Use **Secrets — Webhooks — PM cycle webhook** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [2. `CURSOR_PM_CYCLE_WEBHOOK_URL`](#2-cursor_pm_cycle_webhook_url)
- [Steps](#steps)
- [Test](#test)


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
