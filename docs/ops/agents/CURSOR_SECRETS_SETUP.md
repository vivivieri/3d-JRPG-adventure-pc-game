---
id: cursor-secrets-setup
type: how-to
audience: [pm, builder, release]
phase: [0, 1]
status: active
authority: agents
tokens_est: 900
summary: "Day-one Cursor / GitHub secrets for the factory"
---
# Cursor Secrets Setup

**Hub** — load one pack below.

| Pack | Topic |
|------|-------|
| [`day_one_checklist.md`](secrets/day_one_checklist.md) | Day-one checklist |
| [`webhooks.md`](secrets/webhooks.md) | PM / alert / worker webhooks |
| [`api_keys.md`](secrets/api_keys.md) | API keys (GameLab, GH, Telegram, VO, Cursor) |
| [`scope_troubleshoot.md`](secrets/scope_troubleshoot.md) | Scope, later phases, troubleshooting |
# Cursor Secrets — Day-One Setup (How to Get Every Key)

**Version:** 1.0
**Authority:** All secrets below are **compulsory on day one** before starting the Cloud Agent factory on `game/development` (11 runtime secrets including webhook auth + `CURSOR_API_KEY` for auto token telemetry).
**Where to add:** Cursor **Cloud Agents → your environment → Secrets** — scope **Personal + Runtime Secret** for each.
**Cross-refs:** `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md`, `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md`, `docs/ops/ci-cd/GITHUB_SETUP.md`, `docs/ops/agents/MCP_STACK.md`, `docs/design/vision/VO_HIT_LIST.md`

---
