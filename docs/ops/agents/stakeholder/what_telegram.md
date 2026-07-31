---
id: what-telegram
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 468
summary: "What you get + Telegram setup"
---
# PM Stakeholder Reporting — What you get + Telegram setup

**Hub:** [`PM_STAKEHOLDER_REPORTING.md`](../PM_STAKEHOLDER_REPORTING.md)

## 1. What you get

After each **micro cycle** (issue done), **sprint cycle**, or **phase exit**, the PM stack generates:

| Output | Path |
|--------|------|
| JSON report | `artifacts/stakeholder_reports/latest.json` |
| Markdown | `artifacts/stakeholder_reports/latest.md` |
| HTML dashboard | `artifacts/stakeholder_dashboard.html` |
| Timestamped history | `artifacts/stakeholder_reports/<timestamp>_<kind>.json` |

**Telegram** (optional): compact HTML message to your chat when secrets are set.

---


## 2. One-time Telegram setup

### Step 1 — Create a bot

1. Open Telegram → message [@BotFather](https://t.me/BotFather)
2. `/newbot` → follow prompts → copy **bot token**

### Step 2 — Get your chat ID

1. Message your new bot once (any text)
2. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}` → that is **TELEGRAM_CHAT_ID**

Or message [@userinfobot](https://t.me/userinfobot) for your user id (use for private chats with bot).

### Step 3 — Cursor / GitHub Secrets

**Full day-one guide:** `docs/ops/agents/CURSOR_SECRETS_SETUP.md` §6

| Secret | Value |
|--------|--------|
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your numeric chat id |

Add to **Cursor Cloud Agents → Secrets** and **GitHub repo Secrets** (for CI workflows).

### Step 4 — Test

```bash
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
bash tools/pm_emit_stakeholder_report.sh --trigger agent_cycle_complete --issue P1-00 --agent pm --telegram
```

You should receive a message on Telegram within seconds.

---
