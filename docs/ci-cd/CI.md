# Continuous Integration — GitHub Actions

**Version:** 1.3  
**Workflow:** `.github/workflows/ci.yml` (main) · `.github/workflows/game-ci.yml` (`game/development`)  
**Runner scripts:** `bash tools/run_docs_ci_checks.sh` (main) · `bash tools/run_ci_checks.sh` (game)  
**Authority:** `game/data/qa/acceptance_criteria.json` → `ci_gates` / `docs_ci_gates`  
**Branch policy:** `docs/workflow/BRANCHING.md`

---

## 0. Branch split

| Branch | CI workflow | What runs |
|--------|-------------|-----------|
| **`main`** | `ci.yml` | Docs + design data validation only — **no Godot runtime** |
| **`game/development`** | `game-ci.yml` | Full headless L0–L4 + game gates — **required green before PR merge** |

Game implementation does **not** merge to `main` until ship-ready (M6). **`game/development` CI is a required merge gate** — it will fail until `game/project.godot` and tests are bootstrapped; that is expected, not a reason to treat CI as optional. See `docs/workflow/BRANCHING.md`.

---

## 1. Purpose

CI enforces **measurable, headless gates** on every push and pull request. It aligns with `.cursorrules` §0 (GDAI R&R), `docs/technical/CODE_BASE_CLASS_RULES.md`, `docs/workflow/AI_DEV_WORKFLOW.md` §2, and `docs/qa/ACCEPTANCE_CRITERIA.md`.

CI is **not** a substitute for GDAI MCP editor verification (L3 F5) or human QA (L6).

**Tri-state gates:** Gate commands use exit `0`=PASS, `1`=FAIL, `2`=SKIP. On `game/development`, SKIP is treated as FAIL for required gates (`global_rules.skip_is_not_pass`), **except during Phase 1 bootstrap** (P1-00: `project.godot` exists but `run/main_scene` unset — see `issue_bootstrap.P1-00`). On `main`, SKIP is allowed for game-only gates (lint, animation, feel, boot).

**P1-00 bootstrap runner:** `bash tools/run_bootstrap_ci_checks.sh` — sets `PHASE1_BOOTSTRAP_CI=1` and allows documented SKIP for export, GLB, and lint gates until P1-02.

---

## 2. What CI runs (required — blocks merge)

### `main` — `ci.yml` → `run_docs_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L0_story_data` | `python3 tools/validate_story_data.py` | Exit 0, 0 errors |
| `L0_acceptance_catalog` | `python3 tools/validate_acceptance_criteria.py` | Catalog schema valid |
| `L0_environments_catalog` | `python3 tools/validate_environments.py` | Env catalog valid |
| `L0_sprint_phases` | `python3 tools/validate_sprint_phases.py` | Sprint config valid |
| `L0_base_classes` | `python3 tools/validate_base_classes.py` | `base_classes.json` schema valid |
| `L0_zone_composition` | `python3 tools/validate_zone_composition.py` | Zone composition contract valid |
| `L0_qa_catalog` | `python3 tools/validate_qa_catalog.py` | 3D model QA catalog valid |
| `L0_audio_qa_catalog` | `python3 tools/validate_audio_qa_catalog.py` | BGM/VO QA catalog + brief cross-refs |
| `L0_scene_audio_map` | `python3 tools/validate_scene_audio_map.py` | Scene/zone audio map vs catalog |
| `L0_generation_readiness_backlog` | `python3 tools/validate_generation_readiness_backlog.py` | GR-* traceability |
| `L0_sprint_board` | `python3 tools/validate_sprint_board.py --strict` | Sprint board + issue pack alignment |
| `L0_factory_watchdog` | `python3 tools/validate_factory_watchdog.py` | Factory stall/hang watchdog config |
| `L0_stakeholder_report` | `python3 tools/validate_stakeholder_report_config.py` | Product owner report + Telegram config |
| `L1_python_lint` | `bash tools/check_python_lint.sh` | Exit 0 — ruff on `tools/` |
| `L1_shellcheck` | `bash tools/check_shell_scripts.sh` | Exit 0 — shellcheck on `tools/*.sh` |
| `L1_json_style` | `python3 tools/check_json_style.py` | Exit 0 — format + naming on `game/data/**/*.json` |
| `L1_typescript_lint` | `bash tools/check_typescript_lint.sh` | Exit 0 — SKIP when MCP Pro not installed |
| `L1_markdown_style` | `python3 tools/check_markdown_style.py` | Exit 0 — docs format + links |
| `L1_gdshader_style` | `python3 tools/check_gdshader_style.py` | Exit 0 — NPR shader structure |
| `L1_error_handling` | `bash tools/check_error_handling.sh` | Exit 0 — ruff E722/S110/S112 + bash/GDScript patterns |
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — no ship `.tscn` on `main` |
| `L0_no_secrets` | `bash tools/check_no_secrets.sh` | Exit 0 — no live keys in tracked files |
| `L0_ship_build_security` | `bash tools/check_ship_build_security.sh` | Exit 0 — export strip policy + binary scan when present |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

