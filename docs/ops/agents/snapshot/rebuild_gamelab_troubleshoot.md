---
id: rebuild-gamelab-troubleshoot
type: tutorial
phase: [0, 1]
audience: [pm, builder, architect]
status: active
authority: ops
tokens_est: 652
summary: "Rebuild, GameLab transport, troubleshooting"
---
# Cloud Snapshot Launch — Rebuild, GameLab transport, troubleshooting

**Hub:** [`CLOUD_SNAPSHOT_LAUNCH.md`](../CLOUD_SNAPSHOT_LAUNCH.md)

## 4. Rebuild snapshot (one-time or after toolchain change)

1. Dashboard → environment → **Start Setup Agent**
2. Checkout `game/development`:

   ```bash
   git fetch origin game/development
   git checkout game/development
   ```

3. Upload GDAI purchase zip (not in git):

   ```
   game/addons/gdai-mcp-plugin-godot-YYYYMMDD.zip
   ```

4. Bootstrap:

   ```bash
   bash tools/install_cloud_dev.sh
   bash tools/install_gdai_plugin.sh
   bash tools/install_extended_toolchain.sh
   bash tools/ensure_mcp_stack.sh
   bash tools/check_mcp_ready.sh
   bash tools/check_extended_toolchain.sh
   curl -sf http://127.0.0.1:3571/tools | head -c 100
   ```

5. **Save snapshot** in the dashboard
6. Copy the new snapshot id into `.cursor/environment.json` on `game/development`
7. Commit and push; register MCP servers in the dashboard

**Snapshot must include:** Godot 4.7, GDAI plugin, Godotiq, MCP Pro build, Blender, `uv`, Node — see `docs/ops/agents/GDAI_CLOUD_SETUP.md` §4.

---


## 5. GameLab MCP (`gamelab-mcp`) — known Cursor transport issue

GameLab’s endpoint is **SSE-only** (`GET /sse` → 200; `POST /sse` → 405). Cursor may show:

> Streamable HTTP error: Error POSTing to endpoint: Method Not Allowed

**Workaround** — register via `mcp-remote` in Dashboard → Integrations & MCP:

```json
{
  "mcpServers": {
    "gamelab-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://api.gamelabstudio.co:8765/sse",
        "--transport",
        "sse-only",
        "--allow-http",
        "--header",
        "X-API-Key:${GAMELAB_API_KEY}"
      ],
      "env": {
        "GAMELAB_API_KEY": "set-in-cursor-secrets"
      }
    }
  }
}
```

Store the key in **Cursor Secrets** as `GAMELAB_API_KEY` — never commit it.

---


## 6. Quick troubleshooting

| Problem | Fix |
|---------|-----|
| `build: null` | Launch from environment dashboard on `game/development`, not JIT on `main` |
| GDAI bridge down | Rebuild snapshot with plugin; run `bash tools/ensure_gdai_mcp.sh` |
| `gamelab-mcp` 405 error | Use `mcp-remote` config (§5) |
| Stale snapshot after Godot/MCP upgrade | Re-run §4, save new snapshot, update `snapshot` id in `environment.json` |
| Docs/data only work | Stay on `main` — snapshot not required |
