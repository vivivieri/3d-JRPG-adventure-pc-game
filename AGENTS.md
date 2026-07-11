# AGENTS.md — Cloud Agent instructions

## Cursor Cloud specific instructions

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.3+ Forward+)  
**Design source of truth:** `docs/` on `main` + `game/data/` JSON  
**Implementation plan:** `docs/IMPLEMENTATION_PLAN.md`  
**Workflow:** **GodotPrompter + GDAI MCP only** — see `.cursorrules` §0

### Environment bootstrap

On every cloud agent start:

```bash
bash tools/install_cloud_dev.sh      # Godot, uv, export templates
bash tools/ensure_gdai_mcp.sh        # Editor + GDAI HTTP bridge — REQUIRED
bash tools/check_dev_environment.sh
```

Installed components:
- **Godot 4.3** editor → `godot4` in `~/.local/bin`
- **uv** → GDAI MCP Python stdio bridge
- **Export templates** → `.cache/godot-data/godot/export_templates/`
- **GDAI MCP plugin** → `game/addons/gdai-mcp-plugin-godot/` (dev-only, not in git)

### GodotPrompter + GDAI MCP workflow (mandatory)

Use **both** tools together. **Do not** hand-edit `.tscn` or implement editor work without GDAI MCP.

```
0. bash tools/ensure_gdai_mcp.sh
1. GodotPrompter — plan shaders, GDScript, architecture
2. GDAI MCP     — execute in live Godot Editor (scenes, nodes, materials, F5)
3. GDAI MCP     — verify viewport + debugger; loop until clean
```

### If GDAI MCP is unavailable — NOTIFY USER, DO NOT FALL BACK

| Check | Command / signal |
|-------|------------------|
| HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` |
| Editor running | `pgrep -f 'godot4.*game.*--editor'` |
| Cursor MCP | `godot-mcp` listed in Cursor Settings → MCP (connected) |
| Plugin present | `game/addons/gdai-mcp-plugin-godot/` |

**If `godot-mcp` is not in the agent's MCP server list:**

1. Run `bash tools/ensure_gdai_mcp.sh` (VM bootstrap)
2. Register MCP:
   - **Desktop:** Cursor **Settings → Tools & MCP** → add `godot-mcp`
   - **Cloud:** [cursor.com/agents](https://cursor.com/agents) dashboard → add custom MCP server (see `docs/GDAI_CLOUD_SETUP.md` §4.3)
3. Restart cloud agent
4. Agent: **stop implementation** until `godot-mcp` tools appear

**Never substitute** manual `.tscn` editing or headless-only work for GDAI MCP editor integration.

### Copyright-safe procedural assets

| Type | Generator |
|------|-----------|
| BGM / SFX | `python3 tools/generate_game_audio.py --all` |
| Portrait placeholders | `python3 tools/generate_procedural_portraits.py --all` |
| Manifest | `python3 tools/register_asset.py` |

No web-scraped art/audio. See `docs/ASSET_COMPLIANCE.md`.

### Headless validation (supplement only — not a substitute for GDAI)

Headless tests confirm data/logic after GDAI editor verification:

```bash
export PATH="$HOME/.local/bin:$PATH"
export XDG_DATA_HOME="/workspace/.cache/godot-data"
export XDG_CONFIG_HOME="/workspace/.cache/godot-config"
export XDG_CACHE_HOME="/workspace/.cache/godot-cache"

python3 tools/validate_story_data.py
bash tools/run_playtest_smoke.sh
bash tools/check_asset_compliance.sh
```

### Rendering & environment (Phase 1)

Before building zones, read:
- `docs/RENDERING_GUIDE.md`
- `docs/ENVIRONMENT_KITS.md`
- `docs/ART_DIRECTION.md`

Build order: **ruined_village** vertical slice → beach → caves → palace.  
All scene work via **GDAI MCP** after GodotPrompter plans.

### Secrets (if needed)

Configure in Cursor **Secrets** tab (not committed):
- GDAI plugin license path / download token (if applicable)
- Steam API keys (Phase 8 only)

### Do not ship

- `game/addons/gdai-mcp-plugin-godot/` — dev only, gitignored
- Disable GDAI before Steam export
