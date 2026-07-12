# Continuous Integration — GitHub Actions

**Version:** 1.0  
**Workflow:** `.github/workflows/ci.yml` (main) · `.github/workflows/game-ci.yml` (`game/development`)  
**Runner scripts:** `bash tools/run_docs_ci_checks.sh` (main) · `bash tools/run_ci_checks.sh` (game)  
**Authority:** `game/data/qa/acceptance_criteria.json` → `ci_gates` / `docs_ci_gates`  
**Branch policy:** `docs/BRANCHING.md`

---

## 0. Branch split

| Branch | CI workflow | What runs |
|--------|-------------|-----------|
| **`main`** | `ci.yml` | Docs + design data validation only — **no Godot runtime** |
| **`game/development`** | `game-ci.yml` | Full headless L0–L2 + L4 game gates |

Game implementation does **not** merge to `main` until ship-ready (M6). See `docs/BRANCHING.md`.

---

## 1. Purpose (game branch)

CI enforces **measurable, headless gates** on every push to `main` and every pull request. It aligns with `.cursorrules` §0 (GDAI R&R), `docs/AI_DEV_WORKFLOW.md` §2, and `docs/ACCEPTANCE_CRITERIA.md`.

CI is **not** a substitute for GDAI MCP editor verification (L3) or human QA (L6).

---

## 2. What CI runs (required — blocks merge)

| Gate ID | Command | Pass when |
|---------|---------|-----------|
| `L0_rr_compliance` | `bash tools/check_rr_compliance.sh` | Exit 0 — no hand-built ship `.tscn`; `main_scene` requires `.gdai_built` |
| `L0_story_data` | `python3 tools/validate_story_data.py` | Exit 0, 0 errors |
| `L0_acceptance_catalog` | `python3 tools/validate_acceptance_criteria.py` | Catalog schema valid |
| `L1_unit_tests` | `bash tools/run_unit_tests.sh` | All unit tests pass headless |
| `L2_scene_primitives` | `bash tools/check_scene_visuals.sh` | 0 banned meshes in ship scenes |
| `L2_boot_headless` | `godot4 --headless …` | Exit 0 when `run/main_scene` is set; **SKIP** (not fail) when unset |
| `L4_integration` | `bash tools/run_integration_tests.sh` | Exit 0 (boot step skipped when no `main_scene`) |
| `M5_asset_compliance` | `bash tools/check_asset_compliance.sh` | Exit 0 when manifest exists |

---

## 3. What CI does **not** run

These are **agent-local or ship-only** — intentionally excluded from GitHub Actions:

| Check | Why excluded | Where it runs |
|-------|--------------|---------------|
| `check_mcp_ready.sh` | Commercial GDAI plugin + live editor | `install_cloud_dev.sh`, Cursor cloud agents |
| L3 GDAI F5 viewport | Requires Godot editor + GDAI MCP | Per-scene agent tasks |
| L2 visual/audio/model jury | Needs screenshots + LLM API keys | `run_playtest_smoke.sh` when assets exist |
| L5 E2E three endings | Needs Godot MCP Pro + playable build | Phase 6 gate, release candidates |
| L6 human playtest | Human-only | `docs/PLAYTEST_SCRIPT.md` after L0–L5 |

**Rule:** `SKIP` in CI is allowed for design-phase baselines (e.g. no `main_scene`). `SKIP` is **not** ship pass per `global_rules.skip_is_not_pass`.

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

**MCP autoloads:** `tools/with_ci_godot.sh` strips dev-only GDAI/MCP Pro autoloads when commercial addons are absent (clean GitHub checkout). Does not install or require MCP.

CI **does not** prove scenes were built via GDAI MCP — that requires L3 (agent F5 + marker file). The R&R gate prevents the common bypass: merging hand-edited scenes.

---

## 6. Failure remediation

| Failed gate | Fix |
|-------------|-----|
| `L0_rr_compliance` | Remove hand `.tscn` or build via GDAI MCP + write `.gdai_built` |
| `L0_story_data` | Fix JSON cross-refs; run `python3 tools/validate_story_data.py` |
| `L1_unit_tests` | Fix failing test in `game/tests/unit/` |
| `L2_scene_primitives` | Replace `BoxMesh` etc. with real assets or move to `greybox/` |
| `M5_asset_compliance` | Update `docs/asset_manifest.license.json` |

See `docs/QA_REMEDIATION_LOOP.md` for structured remediation briefs.

---

## 7. Branch protection (recommended)

On GitHub → Settings → Branches → `main`:

- Require status check: **L0–L2 headless gates**
- Require branches up to date before merge

---

## 8. Cross-refs

- `docs/AI_DEV_WORKFLOW.md` §2 — test layers L0–L6
- `docs/ACCEPTANCE_CRITERIA.md` — full gate catalog
- `game/data/qa/acceptance_criteria.json` — machine-readable thresholds
- `AGENTS.md` — cloud agent bootstrap (MCP stack separate from CI)
