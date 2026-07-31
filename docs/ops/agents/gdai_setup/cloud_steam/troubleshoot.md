---
id: troubleshoot
type: how-to
phase: [0, 1]
audience: [pm, builder, release]
status: active
authority: ops
tokens_est: 381
summary: "bash tools/ensure_gdai_mcp.sh"
---
# GDAI Setup — Cloud / Steam / Troubleshoot — Troubleshooting

**Hub:** [`cloud_steam_troubleshoot.md`](../cloud_steam_troubleshoot.md)

## 6. Troubleshooting

| Symptom | Desktop fix | Cloud fix |
|---------|-------------|-------------|
| No GDAI tools in Agent | Godot open → GDAI **Start** → restart Cursor | Run `ensure_gdai_mcp.sh` → register `godot-mcp` in [cursor.com/agents](https://cursor.com/agents) dashboard → restart agent |
| HTTP bridge down | GDAI MCP panel → **Start** | `bash tools/ensure_gdai_mcp.sh` |
| `godot-mcp` missing from MCP catalog | **Settings → Tools & MCP** → add server | **Cloud dashboard** → add custom MCP (`.cursor/mcp.json` alone is not enough) |
| Server won’t start | Path has **no spaces**; `uv --version` | Same + plugin folder present in VM |
| Tools listed but calls fail | Project open in **Editor**, not headless | Kill headless Godot; keep `--editor` process running |
| Port 3572 in use | Stop headless Godot tests | `ensure_gdai_mcp.sh` kills conflicting headless processes |
| macOS dylib warning | See GDAI docs | N/A (cloud uses Linux) |

**Quick health checks:**

```bash
bash tools/ensure_gdai_mcp.sh
curl -sf http://127.0.0.1:3571/tools | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('mcp_tools',[])), 'tools')"
```

GDAI common issues: https://gdaimcp.com/docs/common-issues

---
