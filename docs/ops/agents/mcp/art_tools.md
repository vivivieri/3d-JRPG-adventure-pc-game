---
id: art-tools
type: reference
audience: [visual, builder, pm]
phase: [0, 1]
status: active
authority: ops
tokens_est: 1360
summary: "Which art tool to use (ComfyUI, GameLab, Meshy/Blender, ACE-Step, ElevenLabs) — open before generating zone/UI/3D/audio assets"
---
# MCP — Art Tools

**Hub:** [`MCP_STACK.md`](../MCP_STACK.md)

## When to read

Choosing or wiring an **art generation** path. Skip for pure scene placement (GDAI) once assets exist.

## Jump to

- [ComfyUI / Material Maker](#comfyui--material-maker--zone-npr-albedos)
- [GameLab Studio MCP](#gamelab-studio-mcp--ui--2d-sheets-required)
- [AI 3D + Blender](#ai-3d--blender--offline-hero-pipeline-required-for-turntable-qa)
- [Shader policy](#shader-policy)
- [ACE-Step BGM](#ace-step-15--audio-prototype-replaces-sunoudio)
- [ElevenLabs VO](#elevenlabs--selective-vo-12-clips-not-full-dialogue)

### ComfyUI / Material Maker — zone NPR albedos

**Role:** Stylized tileable wood, stone, ground, hero texture sheets.
**Does NOT:** Edit `.tscn` — hand off to GDAI after export.

**Workflow:**

```
1. READ  docs/design/art/ART_DIRECTION.md palette for target zone
2. ComfyUI (locked workflow) OR Material Maker — tileable albedo (muted coastal decay)
3. python3 tools/palette_remap.py --zone <zone> --input <png>
4. Save PNG → game/assets/textures/zones/<zone>/
5. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>  # see docs/design/art/LICENSES.md
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
1. READ  docs/design/art/ART_DIRECTION.md §4 UI style
2. GameLab MCP — generate UI frame / icon sheet (muted, not candy-bright)
3. palette_remap.py → game/assets/textures/ui/
4. register_asset.py → GDAI assigns in UI .tscn
```

Setup: [gamelabstudio.co](https://gamelabstudio.co/) API key → register `gamelab-mcp` SSE server. **Required** — procedural UI placeholders OK for asset output until GameLab gen ships.

**Design context:** Read `docs/` + `game/data/` before balancing combat or editing JSON. No external design-index MCP.

**Why not Ink (Inkle):** Story spine is JSON-driven (`scenes.json` → `dialogue/` → `flags.json`). Ink adds a second runtime with no v1 benefit. See `docs/design/vision/NARRATIVE_WRITING_GUIDE.md`.


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
**License:** MIT — commercial indie use; register in `docs/design/art/LICENSES.md`.
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
bash tools/generate_ai_bgm.sh --all-prompts               # docs/design/audio/audio_sheets/*.md
```

Prompt catalog: `game/data/audio/ace_step_prompts.json` · QA targets: `game/data/audio/audio_qa_catalog.json` · Briefs: `docs/briefs/audio/`

**Ship rule:** Curated ACE-Step exports per prompt sheet — loudness normalize (-16 LUFS); no human mix pass (`docs/design/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/design/art/ART_AUTOMATION_PIPELINE.md` §7).


### ElevenLabs — selective VO (12 clips, not full dialogue)

**Role:** Short emotional punches at peaks (SC-03, SC-13, SC-16, etc.) — see `docs/design/vision/VO_HIT_LIST.md`.
**Not for:** Full script, tutorials, inspectables, SC-08 crowd (SFX bed), SC-17 endings (music only).

```bash
bash tools/generate_ai_vo.sh --list
bash tools/generate_ai_vo.sh --tier p0 --locale ja
export ELEVENLABS_API_KEY=...   # Cursor Secrets
```

Catalog: `game/data/audio/vo_prompts.json` · QA: `game/data/audio/audio_qa_catalog.json` · Briefs: `docs/briefs/vo/` · Dialogue: `voice_id` on 12 lines in `chapter_01.json`

**Agent rules:** Do not add `voice_id` to new lines without updating `vo_prompts.json` + `VO_HIT_LIST.md`. P0 before P1/P2. Verify ElevenLabs commercial terms before ship.

---
