## Docs / data checklist (required)

- [ ] Changes are **`docs/`**, **`game/data/`**, **`game/locale/`**, or **`tools/`** (validators + `*_lib.py` reference only) — **no Godot ship implementation**
- [ ] **Spec refinement mode** — no `.gd`, `.tscn`, `project.godot`, `game/shaders/`, or `game/assets/` on `main` (`docs/technical/SPEC_FIRST_DEVELOPMENT.md` §10)
- [ ] Linked issue or IMPLEMENTATION_PLAN task reference included
- [ ] If `game/data/` changed: `python3 tools/validate_story_data.py` PASS
- [ ] If `game/data/code/base_classes.json` changed: `python3 tools/validate_base_classes.py` PASS
- [ ] `bash tools/run_docs_ci_checks.sh` PASS

### PM Agent
- [ ] Spec authority preserved — design truth stays in `docs/` + `game/data/`
- [ ] No gameplay implementation smuggled onto `main`
- [ ] Cross-cutting factory feature registered in `workflow_integration_registry.json` (`docs/qa/WORKFLOW_INTEGRATION.md`)
- [ ] `bash tools/check_feature_integration.sh --remind` PASS before merge

---

## Summary

<!-- What doc/data changed and why -->

## Test plan

- [ ] `bash tools/run_docs_ci_checks.sh`
- [ ] `bash tools/check_feature_integration.sh --remind` (if PM hooks, telemetry, secrets, or watchdog touched)
