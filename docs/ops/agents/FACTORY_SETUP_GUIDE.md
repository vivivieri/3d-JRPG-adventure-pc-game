---
id: factory-setup-guide
type: tutorial
phase: [0, 1]
audience: [pm, architect]
status: active
authority: ops
tokens_est: 308
summary: "Multi-agent factory setup — load the phase you are configuring"
---
# Factory Setup Guide

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`what_boundaries.md`](factory_setup/what_boundaries.md) | What you build + control boundaries |
| [`phases_snapshot_secrets_mcp.md`](factory_setup/phases_snapshot_secrets_mcp.md) | Snapshot, secrets, MCP |
| [`automations_github_bootstrap.md`](factory_setup/automations_github_bootstrap.md) | Automations, labels, bootstrap, steady-state |
| [`audit_antipatterns.md`](factory_setup/audit_antipatterns.md) | Audit, anti-patterns, cross-refs |
**Version:** 1.0
**Authority:** End-to-end setup for event-driven PM orchestration + worker Cloud Agents on **snapshot** VMs. Human only at **L6 UAT**.
**Cross-refs:** `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` · `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` · `game/data/qa/factory_automations.json`

---

## Factory hooks

- Worker dispatch entry: `python3 tools/pm_dispatch_workers.py` (see setup pack).
- Secrets checklist + Telegram live in the setup pack siblings.

