---
id: mcp-stack
type: how-to
audience: [pm, builder]
status: active
authority: agents
tokens_est: 1628
---
# MCP Stack — Full Toolchain (Godot 4.7)

**Version:** 2.0
**Applies to:** `main` rebuild workflow — **Godot 4.7 stable**
**Cross-refs:** `.cursorrules` §0–§1, `docs/design/art/ART_AUTOMATION_PIPELINE.md`, `docs/ops/agents/GDAI_CLOUD_SETUP.md`, `docs/ops/agents/PLUGIN_INSTALL_GUIDE.md`, `docs/ops/workflow/AI_DEV_WORKFLOW.md`, `docs/ops/qa/AI_TESTING_SPEC.md`, `docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `docs/ops/qa/QA_REMEDIATION_LOOP.md`, `docs/design/art/ART_DIRECTION.md`, `docs/design/art/ASSET_COMPLIANCE.md`

**Tiered requirements:** All MCP servers (`godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`) are **required** — if missing, **STOP and notify the user**. **Blender** is **required** for M5 turntable QA (`docs/design/art/MODEL_QA.md`). Procedural UI placeholders are OK for **asset output** until GameLab gen ships — the MCP server itself is still required. Offline generators (ComfyUI, ACE-Step) use quality-first fallbacks per `docs/design/art/ART_AUTOMATION_PIPELINE.md`. Do not fall back to manual `.tscn` edits or undocumented web assets.

---
## Full R&R map

| Layer | Tool | Cursor / access | Role |
|-------|------|-----------------|------|
| Plan & code | **GodotPrompter** | Cursor agent | GDScript, shaders, tests, architecture |
| Design context | **`docs/` + `game/data/`** | Repo | Stat formulas, flags, dialogue — authoritative |
| Zone NPR albedos | **ComfyUI** or **Material Maker** | Offline — not MCP | Stylized tileables; `tools/palette_remap.py` post-step |
| UI art generate | **GameLab Studio MCP** | `gamelab-mcp` (SSE) | UI frames, ink borders, icon/VFX sheets **(required)** |
| 3D heroes / props | **Meshy / Tripo / Rodin** + **Blender** (required) | Offline — not MCP | AI 3D → GLB; Mixamo rig; M5 turntable QA |
| Build | **GDAI MCP** | `godot-mcp` | Scenes, nodes, materials, lights, F5 playtest |
| Analyze | **Godotiq** | `godotiq` | Signals, debug console, `ui_map`, validation |
| Test | **Godot MCP Pro** | `godot-mcp-pro` (`--minimal`) | L4/L5 scenarios, asserts, input replay |
| Audio placeholder | `generate_game_audio.py` | Shell | Copyright-safe BGM/SFX until replaced |
| Audio prototype | **ACE-Step 1.5** | Local (`bash tools/install_ace_step.sh`) | Zone + opening/boss/ending hero BGM |
| VO selective | **ElevenLabs** | `ELEVENLABS_API_KEY` + `generate_ai_vo.py` | 12 emotional hit clips — `docs/design/vision/VO_HIT_LIST.md` |
| Marketing trailer | `generate_marketing_trailer.py` | Shell (`ffmpeg`, `numpy`) | Ken Burns pitch PNGs → `steam/trailer*.mp4` |
| Video AI (optional) | Runway / Kling / similar | Offline — not MCP | Marketing trailer b-roll only — never in-game |

```
GodotPrompter (plan/code)
       │
       ├─► ComfyUI / Material Maker ─► zone albedos → palette_remap.py → game/assets/
       ├─► GameLab MCP ─────────────► UI sheets / frames → palette_remap.py → game/assets/
       ├─► AI 3D + Blender (offline) ► hero GLB → import → GDAI places
       ├─► GDAI MCP ────────────────► create/edit scenes, F5 verify
       ├─► Godotiq ─────────────────► trace_flow, signal_map, debug console
       └─► Godot MCP Pro ───────────► run_test_scenario, assert_screen_text
```

**Rule:** Each tool owns its layer. They **supplement** each other — none replaces GDAI for `.tscn` mutations, Godotiq for debug, or MCP Pro for L4/L5 tests.

---

## Role split & conflict rules

| Situation | Required tool |
|-----------|---------------|
| Create/edit `.tscn`, nodes, materials in editor | **GDAI MCP only** |
| Generate tileable zone albedo | **ComfyUI** or **Material Maker** → `palette_remap.py` → **GDAI** assigns |
| Generate UI frame / ink border | **GameLab MCP** → `palette_remap.py` → **GDAI** UI scenes |
| Read stat formula before balancing skill | **`docs/` + `game/data/`** → edit JSON |
| Hero 3D model + stylized albedo | **Meshy/Tripo/Rodin** → Blender → GLB → **GDAI** places |
| Combat signal hang — which signal failed? | **Godotiq** `godotiq_signal_map`, `godotiq_trace_flow` |
| Automated JRPG menu / combat test | **Godot MCP Pro** testing tools |
| Read Godot Output without copy-paste | **Godotiq** `godotiq_read_debug_console` |
| Screenshot game viewport | **GDAI**, **Godotiq**, or **MCP Pro**; save to `artifacts/screenshots/` |
| Zone BGM iteration | **ACE-Step** via `bash tools/generate_ai_bgm.sh` or `generate_game_audio.py` fallback → **GDAI** wires in editor |
| Selective story VO | **ElevenLabs** via `bash tools/generate_ai_vo.sh` — **only** lines with `voice_id` in `chapter_01.json`; never full script |
| Edit node tree / reparent | **GDAI only** |

**Never** use GameLab, Summer Engine, or Fennara for scene graph mutations when GDAI is available.

**Godot MCP Pro full mode (172 tools)** overlaps GDAI for scene editing. Always use **`--minimal`** (35 tools) in Cursor — testing + runtime + input focus only.

---

## Session startup (every agent run)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_dev_environment.sh
bash tools/check_extended_toolchain.sh
```

### Block until all required checks pass

| Check | How |
|-------|-----|
| R&R compliance (no hand `.tscn`) | `bash tools/check_rr_compliance.sh` exit 0 |
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Godotiq WebSocket | Port `6007` listening; GodotIQ plugin enabled |
| MCP Pro server | `tools/godot-mcp-pro-server/build/index.js` exists; plugin enabled |
| Godot Editor | Running with `game/project.godot` open |
| Cursor MCP catalog | **Required:** `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp` |
| GameLab API key | `GAMELAB_API_KEY` in Cursor Secrets |
| Blender | `blender` in PATH — required for M5 turntable QA |
| Offline art/audio | ComfyUI, Material Maker, ACE-Step GPU — document fallback used per task |

If **any required** MCP server or toolchain piece is missing → **STOP and notify the user**. See registration below.

---

## Packs (progressive disclosure)

| Topic | Pack |
|-------|------|
| Install / ports / plugins | [mcp/install.md](mcp/install.md) |
| Art & design tools | [mcp/art_tools.md](mcp/art_tools.md) |
| Testing & QA workflow | [mcp/testing.md](mcp/testing.md) |
| Cost, checklist, troubleshooting | [mcp/setup_and_cost.md](mcp/setup_and_cost.md) |

## Related gates

- Optional L2.5 tournament gate id: `L2_candidate_select` (`docs/ops/qa/CANDIDATE_TOURNAMENT.md`)

