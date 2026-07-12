## Role handoff checklist (required)

Link the GitHub issue. Check every box that applies to this PR.

### PM Agent
- [ ] Linked issue has **phase**, **acceptance gate IDs**, and **`agent/*`** label
- [ ] Scope matches current phase in `game/data/qa/sprint_phases.json` (no phase skip)

### Architect (GodotPrompter)
- [ ] Handoff in issue/PR: design doc row, node tree outline, target **gate IDs**
- [ ] This PR touches **`.gd` / `.gdshader` / tests`** only (no ship `.tscn` edits in Cursor)

### Builder (GDAI MCP)
- [ ] Scenes built via **GDAI MCP** — not hand-edited ship `.tscn`
- [ ] **`game/scenes/.gdai_built`** updated (`verified_f5=true`, `verified_at`, `main_scene` if set)
- [ ] F5 playtest clean in Godot editor

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
  - L1_unit_tests:
  - L2_scene_primitives:
  - L3_gdai_built:
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
