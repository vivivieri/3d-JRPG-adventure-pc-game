---
id: mcp-verify-workflow
type: how-to
phase: [0, 1]
audience: [pm, builder]
status: active
authority: ops
tokens_est: 658
summary: "GDAI — Configure Cloud Agents — MCP register + verify + workflow — 1. Open your cloud environment dashboard, e.g."
---
# GDAI — Configure Cloud Agents — MCP register + verify + workflow

**Hub:** [`cloud_agents.md`](../cloud_agents.md)

## When to read

Use **GDAI — Configure Cloud Agents — MCP register + verify + workflow** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4.3 Register MCP in Cursor dashboard (required for agent tools)](#43-register-mcp-in-cursor-dashboard-required-for-agent-tools)
- [4.4 Verify (cloud)](#44-verify-cloud)
- [4.5 Workflow (mandatory — no manual fallback)](#45-workflow-mandatory-no-manual-fallback)


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
