---
id: cloud-agents
type: how-to
phase: [0, 1]
audience: [pm, builder, release]
status: active
authority: ops
tokens_est: 1234
summary: "Configure Cloud Agents"
---
# GDAI Setup — Cloud / Steam / Troubleshoot — Configure Cloud Agents

**Hub:** [`cloud_steam_troubleshoot.md`](../cloud_steam_troubleshoot.md)

## 4. Configure Cursor — Cloud Agents

Cloud agents run in a remote VM. You need **both** VM bootstrap **and** Cursor dashboard MCP registration.

> **Latest Cursor guidance (2026):** Cloud Agents support MCP servers configured in the **Cloud Agents dashboard** ([cursor.com/agents](https://cursor.com/agents)). Team plans: **Dashboard → Integrations & MCP**.
> A workspace `.cursor/mcp.json` helps the VM but **does not by itself** expose `godot-mcp` tools to the agent — you must register the server in the dashboard and restart the agent.

### 4.1 Environment bootstrap (VM)

**Snapshot ID + launch checklist:** `docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md` — active snapshot `snapshot-20260714-8addf87a-f344-489f-bbe2-da0f57cb66d8`, boot verification, and `main` vs `game/development` pitfalls.

Cloud agents install dependencies via `.cursor/environment.json`:

```bash
bash tools/install_cloud_dev.sh   # Godot 4.7, uv, export templates
bash tools/ensure_gdai_mcp.sh     # Editor + GDAI HTTP bridge — REQUIRED
bash tools/check_dev_environment.sh
```

**Installed by `install_cloud_dev.sh`:**

| Component | Location |
|-----------|----------|
| Godot 4.7 editor | `godot4` → `~/.local/bin` |
| Export templates | `.cache/godot-data/godot/export_templates/` |
| uv | `~/.local/bin/uv` |
| numpy | Python (trailer tool) |

**`ensure_gdai_mcp.sh` does:**

1. Writes `.cursor/mcp.json` for the `godot-mcp` stdio bridge
2. Starts Godot Editor if not running (`--rendering-driver opengl3`)
3. Waits for GDAI HTTP `http://127.0.0.1:3571/tools`
4. Exits non-zero with notify instructions if the bridge is not ready

### 4.2 GDAI plugin in cloud (required — not in git)

GDAI MCP is **commercial** and **gitignored**. Snapshots cloned from GitHub **do not** include it. Install it once, then **save a snapshot**.

**Option A — Rebuild snapshot (recommended)**

1. [cursor.com/agents](https://cursor.com/agents) → your environment → **Start Setup Agent**
2. Upload your purchase zip to the VM:
   ```
   game/addons/gdai-mcp-plugin-godot-YYYYMMDD.zip
   ```
3. Run in the setup terminal:
   ```bash
   bash tools/install_gdai_plugin.sh
   bash tools/ensure_gdai_mcp.sh
   curl -sf http://127.0.0.1:3571/tools | head -c 100
   ```
4. When setup succeeds, **save the snapshot**
5. Future agents boot with the plugin pre-installed

**Option B — Zip in snapshot folder**

If `game/addons/gdai-mcp-plugin-godot*.zip` exists, `install_cloud_dev.sh` auto-extracts on boot.

**Without the plugin:** `ensure_gdai_mcp.sh` fails, `.cursor/mcp.json` is not written, and `godot-mcp` MCP calls fail even if registered in the dashboard.

### 4.3 Register MCP in Cursor dashboard (required for agent tools)

1. Open your cloud environment dashboard, e.g.
   [cursor.com/dashboard/cloud-agents/environments](https://cursor.com/dashboard/cloud-agents/environments)
   → select this repo’s environment.
2. Or go to [cursor.com/agents](https://cursor.com/agents) → MCP / integrations.
3. **Add custom MCP server** named `godot-mcp`:

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "/workspace/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"]
    }
  }
}
```

Use `/workspace/...` for this cloud VM path, or the path shown in the Godot GDAI MCP panel for your environment.

4. **Restart the cloud agent** after saving.
5. Confirm the agent’s MCP catalog lists **`godot-mcp`** (not only Figma/Linear/Notion).

**Cloud MCP note:** `${env:VAR}` interpolation in dashboard MCP config often **fails** on cloud agents — paste literal secret values if your server needs `env` blocks.

### 4.4 Verify (cloud)

Run inside the agent VM:

```bash
bash tools/ensure_gdai_mcp.sh
curl -sf http://127.0.0.1:3571/tools | head -c 200   # should return JSON with mcp_tools
pgrep -af 'godot4.*--editor'                          # editor running
```

In the agent session, MCP catalog must include **`godot-mcp`**.
**Agents must not implement editor/scene work until both checks pass.**

### 4.5 Workflow (mandatory — no manual fallback)

See `.cursorrules` §0 and **`AGENTS.md`**.

| Work | Tool |
|------|------|
| GDScript, shaders, architecture | **GodotPrompter** (Cursor) |
| Scenes, nodes, materials, F5 verify | **GDAI MCP** only |
| Procedural BGM/SFX (copyright-safe) | `python3 tools/generate_game_audio.py` |
| Procedural portrait placeholders | `python3 tools/generate_procedural_portraits.py` |
| Logic/data smoke (after GDAI verify) | `bash tools/run_playtest_smoke.sh` |
| JRPG UI/combat playtest via live editor | GDAI MCP — see `docs/ops/qa/AI_TESTING_SPEC.md` §11 |
| Steam build | **No GDAI** in `game/addons/` |

---
