---
id: session-startup
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 333
summary: "Session startup every run"
---
# MCP Stack — Session startup every run

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Session startup (every agent run)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_dev_environment.sh
bash tools/check_extended_toolchain.sh
```

### Block until all required checks pass

| Check | How |
|-------|-----|
| R&R compliance (no hand `.tscn`) | `bash tools/check_rr_compliance.sh` exit 0 |
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Godotiq WebSocket | Port `6007` listening; GodotIQ plugin enabled |
| MCP Pro server | `tools/godot-mcp-pro-server/build/index.js` exists; plugin enabled |
| Godot Editor | Running with `game/project.godot` open |
| Cursor MCP catalog | **Required:** `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp` |
| GameLab API key | `GAMELAB_API_KEY` in Cursor Secrets |
| Blender | `blender` in PATH — required for M5 turntable QA |
| Offline art/audio | ComfyUI, Material Maker, ACE-Step GPU — document fallback used per task |

If **any required** MCP server or toolchain piece is missing → **STOP and notify the user**. See registration below.

---
