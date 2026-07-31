---
id: godotiq
type: how-to
phase: [0, 1]
audience: [builder, pm]
status: active
authority: ops
tokens_est: 627
summary: "https://godotiq.com/ — set `GODOTIQ_LICENSE_KEY` in MCP env for extra tools."
---
# Plugin Install Guide — Godotiq install

**Hub:** [`PLUGIN_INSTALL_GUIDE.md`](../PLUGIN_INSTALL_GUIDE.md)

## When to read

Use **Plugin Install Guide — Godotiq install** (roles: builder, pm) when executing this procedure Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [Godotiq](#godotiq)
- [What you need](#what-you-need)
- [Local install](#local-install)
- [Cursor — desktop](#cursor-desktop)
- [Cursor — Cloud Agents](#cursor-cloud-agents)
- [Verify Godotiq](#verify-godotiq)


## Godotiq

### What you need

| Piece | How you get it |
|-------|----------------|
| Python package | `pip install godotiq` (script does this) |
| Godot addon | Copied to `game/addons/godotiq/` by install script |
| Cursor bridge | `uvx godotiq` |
| Editor bridge | WebSocket on `127.0.0.1:6007` when GodotIQ plugin is enabled |

**Purchase (optional Pro):** https://godotiq.com/ — set `GODOTIQ_LICENSE_KEY` in MCP env for extra tools.

### Local install

```bash
# From repo root
bash tools/install_godotiq.sh
```

Then in Godot:

1. Open `game/project.godot`
2. **Project → Project Settings → Plugins**
3. Enable **GodotIQ**
4. Confirm in Output: `GodotIQ: WebSocket server listening on 127.0.0.1:6007`

Regenerate MCP config and bootstrap:

```bash
bash tools/write_mcp_config.sh
bash tools/ensure_gdai_mcp.sh
```

### Cursor — desktop

After `write_mcp_config.sh`, `.cursor/mcp.json` should include:

```json
"godotiq": {
  "command": "uvx",
  "args": ["godotiq"],
  "env": {
    "GODOTIQ_PROJECT_ROOT": "/absolute/path/to/game"
  }
}
```

1. **Cursor Settings → Tools & MCP** — add or sync `godotiq`
2. Restart Cursor
3. Keep Godot editor open with **GodotIQ** enabled

**Pro license (optional):**

```json
"env": {
  "GODOTIQ_PROJECT_ROOT": "/absolute/path/to/game",
  "GODOTIQ_LICENSE_KEY": "your-key"
}
```

### Cursor — Cloud Agents

Godotiq installs from the network (no zip upload).

1. In the setup agent terminal:

```bash
bash tools/install_godotiq.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_plugin_compatibility.sh
```

2. Register at [cursor.com/agents](https://cursor.com/agents) → **Integrations & MCP**:

```json
{
  "command": "uvx",
  "args": ["godotiq"],
  "env": {
    "GODOTIQ_PROJECT_ROOT": "/workspace/game"
  }
}
```

3. Restart the cloud agent
4. **Save snapshot** so `game/addons/godotiq/` is pre-installed for future runs

### Verify Godotiq

```bash
ss -tln | grep 6007          # WebSocket listening
bash tools/check_plugin_compatibility.sh
```

---
