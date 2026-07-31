---
id: palette-audio-gates
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 665
summary: "Art Automation Pipeline — Palette remap, audio, M5 gates — All 2D generated art (ComfyUI, GameLab, Material Maker exports) must pass palette remap before ship."
---
# Art Automation Pipeline — Palette remap, audio, M5 gates

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## When to read

Use **Art Automation Pipeline — Palette remap, audio, M5 gates** (roles: visual, builder) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [6. Palette compliance (`palette_remap.py`)](#6-palette-compliance-palette_remappy)
- [7. Audio automation (no human mix)](#7-audio-automation-no-human-mix)
- [8. Quality gates (M5)](#8-quality-gates-m5)


## 6. Palette compliance (`palette_remap.py`)

All **2D generated** art (ComfyUI, GameLab, Material Maker exports) must pass palette remap before ship.

```bash
python3 tools/palette_remap.py --zone ruined_village --input game/assets/textures/zones/ruined_village/wood_planks.png
python3 tools/palette_remap.py --help
```

Maps dominant hues toward zone rows in `docs/design/art/ART_DIRECTION.md` §1. Agents run this **after every external gen**, before `register_asset.py`.

---


## 7. Audio automation (no human mix)

| Stage | Tool | Ship rule |
|-------|------|-----------|
| Dev placeholder | `generate_game_audio.py` | Replace before M5 |
| Zone + hero BGM | ACE-Step 1.5 via `generate_ai_bgm.sh` | **Curated prompt sheet** — normalize to -16 LUFS; register MIT |
| Selective VO | ElevenLabs via `generate_ai_vo.sh` | 12 lines only — `docs/design/vision/VO_HIT_LIST.md` |
| SFX layers | Freesound **CC0-only** + procedural | Register each file |

**No human mix pass or commission** on the ship path. Quality gate = `docs/design/audio/AUDIO_QA.md` (BGM technical + hero jury A6/A7; P0 VO technical + jury V6/V7) + L6 listen.

**On any art/audio/model QA FAIL:** `docs/ops/qa/QA_REMEDIATION_LOOP.md` — brief + one lever change before rebuild (max 3 attempts).

---


## 8. Quality gates (M5)

Before marking M5 complete (`docs/ops/workflow/MILESTONES.md`). **All gates must meet `docs/ops/qa/ACCEPTANCE_CRITERIA.md`** — WARN/SKIP is not ship PASS.

- [ ] `bash tools/check_scene_visuals.sh` passes (no primitives in ship `.tscn`)
- [ ] `L2_model_*` + `L2_visual_*` + `L2_audio_*` + `L2_vo_*` gates PASS with evidence (`artifacts/`)
- [ ] All zone albedos pass `palette_remap.py` + `check_screenshot_palette.py` per zone
- [ ] Single toon ramp family (`RENDERING_GUIDE.md`)
- [ ] Every external asset in `LICENSES.md` + `asset_manifest.license.json`
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] `python3 tools/validate_acceptance_criteria.py` passes
- [ ] 60 FPS @ 1080p on GTX 1060 — SC-02 first
- [ ] No FMV in `game/` — cinematics are Godot-only (`docs/design/ui/CINEMATICS.md`)

---
