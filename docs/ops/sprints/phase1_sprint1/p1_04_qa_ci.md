---
id: p1-04-qa-ci
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 521
summary: "P1-04 QA CI + gate report"
---
# Phase1-Sprint1 — P1-04 QA CI + gate report

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## P1-04 — QA: CI green + Phase 1 gate report

**Title:** `[DEV][P1-04] Phase 1 — CI green + L0–L2 gate report on ruined_village PR`

**Labels:** `agent/qa`, `env/qa`, `gate/L1_unit_tests`, `gate/L2_scene_primitives`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | Sprint QA (all Phase 1 PRs) |
| Lead agent | **qa** |
| Depends on | P1-02 merged |

### Acceptance gate IDs

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L0_acceptance_catalog
L0_base_classes
L0_base_class_compliance
L1_unit_tests
L1_gdscript_lint
L2_scene_primitives
L3_gdai_built
L2_feel_smoke
L2_glb_import
```

**Not in Sprint1 scope:** `L4_integration` (Phase 3+ per `sprint_phases.json`; `INT-BOOT-01` runs when `main_scene` is set).

### Commands

```bash
bash tools/run_ci_checks.sh
bash tools/run_playtest_smoke.sh
```

### Gate report template (paste in PR + issue)

```markdown

## Gate report — Phase1-Sprint1

- Commit: `<sha>`
- Branch: `game/development`

| Gate ID | Result | Evidence |
|---------|--------|----------|
| L0_rr_compliance | PASS | check_rr_compliance.sh exit 0 |
| L0_story_data | PASS | validate_story_data.py |
| L0_base_classes | PASS | validate_base_classes.py |
| L0_base_class_compliance | PASS | check_base_class_compliance.sh |
| L1_unit_tests | PASS | run_unit_tests.sh |
| L1_gdscript_lint | PASS/SKIP | check_gdscript_changed.sh |
| L2_scene_primitives | PASS | check_scene_visuals.sh |
| L3_gdai_built | PASS | .gdai_built verified_f5=true |
| L2_feel_smoke | PASS | run_feel_smoke_checks.sh |
| L2_glb_import | PASS/SKIP | strict when GLBs present |

**Not run (expected):** L4_integration (Phase 3+), L2_visual_jury, L5 E2E, L6 human

**Policy:** WARN ≠ PASS · SKIP ≠ PASS on game branch
```

### On FAIL

```bash
bash tools/qa_emit_remediation.sh visual-palette   # or flow-scenario / model-tech as appropriate
```

Post remediation JSON + gate ID; reassign to Architect or Builder.

### Definition of done

- [ ] `run_ci_checks.sh` PASS on merge commit
- [ ] Gate report in PR description
- [ ] Issue updated with evidence paths

---
