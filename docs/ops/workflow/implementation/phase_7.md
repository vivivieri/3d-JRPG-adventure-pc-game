---
id: implementation-phase-7
type: how-to
audience: [pm, architect, builder]
phase: [7]
status: active
authority: workflow
tokens_est: 546
---
# Implementation Plan — Phase 7

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## Phase 7 — M5 art rebuild

Replace greybox with automated authored assets per `docs/design/art/ART_DIRECTION.md` + `docs/design/art/ART_AUTOMATION_PIPELINE.md`:

| # | Task | Docs |
|---|------|------|
| 7.1 | Hero character models — Urashima, Yuzu, Roku + 5 enemies (Meshy/Tripo/Rodin + Mixamo) | CHARACTER_BIBLE.md |
| 7.1b | GLB post-import NPR sanitizer (`install_glb_import_pipeline.sh`) | MODEL_QA.md §M2b |
| 7.1c | Animation whitelist in `qa_catalog.json` — `check_animation_whitelist.py` | MODEL_QA.md §M2c, CHARACTER_BIBLE §8 |
| 7.2 | Hero set-pieces — torii, `palace_gate_main` (SC-12) | ENVIRONMENT_KITS.md |
| 7.3 | Automated stylized zone textures (ComfyUI/Material Maker + `palette_remap.py`) | ART_AUTOMATION_PIPELINE.md |
| 7.4 | ComfyUI/GameLab portraits (replace procedural silhouettes) | ART_AUTOMATION_PIPELINE.md |
| 7.5 | Curated BGM per act — ACE-Step (`bash tools/generate_ai_bgm.sh`); targets in `audio_qa_catalog.json` | AUDIO_PRODUCTION_GUIDE.md, **GR-004**, **GR-006** |
| 7.6 | SFX + ambient beds per `scene_audio_map.json` | AUDIO_PRODUCTION_GUIDE.md, **GR-006** |
| 7.7 | **ElevenLabs voice casting** — replace `PLACEHOLDER_*` in `vo_prompts.json` (incl. `dialect_voices` for zh-Hant) | VO_HIT_LIST.md, **GR-005** |
| 7.8 | **Generate selective VO** — P0 listen pass → P1/P2; `en`/`ja`/`zh` + `zh-Hant` `cant`/`cmn` (`bash tools/generate_ai_vo.sh`) | VO_HIT_LIST.md, LOCALIZATION.md, **GR-005** |
| 7.9 | Audio QA — `bash tools/run_audio_smoke_checks.sh` + `AUDIO_QA.md` (BGM A6/A7 + P0 VO V6/V7) | AUDIO_QA.md, **GR-004**, **GR-005** |
| 7.10 | Cinematic hero assets — SC-00 opening, SC-12 gate reveal, SC-17 endings | CINEMATICS.md §12 |
| 7.11 | `bash tools/check_asset_compliance.sh` passes on release branch | ASSET_COMPLIANCE.md |
| 7.12 | **M5 visual evidence:** all zone golden screenshots per `zone_composition.json` + `ZONE_COMPOSITION_STRICT=1 bash tools/run_zone_composition_checks.sh` | GENERATION_READINESS §8, **GR-001**, **GR-003** |

**VO clip budget:** 12 clips × 3 locales (`en`, `ja`, `zh`) + 12 × 2 zh-Hant dialects (`cant`, `cmn`) = **60 OGG files**. Runtime `VoiceLinePlayer` ships in Phase 3; clip files land here in M5.

---

