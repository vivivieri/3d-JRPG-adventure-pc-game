---
id: setup-automations
type: how-to
audience: [pm, builder]
phase: [0, 1]
status: active
authority: agents
tokens_est: 1876
summary: "[`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)"
---
# Cloud Agent Setup — One-time setup & automations

**Hub:** [`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)

## 3. One-time setup

### 3.1 Cloud environment snapshot

**Dashboard:** [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game)

Committed boot config:

```json
{
  "install": "bash tools/install_cloud_dev.sh",
  "start": "bash tools/ensure_mcp_stack.sh"
}
```

**Snapshot must include:**

- Godot 4.7 editor running (GDAI controls editor, not headless-only)
- `game/addons/gdai-mcp-plugin-godot/` (commercial — install before snapshot)
- Godotiq + MCP Pro built
- Blender, `uv`, Node
- `curl -sf http://127.0.0.1:3571/tools` returns JSON

See `docs/ops/agents/GDAI_CLOUD_SETUP.md` for plugin + panel **Start**.

### 3.2 Secrets (Cursor Cloud Agents → Secrets)

**Day-one compulsory (all 8):** see **`docs/ops/agents/CURSOR_SECRETS_SETUP.md`** — how to obtain each key, step by step. Verify: `bash tools/check_day_one_secrets.sh`.

| Secret | Day one | Purpose |
|--------|---------|---------|
| `CURSOR_PM_CYCLE_WEBHOOK_URL` | **Yes** | Automation A webhook URL |
| `CURSOR_PM_WEBHOOK_AUTH` | **Yes** | Automation A auth (`Generate auth header`) |
| `CURSOR_FACTORY_ALERT_WEBHOOK_URL` | **Yes** | Automation D webhook URL |
| `CURSOR_ALERT_WEBHOOK_AUTH` | **Yes** | Automation D auth |
| `CURSOR_WORKER_WEBHOOK_URL` | **Yes** | Automation E webhook URL |
| `CURSOR_WORKER_WEBHOOK_AUTH` | **Yes** | Automation E auth |
| `GAMELAB_API_KEY` | **Yes** | GameLab MCP — UI art |
| `GH_TOKEN` | **Yes** | `gh` CLI, issue sync, GitHub dispatch |
| `TELEGRAM_BOT_TOKEN` | **Yes** | Stakeholder Telegram bot |
| `TELEGRAM_CHAT_ID` | **Yes** | Product owner chat id |
| `ELEVENLABS_API_KEY` | **Yes** | Selective VO (12 clips) |
| `CURSOR_API_KEY` | **Yes** | **Auto agent token telemetry** (Cloud Agents usage API) |
| GDAI license / plugin | Phase 1+ | Commercial plugin — separate install |
| `OPENAI_API_KEY` / `GEMINI_API_KEY` | M5+ | Vision/audio jury scripts |

**Scope:** Personal + Runtime Secret for each. Sync webhook URL + auth to **GitHub repo Secrets**: `bash tools/setup_github_actions_secrets.sh`.

**Agent rule:** POST automations with `bash tools/curl_cursor_webhook.sh {pm|alert|worker} @<json>` — never raw `curl` to `api2.cursor.sh` without auth.

### 3.3 MCP (Cloud dashboard — required)

Register in **Dashboard → Integrations & MCP** (`.cursor/mcp.json` alone is not enough for cloud):

| Server | Role |
|--------|------|
| `godot-mcp` | GDAI build |
| `godotiq` | Debug |
| `godot-mcp-pro` | L4/L5 tests |
| `gamelab-mcp` | UI art |

Verify each agent boot:

```bash
bash tools/check_mcp_ready.sh
bash tools/check_extended_toolchain.sh
```

### 3.4 Branch bootstrap (first cycle)

On `game/development`:

1. Merge `main`
2. Complete **P1-00** (`game/project.godot`, tests, CI green)
3. File GitHub issues from `docs/ops/sprints/Phase1-Sprint1-issues.md`

Until P1-00 is done, orchestrator dispatches PM only.

---


## 4. Cursor Automations (event-driven — NOT cron)

**Full setup (snapshot + worker dispatch):** `docs/ops/agents/FACTORY_SETUP_GUIDE.md`
**Catalog:** `game/data/qa/factory_automations.json` · **Prompts:** `docs/ops/agents/automation_prompts/`

Create at [cursor.com/automations](https://cursor.com/automations).

### Automation A — **PM Sprint Master** (primary)

| Field | Value |
|-------|--------|
| **Name** | `PM — cycle dispatch` |
| **Trigger** | **Webhook** (copy URL → `CURSOR_PM_CYCLE_WEBHOOK_URL`) |
| **Repo** | `3d-JRPG-adventure-pc-game` |
| **Branch** | `game/development` (or environment) |
| **Tools** | MCP on, Comment on PR optional, Computer use on |

**Do not** add a schedule trigger.

**Prompt (paste):**

```text
You are PM Agent / Sprint Master for Tides of Urashima.

CONTEXT: You were triggered by a cycle-completion EVENT (not a timer).
Read artifacts/agent_cycle_event.json if present for issue_id, commit_sha, event type.

MANDATORY FIRST COMMAND:
  bash tools/run_pm_orchestrator.sh
If exit != 0: diagnose, escalate via bash tools/pm_emit_escalation.sh, STOP.

Follow docs/ops/agents/PM_AGENT_RUNBOOK.md exactly.

AFTER orchestrator PASS, read artifacts/pm_orchestrator_report.json → next_dispatch:

1. If event was agent_cycle_complete or ci_cycle_complete:
   - Verify previous issue is done on sprint_board.json
   - If next_dispatch empty and sprint_complete: emit sprint_cycle_complete (see below)
   - Else: `python3 tools/pm_dispatch_workers.py --head-only` labels GitHub issues → **Automation E** starts Worker snapshot VMs

   Prompt source: `docs/ops/agents/automation_prompts/pm_cycle_dispatch.md` (see `docs/ops/agents/FACTORY_SETUP_GUIDE.md`)

2. If you complete PM-owned work (e.g. P1-00 bootstrap) in this session:
   bash tools/run_post_agent_cycle.sh --issue <id> --agent pm --commit $(git rev-parse HEAD) --run-orchestrator --alignment-audit

3. If sprint_complete and event sprint_cycle_complete:
   python3 tools/pm_close_sprint.py --next-sprint-number <N>  (dry-run first if unsure)
   Update docs/ops/sprints/ + sprint_board.json; clear carry_over_queue
   bash tools/run_post_agent_cycle.sh --issue <first-issue-new-sprint> --agent pm --commit $(git rev-parse HEAD)

4. If phase exit + L5 PASS on RC commit:
   bash tools/pm_emit_cycle_event.sh uat_ready --tag <tag> --commit <sha>
   STOP — notify human for docs/ops/qa/PLAYTEST_SCRIPT.md (L6). Do not start new workers.

NEVER: skip orchestrator, mark gates PASS without QA evidence, use cron logic.

Cross-cutting factory features (PM hooks, telemetry, secrets, watchdog):
  Register in game/data/qa/workflow_integration_registry.json BEFORE merge.
  Run: bash tools/check_feature_integration.sh --remind
  Authority: docs/ops/qa/WORKFLOW_INTEGRATION.md

Worker agents MUST end every session with:
  bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
This runs done criteria, board update, cycle event (telemetry + stakeholder report), and evidence bundle.
See docs/ops/qa/AGENT_SESSION_TELEMETRY.md §9 and docs/ops/agents/PM_AGENT_RUNBOOK.md §3.
```

### Automation B — **CI failure triage** (required)

| Trigger | **CI completed** — workflow `Game CI` — **failure** on `game/development` |
| Workflow | `.github/workflows/game-ci-failure-triage.yml` |
| Prompt | Run remediation; `bash tools/qa_emit_remediation.sh`; re-dispatch **same issue** via `agent_cycle_failed`; do not mark done |

On **success**, worker emits `agent_cycle_complete` — PM is not triggered by CI pass alone.

### Automation C — **Human UAT notify** (end of pipeline)

| Trigger | **Webhook** separate URL, or manual |
| Event | `uat_ready` only |
| Prompt | Post Slack/email/checklist link to `docs/ops/qa/PLAYTEST_SCRIPT.md`; do not run game code |

### Automation D — **Factory watchdog / human alert** (exception only)

| Field | Value |
|-------|--------|
| **Name** | `Factory — human alert` |
| **Trigger** | Webhook → `CURSOR_FACTORY_ALERT_WEBHOOK_URL` (separate from PM cycle webhook) |
| **Events** | `factory_halt`, recovery exhausted |
| **Prompt** | Notify project owner; link `artifacts/factory_health_report.json`; do **not** start workers |

**Scheduled monitoring (GitHub):** `.github/workflows/factory-watchdog.yml` runs every 2h, calls `run_factory_watchdog.sh --recover` **only when unhealthy**. This is stall insurance — not primary PM dispatch. See `docs/ops/agents/FACTORY_WATCHDOG.md`.

**PM webhook also handles `watchdog_recovery`** — same Automation A; add watchdog branch to PM prompt (see `docs/ops/agents/FACTORY_WATCHDOG.md` §5).

---
