---
id: antipatterns-troubleshoot
type: how-to
audience: [pm, builder]
phase: [0, 1]
status: active
authority: agents
tokens_est: 595
summary: "[`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)"
---
# Cloud Agent Setup — Anti-patterns & troubleshooting

**Hub:** [`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)

## 9. Anti-patterns

| Do not | Why |
|--------|-----|
| Cron PM every N hours | Wastes time between AI cycles |
| Worker starts without session gate | Breaks sequence enforcement |
| Skip `pm_emit_cycle_event.sh` | PM never wakes up |
| PM does Builder `.tscn` work | R&R violation |
| Automate L6 playtest | Required human ship gate |
| Rely on `.cursor/mcp.json` only in cloud | Dashboard registration required |

---


## 10. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Factory stalled after PR merge | Worker forgot `pm_emit_cycle_event.sh` — run manually or `bash tools/run_factory_watchdog.sh --recover` |
| Agent hung mid-session | Heartbeat stale — watchdog emits `watchdog_recovery`; or `pm_record_heartbeat.sh` during long work |
| Runaway recovery | Auto `factory_halt` at max attempts — `--clear-halt` after human fix |
| Webhook 401/404 | Re-copy URL + **Generate auth header** → `CURSOR_*_WEBHOOK_AUTH`; sync via `bash tools/setup_github_actions_secrets.sh`; test `bash tools/curl_cursor_webhook.sh pm @artifacts/agent_cycle_event.json` |
| PM runs but MCP FAIL | Fix snapshot; emit `mcp_blocked`; human fixes secrets |
| CI→PM loop | Ensure `.cycle_pending` cleared; use guarded workflow only |
| Orchestrator dispatch empty, sprint not done | Check `depends_on` / issue status on `sprint_board.json` |

---


## 11. Quick start checklist

- [ ] Environment snapshot with GDAI + MCP PASS
- [ ] **Day-one secrets (all 11 incl. webhook auth)** — `docs/ops/agents/CURSOR_SECRETS_SETUP.md` · `bash tools/check_day_one_secrets.sh`
- [ ] GDAI plugin in snapshot (Phase 1+ scene work)
- [ ] MCP servers in Cloud dashboard
- [ ] **Automation A** + **Automation D** + **Automation E** — webhook + auth header each
- [ ] GitHub repo secrets: `bash tools/setup_github_actions_secrets.sh` (6 webhook URL + auth)
- [ ] `game/development` bootstrapped (P1-00)
- [ ] First cycle close: `bash tools/run_post_agent_cycle.sh --issue P1-00 --agent pm --commit $(git rev-parse HEAD)`
- [ ] Confirm PM Automation starts within seconds, not next day

---


## 12. Cross-refs

- `docs/ops/agents/PM_AGENT_RUNBOOK.md` — PM step list inside each triggered run
- `docs/ops/agents/SPRINT_ORCHESTRATION.md` — board + gates
- `docs/ops/ci-cd/ENVIRONMENTS.md` — dev → qa → **uat** promotion
- `AGENTS.md` — cloud bootstrap
- `docs/ops/agents/GDAI_CLOUD_SETUP.md` — editor + HTTP :3571
