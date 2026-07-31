---
id: audit-antipatterns
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 657
summary: "Audit, anti-patterns, cross-refs"
---
# Factory Setup Guide — Audit, anti-patterns, cross-refs

**Hub:** [`FACTORY_SETUP_GUIDE.md`](../FACTORY_SETUP_GUIDE.md)

## 10. Audit existing setup

### Repo-side (run now)

```bash
bash tools/check_factory_automation_setup.sh
bash tools/run_docs_ci_checks.sh   # includes L0_factory_automations
```

### Per agent run (snapshot proof)

```bash
bash tools/check_snapshot_boot.sh
bash tools/check_mcp_ready.sh
```

Or ask agent to run **cursor-cloud `environment-info`** — need `build.snapshotId`, not `build: null`.

### Dashboard checklist (human)

- [ ] Snapshot id in dashboard matches `.cursor/environment.json`
- [ ] Automation A active — URL + `CURSOR_PM_WEBHOOK_AUTH` in Secrets + GitHub
- [ ] Automation D active — URL + `CURSOR_ALERT_WEBHOOK_AUTH`
- [ ] Automation E active — URL + `CURSOR_WORKER_WEBHOOK_AUTH`
- [ ] Automation E triggers on label `dispatch/ready`
- [ ] All automations use `game/development`, not `main`
- [ ] MCP servers registered (4)
- [ ] Test cycle: worker end → PM wakes < 60s → worker label applied

### Common failures

| Symptom | Fix |
|---------|-----|
| `build: null` | Launch from Environment dashboard, not web/GitHub ad-hoc agent |
| Worker never starts | `github_issue` null → `pm_sync_github_issues.py --create`; check Automation E trigger |
| PM never wakes | Wrong URL/auth or Automation A inactive — `bash tools/curl_cursor_webhook.sh pm @artifacts/agent_cycle_event.json` |
| MCP FAIL on worker | Rebuild snapshot (`rebuild_cloud_snapshot.sh`) |
| Factory stall | Worker skipped `run_post_agent_cycle.sh` → `run_factory_watchdog.sh --recover` |

---


## 11. Anti-patterns

| Do not | Why |
|--------|-----|
| Start implementation agents from ad-hoc web chat | JIT boot — no GDAI |
| Use `main` for Builder work | No Godot project / MCP stack |
| Cron-schedule PM | Rejected — event-driven only |
| Skip Automation E | Workers never auto-spawn |
| Automate L6 playtest | Required human ship gate |

---


## 12. Cross-refs

| Doc | Topic |
|-----|--------|
| `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` | Event architecture + automation prompts index |
| `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` | Snapshot rebuild + Godotiq enable |
| `docs/ops/agents/PM_AGENT_RUNBOOK.md` | PM session steps |
| `docs/ops/agents/SPRINT_ORCHESTRATION.md` | Board + gates |
| `docs/ops/agents/CURSOR_SECRETS_SETUP.md` | All secrets |
| `game/data/qa/factory_automations.json` | Automation catalog (CI validated) |
