# MCP Stack — Full Toolchain (Godot 4.7)

**Version:** 2.0  
**Applies to:** `main` rebuild workflow — **Godot 4.7 stable**  
**Cross-refs:** `.cursorrules` §0–§1, `docs/art/ART_AUTOMATION_PIPELINE.md`, `docs/agents/GDAI_CLOUD_SETUP.md`, `docs/agents/PLUGIN_INSTALL_GUIDE.md`, `docs/workflow/AI_DEV_WORKFLOW.md`, `docs/qa/AI_TESTING_SPEC.md`, `docs/qa/ACCEPTANCE_CRITERIA.md`, `docs/qa/QA_REMEDIATION_LOOP.md`, `docs/art/ART_DIRECTION.md`, `docs/art/ASSET_COMPLIANCE.md`

**Tiered requirements:** All MCP servers (`godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`) are **required** — if missing, **STOP and notify the user**. **Blender** is **required** for M5 turntable QA (`docs/art/MODEL_QA.md`). Procedural UI placeholders are OK for **asset output** until GameLab gen ships — the MCP server itself is still required. Offline generators (ComfyUI, ACE-Step) use quality-first fallbacks per `docs/art/ART_AUTOMATION_PIPELINE.md`. Do not fall back to manual `.tscn` edits or undocumented web assets.

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
| VO selective | **ElevenLabs** | `ELEVENLABS_API_KEY` + `generate_ai_vo.py` | 12 emotional hit clips — `docs/vision/VO_HIT_LIST.md` |
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

## Install — Godot MCP plugins

**Step-by-step:** `docs/agents/PLUGIN_INSTALL_GUIDE.md`, `docs/agents/GDAI_CLOUD_SETUP.md`

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

## Art & design tools

**Canonical policy:** `docs/art/ART_AUTOMATION_PIPELINE.md` — quality-first, zero human artists, tiered MCP.

### ComfyUI / Material Maker — zone NPR albedos

**Role:** Stylized tileable wood, stone, ground, hero texture sheets.  
**Does NOT:** Edit `.tscn` — hand off to GDAI after export.

**Workflow:**

```
1. READ  docs/art/ART_DIRECTION.md palette for target zone
2. ComfyUI (locked workflow) OR Material Maker — tileable albedo (muted coastal decay)
3. python3 tools/palette_remap.py --zone <zone> --input <png>
4. Save PNG → game/assets/textures/zones/<zone>/
5. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>  # see docs/art/LICENSES.md
6. GodotPrompter — tune toon shader if needed
7. GDAI MCP — assign materials in zone .tscn, F5 verify
8. bash tools/check_asset_compliance.sh
```

**Art constraints:** Muted palette (`#8B9DAF` fog, `#5C4A3A` wood, `#4AE8D8` biolume). Japanese coastal motifs — **not** bright Ghibli candy, not PBR realism, no European medieval reads.

### GameLab Studio MCP — UI & 2D sheets (required)

**Role:** Ink-wash UI frames, combat icon sheets, menu borders, VFX sprite sheets.  
**Does NOT:** Default path for zone tileables (use ComfyUI/Material Maker) or `.tscn` edits.

**Workflow:**

```
1. READ  docs/art/ART_DIRECTION.md §4 UI style
2. GameLab MCP — generate UI frame / icon sheet (muted, not candy-bright)
3. palette_remap.py → game/assets/textures/ui/
4. register_asset.py → GDAI assigns in UI .tscn
```

