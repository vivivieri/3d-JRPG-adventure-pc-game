---
id: errors-tests-checklist
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 519
summary: "Errors, comments, tests, assets, PR checklist"
---
# Code Style — Errors, comments, tests, assets, PR checklist

**Hub:** [`CODE_STYLE.md`](../CODE_STYLE.md)

## When to read

Use **Code Style — Errors, comments, tests, assets, PR checklist** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [9. Error handling](#9-error-handling)
- [10. Comments](#10-comments)
- [11. Tests](#11-tests)
- [12. Copyright & assets](#12-copyright-assets)
- [13. Quick checklist (PR / commit)](#13-quick-checklist-pr-commit)


## 9. Error handling

| Situation | Pattern |
|-----------|---------|
| Missing JSON | `push_error()` + return early; boot fails loud in dev |
| Missing asset | Fallback only for dev placeholders; ship = assert + compliance script |
| Invalid flag access | Return default `false`; log once in debug builds |

Keep error handling minimal — this is a linear game, not a live service.

---


## 10. Comments

- **Self-documenting names** over comments for obvious logic
- Comment **why** for: flag timing, boss phase transitions, audio duck exceptions (SC-16)
- Link to doc sections for complex design: `# SC-07 silent — PUZZLE_DESIGN.md`

---


## 11. Tests

| Location | Style |
|----------|-------|
| `game/tests/unit/` | Extend `test_runner.gd`; no engine restart per assert |
| Python validators | `tools/validate_story_data.py`, `validate_base_classes.py` for data integrity |
| GDScript lint | `tools/check_gdscript_changed.sh` on changed `.gd` (L1 gate) |
| MCP Pro | Scenario names match `AI_TESTING_SPEC.md` |

---


## 12. Copyright & assets

- No web imports without `register_asset.py` + `LICENSES.md`
- Procedural generators OK for dev; ship assets per `ASSET_COMPLIANCE.md`

---


## 13. Quick checklist (PR / commit)

- [ ] Typed GDScript matches surrounding file
- [ ] No string-based signal connections
- [ ] Story changes have `validate_story_data.py` pass
- [ ] New flags in `flags.json` + `scenes.json` setter
- [ ] New JSON IDs snake_case
- [ ] `.tscn` changes via GDAI MCP when available
