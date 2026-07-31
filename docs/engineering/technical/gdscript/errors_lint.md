---
id: errors-lint
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [builder, architect]
status: active
authority: engineering
tokens_est: 436
summary: "Keep handling minimal — linear single-player game, not a live service."
---
# GDScript Style — Errors, comments, lint/tests

**Hub:** [`GDSCRIPT_STYLE.md`](../GDSCRIPT_STYLE.md)

## When to read

Use **GDScript Style — Errors, comments, lint/tests** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [12. Error handling](#12-error-handling)
- [13. Comments & documentation](#13-comments-documentation)
- [14. Lint & tests (CI)](#14-lint-tests-ci)
- [gdlint (gdtoolkit)](#gdlint-gdtoolkit)


## 12. Error handling

| Situation | Pattern |
|-----------|---------|
| Missing JSON at boot | `push_error()` + return; fail loud in dev |
| Missing asset (ship) | Assert + `check_asset_compliance.sh` |
| Unknown flag | Return default `false` |
| After `await` | `is_instance_valid(self)` / `is_instance_valid(node)` |

Keep handling minimal — linear single-player game, not a live service.

---


## 13. Comments & documentation

```gdscript

## 14. Lint & tests (CI)

```bash
bash tools/check_gdscript_changed.sh   # gdlint on changed .gd — L1_gdscript_lint
bash tools/run_unit_tests.sh           # L1_unit_tests
bash tools/check_base_class_compliance.sh
```

### gdlint (gdtoolkit)

Install: `bash tools/install_ci_deps.sh` or `pip install gdtoolkit`

Common gdlint rules aligned with [Godot style guide](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_styleguide.html):

| Rule area | Expectation |
|-----------|-------------|
| Line length | 100 chars (gdlint default configurable) |
| Trailing whitespace | None |
| Mixed tabs/spaces | Spaces only (4 per indent) |
| Unused arguments | Prefix with `_` — `_delta` |
| Class name vs file | `class_name` matches file purpose |

---
