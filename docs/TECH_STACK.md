# Technology stack (latest)

**Updated:** July 2026 — pin versions here; install scripts read `GODOT_VERSION` from `tools/install_cloud_dev.sh`.

## Engine

| Component | Version | Notes |
|-----------|---------|-------|
| **Godot Engine** | **4.7 stable** (Jun 2026) | Forward+ renderer; `GODOT_VERSION=4.7-stable` in cloud install |
| **GDScript** | Godot 4.7 | Typed scripts per `.cursorrules` |

## AI development stack

| Tool | Role |
|------|------|
| **GodotPrompter** (Cursor) | Plan + write `.gd`, `.gdshader`, tests |
| **GDAI MCP** (`godot-mcp`) | Build scenes in editor |
| **Godotiq** (`godotiq`) | Analyze signals, debug, `ui_map` |
| **Godot MCP Pro** (`godot-mcp-pro`) | Automated test scenarios (`--minimal` mode) |

See `docs/MCP_STACK.md`.

## MCP plugin compatibility (Godot 4.7)

**Full audit:** `docs/PLUGIN_COMPATIBILITY.md` — run `bash tools/check_plugin_compatibility.sh` before Phase 1.

| Plugin | Min Godot | 4.7 status | Action |
|--------|-----------|--------------|--------|
| GDAI MCP 0.3.2 | 4.2+ | Verified | Re-download if editor errors |
| Godotiq 0.5.15 | 4.x | Verified | `bash tools/install_godotiq.sh`; enable GodotIQ |
| Godot MCP Pro | 4.4+ | Not installed | `bash tools/install_godot_mcp_pro.sh` (L4/L5) |
| GodotSteam | **4.20+** | 4.15 loads (dev); upgrade for ship | `bash tools/install_godotsteam.sh` (Phase 8) |

## Ship (Phase 8)

| Component | Version |
|-----------|---------|
| GodotSteam | **4.20+** (Godot 4.7) — `bash tools/install_godotsteam.sh` |

## Upgrade Godot

```bash
# Cloud / CI — re-download editor + templates
GODOT_VERSION=4.7-stable bash tools/install_cloud_dev.sh

# Local — install Godot 4.7 from https://godotengine.org/download
# Open project once in editor to migrate project.godot if prompted
```

After any engine bump: run `bash tools/run_playtest_smoke.sh` and re-verify MCP plugins in Godot.
