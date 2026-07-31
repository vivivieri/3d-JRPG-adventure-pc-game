---
id: game-development
type: reference
audience: [release, qa, pm]
phase: [6, 8]
status: active
authority: ci-cd
tokens_est: 1229
summary: "game/development game-ci gate table (L0–L4) + Windows run job + CD — open when greening Game CI or explaining SKIP≠PASS on export"
---
# CI — What Runs (`game/development`)

**Hub:** [`what_runs.md`](../what_runs.md)

## When to read

Debugging **Game CI** on `game/development` (`game-ci.yml` / `run_ci_checks.sh`). For the short role-oriented list see [`gates_by_branch.md`](../../../../cheat-sheets/controls/gates_by_branch.md). Machine authority: `game/data/qa/acceptance_criteria.json`.

## Jump to

- [L0 / L1 gates](#l0--l1--run_ci_checkssh)
- [L2+ / L4 gates](#l2--l4--run_ci_checkssh)
- [Windows export run job](#windows-export-run-windows-latest)
- [CD artifacts](#cd-cd-artifactyml)

### L0 / L1 — `run_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — ship `.tscn` allowed when `.gdai_built` has `verified_f5=true` |
| `L0_game_branch_bootstrap` | `bash tools/check_game_branch_bootstrap.sh` | Exit 0 — `game/project.godot` present (**FAIL** if missing) |
| `L0_vo_casting` | `python3 tools/validate_vo_casting.py` | Exit 0 — WARN until M5; CD sets `VO_CASTING_REQUIRED=1` |
| `L0_story_data` | `python3 tools/validate_story_data.py` | Exit 0, 0 errors |
| `L0_acceptance_catalog` | `python3 tools/validate_acceptance_criteria.py` | Catalog schema valid |
| `L0_base_classes` | `python3 tools/validate_base_classes.py` | Registry schema + component script refs |
| `L1_unit_tests` | `bash tools/run_unit_tests.sh` | All unit tests pass headless |
| `L1_python_lint` | `bash tools/check_python_lint.sh` | Exit 0 — ruff on `tools/` |
| `L1_shellcheck` | `bash tools/check_shell_scripts.sh` | Exit 0 — shellcheck on `tools/*.sh` |
| `L1_json_style` | `python3 tools/check_json_style.py` | Exit 0 — JSON format + naming on `game/data/` |
| `L1_typescript_lint` | `bash tools/check_typescript_lint.sh` | Exit 0 — ESLint/tsc when MCP Pro installed |
| `L1_markdown_style` | `python3 tools/check_markdown_style.py` | Exit 0 — docs format, whitespace, headings, links |
| `L1_gdshader_style` | `python3 tools/check_gdshader_style.py` | Exit 0 — shader templates + game/shaders |
| `L1_scene_style` | `bash tools/check_scene_style.sh` | Exit 0 — static .tscn lint; SKIP when no `game/scenes` |
| `L1_error_handling` | `bash tools/check_error_handling.sh` | Exit 0 — exception/error message patterns |
| `L1_workflow_yaml` | `bash tools/check_workflow_yaml.sh` | Exit 0 — actionlint on workflow YAML |
| `L1_mypy_libs` | `bash tools/check_mypy_libs.sh` | Exit 0 — mypy on reference `*_lib.py` modules |
| `L1_gdscript_lint` | `bash tools/check_gdscript_changed.sh` | Exit 0 — exit **2** SKIP when no `.gd` diff (FAIL on game branch) |
| `L1_gdscript_lint_all` | `bash tools/check_gdscript_all.sh` | Exit 0 — full-tree gdlint; **2** SKIP when no `game/scripts` |
| `L0_base_class_compliance` | `bash tools/check_base_class_compliance.sh` | Exit 0 — no rogue native `extends` (`CharacterBody3D`/`Area3D`/`Node`) |

### L2+ / L4 — `run_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L2_scene_primitives` | `bash tools/check_scene_visuals.sh` | 0 banned meshes in ship scenes |
| `L3_gdai_built` | `bash tools/check_l3_gdai_built.sh` | Exit 0 — **SKIP** when no scene diff; else `.gdai_built` updated + `verified_f5=true` |
| `L2_animation_whitelist` | `python3 tools/check_animation_whitelist.py --phase m5 --strict` | Exit 0 — required ⊆ clips ⊆ `allowed_animations` |
| `L2_feel_smoke` | `bash tools/run_feel_smoke_checks.sh` | Exit 0 — `feel_thresholds.json` + player constants |
| `L2_perf_catalog` | `bash tools/run_perf_review_checks.sh` | Exit 0 — perf baseline catalogs |
| `L2_linux_export_smoke` | `bash tools/run_linux_export_smoke.sh` | Exit 0 — Linux export + headless run; SKIP when no `project.godot` |
| `L2_windows_cross_export` | `bash tools/run_windows_cross_export.sh` | Exit 0 — Windows `.exe` cross-export on ubuntu; SKIP when no `project.godot` |
| `L2_glb_import` | `python3 tools/check_glb_import_scripts.py --strict` | Exit 0 — GLB `.import` post-import script set |
| `L2_boot_headless` | `godot4 --headless …` | Exit 0 when `run/main_scene` is set; exit **2** SKIP when unset |
| `L4_integration` | `bash tools/run_integration_tests.sh` | Exit 0 — `INT-BOOT-01`; fails if `integration_scenarios.json` required scenarios missing |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

### Windows export run (windows-latest)

Second job — `windows-export-run`:

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L2_windows_export_run` | `bash tools/run_windows_export_run.sh` | Exit 0 — Windows export + native `.exe` headless run; **exit 2 SKIP → FAIL** (SKIP≠PASS) |

See `docs/ops/qa/PLATFORM_SUPPORT.md` — Linux run on ubuntu CI; Windows **run** on windows-latest CI.

### CD (`cd-artifact.yml`)

Exports **Linux + Windows**, packages both Steam depot zips — required for v1 (`docs/ops/qa/PLATFORM_SUPPORT.md`).
