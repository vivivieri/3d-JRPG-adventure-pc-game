# GDAI MCP — local & cloud dev setup

**GDAI MCP** is a **dev-only** Godot 4 plugin that lets Cursor (and other MCP clients) control the **Godot Editor** — create scenes, move nodes, read script errors, etc.

Official docs: https://gdaimcp.com/docs/installation

This repo does **not** commit the plugin. It is gitignored so Steam/release builds stay clean. Only **GodotSteam** ships under `game/addons/`.

---

## What you need (3 pieces)

| Piece | Purpose |
|-------|---------|
| **Godot Editor** | Project open at `game/project.godot`, plugin enabled, MCP server **Started** |
| **`gdai_mcp_server.py`** | Stdio bridge run via `uv` (inside the plugin folder) |
| **Cursor MCP config** | Points Cursor at that Python server |

**Important:** GDAI controls the **editor**, not headless Godot. The screenshot runner (`tools/capture_screenshots.sh`) uses headless Godot and does **not** replace GDAI.

**Startup order:** open Godot → start GDAI MCP in the editor panel → then use Cursor. If tools are missing, restart Cursor after Godot is running.

---

## 1. Prerequisites

### `uv` (required by GDAI)

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.sh | iex"
```

### Godot 4.3+

Open `game/project.godot` in the editor (same version as the project — see `README.md`).

---

## 2. Install the plugin (local, dev only)

1. Purchase/download from https://gdaimcp.com/ (commercial plugin).
2. Extract the zip — you get `addons/gdai-mcp-plugin-godot/`.
3. Copy that folder to:

   ```
   game/addons/gdai-mcp-plugin-godot/
   ```

4. In Godot: **Project → Project Settings → Plugins** → enable **GDAI MCP**.
5. Open the **GDAI MCP** tab in the bottom panel → **Start** the MCP server.
6. Copy the JSON config shown in that panel.

### Recommended editor settings

**Editor → Editor Settings** (enable **Advanced Settings**):

- Auto Reload Scripts on External Change — **On**
- Auto Reload and Parse Scripts on Save — **On**

### Path without spaces

GDAI can fail if the project or `gdai_mcp_server.py` path contains spaces. Prefer a short path, e.g. `~/dev/3d-JRPG-adventure-pc-game`.

---

## 3. Configure Cursor (desktop — recommended)

1. **Cursor Settings → MCP → Add new global MCP server**
2. Paste the JSON from the GDAI MCP panel. Example shape:

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": [
        "run",
        "/absolute/path/to/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
      ]
    }
  }
}
```

3. Replace the path with your machine’s absolute path to `gdai_mcp_server.py`.
4. Confirm the server shows as connected (green) in MCP settings.

### Optional project template

You can copy `.cursor/mcp.json.example` to `~/.cursor/mcp.json` and fill in your path. Do **not** commit real paths or secrets.

---

## 4. Cloud Agent setup

Cloud agents use `.cursor/environment.json` to install dependencies automatically:

```bash
bash tools/install_cloud_dev.sh   # Godot 4.3, uv, export templates, numpy
bash tools/check_dev_environment.sh
```

See **`AGENTS.md`** for full cloud workflow (GodotPrompter + GDAI MCP, headless validation).

### Installed by `install_cloud_dev.sh`

| Component | Location |
|-----------|----------|
| Godot 4.3 editor | `godot4` → `~/.local/bin` |
| Export templates | `.cache/godot-data/godot/export_templates/` |
| uv | `~/.local/bin/uv` |
| numpy | Python (trailer tool) |

Godot editor auto-starts via `tools/start_godot_editor.sh` (uses `--rendering-driver opengl3` in cloud VMs).

### GDAI in cloud (manual step)

GDAI MCP is **commercial** and not in git. To use in cloud:

1. Copy plugin to `game/addons/gdai-mcp-plugin-godot/` (upload or environment secret)
2. Re-run `bash tools/install_cloud_dev.sh` — auto-writes `.cursor/mcp.json`
3. In Godot editor: enable plugin → **Start** MCP server
4. Register MCP in Cursor dashboard if not using project `.cursor/mcp.json`

Without GDAI, cloud agents can still edit `.gd` / `.tscn` / shaders and validate with:

```bash
godot4 --headless --path game --quit-after 2
```

### Hybrid workflow (recommended)

| Work | Where |
|------|--------|
| Godot code, shaders, environment zones | **Cloud Agent** (`godot4` + headless validation) |
| GDAI in-editor polish | **Cloud or local** — after plugin installed |
| Scene nudging, material tweaks in viewport | **GDAI MCP** when editor + plugin running |
| Steam build | **No GDAI** in `game/addons/` |

---

## 5. Before Steam / release export

1. **Disable** the GDAI MCP plugin in **Project → Project Settings → Plugins**.
2. **Remove** `game/addons/gdai-mcp-plugin-godot/` from the export tree (it should not exist on release machines if you follow gitignore).
3. Run `./tools/export_windows.sh` as usual — only `godotsteam` should remain in `addons/`.

See also: `steam/GODOTSTEAM_SETUP.md`, `game/addons/godotsteam/README.md`.

---

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| No MCP tools in Cursor | Open Godot first; start GDAI server; restart Cursor |
| Server won’t start | Check path has **no spaces**; verify `uv --version` |
| Tools listed but calls fail | Confirm project is open in Editor, not just headless Godot |
| macOS dylib warning | See GDAI docs: “Apple could not verify libgdai-mcp-plugin-godot…” |

Common issues: https://gdaimcp.com/docs/common-issues

---

## 7. This repo’s shipped addons

| Addon | Shipped? | Path |
|-------|----------|------|
| GodotSteam | Yes | `game/addons/godotsteam/` |
| GDAI MCP | **No (dev only)** | `game/addons/gdai-mcp-plugin-godot/` (gitignored) |

Environment visuals are primarily built in `game/scripts/world/zone_visuals.gd` and `game/scripts/world/terrain_shapes.gd` so cloud agents can improve zones without GDAI.
