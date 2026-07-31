---
id: phase-4-6
type: reference
phase: [0, 1, 8]
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 601
summary: "AI Dev — Phases 4–6 — covers Phase 4 — Combat vertical slice; Phase 5 — Chapter 1 dungeons; Phase 6 — Full story & endings"
---
# AI Dev — Phases 4–6

**Hub:** [`phase_acceptance.md`](../../phase_acceptance.md)

## When to read

Use **AI Dev — Phases 4–6** (roles: pm, qa, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Phase 4 — Combat vertical slice](#phase-4-combat-vertical-slice)
- [Phase 5 — Chapter 1 dungeons](#phase-5-chapter-1-dungeons)
- [Phase 6 — Full story & endings](#phase-6-full-story-endings)


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
