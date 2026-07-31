---
id: phase-7-8
type: reference
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 538
summary: "L0–L5 on release candidate → **then** L6 human QA → export."
---
# AI Dev — Phases 7–8

**Hub:** [`phase_acceptance.md`](../../phase_acceptance.md)

### Phase 7 — M5 art rebuild

| # | Criterion | Verification |
|---|-----------|--------------|
| 7.1 | No primitive/Kenney placeholder art in shipping scenes | `check_asset_compliance.sh` + human review |
| 7.2 | Hero meshes: Urashima, Yuzu, Roku per `CHARACTER_BIBLE.md` | Screenshot gate |
| 7.3 | Automated stylized zone textures per zone (`palette_remap.py`) | Art checklist |
| 7.4 | Curated BGM per `audio_qa_catalog.json` + `AUDIO_PRODUCTION_GUIDE.md` | `L2_audio_technical` + `L2_audio_jury` |
| 7.5 | SFX + ambient beds per `scene_audio_map.json` | `validate_scene_audio_map.py` + in-game verify |
| 7.6 | Selective VO: 12 clips × locales + zh-Hant dialects; `generate_ai_vo.sh --list` = 60 files | File manifest + `run_audio_smoke_checks.sh` |
| 7.7 | P0 VO: `L2_vo_technical` all locales + `L2_vo_jury` on `en` gate | `check_audio_vo.py` + `review_vo_vision.py` |
| 7.8 | Cinematic hero assets (SC-00, SC-12, SC-17) per `CINEMATICS.md` §12 | GDAI F5 |
| 7.9 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |
| 7.12 | All zone golden screenshots + `ZONE_COMPOSITION_STRICT=1` composition smoke (**GR-001**, **GR-003**) | `run_visual_smoke_checks.sh` + `run_zone_composition_checks.sh` |



### Phase 8 — Ship prep

**Order:** L0–L5 on release candidate → **then** L6 human QA → export.

| # | Criterion | Verification |
|---|-----------|--------------|
| 8.1 | GDAI MCP plugin **disabled and removed** from export tree | Manual + export preset review |
| 8.2 | Windows export succeeds (`tools/export_windows.sh`) | Artifact exists |
| 8.3 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |
| 8.4 | Steam achievements unlock per `ACHIEVEMENTS.md` | Integration test |
| 8.5 | **L0–L5 pass** on release candidate | All AI test scripts exit 0 |
| 8.6 | **Human QA** `docs/ops/qa/PLAYTEST_SCRIPT.md` ≥80% complete without guide | Human sign-off **after 8.5** |

---
