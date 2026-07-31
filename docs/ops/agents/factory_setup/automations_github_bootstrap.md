---
id: automations-github-bootstrap
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 1096
summary: "Automations, labels, bootstrap, steady-state"
---
# Factory Setup Guide — Automations, labels, bootstrap, steady-state

**Hub:** [`FACTORY_SETUP_GUIDE.md`](../FACTORY_SETUP_GUIDE.md)

## 6. Phase 4 — Cursor Automations (dashboard)

Machine-readable catalog: `game/data/qa/factory_automations.json`
Prompt files: `docs/ops/agents/automation_prompts/`

### Automation A — PM cycle dispatch (required)

| Field | Value |
|-------|--------|
| Trigger | **Webhook** → `CURSOR_PM_CYCLE_WEBHOOK_URL` |
| Repo / branch | `3d-JRPG-adventure-pc-game` / `game/development` |
| Schedule | **None** |
| Prompt | Paste `docs/ops/agents/automation_prompts/pm_cycle_dispatch.md` |

### Automation B — CI failure triage (required)

Handled by `.github/workflows/game-ci-failure-triage.yml` posting to PM webhook.
Optional duplicate in Cursor automations on **CI failure** for `Game CI` on `game/development`.
Prompt: `docs/ops/agents/automation_prompts/ci_failure_triage.md`

### Automation C — UAT notify (optional)

Webhook on `uat_ready` only. Prompt: `docs/ops/agents/automation_prompts/uat_notify.md`

### Automation D — Factory alert (required)

| Field | Value |
|-------|--------|
| Trigger | Webhook → `CURSOR_FACTORY_ALERT_WEBHOOK_URL` |
| Prompt | `docs/ops/agents/automation_prompts/factory_alert.md` |

### Automation E — Worker (required for 100% automation)

This closes the **worker spawn gap**.

> **Cursor UI note:** Many accounts only show **PR label** triggers, not **issue label** triggers. Use the **webhook + GitHub Actions** bridge below instead of a GitHub label trigger in Cursor.

| Field | Value |
|-------|--------|
| Name | `Worker — sprint issue` |
| Trigger | **Webhook** → `CURSOR_WORKER_WEBHOOK_URL` |
| Repo / branch | `3d-JRPG-adventure-pc-game` / `game/development` |
| Tools | MCP **on** (all Godot MCPs + gamelab) |
| Prompt | Paste `docs/ops/agents/automation_prompts/worker_sprint_issue.md` |

**GitHub Actions bridge** (repo workflow `.github/workflows/worker-dispatch.yml`):

1. Save Automation E with **Webhook** trigger → copy URL
2. GitHub → **Settings → Secrets and variables → Actions** → `CURSOR_WORKER_WEBHOOK_URL` = same URL
3. Merge `worker-dispatch.yml` to `game/development` (fires on `issues.labeled` → `dispatch/ready`)

**How PM triggers it:** orchestrator step `dispatch_workers` runs:

```bash
python3 tools/pm_dispatch_workers.py --head-only
```

That adds labels `dispatch/ready`, `status/in-progress`, `agent/<role>` on the linked GitHub issue and writes `artifacts/worker_dispatch_manifest.json`.

> **Cursor UI note:** If your automations UI only shows repo/branch (no explicit “Environment” dropdown), automations still reuse the **saved Environment for the same repo** when configured. Confirm with `environment-info` → non-null `build.snapshotId` after a test run.

---


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
