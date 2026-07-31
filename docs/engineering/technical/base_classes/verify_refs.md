---
id: verify-refs
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 315
summary: "Code Base Class Rules — Verification + cross-refs — python3 tools/validate_base_classes.py"
---
# Code Base Class Rules — Verification + cross-refs

**Hub:** [`CODE_BASE_CLASS_RULES.md`](../CODE_BASE_CLASS_RULES.md)

## When to read

Use **Code Base Class Rules — Verification + cross-refs** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Verification](#5-verification)
- [6. Cross-refs](#6-cross-refs)


## 5. Verification

```bash
python3 tools/validate_base_classes.py
bash tools/check_base_class_compliance.sh   # native extends audit
bash tools/check_rr_compliance.sh
bash tools/check_animation_whitelist.py --phase m5 --strict   # when GLB present on game branch
bash tools/install_glb_import_pipeline.sh   # once per dev env (game/development)
python3 tools/check_glb_import_scripts.py --strict
```

On `game/development` CI: `L0_base_classes`, `L0_base_class_compliance`, `L2_animation_whitelist`, `L2_glb_import`, `L2_feel_smoke`, `L1_gdscript_lint`. SKIP (exit 2) is FAIL on game branch per `tools/gate_lib.sh`.

---


## 6. Cross-refs

- `docs/design/art/CHARACTER_BIBLE.md` — rig + animation names
- `docs/design/art/MODEL_QA.md` — GLB import + post-import
- `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — gate enforcement
