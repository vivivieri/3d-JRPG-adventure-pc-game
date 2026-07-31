---
id: part-b
type: reference
phase: [0, 1, 8]
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 1021
summary: "AI Dev — Phase Acceptance (B)"
---
# AI Dev — Phase Acceptance — AI Dev — Phase Acceptance (B)

**Hub:** [`phase_acceptance.md`](../phase_acceptance.md)

### Phase 4 — Combat vertical slice

| # | Criterion | Verification |
|---|-----------|--------------|
| 4.1 | Combat UI: HP/MP, action menu, battle log, enemy intent | GDAI F5 |
| 4.2 | SC-05 Salt Crab tutorial completable | Integration `test_combat_round.gd` |
| 4.3 | Damage matches `COMBAT_SYSTEMS.md` worked examples | Unit `test_damage_calculator.gd` |
| 4.4 | Turn order by speed per `SKILLS_BIBLE.md` | Unit test |
| 4.5 | Boss framework shows phase banner | GDAI F5 |
| 4.6 | L0–L4 pass | All test scripts |


### Phase 5 — Chapter 1 dungeons

| # | Criterion | Verification |
|---|-----------|--------------|
| 5.1 | `tidal_caves.tscn` lighting/palette pass per `ENVIRONMENT_KITS.md` §5 (greybox meshes OK — final art is Phase 7) | GDAI screenshot |
| 5.2 | SC-07 water puzzle: silent, no VO; state machine matches `PUZZLE_DESIGN.md` | Unit + GDAI F5 |
| 5.3 | Shore Wraith SC-09 win/lose paths | Integration test |
| 5.4 | Yuzu joins at SC-10; party size = 2 | Flag unit test |
| 5.5 | SC-08 vignette plays; whisper SFX bed, no full VO | GDAI F5 |
| 5.6 | L0–L4 pass | All test scripts |


### Phase 6 — Full story & endings

| # | Criterion | Verification |
|---|-----------|--------------|
| 6.0 | Expand `palace_sentinel` `CHARACTER_BIBLE.md` to boss-standard row **before** SC-14 mesh work (**GR-002**) | Doc review; backlog `status: done` |
| 6.1 | Dragon Palace Gate zone per `ENVIRONMENT_KITS.md` §6 | GDAI + screenshot |
| 6.2 | Palace Sentinel + Tide Keeper per `BOSS_DESIGNS.md` | Integration test |
| 6.3 | SC-16 choice UI blocks attack input per `ENDING_DESIGN.md` | GDAI F5 |
| 6.4 | All 3 endings reachable: Rewind, Anchor, Drift | E2E `test_three_endings.gd` |
| 6.5 | Credits roll after each ending | E2E test |
| 6.6 | SC-12 gate cinematic + SC-11 flashback skippable after 3s | GDAI F5 |
| 6.7 | `bash tools/run_e2e_playthrough.sh` passes | Exit 0 |
| 6.8 | L0–L5 pass | All test scripts |


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
