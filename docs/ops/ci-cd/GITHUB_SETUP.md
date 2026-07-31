---
id: github-setup
type: tutorial
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 235
summary: "Repo/Actions setup — load quick script or manual UI"
---
# GitHub Setup

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`quick_manual.md`](github_setup/quick_manual.md) | Quick setup + manual UI |
| [`secrets_verify.md`](github_setup/secrets_verify.md) | CD secrets + verify |
| [`mcp_troubleshoot.md`](github_setup/mcp_troubleshoot.md) | Optional MCP + troubleshooting |
**Script:** `bash tools/setup_github_project.sh`
**Requires:** `GH_TOKEN` with **Issues**, **Pull requests**, **Actions**, **Secrets** (read/write for Actions repo secrets), and **Administration** (for branch protection)
**How to create token:** `docs/ops/agents/CURSOR_SECRETS_SETUP.md` §5 (day-one compulsory)
**Cross-refs:** `docs/ops/agents/PROJECT_MANAGEMENT.md`, `docs/ops/ci-cd/ENVIRONMENTS.md`

---