### `game/development` — `game-ci.yml` → `run_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — ship `.tscn` allowed when `.gdai_built` has `verified_f5=true` |
| `L0_story_data` | `python3 tools/validate_story_data.py` | Exit 0, 0 errors |
| `L0_acceptance_catalog` | `python3 tools/validate_acceptance_criteria.py` | Catalog schema valid |
| `L0_base_classes` | `python3 tools/validate_base_classes.py` | Registry schema + component script refs |
| `L1_unit_tests` | `bash tools/run_unit_tests.sh` | All unit tests pass headless |
| `L1_python_lint` | `bash tools/check_python_lint.sh` | Exit 0 — ruff on `tools/` |
| `L1_shellcheck` | `bash tools/check_shell_scripts.sh` | Exit 0 — shellcheck on `tools/*.sh` |
| `L1_json_style` | `python3 tools/check_json_style.py` | Exit 0 — JSON format + naming on `game/data/` |
| `L1_typescript_lint` | `bash tools/check_typescript_lint.sh` | Exit 0 — ESLint/tsc when MCP Pro installed |
| `L1_markdown_style` | `python3 tools/check_markdown_style.py` | Exit 0 — docs format + links |
| `L1_gdshader_style` | `python3 tools/check_gdshader_style.py` | Exit 0 — shader templates + game/shaders |
| `L1_scene_style` | `bash tools/check_scene_style.sh` | Exit 0 — static .tscn lint; SKIP when no `game/scenes` |
| `L1_error_handling` | `bash tools/check_error_handling.sh` | Exit 0 — exception/error message patterns |
| `L1_gdscript_lint` | `bash tools/check_gdscript_changed.sh` | Exit 0 — exit **2** SKIP when no `.gd` diff (FAIL on game branch) |
| `L1_gdscript_lint_all` | `bash tools/check_gdscript_all.sh` | Exit 0 — full-tree gdlint; **2** SKIP when no `game/scripts` |
| `L0_base_class_compliance` | `bash tools/check_base_class_compliance.sh` | Exit 0 — no rogue native `extends` (`CharacterBody3D`/`Area3D`/`Node`) |
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

