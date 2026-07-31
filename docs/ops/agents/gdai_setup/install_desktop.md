---
id: install-desktop
type: how-to
audience: [builder, pm, architect]
status: active
authority: ops
tokens_est: 589
summary: "Install plugin + desktop Cursor"
---
# GDAI Cloud Setup — Install plugin + desktop Cursor

**Hub:** [`GDAI_CLOUD_SETUP.md`](../GDAI_CLOUD_SETUP.md)

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


## 3. Configure Cursor — Desktop (local IDE)

Use this when running Cursor on your machine with a local Godot editor.

### 3.1 Get the JSON from Godot (authoritative)

1. Open **GDAI MCP** tab in the Godot bottom panel.
2. Click **Start** the MCP server.
3. **Copy the JSON config** shown in that panel (paths match your machine).

### 3.2 Register in Cursor

**Method A — UI (recommended):**

1. Open **Cursor Settings** (`Ctrl+Shift+J` / `Cmd+Shift+J`).
2. Go to **Tools & MCP**.
3. Click **Add new global MCP server** (or edit project config).
4. Paste the JSON from the GDAI MCP panel.

**Method B — project file (team-shared):**

Create or edit `.cursor/mcp.json` in the project root:

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

Replace the path with your machine’s absolute path (or use the path from the GDAI panel).
Template: `.cursor/mcp.json.example`

### 3.3 Verify (desktop)

1. Restart Cursor.
2. **Settings → Tools & MCP** — `godot-mcp` shows **connected** (green).
3. Godot editor is open with this project.
4. In chat, Agent should list GDAI tools (scene tree, run scene, etc.).

---
