---
id: summary-engine-gdai
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, pm]
status: active
authority: engineering
tokens_est: 588
summary: "Summary, engine, GDAI"
---
# Plugin Compatibility — Summary, engine, GDAI

**Hub:** [`PLUGIN_COMPATIBILITY.md`](../PLUGIN_COMPATIBILITY.md)

## Summary

| Plugin | Installed | Vendor min | 4.7 status | VM verified | Blocker? |
|--------|-----------|------------|------------|-------------|----------|
| **GDAI MCP** | v0.3.2 | Godot 4.2+ | **Compatible** | HTTP :3571, 35 tools | No |
| **Godotiq** | v0.5.15 | Godot 4.x | **Compatible** | Addon + pip; enable in editor | No |
| **Godot MCP Pro** | Not installed | Godot 4.4+ | **Expected OK** | Needs purchased zip | Yes for L4/L5 |
| **GodotSteam** | v4.15 (stale) | **4.20+** for 4.7 | **Upgrade before ship** | Class loads on Linux; vendor breaks at 4.20 | No until Phase 8 |

**Verdict:** GDAI + Godotiq are verified on Godot 4.7. Per `.cursorrules` §0 /
`MCP_STACK.md`, the **full** stack (incl. `godot-mcp-pro`, `gamelab-mcp`) and **Blender** (M5 turntable) are **required** —
if any piece is missing, agents must **notify the user** rather than silently proceed.
Hard blocks: MCP Pro before any L4/L5 phase gate (Phase 2+); GodotSteam upgrade to 4.20+ before
Steam export (Phase 8).

---


## Godot Engine 4.7.stable

| Check | Result |
|-------|--------|
| `godot4 --version` | `4.7.stable.official` |
| Headless boot | Pass (`bash tools/run_playtest_smoke.sh` 4/4) |
| `config/features` | `4.7`, Forward Plus |

---


## GDAI MCP (build — primary)

| Field | Value |
|-------|-------|
| **Version** | 0.3.2 (`game/addons/gdai-mcp-plugin-godot/plugin.cfg`) |
| **Vendor docs** | Godot **4.2+** — https://gdaimcp.com/docs |
| **Changelog** | 4.5 support (0.2.4), 4.6 fixes (0.3.0); no explicit 4.7 line yet |
| **Cursor MCP** | `godot-mcp` |
| **Bridge** | HTTP `127.0.0.1:3571` + stdio `gdai_mcp_server.py` |
| **project.godot** | Enabled + `GDAIMCPRuntime` autoload |

### Runtime verification (this VM)

- `bash tools/ensure_gdai_mcp.sh` — editor up, **35 tools** on :3571
- Headless quit shows `Capture not registered: 'gdaimcp'` — cosmetic on CLI exit, not a build blocker

### Risk

Low. Vendor targets entire 4.x line; watch Discord for 4.7-specific patches. Re-download latest zip if editor panel errors appear.

---
