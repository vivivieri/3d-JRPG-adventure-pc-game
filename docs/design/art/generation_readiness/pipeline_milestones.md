---
id: pipeline-milestones
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 828
summary: "Pipeline checklist, milestones, next docs"
---
# Generation Readiness — Pipeline checklist, milestones, next docs

**Hub:** [`GENERATION_READINESS.md`](../GENERATION_READINESS.md)

## 6. Pipeline checklist (agent order)

For each new hero mesh or zone slice:

```
1. READ   CHARACTER_BIBLE / ENVIRONMENT_KITS row + ART_DIRECTION palette
2. WRITE  docs/briefs/<id>.md (§3 template)
3. GEN    Meshy/ComfyUI/Material Maker per ART_AUTOMATION_PIPELINE.md
4. POST   palette_remap.py → register_asset.py
5. IMPORT bash tools/install_glb_import_pipeline.sh (characters/props)
6. MEASURE  python3 tools/check_model_technical.py --model <id>
7. MEASURE  python3 tools/check_animation_whitelist.py --phase m5 --strict
8. PLACE  GDAI MCP in zone — gameplay screenshot
9. JURY   L2_model_jury + L2_visual_jury (when keys exist)
10. HUMAN L6 feel checklist — only after L5 green
```

---


## 7. What “ready for generation” means per milestone

| Milestone | Characters | Zones | Human expectation |
|-----------|------------|-------|-------------------|
| **Phase 1 slice** | `urashima` + village set-pieces briefs | `ruined_village` brief | Golden shots pending capture |
| **Phase 4** | Party + salt crab briefs ✅ | `beach_shore` brief ✅ | Combat read at 6 m |
| **M5 ship** | All `m5` catalog rows have briefs ✅ | All player zones briefed ✅ | L2 juries + L6 feel ≥3.5 |
| **M6 Steam** | Portrait parity with field model | No greybox in any player scene | L6 ≥80% complete |

---


## 8. Recommended next docs/data (priority)

| Priority | Deliverable | Owner | Status |
|----------|-------------|-------|--------|
| P0 | All `qa_catalog.json` + player-zone briefs | Architect + Visual | ✅ Done (17 briefs) |
| P0 | Golden screenshot path enforced (`VISUAL_SMOKE_STRICT=1` on M5) | QA | Pending capture |
| P1 | `game/data/qa/zone_composition.json` — machine-readable §5 table | Architect | ✅ Done |
| P1 | `animation_timing` block in `qa_catalog.json` (duration_ms, loop) | Architect | ✅ Done |
| P2 | Expand `palace_sentinel` CHARACTER_BIBLE row to boss standard | PM + Visual | ✅ Done (GR-002) |
| P2 | `L2_zone_composition` smoke script | QA | ✅ Script; strict at M5 via **GR-003** / Phase 7.12 |
| P1 | `audio_qa_catalog.json` + hero BGM + P0 VO briefs | Architect + Audio | ✅ Done (**GR-004**, **GR-005**) |
| P1 | `scene_audio_map.json` machine-readable | Architect | ✅ Done (**GR-006**) |

**Implementation traceability:** `game/data/qa/generation_readiness_backlog.json` — **GR-001** … **GR-006** map to `IMPLEMENTATION_PLAN.md` tasks and phase gates (validated L0 on `main`).

---


## 9. Cross-refs

| Need | Doc |
|------|-----|
| What to build | `IMPLEMENTATION_PLAN.md` |
| How assets are generated | `ART_AUTOMATION_PIPELINE.md` |
| Character look | `CHARACTER_BIBLE.md` |
| Generation briefs | `briefs/` |
| Zone modules | `ENVIRONMENT_KITS.md` |
| Measurable pass/fail | `ACCEPTANCE_CRITERIA.md` |
| Audio QA (BGM + P0 VO) | `AUDIO_QA.md`, `game/data/audio/audio_qa_catalog.json` |
| Model polish cadence + direction authority | `MODEL_QA.md` §8–§9 |
| Feel targets | `GAME_FEEL.md`, `game/data/qa/feel_thresholds.json` |
| Human playtest | `PLAYTEST_SCRIPT.md` §7b |
