---
id: mcp-troubleshoot
type: tutorial
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 234
summary: "Optional MCP + troubleshooting"
---
# GitHub Setup — Optional MCP + troubleshooting

**Hub:** [`GITHUB_SETUP.md`](../GITHUB_SETUP.md)

## 5. Optional MCP (not GitHub)

| Tool | Setup |
|------|-------|
| **Linear** | Cursor → Integrations → Linear MCP → authenticate |
| **Notion** | Cursor → Integrations → Notion MCP → authenticate |

Game design authority stays in `docs/` + `game/data/` — PM tools track work only.

---


## 6. Troubleshooting

| Error | Fix |
|-------|-----|
| `GH_TOKEN not set` | Add to Cursor Secrets or `export GH_TOKEN=...` |
| Branch protection 403 | Need repo admin + GitHub Pro for private rules on free org |
| Label already exists | Script uses `--force` / PATCH — safe to re-run |
| Environment not in workflow | First workflow run auto-creates; script pre-creates for reviewers |
