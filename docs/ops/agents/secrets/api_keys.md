---
id: api-keys
type: how-to
audience: [pm, builder, release]
phase: [0, 1]
status: active
authority: agents
tokens_est: 1354
summary: "API keys"
---
# Cursor Secrets Setup — API keys

**Hub:** [`CURSOR_SECRETS_SETUP.md`](../CURSOR_SECRETS_SETUP.md)

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

**Cross-ref:** `docs/ops/agents/MCP_STACK.md` § GameLab Studio MCP · `docs/design/art/ART_AUTOMATION_PIPELINE.md`

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
| Secrets | Read and write *(GitHub Actions repo secrets via `setup_github_actions_secrets.sh`)* |
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

**Cross-ref:** `docs/ops/ci-cd/GITHUB_SETUP.md` §1

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

**Cross-ref:** `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md` §2

---


## 7. `ELEVENLABS_API_KEY`

**What it is:** API key for **selective VO** — 12 emotional clips only (`docs/design/vision/VO_HIT_LIST.md`), not full dialogue.

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

Remove `--dry-run` when ready to generate. Log commercial terms in `docs/design/art/LICENSES.md` before ship.

**Cross-ref:** `docs/design/vision/VO_HIT_LIST.md` § AI VO setup · `docs/design/audio/AUDIO_PRODUCTION_GUIDE.md`

---


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
