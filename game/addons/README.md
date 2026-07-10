# Addons (dev & ship)

Plugins in this folder extend Godot. **Only ship-safe addons** go in release builds.

## GDAI MCP (dev only — gitignored)

**Purpose:** Lets Cursor control the Godot Editor (scenes, nodes, errors).  
**License:** Commercial — https://gdaimcp.com/

```bash
# After purchase, extract and copy:
cp -r /path/to/gdai-mcp-plugin-godot game/addons/
```

1. Godot → **Project → Project Settings → Plugins** → enable **GDAI MCP**
2. Bottom panel → **GDAI MCP** → **Start**
3. Copy MCP JSON into `~/.cursor/mcp.json` (see `.cursor/mcp.json.example`)

**Not shipped** — remove or disable before Steam export.

## GodotSteam (ship — add in Phase 8)

**Purpose:** Steam API integration.  
**Docs:** `steam/GODOTSTEAM_SETUP.md`

```bash
# When ready:
bash tools/install_godotsteam.sh   # script added in later phase
```

Place binaries under `game/addons/godotsteam/` per upstream README.

## Policy

| Addon | Dev | Ship |
|-------|-----|------|
| gdai-mcp-plugin-godot | ✅ | ❌ |
| godotsteam | ✅ | ✅ |

Log licenses in `docs/LICENSES.md` before commit.
