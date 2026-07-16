## Role handoff checklist (required)

Link the GitHub issue. Check every box that applies to this PR.

### PM Agent
- [ ] Linked issue has **phase**, **acceptance gate IDs**, and **`agent/*`** label
- [ ] Scope matches current phase in `game/data/qa/sprint_phases.json` (no phase skip)

### Architect (GodotPrompter)
- [ ] Handoff in issue/PR: design doc row, node tree outline, target **gate IDs**
- [ ] This PR touches **`.gd` / `.gdshader` / tests`** only (no ship `.tscn` edits in Cursor)
- [ ] New gameplay scripts **extend** base classes in `game/data/code/base_classes.json` — no rogue native `extends`
- [ ] Changed `.gd` files pass `bash tools/check_gdscript_changed.sh` (`gdtoolkit` via `install_ci_deps.sh`)

### Builder (GDAI MCP)
- [ ] Scenes built via **GDAI MCP** — not hand-edited ship `.tscn`
- [ ] Uses **component scenes** from `LEVEL_DESIGN.md` §1b where applicable
- [ ] **`game/scenes/.gdai_built`** updated (`verified_f5=true`, `verified_at`, `main_scene` if set)
- [ ] F5 playtest clean in Godot editor
- [ ] **`L3_perf_review`** when scenes/shaders/materials/meshes/lights/fog changed — Godotiq `perf_snapshot` → `artifacts/perf_reviews/<zone>_<sha>.json`
- [ ] Rigged GLB: `required_animations` ⊆ clips ⊆ `allowed_animations`; post-import via `install_glb_import_pipeline.sh`

### Performance review (Builder or QA — not a code review)
- [ ] **`baseline_id: reference_linux_cloud`** on snapshot (primary dev) or **`reference_pc_gtx1060`** for Windows depot
- [ ] Walk affected zone 30s at gameplay camera; FPS **≥ 55** in editor (60 target @ 1080p Medium)
- [ ] **≤ 8** materials visible per view (`perf_thresholds.json`)
- [ ] Draw calls **< 1000** or remediation brief filed
- [ ] Post-fix: re-run original repro + adjacent scenes + affected **`INT-*`** when flows changed

### QA Agent
- [ ] Gate report below with **commit SHA**, **gate IDs**, **PASS/FAIL**, **evidence paths**
- [ ] `bash tools/run_ci_checks.sh` PASS locally (or CI green on this PR)

### Flow Agent (if L4/L5 touched)
- [ ] `bash tools/run_integration_tests.sh` PASS when narrative/combat flows changed
- [ ] L5 only when phase/milestone requires it (not SKIP for ship)

---

## Gate report (QA — paste results)

```
Commit:
Gates:
  - L0_rr_compliance:
  - L0_story_data:
  - L0_base_classes:
  - L0_base_class_compliance:
  - L1_unit_tests:
  - L1_gdscript_lint:
  - L2_scene_primitives:
  - L2_animation_whitelist:
  - L2_feel_smoke:
  - L2_perf_catalog:
  - L2_glb_import:
  - L3_gdai_built:
  - L3_perf_review:
  - L4_integration:
Evidence paths:
```

---

## Summary

<!-- What changed and why -->

## Test plan

- [ ] `bash tools/run_ci_checks.sh`
- [ ] `bash tools/check_rr_compliance.sh`
- [ ] `bash tools/check_l3_gdai_built.sh` (if scenes or main_scene changed)
- [ ] `bash tools/run_perf_review_checks.sh` (L2 catalog; L3 snapshot if scene/visual)
- [ ] `python3 tools/validate_base_classes.py` (if `base_classes.json` changed)
- [ ] `bash tools/install_glb_import_pipeline.sh` (if new GLBs added)
- [ ] `python3 tools/check_glb_import_scripts.py --strict` (if models changed)
