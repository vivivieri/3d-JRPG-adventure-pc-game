# AGENTS.md — Cloud Agent instructions

## Cursor Cloud specific instructions

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.7 Forward+)  
**Design source of truth:** `docs/` on `main` + `game/data/` JSON  
**Implementation plan:** `docs/IMPLEMENTATION_PLAN.md`  
**Workflow:** **GodotPrompter + full MCP toolchain** — see `.cursorrules` §0, `docs/MCP_STACK.md`, `docs/AI_DEV_WORKFLOW.md`

| Tool / MCP server | Role |
|-------------------|------|
| GodotPrompter | Plan, GDScript, shaders, tests |
| `godot-mcp` (GDAI) | **Build** scenes |
| `godotiq` | **Analyze** signals/debug |
| `godot-mcp-pro` | **Test** scenarios/asserts (L4/L5) |
| `gamelab-mcp` | **Art generate** — textures, UI sheets |
| `notion` | **Design context** — formulas, lore, balance |
| Blender + AI Render | **3D hero pipeline** (offline) |
| `generate_game_audio.py` + Suno/Udio | **Audio** placeholders + zone BGM prototypes |

**All tools are required.** If any are missing → STOP and notify user. See `docs/MCP_STACK.md`.

### Environment bootstrap

On every cloud agent start:

```bash
bash tools/install_cloud_dev.sh      # Godot, uv, Godotiq, MCP Pro
bash tools/ensure_mcp_stack.sh       # Editor + MCP bridges — REQUIRED
bash tools/check_dev_environment.sh
```

Installed components:
- **Godot 4.7** editor → `godot4` in `~/.local/bin`
- **uv / uvx** → GDAI + Godotiq MCP bridges
- **Node.js** → Godot MCP Pro server (if installed)
- **GDAI MCP** → `game/addons/gdai-mcp-plugin-godot/` (commercial)
- **Godotiq** → `game/addons/godotiq/` (`bash tools/install_godotiq.sh`)
- **Godot MCP Pro** → `game/addons/godot_mcp/` + `tools/godot-mcp-pro-server/` (commercial)

### MCP workflow (mandatory — all tools)

```
0. bash tools/ensure_mcp_stack.sh
1. GodotPrompter — plan GDScript, shaders, tests
2. notion — design context before data/combat edits
3. gamelab-mcp — generate textures/UI → game/assets/
4. godot-mcp (GDAI) — build scenes, materials, F5 verify
5. godotiq — trace_flow / signal_map when debugging systems
6. godot-mcp-pro — run_test_scenario for L4/L5 playthrough asserts
7. Blender offline — hero GLB meshes when 3D art task requires it
```

**Scene edits:** GDAI only. Do not hand-edit `.tscn`.

### If MCP unavailable — NOTIFY USER, DO NOT FALL BACK

| Server | Check |
|--------|-------|
| GDAI | `curl -sf http://127.0.0.1:3571/tools`; plugin + `godot-mcp` in Cursor |
| Godotiq | `game/addons/godotiq/`; `godotiq` in Cursor MCP |
| MCP Pro | `tools/godot-mcp-pro-server/build/index.js`; `godot-mcp-pro` in Cursor |
| GameLab | `gamelab-mcp` in Cursor MCP; API key in Secrets |
| Notion | `notion` in Cursor Integrations |
| Blender | Installed locally for hero 3D pipeline |

Register all installed servers in Cursor (desktop Settings or cloud dashboard). See `docs/MCP_STACK.md`.

### Copyright-safe procedural assets

| Type | Generator |
|------|-----------|
| BGM / SFX | `python3 tools/generate_game_audio.py --all` |
| Portrait placeholders | `python3 tools/generate_procedural_portraits.py --all` |
| Manifest | `python3 tools/register_asset.py` |

No web-scraped art/audio. See `docs/ASSET_COMPLIANCE.md`.

### Automated testing (required every commit)

See `docs/AI_DEV_WORKFLOW.md` for full policy and **phase acceptance criteria**.

```bash
export PATH="$HOME/.local/bin:$PATH"
export XDG_DATA_HOME="/workspace/.cache/godot-data"
export XDG_CONFIG_HOME="/workspace/.cache/godot-config"
export XDG_CACHE_HOME="/workspace/.cache/godot-cache"

python3 tools/validate_story_data.py   # L0 data validation
bash tools/run_unit_tests.sh           # L1 unit tests
bash tools/run_playtest_smoke.sh       # L2 smoke (includes L0+L1)
bash tools/run_integration_tests.sh    # L4 phase gates (Phase 2+)
bash tools/run_e2e_playthrough.sh      # L5 endings (Phase 6+; blocks human QA)
bash tools/check_asset_compliance.sh
```

GDAI MCP F5 = **L3**; Godotiq = debug/trace; Godot MCP Pro = L4/L5 scenarios (`docs/AI_TESTING_SPEC.md`, `docs/MCP_STACK.md`).

**Human QA:** Only after L0–L5 pass — `docs/PLAYTEST_SCRIPT.md` (`docs/AI_TESTING_SPEC.md` §8).

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

- Do not ship: `game/addons/gdai-mcp-plugin-godot/`, `game/addons/godotiq/`, `game/addons/godot_mcp/`
- Disable GDAI before Steam export
