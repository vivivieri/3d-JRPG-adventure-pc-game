---
id: what-boundaries
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 539
summary: "What you build + control boundaries"
---
# Factory Setup Guide — What you build + control boundaries

**Hub:** [`FACTORY_SETUP_GUIDE.md`](../FACTORY_SETUP_GUIDE.md)

## 1. What you are building

| Goal | Mechanism |
|------|-----------|
| PM auto-orchestration | **Automation A** webhook → `run_pm_orchestrator.sh` |
| Worker auto-dispatch | `pm_dispatch_workers.py` → GitHub label `dispatch/ready` → **Automation E** |
| Every implementation agent on snapshot | Saved Environment + `check_snapshot_boot.sh` gate |
| No cron | Event-driven only (`agent_cycle_complete` webhook) |
| Human at end only | `uat_ready` → L6 playtest (`docs/ops/qa/PLAYTEST_SCRIPT.md`) |

```mermaid
sequenceDiagram
  participant W as Worker AI<br/>(snapshot VM)
  participant GH as GitHub Issue
  participant EV as post_agent_cycle
  participant WH as PM Webhook
  participant PM as PM AI
  participant WE as Worker Automation

  W->>W: session gate → work → PR
  W->>EV: run_post_agent_cycle.sh
  EV->>WH: agent_cycle_complete
  WH->>PM: Automation A
  PM->>PM: run_pm_orchestrator.sh
  PM->>GH: pm_dispatch_workers.py labels dispatch/ready
  GH->>WE: label trigger
  WE->>W: new snapshot VM
```

---


## 2. Control boundaries (read this first)

| You control (repo + scripts) | Cursor team owner controls (dashboard) |
|------------------------------|----------------------------------------|
| `game/data/qa/sprint_board.json` | Saving Environment **snapshot** |
| `pm_dispatch_workers.py` | Creating **Automations** at cursor.com/automations |
| Webhook **payload** scripts | Pasting automation **prompts** from `docs/ops/agents/automation_prompts/` |
| CI workflows posting webhooks | **Integrations & MCP** server registration |
| Preflight / snapshot boot **gates** | Cursor Secrets UI |

**Repo cannot force snapshot boot** — it can **detect JIT boot and halt dispatch**.

Verify repo wiring anytime:

```bash
bash tools/check_factory_automation_setup.sh
python3 tools/validate_factory_automations.py   # L0_factory_automations
```

---
