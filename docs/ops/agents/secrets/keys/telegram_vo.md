---
id: telegram-vo
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 560
summary: "Telegram + ElevenLabs"
---
# Secrets — API Keys — Telegram + ElevenLabs

**Hub:** [`api_keys.md`](../api_keys.md)

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
