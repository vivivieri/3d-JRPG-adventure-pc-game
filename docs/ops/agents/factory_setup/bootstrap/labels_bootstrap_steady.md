---
id: labels-bootstrap-steady
type: how-to
audience: [pm]
status: active
authority: ops
tokens_est: 433
summary: "Labels + bootstrap + steady-state"
---
# Factory Setup — Automations & Bootstrap — Labels + bootstrap + steady-state

**Hub:** [`automations_github_bootstrap.md`](../automations_github_bootstrap.md)

## 7. Phase 5 — GitHub labels + issues

```bash
export GH_TOKEN=…
bash tools/setup_github_project.sh
bash tools/setup_github_actions_secrets.sh   # needs GH_TOKEN Secrets write
```

Creates `dispatch/ready`, `agent/*`, `status/*` labels.

For full automation, enable GitHub issue links on the sprint board:

1. Set `orchestration.require_github_issues: true` in `game/data/qa/sprint_board.json`
2. Create issues:

   ```bash
   python3 tools/pm_sync_github_issues.py --create
   ```

---



## 8. Phase 6 — Bootstrap factory loop

From an Environment-launched PM agent:

```bash
bash tools/run_pm_orchestrator.sh
python3 tools/pm_dispatch_workers.py --dry-run   # inspect manifest
bash tools/run_post_agent_cycle.sh --issue P1-00 --agent pm --commit $(git rev-parse HEAD)
```

Test webhook:

```bash
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-00 --agent pm --note "factory bootstrap"
```

PM Automation should start within seconds.

---



## 9. Steady-state loop (no human)

1. **Worker** (Automation E, snapshot VM): `run_agent_session_gate.sh` → work → PR → `run_post_agent_cycle.sh`
2. **Webhook** → Automation A (PM)
3. **PM**: `run_pm_orchestrator.sh` → `pm_dispatch_workers.py`
4. **GitHub** issue labeled `dispatch/ready` → Automation E → new Worker snapshot VM
5. Repeat until `sprint_complete` → PM closes sprint → next pack
6. After L5 on RC: `uat_ready` → **you** run L6 only

---
