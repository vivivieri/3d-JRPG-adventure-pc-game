---
id: godotiq-mcp-pro
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, pm]
status: active
authority: engineering
tokens_est: 562
summary: "- Uses Godot 4.5+ script logger when available (`godotiq_logger.gd`) — benefits on 4.7"
---
# Plugin Compatibility — Godotiq + MCP Pro

**Hub:** [`PLUGIN_COMPATIBILITY.md`](../PLUGIN_COMPATIBILITY.md)

## When to read

Use **Plugin Compatibility — Godotiq + MCP Pro** (roles: architect, builder, pm) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [Godotiq (analyze & debug)](#godotiq-analyze-debug)
- [Godot 4.7 notes](#godot-47-notes)
- [Runtime verification](#runtime-verification)
- [Godot MCP Pro (test — L4/L5)](#godot-mcp-pro-test-l4l5)
- [Expected compatibility](#expected-compatibility)


## Godotiq (analyze & debug)

| Field | Value |
|-------|-------|
| **Addon** | 0.5.15 (`game/addons/godotiq/`) |
| **pip** | `godotiq==0.5.15` |
| **Vendor** | Godot **4.x** — https://godotiq.com/ |
| **Cursor MCP** | `godotiq` (`uvx godotiq`, `GODOTIQ_PROJECT_ROOT=/workspace/game`) |
| **Bridge** | WebSocket `127.0.0.1:6007` (editor plugin) |
| **project.godot** | **Enable GodotIQ** in Project → Plugins |

### Godot 4.7 notes

- Uses Godot 4.5+ script logger when available (`godotiq_logger.gd`) — benefits on 4.7
- Community tier: 24 MCP tools; Pro optional via `GODOTIQ_LICENSE_KEY`

### Runtime verification

1. `bash tools/install_godotiq.sh`
2. Enable **GodotIQ** plugin (in `project.godot` `editor_plugins`)
3. `bash tools/ensure_gdai_mcp.sh` (starts editor)
4. **Verified:** `GodotIQ: WebSocket server listening on 127.0.0.1:6007` + logger on Godot 4.5+
5. Register `godotiq` in Cursor MCP dashboard (cloud agents)

---


## Godot MCP Pro (test — L4/L5)

| Field | Value |
|-------|-------|
| **Status** | **Not installed** on this VM (commercial zip required) |
| **Vendor docs** | Godot **4.4+**, tested through **4.6** — https://godot-mcp.abyo.net/ |
| **Cursor MCP** | `godot-mcp-pro` with `--minimal` (35 tools) recommended |
| **Bridge** | WebSocket `127.0.0.1:6505` (default) |
| **Requires** | Node.js 18+, `bash tools/install_godot_mcp_pro.sh` |

### Expected compatibility

Vendor guides state **4.4+**; no known 4.7 break. Install from latest purchased zip before integration/E2E testing.

```bash
# Place zip: game/addons/godot-mcp-pro*.zip
bash tools/install_godot_mcp_pro.sh
# Enable: Project → Plugins → Godot MCP Pro
```

---
