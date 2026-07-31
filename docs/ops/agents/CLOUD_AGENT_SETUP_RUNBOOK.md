---
id: cloud-agent-setup-runbook
type: how-to
audience: [pm, builder]
phase: [0, 1]
status: active
authority: agents
tokens_est: 397
summary: "load the pack for your setup step."
---
# Cloud Agent Setup Runbook

**Hub** — load the pack for your setup step.

| Pack | Topic |
|------|-------|
| [`goal_architecture.md`](cloud_setup/goal_architecture.md) | Goal & architecture |
| [`setup_automations.md`](cloud_setup/setup_automations.md) | One-time setup & automations |
| [`cycle_events.md`](cloud_setup/cycle_events.md) | End-of-cycle & events |
| [`github_timeline.md`](cloud_setup/github_timeline.md) | GitHub path & timeline |
| [`antipatterns_troubleshoot.md`](cloud_setup/antipatterns_troubleshoot.md) | Anti-patterns & troubleshooting |

## Factory surfaces (always on this hub)

Keep these strings discoverable for `L0_workflow_integration` / agent boot:

| Surface | Doc / command |
|---------|----------------|
| End-of-cycle | `bash tools/run_post_agent_cycle.sh` |
| Token telemetry | `CURSOR_API_KEY` — see secrets setup |
| Stall recovery | `bash tools/run_factory_watchdog.sh` |
| Factory install | [`FACTORY_SETUP_GUIDE.md`](FACTORY_SETUP_GUIDE.md) |

# Cloud Agent Setup Runbook — Event-Driven Multi-Agent Factory

**Version:** 1.0
**Authority:** How to run Tides of Urashima on **Cursor Cloud Agents** until automated gates pass, then **notify human for UAT**.
**Cross-refs:** `docs/ops/agents/PM_AGENT_RUNBOOK.md`, `docs/ops/agents/SPRINT_ORCHESTRATION.md`, `docs/ops/agents/GDAI_CLOUD_SETUP.md`, `game/data/qa/agent_cycle_events.json`, `.cursor/environment.json`

---
