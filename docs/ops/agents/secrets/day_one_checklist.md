---
id: day-one-checklist
type: how-to
audience: [pm, builder, release]
phase: [0, 1]
status: active
authority: agents
tokens_est: 658
summary: "(Settings → Secrets and variables → Actions):"
---
# Cursor Secrets Setup — Day-one checklist

**Hub:** [`CURSOR_SECRETS_SETUP.md`](../CURSOR_SECRETS_SETUP.md)

## When to read

Use **Cursor Secrets Setup — Day-one checklist** (roles: pm, builder, release) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



## 1. Day-one checklist (all compulsory)

| Secret | Purpose | How to get (section) |
|--------|---------|----------------------|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | Event-driven PM dispatch | [§2](#2-cursor_pm_cycle_webhook_url) |
| `CURSOR_PM_WEBHOOK_AUTH` | Auth header for Automation A webhook | [§2](#2-cursor_pm_cycle_webhook_url) |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | Factory halt / human alert | [§3](#3-cursor_factory_alert_webhook_url) |
| `CURSOR_ALERT_WEBHOOK_AUTH` | Auth header for Automation D webhook | [§3](#3-cursor_factory_alert_webhook_url) |
| `CURSOR_WORKER_WEBHOOK_URL` | Worker dispatch (Automation E) | [§3b](#3b-cursor_worker_webhook) |
| `CURSOR_WORKER_WEBHOOK_AUTH` | Auth header for Automation E webhook | [§3b](#3b-cursor_worker_webhook) |
| `GAMELAB_API_KEY` | GameLab MCP — UI art generation | [§4](#4-gamelab_api_key) |
| `GH_TOKEN` | `gh` CLI, issue sync, GitHub Actions dispatch | [§5](#5-gh_token) |
| `TELEGRAM_BOT_TOKEN` | Stakeholder status → product owner | [§6](#6-telegram_bot_token--telegram_chat_id) |
| `TELEGRAM_CHAT_ID` | Your Telegram chat id | [§6](#6-telegram_bot_token--telegram_chat_id) |
| `ELEVENLABS_API_KEY` | Selective VO generation (12 clips) | [§7](#7-elevenlabs_api_key) |
| `CURSOR_API_KEY` | **Auto agent token telemetry** (Cloud Agents usage API) | [§8](#8-cursor_api_key) |

**Also add to GitHub repo Secrets** (Settings → Secrets and variables → Actions):

| Secret | Why |
|--------|-----|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | `.github/workflows/agent-cycle-pm.yml`, `factory-watchdog.yml`, CI triage |
| `CURSOR_PM_WEBHOOK_AUTH` | Same workflows + `tools/curl_cursor_webhook.sh pm` |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | `factory-watchdog.yml` when recovery exhausted |
| `CURSOR_ALERT_WEBHOOK_AUTH` | `tools/curl_cursor_webhook.sh alert` |
| `CURSOR_WORKER_WEBHOOK_URL` | `.github/workflows/worker-dispatch.yml` (Automation E bridge) |
| `CURSOR_WORKER_WEBHOOK_AUTH` | `tools/curl_cursor_webhook.sh worker` |
| `TELEGRAM_BOT_TOKEN` | CI stakeholder reports (if workflow sends Telegram) |
| `TELEGRAM_CHAT_ID` | Same |

After Cursor Secrets are set, sync into GitHub Actions (needs `GH_TOKEN` with **Secrets: Read and write**):

```bash
bash tools/setup_github_actions_secrets.sh
```

Verify after setup:

```bash
bash tools/check_day_one_secrets.sh
```

---
