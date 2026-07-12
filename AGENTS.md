# AGENTS.md — Cloud Agent instructions

## Cursor Cloud specific instructions

**Repo:** Tides of Urashima — stylized 3D JRPG (Godot 4.7 Forward+)  
**Design source of truth:** `docs/` on `main` + `game/data/` JSON  
**Documentation index:** `docs/README.md`  
**Build order:** `docs/IMPLEMENTATION_PLAN.md` (M5 art → M6 Steam) — checklist in `docs/MILESTONES.md`  
**Implementation plan:** `docs/IMPLEMENTATION_PLAN.md`  
**Workflow:** **GodotPrompter + full MCP toolchain** — see `.cursorrules` §0, `docs/MCP_STACK.md`, `docs/AI_DEV_WORKFLOW.md`

| Tool / MCP server | Role |
|-------------------|------|
| GodotPrompter | Plan, GDScript, shaders, tests |
| `godot-mcp` (GDAI) | **Build** scenes |
| `godotiq` | **Analyze** signals/debug |
| `godot-mcp-pro` | **Test** scenarios/asserts (L4/L5) |
| `gamelab-mcp` | **UI art** — frames, icon sheets *(P1 — WARN if absent)* |
| ComfyUI / Material Maker | **Zone NPR albedos** — offline |
| Meshy / Tripo / Rodin + Blender | **3D hero pipeline** — offline |
| `generate_game_audio.py` + ACE-Step 1.5 | **Audio** placeholders + zone/opening/boss/ending hero BGM |
| `generate_ai_vo.py` + ElevenLabs | **Selective VO** — 12 emotional clips only (`docs/VO_HIT_LIST.md`) |

**P0 MCP required** (`godot-mcp`, `godotiq`, `godot-mcp-pro`). Art generators tiered — see `docs/ART_AUTOMATION_PIPELINE.md`. If P0 missing → STOP and notify user.

### Environment bootstrap

On every cloud agent start:

```bash
bash tools/install_cloud_dev.sh      # Godot, uv, Godotiq, MCP Pro, Blender
bash tools/ensure_mcp_stack.sh       # Editor + MCP bridges — REQUIRED
bash tools/install_extended_toolchain.sh  # Blender, audio placeholders, GameLab config
bash tools/check_extended_toolchain.sh    # Full toolchain status
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
2. docs/ + game/data/ — design context before data/combat edits
3. ComfyUI/Material Maker or gamelab-mcp — art gen → palette_remap.py → game/assets/
4. godot-mcp (GDAI) — build scenes, materials, F5 verify
5. godotiq — trace_flow / signal_map when debugging systems
6. godot-mcp-pro — run_test_scenario for L4/L5 playthrough asserts
7. Meshy/Blender offline — hero GLB meshes when 3D art task requires it
```

**Scene edits:** GDAI only. Do not hand-edit `.tscn`.

### If MCP unavailable — NOTIFY USER, DO NOT FALL BACK

| Server | Check |
|--------|-------|
| GDAI | `curl -sf http://127.0.0.1:3571/tools`; plugin + `godot-mcp` in Cursor |
| Godotiq | `game/addons/godotiq/`; `godotiq` in Cursor MCP |
| MCP Pro | `tools/godot-mcp-pro-server/build/index.js`; `godot-mcp-pro` in Cursor |
| GameLab | `gamelab-mcp` in Cursor MCP; API key in Secrets *(WARN if absent — UI art)* |
| ComfyUI / Material Maker | Local install for zone albedos |

Register all installed servers in Cursor (desktop Settings or cloud dashboard). See `docs/MCP_STACK.md`.

### Copyright-safe procedural assets

| Type | Generator |
|------|-----------|
| Zone NPR albedos | ComfyUI / Material Maker + `palette_remap.py` |
| UI art | GameLab MCP (when key set) |
| BGM / SFX | `python3 tools/generate_game_audio.py --all` + ACE-Step ship path |
| Selective VO | `bash tools/generate_ai_vo.sh --tier p0` (needs `ELEVENLABS_API_KEY`) |
| Portrait placeholders | `python3 tools/generate_procedural_portraits.py --all` |
| Manifest | `python3 tools/register_asset.py add --help` |

No web-scraped art/audio. See `docs/ASSET_COMPLIANCE.md`.

### Automated testing & QA (required every commit)

See `docs/AI_DEV_WORKFLOW.md` for policy and `docs/ACCEPTANCE_CRITERIA.md` for **measurable** pass/fail.

```bash
export PATH="$HOME/.local/bin:$PATH"
export XDG_DATA_HOME="/workspace/.cache/godot-data"
export XDG_CONFIG_HOME="/workspace/.cache/godot-config"
export XDG_CACHE_HOME="/workspace/.cache/godot-cache"

python3 tools/validate_story_data.py          # L0
python3 tools/validate_acceptance_criteria.py # catalog lint
bash tools/run_unit_tests.sh                  # L1
bash tools/run_playtest_smoke.sh              # L2 (data + boot + art smokes)
bash tools/run_integration_tests.sh           # L4 phase gates (Phase 2+)
bash tools/run_e2e_playthrough.sh             # L5 (Phase 6+; blocks human QA)
bash tools/check_asset_compliance.sh
```

| QA domain | Policy doc | On FAIL |
|-----------|------------|---------|
| Acceptance thresholds | `docs/ACCEPTANCE_CRITERIA.md` | Fix metric; cite gate id in report |
| 3D models | `docs/MODEL_QA.md` | `qa_emit_remediation.sh model-tech\|model-jury` |
| Visuals | `docs/VISUAL_QA.md` | `qa_emit_remediation.sh visual-palette\|visual-jury` |
| Audio | `docs/AUDIO_QA.md` | `qa_emit_remediation.sh audio-tech\|audio-jury` |
| Game flow | `docs/FLOW_QA.md` | `qa_emit_remediation.sh flow-scenario INT-*` |
| Iteration | `docs/QA_REMEDIATION_LOOP.md` | One lever per attempt; max 3 |

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
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` — visual + model turntable jury
- `OPENAI_API_KEY` / `GEMINI_API_KEY` — audio listen jury
- Steam API keys (Phase 8 only)

### Do not ship

- Do not ship: `game/addons/gdai-mcp-plugin-godot/`, `game/addons/godotiq/`, `game/addons/godot_mcp/`
- Disable GDAI before Steam export
