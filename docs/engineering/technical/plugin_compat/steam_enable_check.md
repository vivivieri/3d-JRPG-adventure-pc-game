---
id: steam-enable-check
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, pm]
status: active
authority: engineering
tokens_est: 657
summary: "Plugin Compatibility — Steam, enablement, check, fail, related — Headless `ClassDB.class_exists('Steam')` on Godot 4.7 with 4.15 → passes on this VM (Linux). Ve"
---
# Plugin Compatibility — Steam, enablement, check, fail, related

**Hub:** [`PLUGIN_COMPATIBILITY.md`](../PLUGIN_COMPATIBILITY.md)

## When to read

Use **Plugin Compatibility — Steam, enablement, check, fail, related** (roles: architect, builder, pm) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [GodotSteam (ship — Phase 8 only)](#godotsteam-ship-phase-8-only)
- [Runtime verification](#runtime-verification)
- [Fix (before export)](#fix-before-export)
- [Editor plugin enablement](#editor-plugin-enablement)
- [Automated check](#automated-check)
- [If a plugin fails on 4.7](#if-a-plugin-fails-on-47)
- [Related](#related)


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

- `docs/engineering/technical/TECH_STACK.md` — version pins
- `docs/ops/agents/MCP_STACK.md` — role split and ports
- `game/addons/README.md` — install commands
