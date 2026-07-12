## Docs / data checklist (required)

- [ ] Changes are **`docs/`**, **`game/data/`**, or **`tools/`** validators only — no Godot implementation
- [ ] Linked issue or IMPLEMENTATION_PLAN task reference included
- [ ] If `game/data/` changed: `python3 tools/validate_story_data.py` PASS
- [ ] If `game/data/code/base_classes.json` changed: `python3 tools/validate_base_classes.py` PASS
- [ ] `bash tools/run_docs_ci_checks.sh` PASS

### PM Agent
- [ ] Spec authority preserved — design truth stays in `docs/` + `game/data/`
- [ ] No gameplay implementation smuggled onto `main`

---

## Summary

<!-- What doc/data changed and why -->

## Test plan

- [ ] `bash tools/run_docs_ci_checks.sh`
