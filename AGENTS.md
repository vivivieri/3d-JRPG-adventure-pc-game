# AGENTS.md — Cloud Agent instructions

## Cursor Cloud specific instructions

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.3+ Forward+)  
**Design source of truth:** `docs/` on `main` + `game/data/` JSON  
**Implementation plan:** `docs/IMPLEMENTATION_PLAN.md`

### Environment bootstrap

On every cloud agent start, dependencies are installed via `.cursor/environment.json`:

```bash
bash tools/install_cloud_dev.sh   # also runs automatically as install step
bash tools/check_dev_environment.sh
```

Installed components:
- **Godot 4.3** editor → `godot4` in `~/.local/bin`
- **uv** → GDAI MCP Python bridge
- **Export templates** → `.cache/godot-data/godot/export_templates/`
- **numpy** → trailer generator
- **Project folders** → `tools/setup_dev_environment.sh`

### GodotPrompter + GDAI MCP workflow

Use **both** tools together (see `.cursorrules`):

1. **GodotPrompter** — plan shaders, GDScript, architecture
2. **GDAI MCP** — execute in live Godot Editor (requires plugin + editor running)

**GDAI MCP plugin** is commercial and **not in git**. To enable in cloud:

1. Add `game/addons/gdai-mcp-plugin-godot/` (upload or secret mount)
2. Re-run `bash tools/install_cloud_dev.sh` (writes `.cursor/mcp.json`)
3. Godot editor starts via `tools/start_godot_editor.sh` (environment `start` command)
4. In Godot: enable **GDAI MCP** plugin → **Start** server
5. Restart Cursor MCP if tools do not appear

Without GDAI: edit `.gd` / `.tscn` / `.gdshader` files directly and validate with headless Godot.

### Headless validation

```bash
export PATH="$HOME/.local/bin:$PATH"
export XDG_DATA_HOME="/workspace/.cache/godot-data"
export XDG_CONFIG_HOME="/workspace/.cache/godot-config"
export XDG_CACHE_HOME="/workspace/.cache/godot-cache"

godot4 --headless --path game --quit-after 2
python3 tools/validate_story_data.py
bash tools/check_asset_compliance.sh   # when assets exist
```

### Rendering & environment (Phase 1)

Before building zones, read:
- `docs/RENDERING_GUIDE.md`
- `docs/ENVIRONMENT_KITS.md`
- `docs/ART_DIRECTION.md`

Build order: **ruined_village** vertical slice → beach → caves → palace.

Muted coastal palette — **not** bright anime/Ghibli defaults.

### Secrets (if needed)

Configure in Cursor **Secrets** tab (not committed):
- GDAI plugin license path / download token (if applicable)
- Steam API keys (Phase 8 only)

### Do not ship

- `game/addons/gdai-mcp-plugin-godot/` — dev only, gitignored
- Disable GDAI before Steam export
