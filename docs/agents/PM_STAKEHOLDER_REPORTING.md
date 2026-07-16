# PM Stakeholder Reporting — Product Owner Status Dashboard

**Version:** 1.0  
**Audience:** Product Owner (stakeholder)  
**Authority:** Mandatory PM duty after each cycle, sprint close, and phase exit.  
**Cross-refs:** `docs/agents/PM_AGENT_RUNBOOK.md`, `game/data/qa/stakeholder_report_config.json`

---

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

**Full day-one guide:** `docs/agents/CURSOR_SECRETS_SETUP.md` §6

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

## 3. When reports fire (automatic)

| Event | Telegram default | Report kind |
|-------|------------------|-------------|
| `agent_cycle_complete` | **Yes** | micro_cycle |
| `agent_cycle_failed` | **Yes** | failure alert |
| `sprint_cycle_complete` | **Yes** | sprint summary |
| `phase_exit` | **Yes** | phase exit |
| `uat_ready` | **Yes** | UAT handoff |
| `watchdog_recovery` / `mcp_blocked` | **Yes** | factory alert |
| `pm_session` (orchestrator end) | No (artifacts only) | dispatch snapshot |

Wired in `tools/pm_emit_cycle_event.sh` — every cycle event emits a stakeholder report.

PM orchestrator step 10 writes `pm_session` report (dashboard refresh without Telegram spam).

---

## 4. PM manual commands

```bash
# After sprint review (P1-06) — phase exit to product owner
bash tools/pm_emit_stakeholder_report.sh --trigger phase_exit --telegram

# Force Telegram on any trigger
bash tools/pm_emit_stakeholder_report.sh --trigger pm_session --telegram

# Artifacts only
bash tools/pm_emit_stakeholder_report.sh --trigger agent_cycle_complete --issue P1-01 --agent architect --no-telegram
```

---

## 5. Report contents

- Sprint progress (% done, issue table)
- Active phase + exit gates
- Last cycle (issue, agent, commit)
- Next dispatch from orchestrator
- Factory health (watchdog, halt, session budget)
- Blockers / stale issues
- GitHub links

---

## 6. HTML dashboard

Open locally or download from Cloud Agent artifacts:

```bash
# After any report
xdg-open artifacts/stakeholder_dashboard.html   # Linux
open artifacts/stakeholder_dashboard.html       # macOS
```

Dark-themed single page — progress bar, issue table, full JSON for audit.

---

## 7. PM Agent duty (enforced)

After every worker cycle:

1. `pm_update_issue.py` → done
2. `pm_emit_cycle_event.sh agent_cycle_complete` → **includes stakeholder report + Telegram**
3. On sprint close: ensure `sprint_cycle_complete` event (Telegram sprint summary)
4. On phase review issue done: `pm_emit_stakeholder_report.sh --trigger phase_exit --telegram`

Skipping stakeholder report = incomplete PM handoff (cite `invalid_pass_patterns` in acceptance criteria).

---

## 8. Troubleshooting

| Symptom | Fix |
|---------|-----|
| No Telegram | Check `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`; message bot first |
| HTTP 400 Bad Request | HTML parse error — check BotFather token; try `--no-telegram` and read `latest.md` |
| Empty dashboard | Run `bash tools/run_pm_orchestrator.sh` first (populates orchestrator report) |
| Report not on cycle | Ensure `pm_emit_cycle_event.sh` ran (not manual git only) |

---

## 9. Cross-refs

- `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — Automation secrets
- `docs/agents/FACTORY_WATCHDOG.md` — factory health section in report
- `game/data/qa/stakeholder_report_config.json` — trigger toggles
