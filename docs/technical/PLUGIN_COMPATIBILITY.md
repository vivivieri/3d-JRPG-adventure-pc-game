# Plugin compatibility matrix (Godot 4.7)

**Engine pin:** `GODOT_VERSION=4.7-stable` (`tools/install_cloud_dev.sh`)  
**Audit date:** July 2026  
**Check script:** `bash tools/check_plugin_compatibility.sh [--with-editor]`

Run this audit **before Phase 1 build** and after any engine or plugin upgrade.

---

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

## GodotSteam (ship — Phase 8 only)

| Field | Value |
|-------|-------|
| **VM install** | **4.15** (readme in `game/addons/godotsteam/`) |
| **Required for 4.7** | **4.20+** — Godot 4.7 changed `callable_method_pointer.h` → `callable_mp.h` |
| **Source** | https://codeberg.org/godotsteam/godotsteam/releases |

### Runtime verification

Headless `ClassDB.class_exists("Steam")` on Godot 4.7 with **4.15** → **passes on this VM (Linux)**. Vendor still requires **4.20+** for official 4.7 support (`callable_mp.h` break, Windows Steam API auto-update, Project Settings changes). **Upgrade before export** even if basic load succeeds.

### Fix (before export)

```bash
rm -rf game/addons/godotsteam
GODOTSTEAM_VERSION=4.20 bash tools/install_godotsteam.sh
```

Do **not** mix module and GDExtension builds. Remove all MCP dev plugins before Steam export.

---

## Editor plugin enablement

After install, `project.godot` should include:

```ini
[editor_plugins]
enabled=PackedStringArray(
  "res://addons/gdai-mcp-plugin-godot/plugin.cfg",
  "res://addons/godotiq/plugin.cfg"
)
# Add when MCP Pro installed:
# "res://addons/godot_mcp/plugin.cfg"
```

---

## Automated check

```bash
# Quick (no editor start)
bash tools/check_plugin_compatibility.sh

# Full (starts editor via ensure_gdai_mcp if needed)
bash tools/check_plugin_compatibility.sh --with-editor
```

Included in smoke: `bash tools/run_playtest_smoke.sh` runs dev environment check (GDAI HTTP when editor is up).

---

## If a plugin fails on 4.7

1. Update to latest vendor release (re-run install script).
2. Check vendor Discord/changelog for 4.7 patch.
3. Last resort: pin engine to **4.6.stable** in `tools/install_cloud_dev.sh` and re-run smoke + this audit.

---

## Related

- `docs/technical/TECH_STACK.md` — version pins
- `docs/agents/MCP_STACK.md` — role split and ports
- `game/addons/README.md` — install commands
