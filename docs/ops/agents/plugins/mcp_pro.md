---
id: mcp-pro
type: how-to
phase: [0, 1]
audience: [builder, pm]
status: active
authority: ops
tokens_est: 1045
summary: "Plugin Install Guide — Godot MCP Pro install — Use `--minimal` mode in Cursor (35 tools) so MCP Pro does not overlap GDAI for scene editing. See."
---
# Plugin Install Guide — Godot MCP Pro install

**Hub:** [`PLUGIN_INSTALL_GUIDE.md`](../PLUGIN_INSTALL_GUIDE.md)

## When to read

Use **Plugin Install Guide — Godot MCP Pro install** (roles: builder, pm) when executing this procedure Jump to a section below instead of reading end-to-end (9 sections).

## Jump to

- [Godot MCP Pro](#godot-mcp-pro)
- [What you need](#what-you-need)
- [Step 1 — Obtain the zip](#step-1-obtain-the-zip)
- [Step 2 — Install](#step-2-install)
- [Step 3 — Enable in Godot](#step-3-enable-in-godot)
- [Step 4 — Cursor MCP config](#step-4-cursor-mcp-config)
- [Cursor — desktop](#cursor-desktop)
- [Cursor — Cloud Agents](#cursor-cloud-agents)
- [Verify Godot MCP Pro](#verify-godot-mcp-pro)


## Godot MCP Pro

### What you need

| Piece | How you get it |
|-------|----------------|
| Purchased zip | https://godot-mcp.abyo.net/ or https://y1uda.itch.io/godot-mcp-pro |
| Godot addon | `game/addons/godot_mcp/` (from zip) |
| Node MCP server | `tools/godot-mcp-pro-server/` (from zip, `npm run build`) |
| Node.js | 18+ (`node --version`) |
| Editor bridge | WebSocket on `127.0.0.1:6505` (default) |

Use **`--minimal`** mode in Cursor (35 tools) so MCP Pro does not overlap GDAI for scene editing. See `docs/ops/agents/MCP_STACK.md`.

### Step 1 — Obtain the zip

1. Purchase at https://godot-mcp.abyo.net/ ($15, lifetime updates)
2. Download the **full package** (must include `addons/godot_mcp/` and `server/` with `package.json`)
3. Place in the repo (any matching name):

```
game/addons/godot-mcp-pro.zip
```

Accepted patterns: `godot-mcp-pro*.zip`, `godot_mcp_pro*.zip`

Or set an explicit path:

```bash
export GODOT_MCP_PRO_ZIP=/path/to/your/godot-mcp-pro.zip
```

### Step 2 — Install

```bash
bash tools/install_godot_mcp_pro.sh
```

This extracts:

- `game/addons/godot_mcp/` — Godot editor plugin
- `tools/godot-mcp-pro-server/` — Node server (`npm install && npm run build`)

Success marker: `tools/godot-mcp-pro-server/build/index.js` exists.

### Step 3 — Enable in Godot

1. Open `game/project.godot`
2. **Project → Project Settings → Plugins**
3. Enable **Godot MCP Pro**
4. Check the MCP Pro panel — connection to port **6505**

Add to `project.godot` `editor_plugins` if not already present:

```ini
"res://addons/godot_mcp/plugin.cfg"
```

### Step 4 — Cursor MCP config

```bash
bash tools/write_mcp_config.sh
```

Expected entry:

```json
"godot-mcp-pro": {
  "command": "node",
  "args": [
    "/absolute/path/to/tools/godot-mcp-pro-server/build/index.js",
    "--minimal"
  ],
  "env": {
    "GODOT_MCP_PORT": "6505"
  }
}
```

**Mode options** (set via `GODOT_MCP_PRO_MODE` before `write_mcp_config.sh`):

| Mode | Flag | Tools | Use when |
|------|------|-------|----------|
| Minimal | `--minimal` | 35 | Cursor (recommended — testing focus) |
| Lite | `--lite` | 84 | Windsurf, 100-tool limits |
| Full | (none) | 175 | Claude Code, no overlap concern |

### Cursor — desktop

1. **Cursor Settings → Tools & MCP** — add `godot-mcp-pro`
2. Restart Cursor
3. Godot editor open + **Godot MCP Pro** plugin enabled

### Cursor — Cloud Agents

The zip is **not in git**. You must upload it once, then save a snapshot.

1. [cursor.com/agents](https://cursor.com/agents) → **Start Setup Agent**
2. Upload zip to:

```
/workspace/game/addons/godot-mcp-pro.zip
```

3. Run:

```bash
bash tools/install_godot_mcp_pro.sh
bash tools/write_mcp_config.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_plugin_compatibility.sh
```

4. Register **godot-mcp-pro** in **Integrations & MCP**:

```json
{
  "command": "node",
  "args": [
    "/workspace/tools/godot-mcp-pro-server/build/index.js",
    "--minimal"
  ],
  "env": {
    "GODOT_MCP_PORT": "6505"
  }
}
```

5. **Save snapshot** (addon + built server persist for future agents)
6. Restart the cloud agent

**Tip:** Leave the zip in `game/addons/` inside the snapshot so a future `install_godot_mcp_pro.sh` can re-run on boot if needed (same pattern as GDAI).

### Verify Godot MCP Pro

```bash
test -f tools/godot-mcp-pro-server/build/index.js && echo "server OK"
node --version    # must be 18+
ss -tln | grep 6505
bash tools/check_plugin_compatibility.sh --with-editor
```

---
