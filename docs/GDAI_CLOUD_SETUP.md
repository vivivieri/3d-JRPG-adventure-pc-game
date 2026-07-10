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

## 4. Cloud Agent setup (experimental)

Cloud agents on this repo today use **code-driven** environments (`zone_visuals.gd`, `terrain_shapes.gd`) and **headless** Godot for screenshots. GDAI is **optional** and harder in cloud because the **Editor must stay open** for the whole agent run.

### What works well in cloud

- Procedural environment edits in GDScript
- `./tools/capture_screenshots.sh`
- PR screenshot updates under `steam/screenshots-capture/`

### What GDAI adds (usually local)

- In-editor scene/node placement and polish
- Live script error / output log inspection from the editor

### If you want to try GDAI in a Cursor Cloud environment

1. **Install in the environment image**
   - `uv`
   - Full **Godot 4.3 editor** (not only the headless binary in `.godot-sdk/`)
   - Manually copy `gdai-mcp-plugin-godot` into `game/addons/` on the VM (same as local; not in git)

2. **Register MCP for Cloud Agents**
   - Open https://cursor.com/agents → **MCP** dropdown → add a **stdio** server
   - Use the same `uv run .../gdai_mcp_server.py` command
   - Team plans: **Dashboard → Integrations & MCP**

3. **Start Godot Editor before / during the agent run**

   ```bash
   export DISPLAY="${DISPLAY:-:1}"
   /path/to/Godot --path game/project.godot --editor &
   ```

   Enable the plugin once per environment (or bake it into a saved environment snapshot with the plugin already enabled in `project.godot` user settings — dev VMs only).

4. **Expect fragility**
   - Editor must remain running with MCP **Started**
   - Plugin license is per-seat/commercial — confirm terms for CI/cloud use
   - Stdio MCP runs inside the agent VM; HTTP MCP is preferred for secrets when possible (GDAI uses stdio)

### Hybrid workflow (recommended for *Tides of Urashima*)

| Work | Where |
|------|--------|
| Zone rewrites, terrain, screenshots | **Cloud Agent** |
| Palace prop nudging, scene polish, material tweaks | **Local Godot + GDAI** |
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
