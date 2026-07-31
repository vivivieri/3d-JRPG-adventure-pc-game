---
id: mcp-troubleshoot
type: tutorial
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 274
summary: "Game design authority stays in `docs/` + `game/data/` — PM tools track work only."
---
# GitHub Setup — Optional MCP + troubleshooting

**Hub:** [`GITHUB_SETUP.md`](../GITHUB_SETUP.md)

## When to read

Use **GitHub Setup — Optional MCP + troubleshooting** (roles: pm, release) when learning/setup for the first time Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Optional MCP (not GitHub)](#5-optional-mcp-not-github)
- [6. Troubleshooting](#6-troubleshooting)


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