Setup: [gamelabstudio.co](https://gamelabstudio.co/) API key → register `gamelab-mcp` SSE server. **Required** — procedural UI placeholders OK for asset output until GameLab gen ships.

**Design context:** Read `docs/` + `game/data/` before balancing combat or editing JSON. No external design-index MCP.

**Why not Ink (Inkle):** Story spine is JSON-driven (`scenes.json` → `dialogue/` → `flags.json`). Ink adds a second runtime with no v1 benefit. See `docs/vision/NARRATIVE_WRITING_GUIDE.md`.

### AI 3D + Blender — offline hero pipeline (required for turntable QA)

**Role:** Automated stylized meshes and albedos for Japanese coastal heroes and set-pieces.  
**Not MCP** — offline batch before Godot import.

```
Meshy / Tripo / Rodin → Blender (decimate, UV) → ComfyUI/Material Maker albedo
  → palette_remap.py → GLB → game/assets/models/
  → toon_base.gdshader → Mixamo rig → GDAI MCP places in zone scene
```

**Use for:** Characters, torii, lacquer box, palace trim (poly budgets per `ART_DIRECTION.md`).

### Shader policy

External cel-shading preset packs are **reference only** — GodotPrompter authors the project’s single `toon_base.gdshader` ramp family. No full PBR `StandardMaterial3D` in player-facing scenes.

### ACE-Step 1.5 — audio prototype (replaces Suno/Udio)

**Role:** Zone loops, opening movie, boss fight, boss intro cinematics, ending hero scores.  
**License:** MIT — commercial indie use; register in `docs/art/LICENSES.md`.  
**Also required:** `python3 tools/generate_game_audio.py` for instant procedural fallback.

**Install:**

```bash
bash tools/install_ace_step.sh          # clone to .cache/ace-step-1.5
cd .cache/ace-step-1.5 && uv run acestep   # Gradio UI
# or: uv run acestep-api  →  export ACESTEP_API_URL=http://127.0.0.1:8001
```

**Generate:**

```bash
bash tools/generate_ai_bgm.sh --list
bash tools/generate_ai_bgm.sh --category opening          # menu, prologue, opening hero
bash tools/generate_ai_bgm.sh --category boss_cinematic   # SC-09/14/15 intro movies
bash tools/generate_ai_bgm.sh --category ending           # SC-17a/b/c hero endings
bash tools/generate_ai_bgm.sh --category zone --fallback  # procedural if no GPU
bash tools/generate_ai_bgm.sh --all-prompts               # docs/audio/audio_sheets/*.md
```

Prompt catalog: `game/data/audio/ace_step_prompts.json` · QA targets: `game/data/audio/audio_qa_catalog.json` · Briefs: `docs/generation_briefs/audio/`

**Ship rule:** Curated ACE-Step exports per prompt sheet — loudness normalize (-16 LUFS); no human mix pass (`docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/art/ART_AUTOMATION_PIPELINE.md` §7).

### ElevenLabs — selective VO (12 clips, not full dialogue)

**Role:** Short emotional punches at peaks (SC-03, SC-13, SC-16, etc.) — see `docs/vision/VO_HIT_LIST.md`.  
**Not for:** Full script, tutorials, inspectables, SC-08 crowd (SFX bed), SC-17 endings (music only).

```bash
bash tools/generate_ai_vo.sh --list
bash tools/generate_ai_vo.sh --tier p0 --locale ja
export ELEVENLABS_API_KEY=...   # Cursor Secrets
```

Catalog: `game/data/audio/vo_prompts.json` · QA: `game/data/audio/audio_qa_catalog.json` · Briefs: `docs/generation_briefs/vo/` · Dialogue: `voice_id` on 12 lines in `chapter_01.json`

**Agent rules:** Do not add `voice_id` to new lines without updating `vo_prompts.json` + `VO_HIT_LIST.md`. P0 before P1/P2. Verify ElevenLabs commercial terms before ship.

---

## Explicitly rejected (do not adopt)

| Tool | Reason |
|------|--------|
| **Summer Engine** | Replaces Godot 4.7 editor; invalidates GDAI stack |
| **Fennara (FAR)** | Fourth scene editor; overlaps GDAI/Godotiq/MCP Pro |
| **Ink narrative rewrite** | JSON spine already defined |
| **Kenney town kits** | European visual read; banned for player-facing builds |
| **Kenney knight / Castle kit** | Deprecated for ship (`ART_DIRECTION.md`) |
| **Notion MCP** | `docs/` + `game/data/` are authoritative — duplicate index adds OAuth friction, no ship value |

---

## Licenses & cost

| Tool | License | Cost | In git? |
|------|---------|------|---------|
| GDAI MCP | Commercial | ~$19 | ❌ gitignored |
| Godotiq Community | MIT (pip) | Free | ❌ addon gitignored |
| Godotiq Pro | Commercial | $19 one-time | Optional upgrade |
| Godot MCP Pro | Commercial | $15 one-time | ❌ gitignored |
| GameLab Studio | Commercial | Free tier + paid | API key in Secrets |
| Blender | OSS | Free | Offline |
| ACE-Step 1.5 | MIT | Free (local GPU) | `.cache/ace-step-1.5` gitignored |

**Ship builds:** disable/remove all Godot dev plugins before Steam export.

---

## User setup checklist (purchase & secrets)

Run: `bash tools/install_extended_toolchain.sh` then `bash tools/check_extended_toolchain.sh`

| Tool | You need to buy? | What you do |
|------|------------------|-------------|
| **GDAI MCP** | ✅ ~$19 one-time | Already installed — keep zip in cloud snapshot |
| **Godotiq** | ❌ Free (Pro $19 optional) | Already installed |
| **Godot MCP Pro** | ✅ $15 one-time | Already installed |
| **GameLab Studio** | Paid OK for quality; free tier for light UI | Sign up → API key → **Cursor Secrets: `GAMELAB_API_KEY`** → re-run install script |
| **ComfyUI / Material Maker** | ❌ Free | Local install; locked stylized workflows per `ART_AUTOMATION_PIPELINE.md` |
| **Meshy / Tripo / Rodin** | Paid OK for hero quality | Service ToS → register outputs in `LICENSES.md` |
| **Blender** | ❌ Free | Auto-installed in cloud via `install_extended_toolchain.sh` |
| **ACE-Step 1.5** | ❌ Free (local GPU) | `bash tools/install_ace_step.sh`; prompts in `game/data/audio/ace_step_prompts.json` |
| **ElevenLabs VO** | Paid API | `ELEVENLABS_API_KEY` in Cursor Secrets; `bash tools/generate_ai_vo.sh` |
| **generate_game_audio.py** | ❌ Free (repo tool) | Procedural fallback — auto on install |

**Cursor cloud dashboard:** Register P0 MCP servers from `.cursor/mcp.json`; add `gamelab-mcp` when `GAMELAB_API_KEY` is set. Restart agent after saving.

**Cannot be automated by agents:** GameLab API key (unless you add secret), ElevenLabs API key (unless you add secret), ACE-Step GPU generation (use prompt sheets + export), ComfyUI workflow runs (local GPU).

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

## Testing & QA workflow

See `docs/qa/AI_TESTING_SPEC.md` §11 and `docs/qa/ACCEPTANCE_CRITERIA.md` (measurable gates).

| Layer | Tools | MCP role |
|-------|-------|----------|
| L0–L2 | Shell scripts (no MCP) | — |
| L3 | GDAI F5 + screenshot; Godotiq `godotiq_ui_map` for menus | `godot-mcp` |
| L4 | Godot MCP Pro `run_test_scenario`; Godotiq `godotiq_verify_project_runs` | `godot-mcp-pro`, `godotiq` |
| L5 | Godot MCP Pro input replay + `assert_screen_text`; Godotiq `godotiq_trace_flow` on failure | `godot-mcp-pro`, `godotiq` |
| L6 | Human — **after** L5 | — |

### QA stack (every commit + per art/flow task)

**Catalog:** `game/data/qa/acceptance_criteria.json` · **Policy:** `docs/qa/ACCEPTANCE_CRITERIA.md`

```bash
python3 tools/validate_story_data.py          # L0_story_data
python3 tools/validate_acceptance_criteria.py
bash tools/run_playtest_smoke.sh              # L2 bundle
bash tools/run_candidate_tournament.sh      # L2_candidate_select — pre-merge when policy requires
bash tools/run_model_smoke_checks.sh          # when urashima.glb exists
bash tools/run_visual_smoke_checks.sh         # when zone screenshot exists
bash tools/run_audio_smoke_checks.sh          # when bgm_village.ogg and/or P0 VO gate clip exist
bash tools/run_integration_tests.sh           # L4 / INT-*
bash tools/run_e2e_playthrough.sh             # L5 — not SKIP
```

| Domain | Doc | FAIL → |
|--------|-----|--------|
| Thresholds | `ACCEPTANCE_CRITERIA.md` | Cite gate id + measured value |
| 3D | `MODEL_QA.md` | `qa_emit_remediation.sh model-*` |
| Visual | `VISUAL_QA.md` | `qa_emit_remediation.sh visual-*` |
| Tournament | `CANDIDATE_TOURNAMENT.md` | `L2_candidate_select` comparison artifact; one winner per scope |
| Audio (BGM) | `AUDIO_QA.md` | `qa_emit_remediation.sh audio-tech\|audio-jury` |
| Audio (P0 VO) | `AUDIO_QA.md` §A4–A5 | `qa_emit_remediation.sh vo-tech\|vo-jury` |
| Flow | `FLOW_QA.md` | `qa_emit_remediation.sh flow-scenario` |
| Iteration | `QA_REMEDIATION_LOOP.md` | `qa_remediation_brief.py` |

**Rules:** WARN ≠ PASS · SKIP ≠ PASS · jury needs ≥2 models @ confidence ≥ 0.65 · vision keys in Cursor Secrets.

### Example prompts

**Zone albedo (ComfyUI/Material Maker → GDAI):**

```
Generate seamless tileable weathered wood albedo, muted #5C4A3A, Japanese coastal decay, 1024×1024
via Material Maker or ComfyUI locked workflow.
Run: python3 tools/palette_remap.py --zone ruined_village --input game/assets/textures/zones/ruined_village/wood_planks.png
Then using godot-mcp only: assign to pier meshes in ruined_village.tscn. F5 verify.
```

**UI frame (GameLab → GDAI):**

```
Using gamelab-mcp: generate ink-wash menu border, muted palette, 512×128.
palette_remap.py → game/assets/textures/ui/menu_border.png → assign in tab_menu.tscn.
```

**Combat balance (docs → code):**

```
Read docs/gameplay/COMBAT_SYSTEMS.md + game/data/skills.json for turn-order and damage formulas.
Update game/data/skills.json and CombatManager.gd to match.
Run bash tools/run_unit_tests.sh.
```

**Debug hung turn (Godotiq):**

```
Use godotiq_signal_map and godotiq_trace_flow on CombatManager.
Read debug console. GDAI only if a .tscn fix is needed.
```

**Automated combat menu (MCP Pro):**

```
Using godot-mcp-pro: run_test_scenario for SC-05 tutorial.
Assert battle menu text visible.
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Any required MCP missing from catalog | Register in Cursor dashboard; restart agent |
| Too many MCP tools in Cursor | MCP Pro: use `--minimal` in mcp.json args |
| GDAI + MCP Pro both edit scene | **Rule:** GDAI builds; MCP Pro tests only |
| Godotiq bridge offline | Enable GodotIQ plugin; wait 5s |
| GameLab SSE fails | Check API key in Secrets; verify SSE URL |
| `node` not found | Install Node 18+ for Godot MCP Pro |

---

## Related

- `docs/cheat-sheets/RR_CHEATSHEET.md` — printable one-page R&R summary
- `docs/art/ART_AUTOMATION_PIPELINE.md` — quality-first art/audio automation policy
- `docs/qa/ACCEPTANCE_CRITERIA.md` — measurable QA gates (WARN/SKIP ≠ PASS)
- `docs/qa/QA_REMEDIATION_LOOP.md` — FAIL iteration policy
- `docs/art/MODEL_QA.md` · `docs/art/VISUAL_QA.md` · `docs/audio/AUDIO_QA.md` · `docs/qa/FLOW_QA.md`
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `game/.godotiq.json` — Godotiq project conventions
- `game/addons/README.md` — addon policy
- `.cursor/mcp.json.example` — MCP config template
- `docs/agents/PLUGIN_INSTALL_GUIDE.md` — install steps
- `docs/agents/GDAI_CLOUD_SETUP.md` — cloud snapshot & GDAI bootstrap
