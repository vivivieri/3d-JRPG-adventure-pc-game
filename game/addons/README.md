# Addons (dev & ship)

Plugins in this folder extend Godot. **Only ship-safe addons** go in release builds.

See **`docs/MCP_STACK.md`** for how GDAI + Godotiq + Godot MCP Pro work together.

## GDAI MCP (dev — build primary)

**Purpose:** Editor/scene control for AI agents (`.tscn`, nodes, materials).  
**License:** Commercial — https://gdaimcp.com/  
**Cursor MCP name:** `godot-mcp`

```bash
bash tools/install_gdai_plugin.sh
```

Enable **GDAI MCP** plugin → panel → **Start**.

## Godotiq (dev — analyze & debug)

**Purpose:** Signal tracing, dependency graphs, `ui_map`, debug console, `verify_project_runs`.  
**License:** MIT community (free) / Pro optional — https://godotiq.com/  
**Cursor MCP name:** `godotiq`

```bash
bash tools/install_godotiq.sh
```

Enable **GodotIQ** plugin. Config: `game/.godotiq.json`

## Godot MCP Pro (dev — automated testing)

**Purpose:** `run_test_scenario`, `assert_screen_text`, input replay, screenshot compare.  
**License:** Commercial — https://godot-mcp.abyo.net/ ($15)  
**Cursor MCP name:** `godot-mcp-pro` (use `--minimal` mode in mcp.json)

```bash
# Place purchased zip in game/addons/
bash tools/install_godot_mcp_pro.sh
```

Requires Node.js 18+. Enable **Godot MCP Pro** plugin.

## Bootstrap all MCP servers

```bash
bash tools/ensure_mcp_stack.sh
bash tools/write_mcp_config.sh   # regenerates .cursor/mcp.json
```

## GodotSteam (ship — Phase 8)

**Purpose:** Steam API integration.  
**Docs:** `steam/GODOTSTEAM_SETUP.md`

## Policy

| Addon | Dev | Ship | Role |
|-------|-----|------|------|
| gdai-mcp-plugin-godot | ✅ | ❌ | Build |
| godotiq | ✅ | ❌ | Analyze |
| godot_mcp (MCP Pro) | ✅ | ❌ | Test |
| godotsteam | ✅ | ✅ | Steam |

**Before Steam export:** disable and remove all MCP dev plugins.

Log licenses in `docs/LICENSES.md`.
