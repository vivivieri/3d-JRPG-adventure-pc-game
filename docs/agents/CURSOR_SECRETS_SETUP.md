# Cursor Secrets — Day-One Setup (How to Get Every Key)

**Version:** 1.0  
**Authority:** All secrets below are **compulsory on day one** before starting the Cloud Agent factory on `game/development`.  
**Where to add:** Cursor **Cloud Agents → your environment → Secrets** — scope **Personal + Runtime Secret** for each.  
**Cross-refs:** `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md`, `docs/agents/PM_STAKEHOLDER_REPORTING.md`, `docs/ci-cd/GITHUB_SETUP.md`, `docs/agents/MCP_STACK.md`, `docs/vision/VO_HIT_LIST.md`

---

## 1. Day-one checklist (all compulsory)

| Secret | Purpose | How to get (section) |
|--------|---------|----------------------|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | Event-driven PM dispatch | [§2](#2-cursor_pm_cycle_webhook_url) |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | Factory halt / human alert | [§3](#3-cursor_factory_alert_webhook_url) |
| `GAMELAB_API_KEY` | GameLab MCP — UI art generation | [§4](#4-gamelab_api_key) |
| `GH_TOKEN` | `gh` CLI, issue sync, GitHub Actions dispatch | [§5](#5-gh_token) |
| `TELEGRAM_BOT_TOKEN` | Stakeholder status → product owner | [§6](#6-telegram_bot_token--telegram_chat_id) |
| `TELEGRAM_CHAT_ID` | Your Telegram chat id | [§6](#6-telegram_bot_token--telegram_chat_id) |
| `ELEVENLABS_API_KEY` | Selective VO generation (12 clips) | [§7](#7-elevenlabs_api_key) |

**Also add to GitHub repo Secrets** (Settings → Secrets and variables → Actions):

| Secret | Why |
|--------|-----|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | `.github/workflows/agent-cycle-pm.yml`, `factory-watchdog.yml`, CI triage |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | `factory-watchdog.yml` when recovery exhausted |
| `TELEGRAM_BOT_TOKEN` | CI stakeholder reports (if workflow sends Telegram) |
| `TELEGRAM_CHAT_ID` | Same |

Verify after setup:

```bash
bash tools/check_day_one_secrets.sh
```

---

## 2. `CURSOR_PM_CYCLE_WEBHOOK_URL`

**What it is:** The inbound webhook URL for **Automation A — PM cycle dispatch**. Workers and `pm_emit_cycle_event.sh` POST here when a cycle completes; PM wakes in seconds.

### Steps

1. Open [cursor.com/automations](https://cursor.com/automations) → **New automation**
2. **Name:** `PM — cycle dispatch`
3. **Repo:** `3d-JRPG-adventure-pc-game` · **Branch:** `game/development`
4. **Trigger:** **Webhook** only — **no schedule**
5. **Agent instructions:** paste from `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` §4 Automation A (includes watchdog recovery branch)
6. **Tools:** remove Memories; Godot MCPs not needed for PM
7. **Save** → set **Active**
8. **Triggers** → copy the webhook URL (`https://api2.cursor.sh/auto...`)
9. Cursor environment **Secrets** → name `CURSOR_PM_CYCLE_WEBHOOK_URL` → paste URL
10. GitHub repo **Secrets** → same name, same URL

### Test

```bash
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-00 --agent pm --note "webhook test"
```

Expect PM Automation to start within seconds. If HTTP 401, re-copy URL from automation settings (webhook may have rotated).

**Full prompt + watchdog branch:** `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` §4 · `docs/agents/FACTORY_WATCHDOG.md` §5

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
8. Copy webhook URL → Cursor secret `CURSOR_FACTORY_ALERT_WEBHOOK_URL`
9. GitHub repo **Secrets** → same name, same URL

### Test (optional)

```bash
bash tools/run_factory_watchdog.sh --halt "test alert — ignore"
bash tools/run_factory_watchdog.sh --clear-halt
```

**Cross-ref:** `docs/agents/FACTORY_WATCHDOG.md` §5 Automation D

---

## 4. `GAMELAB_API_KEY`

**What it is:** API key for **GameLab Studio MCP** (`gamelab-mcp`) — ink-wash UI frames, combat icon sheets, menu borders.

### Steps

1. Sign up at [gamelabstudio.co](https://gamelabstudio.co/)
2. Dashboard / account → **API key** (or developer settings)
3. Copy the key
4. Cursor **Secrets** → `GAMELAB_API_KEY` → paste key
5. **Dashboard → Integrations & MCP** → register **gamelab-mcp** (SSE) if not already listed
6. Re-run on environment:

```bash
bash tools/install_extended_toolchain.sh
bash tools/check_extended_toolchain.sh
```

Automation **Builder** agents: **Tools → MCP ON → + Add Tool or MCP → gamelab-mcp**.

**Cross-ref:** `docs/agents/MCP_STACK.md` § GameLab Studio MCP · `docs/art/ART_AUTOMATION_PIPELINE.md`

---

## 5. `GH_TOKEN`

**What it is:** GitHub fine-grained personal access token for shell `gh`, `pm_sync_github_issues.py`, `repository_dispatch`, and `setup_github_project.sh` (labels, branch protection).

> Cursor’s built-in GitHub integration ≠ `gh` in the Cloud Agent VM. **`GH_TOKEN` is required day one** for factory scripts.

### Steps

1. GitHub → **Settings** → **Developer settings** → **Fine-grained personal access tokens** → **Generate**
2. **Repository access:** Only `vivivieri/3d-JRPG-adventure-pc-game` (or your fork)
3. **Permissions:**

| Permission | Access |
|------------|--------|
| Issues | Read and write |
| Pull requests | Read and write |
| Actions | Read |
| Contents | Read (and write if agents push via `gh`) |
| Administration | Read and write *(branch protection via setup script)* |

4. Generate → copy token (`github_pat_...` or classic `ghp_...`)
5. Cursor **Secrets** → `GH_TOKEN` → paste token
6. Verify:

```bash
export GH_TOKEN="your_token"
gh auth status
bash tools/setup_github_project.sh --dry-run
```

**Cross-ref:** `docs/ci-cd/GITHUB_SETUP.md` §1

---

## 6. `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`

**What it is:** Sends compact HTML status to the product owner after each cycle, sprint close, watchdog recovery, and MCP block.

### `TELEGRAM_BOT_TOKEN`

1. Open Telegram → message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow prompts (bot display name + username ending in `bot`)
4. Copy the **HTTP API token** BotFather returns (`123456789:ABCdef...`)
5. Cursor **Secrets** → `TELEGRAM_BOT_TOKEN`

### `TELEGRAM_CHAT_ID`

1. Message your new bot once (any text)
2. Open in browser (replace `<TOKEN>`):

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. Find `"chat":{"id":123456789}` → that number is **`TELEGRAM_CHAT_ID`**

Alternative: message [@userinfobot](https://t.me/userinfobot) for your user id (private chat with bot).

4. Cursor **Secrets** → `TELEGRAM_CHAT_ID` → paste numeric id (no quotes in UI)
5. Optional: GitHub repo Secrets for CI workflows

### Test

```bash
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
bash tools/pm_emit_stakeholder_report.sh --trigger agent_cycle_complete --issue P1-00 --agent pm --telegram
```

**Cross-ref:** `docs/agents/PM_STAKEHOLDER_REPORTING.md` §2

---

## 7. `ELEVENLABS_API_KEY`

**What it is:** API key for **selective VO** — 12 emotional clips only (`docs/vision/VO_HIT_LIST.md`), not full dialogue.

### Steps

1. Create account at [elevenlabs.io](https://elevenlabs.io)
2. **Profile** → **API keys** (or Settings → API) → **Create API key**
3. Copy key
4. Cursor **Secrets** → `ELEVENLABS_API_KEY`
5. (Before first generate) Update voice IDs in `game/data/audio/vo_prompts.json` per casting notes
6. Verify:

```bash
bash tools/generate_ai_vo.sh --list
bash tools/generate_ai_vo.sh --tier p0 --locale en --dry-run
```

Remove `--dry-run` when ready to generate. Log commercial terms in `docs/art/LICENSES.md` before ship.

**Cross-ref:** `docs/vision/VO_HIT_LIST.md` § AI VO setup · `docs/audio/AUDIO_PRODUCTION_GUIDE.md`

---

## 8. Secret scope and placement

| Setting | Value |
|---------|--------|
| **Scope** | Personal + Runtime Secret *(each secret)* |
| **Cursor environment** | All 7 secrets above |
| **GitHub Actions** | At minimum both webhook URLs; Telegram if CI sends reports |

Do **not** commit secrets to git. Do **not** paste tokens in issues, PRs, or agent prompts.

---

## 9. What is *not* day one (later phases)

| Secret | When |
|--------|------|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` | M5+ visual/model/audio jury scripts |
| GDAI license / plugin zip | Phase 1+ scene work (commercial — separate from this list) |
| `GODOT_SCRIPT_ENCRYPTION_KEY` | M6 RC ship export — PCK encryption (GitHub `steam-production` only) |
| `GODOT_SAVE_HMAC_KEY` | M6 RC ship export — save-slot HMAC pepper (same environment) |
| Steam API keys | Phase 8 only |

Generate ship keys (store output in GitHub Secrets — never commit):

```bash
bash tools/generate_ship_protection_keys.sh
```

See `docs/qa/SECURITY.md` §9 for custom template build + `SHIP_RELEASE=1` export flow.

---

## 10. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `check_day_one_secrets.sh` FAIL | Re-read section for missing secret; confirm Runtime Secret scope |
| PM never wakes after cycle | `CURSOR_PM_CYCLE_WEBHOOK_URL` wrong or automation Inactive |
| No halt alert | `CURSOR_FACTORY_ALERT_WEBHOOK_URL` missing or Factory automation Inactive |
| `gh: not authenticated` | Set `GH_TOKEN`; run `gh auth status` |
| GameLab MCP missing | `GAMELAB_API_KEY` + Integrations & MCP + `write_mcp_config.sh` |
| Telegram silent | Message bot first; verify chat id via `getUpdates` |
| ElevenLabs 401 | Regenerate key; check account credits |

---

## 11. Cross-refs

- `docs/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — automations + factory architecture
- `docs/agents/FACTORY_WATCHDOG.md` — alert vs PM webhooks
- `docs/agents/PM_STAKEHOLDER_REPORTING.md` — Telegram report content
- `docs/ci-cd/GITHUB_SETUP.md` — labels, environments, branch protection
- `AGENTS.md` — cloud bootstrap order
