---
id: qa-gates
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 855
summary: "[`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)"
---
# R&R — qa-gate-layers

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## QA gate layers

| Layer | Who | Examples |
|-------|-----|----------|
| L0 | Shell / QA | `L0_story_data`, `L0_rr_compliance`, `L0_base_classes`, `L0_base_class_compliance` |
| L1 | QA + Architect | `L1_unit_tests`, `L1_gdscript_lint` |
| L2 | QA + Visual | `L2_scene_primitives`, `L2_animation_whitelist`, `L2_feel_smoke`, `L2_glb_import`, `L2_visual_palette`, jury |
| L3 | Builder + QA | **`L3_gdai_built`** (CI — marker in scene diff) · **`L3_gdai_f5`** (editor F5) · **`L3_perf_review`** (FPS / draw calls — agent-local) |
| L4 | Flow | `L4_integration` |
| L5 | Flow | `L5_e2e_three_endings` |
| L6 | Human | Playtest sign-off — **after** L0–L5 |

**Policy:** WARN ≠ PASS · SKIP ≠ PASS · F5 alone ≠ visual PASS.

### Evidence by test layer (L0–L6)

**Rule:** `acceptance_criteria.json` → `evidence_required_for_pass: true`. Cite paths in PR gate report and sprint bundle.

| Layer | Who defines cases | Who runs | Evidence required? | Screenshot | Video | Typical paths |
|-------|-------------------|----------|--------------------|------------|-------|---------------|
| **L0** | Design data / policy | Dev / CI | JSON + CI log | No | No | `game/data/`, `game/scenes/.gdai_built` |
| **L1** | **Architect** (`game/tests/unit/`) | Dev / CI | CI log (optional export) | No | No | `artifacts/test-reports/` (optional) |
| **L2** | QA policy + catalogs | QA / CI | Gate output; screenshot when assets exist | **Yes** (visual/audio/model smokes) | No | `artifacts/screenshots/`, `artifacts/visual_reviews/*.jury.json`, `artifacts/model_reviews/`, `artifacts/audio_reviews/` |
| **L3** | `AI_TESTING_SPEC.md` §5 + sprint issue | Builder + QA | **Yes** — F5 + screenshot for scene/visual work; **perf JSON** when scenes/shaders change | **Yes — required** | No | `artifacts/screenshots/<phase>_<scene>_<view>.png`, `artifacts/perf_reviews/<zone>_<sha>.json` |
| **L4** | **Architect** (`integration_scenarios.json`) | Flow / QA | Scenario pass/fail; screenshots for UI flows | Optional | No | `artifacts/flow_reviews/`, CI log |
| **L5** | **Architect** (`AI_TESTING_SPEC.md` §7 E2E matrix) | Flow / QA | E2E pass/fail on same commit | Optional | **Optional** | `artifacts/videos/e2e_<ending>_<date>.mp4` |
| **L6** | `PLAYTEST_SCRIPT.md` | Human | Bug report + repro steps | Recommended (S0–S1) | Recommended (S0–S1) | GitHub issue; `artifacts/qa_reports/L6_human_playtest.json` |

**Invalid PASS:** F5 with 0 errors but no screenshot · visual PASS without `artifacts/screenshots/` · issue `done` without evidence bundle.

**Who stores evidence:**

| Role | Responsibility |
|------|----------------|
| **Architect** | Writes unit/integration/E2E test cases; does not claim visual PASS |
| **Builder** | F5 + captures screenshots to `artifacts/screenshots/` on visual tasks |
| **QA** | Runs gates, vision jury, pastes gate report in PR, bundles per issue |
| **PM** | Verifies `pm_check_done_criteria` before closing sprint issue |

**Bundle per sprint issue:**

```bash
python3 tools/pm_bundle_evidence.py <issue_id> \
  --gate <gate_id> \
  --artifact artifacts/screenshots/phase1_ruined_village_gameplay.png
# → artifacts/sprint_evidence/<issue_id>/manifest.json
```

**Full spec:** `docs/ops/qa/AI_TESTING_SPEC.md` · `docs/design/art/VISUAL_QA.md` · `docs/ops/qa/QA_AND_BUG_PROCESS.md` §3

---

