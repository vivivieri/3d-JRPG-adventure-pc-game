---
id: install
type: how-to
audience: [pm, builder]
status: active
authority: agents
tokens_est: 640
---
# MCP — Install

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## Install — Godot MCP plugins

**Step-by-step:** `docs/ops/agents/PLUGIN_INSTALL_GUIDE.md`, `docs/ops/agents/GDAI_CLOUD_SETUP.md`

### 1. GDAI MCP

```bash
bash tools/install_gdai_plugin.sh    # zip in game/addons/
```

Enable **GDAI MCP** plugin → panel → **Start**.

### 2. Godotiq

```bash
bash tools/install_godotiq.sh
```

Enable **GodotIQ** plugin. Pro license (optional upgrade): `GODOTIQ_LICENSE_KEY` in MCP env.

### 3. Godot MCP Pro

```bash
# Full package zip: game/addons/godot-mcp-pro*.zip
bash tools/install_godot_mcp_pro.sh
```

Requires **Node.js 18+**. Enable **Godot MCP Pro** plugin.

### 4. Bootstrap all Godot bridges

```bash
bash tools/ensure_mcp_stack.sh
```

Writes `.cursor/mcp.json` for installed Godot MCP servers, starts editor, checks HTTP/WebSocket bridges.

---

## Install — Cursor MCP servers

Register **every** server in Cursor (desktop Settings → Tools & MCP, or [cursor.com/agents](https://cursor.com/agents) cloud dashboard). Restart agent after save.

`tools/write_mcp_config.sh` generates Godot-related entries. Merge with GameLab manually when `GAMELAB_API_KEY` is set (Cursor Secrets tab).

### Full `mcpServers` example

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "/workspace/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"]
    },
    "godotiq": {
      "command": "uvx",
      "args": ["godotiq"],
      "env": {
        "GODOTIQ_PROJECT_ROOT": "/workspace/game"
      }
    },
    "godot-mcp-pro": {
      "command": "node",
      "args": [
        "/workspace/tools/godot-mcp-pro-server/build/index.js",
        "--minimal"
      ],
      "env": {
        "GODOT_MCP_PORT": "6505"
      }
    },
    "gamelab-mcp": {
      "type": "sse",
      "url": "http://api.gamelabstudio.co:8765/sse",
      "headers": {
        "X-API-Key": "YOUR_GAMELAB_API_KEY"
      }
    }
  }
}
```

**GameLab API key:** Store in Cursor Secrets — not committed to git.

Template: `.cursor/mcp.json.example`

---

## Ports (defaults)

| Server | Port | Check |
|--------|------|-------|
| GDAI HTTP | 3571 | `curl -sf http://127.0.0.1:3571/tools` |
| Godotiq WebSocket | 6007 | GodotIQ plugin auto-connects |
| Godot MCP Pro | 6505 | Plugin panel in editor |

---

## Godot editor plugins (enable all)

| Plugin | MCP server |
|--------|------------|
| GDAI MCP | `godot-mcp` |
| GodotIQ | `godotiq` |
| Godot MCP Pro | `godot-mcp-pro` |

Start **GDAI MCP** panel → **Start** after editor opens.

---

