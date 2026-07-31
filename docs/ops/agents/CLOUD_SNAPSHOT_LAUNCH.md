---
id: cloud-snapshot-launch
type: tutorial
phase: [0, 1]
audience: [pm, builder, architect]
status: active
authority: ops
tokens_est: 255
summary: "Snapshot launch — load dashboard branch, checklist, or rebuild"
---
# Cloud Snapshot Launch

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`dashboard_branch.md`](snapshot/dashboard_branch.md) | Dashboard branch + active snapshot + skip reasons |
| [`launch_checklist.md`](snapshot/launch_checklist.md) | Launch checklist every session |
| [`rebuild_gamelab_troubleshoot.md`](snapshot/rebuild_gamelab_troubleshoot.md) | Rebuild, GameLab transport, troubleshooting |
**Authority:** How to boot **game/development** Cloud Agents from the saved environment snapshot — not JIT from `main`.
**Cross-refs:** `docs/ops/agents/GDAI_CLOUD_SETUP.md` · `docs/ops/agents/MCP_STACK.md` · `docs/ops/qa/PLATFORM_SUPPORT.md` · `.cursor/environment.json`

---

## Factory hooks (registry keywords)

- Boot verify: `bash tools/check_snapshot_boot.sh --report`

