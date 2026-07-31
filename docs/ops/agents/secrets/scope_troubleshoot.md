---
id: scope-troubleshoot
type: how-to
audience: [pm, builder, release]
phase: [0, 1]
status: active
authority: agents
tokens_est: 612
summary: "Scope, later phases, troubleshooting"
---
# Cursor Secrets Setup — Scope, later phases, troubleshooting

**Hub:** [`CURSOR_SECRETS_SETUP.md`](../CURSOR_SECRETS_SETUP.md)

## 9. Secret scope and placement

| Setting | Value |
|---------|--------|
| **Scope** | Personal + Runtime Secret *(each secret)* |
| **Cursor environment** | All 8 secrets above |
| **GitHub Actions** | At minimum both webhook URLs; Telegram if CI sends reports |

Do **not** commit secrets to git. Do **not** paste tokens in issues, PRs, or agent prompts.

---


## 10. What is *not* day one (later phases)

| Secret | When |
|--------|------|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` | M5+ visual/model/audio jury scripts — **optional** if you run the agent-driven jury (`docs/ops/qa/AGENT_JURY.md`), which uses Cursor's own LLMs via subagents and needs no provider keys |
| GDAI license / plugin zip | Phase 1+ scene work (commercial — separate from this list) |
| `GODOT_SCRIPT_ENCRYPTION_KEY` | M6 RC ship export — PCK encryption (GitHub `steam-production` only) |
| `GODOT_SAVE_HMAC_KEY` | M6 RC ship export — save-slot HMAC pepper (same environment) |
| Steam API keys | Phase 8 only |

Generate ship keys (store output in GitHub Secrets — never commit):

```bash
bash tools/generate_ship_protection_keys.sh
```

See `docs/ops/qa/SECURITY.md` §9 for custom template build + `SHIP_RELEASE=1` export flow.

---


## 11. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `check_day_one_secrets.sh` FAIL | Re-read section for missing secret; confirm Runtime Secret scope |
| PM never wakes after cycle | `CURSOR_PM_CYCLE_WEBHOOK_URL` wrong or automation Inactive |
| No halt alert | `CURSOR_FACTORY_ALERT_WEBHOOK_URL` missing or Factory automation Inactive |
| `gh: not authenticated` | Set `GH_TOKEN`; run `gh auth status` |
| GameLab MCP missing | `GAMELAB_API_KEY` + Integrations & MCP + `write_mcp_config.sh` |
| Telegram silent | Message bot first; verify chat id via `getUpdates` |
| ElevenLabs 401 | Regenerate key; check account credits |
| Tokens not in telemetry | Set `CURSOR_API_KEY`; run `bash tools/check_agent_telemetry_ready.sh` |
| `tokens_fetch_status: pending` | Run `python3 tools/pm_sync_agent_session_tokens.py` after a few minutes |

---


## 12. Cross-refs

- `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — automations + factory architecture
- `docs/ops/agents/FACTORY_WATCHDOG.md` — alert vs PM webhooks
- `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md` — Telegram report content
- `docs/ops/ci-cd/GITHUB_SETUP.md` — labels, environments, branch protection
- `AGENTS.md` — cloud bootstrap order
