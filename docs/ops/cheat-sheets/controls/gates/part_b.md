---
id: part-b
type: reference
phase: [0, 1]
audience: [pm, qa, release]
status: active
authority: ops
tokens_est: 617
summary: "Controls — Gates by Branch (B)"
---
# Controls — Gates by Branch — Controls — Gates by Branch (B)

**Hub:** [`gates_by_branch.md`](../gates_by_branch.md)

### `game/development` — `game-ci.yml` → `run_ci_checks.sh`

| Gate | Role mainly enforced |
|------|----------------------|
| `L0_rr_compliance` | **Builder** — GDAI-verified ship `.tscn` only (`.gdai_built`) |
| `L0_game_branch_bootstrap` | **PM** — `project.godot` required |
| `L0_vo_casting` | **Visual** / audio — no PLACEHOLDER_* at M5/CD |
| `L0_story_data` | **Architect** / data |
| `L0_acceptance_catalog` | **QA** catalog |
| `L0_workflow_integration` | **PM** — factory feature registry parity |
| `L0_candidate_tournament` | **PM** — golden harness + tournament policy schema |
| `L0_base_classes` | **Architect** — base class registry |
| `L1_unit_tests` | **Architect** |
| `L2_scene_primitives` | **Builder** / **Visual** |
| `L2_boot_headless` | **Builder** (when `main_scene` set) |
| `L3_gdai_built` | **Builder** — marker updated with scene diff |
| `L2_animation_whitelist` | **Builder** / **Visual** — required ⊆ Mixamo clips ⊆ whitelist |
| `L2_feel_smoke` | **Architect** — `GAME_FEEL.md` constants |
| `L2_perf_catalog` | **QA** / **Builder** — `perf_thresholds.json` catalog |
| `L2_glb_import` | **Builder** / **Visual** — post-import toon pipeline |
| `L2_candidate_select` | **Builder** / **Visual** — champion/challenger evidence (pre-merge, non-ship) |
| `L1_gdscript_lint` | **Architect** — changed `.gd` files (`gdtoolkit` required) |
| `L1_python_lint` | **Architect** / **QA** — ruff on `tools/` |
| `L1_shellcheck` | **Architect** — shellcheck on gate scripts |
| `L1_json_style` | **Architect** — JSON format + naming |
| `L1_markdown_style` | **Architect** — docs format + links |
| `L1_gdshader_style` | **Visual** — shader templates |
| `L1_scene_style` | **Builder** — static `.tscn` lint |
| `L1_error_handling` | **QA** — cross-language error patterns |
| `L1_workflow_yaml` | **Release** — GitHub Actions YAML lint |
| `L1_mypy_libs` | **Architect** — typed reference libraries |
| `L0_base_class_compliance` | **Architect** — no rogue native extends |
| `L4_integration` | **Flow** |
| `M5_asset_compliance` | **Release** / compliance |

**Not in CI (agent-local):** `check_mcp_ready.sh`, full **L3 F5 viewport**, L2 jury, **L5 E2E**, **L6 human**.

---