**Second job — `windows-export-run` (windows-latest):**

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L2_windows_export_run` | `bash tools/run_windows_export_run.sh` | Exit 0 — Windows export + native `.exe` headless run; SKIP when no `project.godot` |

See `docs/qa/PLATFORM_SUPPORT.md` — Linux run on ubuntu CI; Windows **run** on windows-latest CI.

---

## 3. What CI does **not** run

These are **agent-local or ship-only** — intentionally excluded from GitHub Actions:

| Check | Why excluded | Where it runs |
|-------|--------------|---------------|
| `check_mcp_ready.sh` | Commercial GDAI plugin + live editor | `install_cloud_dev.sh`, Cursor cloud agents |
| L3_gdai_f5 (full viewport) | Requires Godot editor + GDAI MCP F5 | Per-scene agent tasks |
| `L2_windows_export_run` | Requires Windows host | `game-ci.yml` **windows-latest** job (not ubuntu `run_ci_checks.sh`) |
| L2 visual/audio/model jury | Needs screenshots + LLM API keys | `run_playtest_smoke.sh` when assets exist |
| L5 E2E three endings | Needs Godot MCP Pro + playable build | Phase 6 gate, release candidates |
| L6 human playtest | Human-only — **required ship gate** | `docs/qa/PLAYTEST_SCRIPT.md` after L0–L5 (Phase 8 prod CD) |

**Rule:** Exit **2** = SKIP. On `main`, SKIP is allowed for game-only gates. On `game/development`, `tools/gate_lib.sh` treats SKIP as **FAIL** for required gates (`global_rules.skip_is_not_pass`). Ship/M5 still requires real PASS with evidence — not SKIP.

---

## 4. Local reproduction

**Main branch (docs/data):**

```bash
bash tools/run_docs_ci_checks.sh
```

**Game branch (`game/development`):**

```bash
bash tools/install_ci_deps.sh
bash tools/run_ci_checks.sh
```

Full dev smoke (includes extended toolchain + jury when assets exist):

```bash
bash tools/install_cloud_dev.sh   # requires GDAI stack for scene work
bash tools/run_playtest_smoke.sh
```

---

## 5. R&R alignment (`.cursorrules` §0)

CI **hard-blocks**:

- Ship `.tscn` without valid `game/scenes/.gdai_built` (`verified_f5=true`)
- `run/main_scene` set without matching `.gdai_built` + `verified_f5=true`
- Ship scene or `main_scene` changed in PR without updating `.gdai_built` (`L3_gdai_built`)
- Rogue native `extends` outside registered base classes (`L0_base_class_compliance`)
- Changed `.gd` files failing `gdlint` (`L1_gdscript_lint`) — `gdtoolkit` required on game branch
- Rigged GLB: missing `required_animations`, extra clip names, or missing post-import script (`L2_animation_whitelist`, `L2_glb_import`)
- Game-feel constants missing when `FEEL_SMOKE_STRICT=1` (`L2_feel_smoke`)

**MCP autoloads:** `tools/with_ci_godot.sh` strips dev-only GDAI/MCP Pro autoloads when commercial addons are absent (clean GitHub checkout). Does not install or require MCP.

CI **does not** replace full L3 F5 viewport verify in the editor — `L3_gdai_built` catches the common bypass (scene diff without Builder marker).

---

## 6. Failure remediation

| Failed gate | Fix |
|-------------|-----|
| `L0_rr_compliance` | Remove hand `.tscn` or build via GDAI MCP + write `.gdai_built` |
| `L0_story_data` | Fix JSON cross-refs; run `python3 tools/validate_story_data.py` |
| `L0_base_classes` | Fix `game/data/code/base_classes.json` schema; see `docs/technical/CODE_BASE_CLASS_RULES.md` |
| `L0_base_class_compliance` | Extend `PlayerController` / `Combatant` / `Interactable` bases — no rogue native `extends` |
| `L1_unit_tests` | Fix failing test in `game/tests/unit/` |
| `L1_gdscript_lint` | Fix `gdlint` warnings; run `bash tools/install_ci_deps.sh` if missing |
| `L2_scene_primitives` | Replace `BoxMesh` etc. with real assets or move to `greybox/` |
| `L2_animation_whitelist` | Add missing required clips or update `qa_catalog.json` |
| `L2_feel_smoke` | Add `INPUT_LATENCY` etc. per `game/data/qa/feel_thresholds.json` |
| `L2_glb_import` | `bash tools/install_glb_import_pipeline.sh` then reimport GLBs |
| `L3_gdai_built` | Rebuild scene via GDAI MCP; update `game/scenes/.gdai_built` |
| `M5_asset_compliance` | Update `docs/asset_manifest.license.json` |

See `docs/qa/QA_REMEDIATION_LOOP.md` for structured remediation briefs.

---

## 7. Branch protection (recommended)

On GitHub → Settings → Branches, or via:

```bash
export GH_TOKEN=github_pat_...   # admin PAT in Cursor Secrets
bash tools/setup_github_project.sh
```

| Branch | Required status check | PR reviews |
|--------|----------------------|------------|
| `main` | **Docs + design data gates** | 1 approval |
| `game/development` | **L0–L2 headless gates** | 1 approval |

Manual fallback: `docs/ci-cd/GITHUB_SETUP.md` §2.

---

## 8. Cross-refs

- `docs/technical/CODE_BASE_CLASS_RULES.md` — extend-only base classes + component catalog
- `docs/workflow/AI_DEV_WORKFLOW.md` §2 — test layers L0–L6
- `docs/qa/ACCEPTANCE_CRITERIA.md` — full gate catalog
- `docs/cheat-sheets/CONTROLS_CHEATSHEET.md` — per-role enforcement map
- `docs/ci-cd/CD.md` — continuous deployment (tags on `game/development`)
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `AGENTS.md` — cloud agent bootstrap (MCP stack separate from CI)
