# Continuous Integration — GitHub Actions

**Version:** 1.1  
**Workflow:** `.github/workflows/ci.yml` (main) · `.github/workflows/game-ci.yml` (`game/development`)  
**Runner scripts:** `bash tools/run_docs_ci_checks.sh` (main) · `bash tools/run_ci_checks.sh` (game)  
**Authority:** `game/data/qa/acceptance_criteria.json` → `ci_gates` / `docs_ci_gates`  
**Branch policy:** `docs/BRANCHING.md`

---

## 0. Branch split

| Branch | CI workflow | What runs |
|--------|-------------|-----------|
| **`main`** | `ci.yml` | Docs + design data validation only — **no Godot runtime** |
| **`game/development`** | `game-ci.yml` | Full headless L0–L4 + game gates |

Game implementation does **not** merge to `main` until ship-ready (M6). See `docs/BRANCHING.md`.

---

## 1. Purpose

CI enforces **measurable, headless gates** on every push and pull request. It aligns with `.cursorrules` §0 (GDAI R&R), `docs/CODE_BASE_CLASS_RULES.md`, `docs/AI_DEV_WORKFLOW.md` §2, and `docs/ACCEPTANCE_CRITERIA.md`.

CI is **not** a substitute for GDAI MCP editor verification (L3 F5) or human QA (L6).

**Tri-state gates:** Gate commands use exit `0`=PASS, `1`=FAIL, `2`=SKIP. On `game/development`, SKIP is treated as FAIL for required gates (`global_rules.skip_is_not_pass`). On `main`, SKIP is allowed for game-only gates (lint, animation, feel, boot).

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
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — no ship `.tscn` on `main` |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

### `game/development` — `game-ci.yml` → `run_ci_checks.sh`

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — no hand-built ship `.tscn`; `main_scene` requires `.gdai_built` |
| `L0_story_data` | `python3 tools/validate_story_data.py` | Exit 0, 0 errors |
| `L0_acceptance_catalog` | `python3 tools/validate_acceptance_criteria.py` | Catalog schema valid |
| `L0_base_classes` | `python3 tools/validate_base_classes.py` | `base_classes.json` schema valid |
| `L1_unit_tests` | `bash tools/run_unit_tests.sh` | All unit tests pass headless |
| `L1_gdscript_lint` | `bash tools/check_gdscript_changed.sh` | Exit 0 — **SKIP** when no `.gd` diff |
| `L0_base_class_compliance` | `bash tools/check_base_class_compliance.sh` | Exit 0 — no rogue `CharacterBody3D` controllers |
| `L2_scene_primitives` | `bash tools/check_scene_visuals.sh` | 0 banned meshes in ship scenes |
| `L3_gdai_built` | `bash tools/check_l3_gdai_built.sh` | Exit 0 — **SKIP** when no scene diff; else `.gdai_built` updated + `verified_f5=true` |
| `L2_animation_whitelist` | `python3 tools/check_animation_whitelist.py --phase 1` | Exit 0 — **SKIP** when no rigged GLB on disk |
| `L2_boot_headless` | `godot4 --headless …` | Exit 0 when `run/main_scene` is set; **SKIP** when unset |
| `L4_integration` | `bash tools/run_integration_tests.sh` | Exit 0 (boot step skipped when no `main_scene`) |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

---

## 3. What CI does **not** run

These are **agent-local or ship-only** — intentionally excluded from GitHub Actions:

| Check | Why excluded | Where it runs |
|-------|--------------|---------------|
| `check_mcp_ready.sh` | Commercial GDAI plugin + live editor | `install_cloud_dev.sh`, Cursor cloud agents |
| L3_gdai_f5 (full viewport) | Requires Godot editor + GDAI MCP F5 | Per-scene agent tasks |
| L2 visual/audio/model jury | Needs screenshots + LLM API keys | `run_playtest_smoke.sh` when assets exist |
| L5 E2E three endings | Needs Godot MCP Pro + playable build | Phase 6 gate, release candidates |
| L6 human playtest | Human-only | `docs/PLAYTEST_SCRIPT.md` after L0–L5 |

**Rule:** `SKIP` in CI is allowed for design-phase baselines (e.g. no `main_scene`, no GLB yet). `SKIP` is **not** ship pass per `global_rules.skip_is_not_pass`.

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

Full dev smoke (includes MCP warnings, optional jury):

```bash
bash tools/install_cloud_dev.sh   # requires GDAI stack for scene work
bash tools/run_playtest_smoke.sh
```

---

## 5. R&R alignment (`.cursorrules` §0)

CI **hard-blocks**:

- Committed ship `.tscn` outside `greybox/` / `_dev/` without `game/scenes/.gdai_built`
- `run/main_scene` set without matching `.gdai_built` + `verified_f5=true`
- Ship scene or `main_scene` changed in PR without updating `.gdai_built` (`L3_gdai_built`)
- New `CharacterBody3D` player stacks outside `PlayerController` (`L0_base_class_compliance`)
- Changed `.gd` files failing `gdlint` (`L1_gdscript_lint`)
- Rigged GLB animation names outside `qa_catalog.json` → `allowed_animations` (`L2_animation_whitelist`)

**MCP autoloads:** `tools/with_ci_godot.sh` strips dev-only GDAI/MCP Pro autoloads when commercial addons are absent (clean GitHub checkout). Does not install or require MCP.

CI **does not** replace full L3 F5 viewport verify in the editor — `L3_gdai_built` catches the common bypass (scene diff without Builder marker).

---

## 6. Failure remediation

| Failed gate | Fix |
|-------------|-----|
| `L0_rr_compliance` | Remove hand `.tscn` or build via GDAI MCP + write `.gdai_built` |
| `L0_story_data` | Fix JSON cross-refs; run `python3 tools/validate_story_data.py` |
| `L0_base_classes` | Fix `game/data/code/base_classes.json` schema; see `docs/CODE_BASE_CLASS_RULES.md` |
| `L0_base_class_compliance` | Extend `PlayerController` / `Combatant` / `Interactable` — do not add new controller roots |
| `L1_unit_tests` | Fix failing test in `game/tests/unit/` |
| `L1_gdscript_lint` | Fix `gdlint` warnings on changed `.gd` files |
| `L2_scene_primitives` | Replace `BoxMesh` etc. with real assets or move to `greybox/` |
| `L2_animation_whitelist` | Rename Mixamo clips or update `qa_catalog.json` → `allowed_animations` |
| `L3_gdai_built` | Rebuild scene via GDAI MCP; update `game/scenes/.gdai_built` |
| `M5_asset_compliance` | Update `docs/asset_manifest.license.json` |

See `docs/QA_REMEDIATION_LOOP.md` for structured remediation briefs.

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

Manual fallback: `docs/GITHUB_SETUP.md` §2.

---

## 8. Cross-refs

- `docs/CODE_BASE_CLASS_RULES.md` — extend-only base classes + component catalog
- `docs/AI_DEV_WORKFLOW.md` §2 — test layers L0–L6
- `docs/ACCEPTANCE_CRITERIA.md` — full gate catalog
- `docs/CONTROLS_CHEATSHEET.md` — per-role enforcement map
- `docs/CD.md` — continuous deployment (tags on `game/development`)
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `AGENTS.md` — cloud agent bootstrap (MCP stack separate from CI)
