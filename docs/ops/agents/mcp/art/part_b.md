---
id: part-b
type: reference
phase: [0, 1]
audience: [visual, builder, pm]
status: active
authority: ops
tokens_est: 694
summary: "External cel-shading preset packs are **reference only** — GodotPrompter authors the project’s single `toon_base.gdshader` ramp family. No full PBR `StandardMat"
---
# MCP — Art Tools — MCP — Art Tools (B)

**Hub:** [`art_tools.md`](../art_tools.md)

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
