---
id: one-time
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 893
summary: "Cloud Setup — Automations — One-time setup — Dashboard: Cloud Agents → Environments"
---
# Cloud Setup — Automations — One-time setup

**Hub:** [`setup_automations.md`](../setup_automations.md)

## When to read

Use **Cloud Setup — Automations — One-time setup** (roles: pm, architect) when learning/setup for the first time Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [3. One-time setup](#3-one-time-setup)
- [3.1 Cloud environment snapshot](#31-cloud-environment-snapshot)
- [3.2 Secrets (Cursor Cloud Agents → Secrets)](#32-secrets-cursor-cloud-agents-secrets)
- [3.3 MCP (Cloud dashboard — required)](#33-mcp-cloud-dashboard-required)
- [3.4 Branch bootstrap (first cycle)](#34-branch-bootstrap-first-cycle)


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
