---
id: gates-by-branch
type: reference
audience: [pm, qa, release]
phase: [0, 1]
status: active
authority: ops
tokens_est: 1222
summary: "Which CI gates run on main vs game/development — open for PR gate triage or “why did CI skip/fail” by branch"
---
# Controls — Gates by Branch

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

## When to read

Need the **branch → gate list** cheat sheet. For full pass commands see `required_gates/runs/` or `acceptance_criteria.json`.

## Jump to

- [`main` docs CI](#main--ciyml--run_docs_ci_checkssh)
- [`game/development` game CI](#gamedevelopment--game-ciyml--run_ci_checkssh)

### `main` — `ci.yml` → `run_docs_ci_checks.sh`

**Full list:** `docs_ci_gates.required_gates` in `acceptance_criteria.json` (kept in sync by `L0_doc_sync`). Highlights:

| Gate | Enforces |
|------|----------|
| `L0_story_data` | Data JSON valid |
| `L0_acceptance_catalog` | Gate catalog schema |
| `L0_sprint_board` | Sprint board + done-SHA truth |
| `L0_game_branch_bootstrap` | P1-00 — warns if `game/development` tip lacks `project.godot` |
| `L0_vo_casting` | PLACEHOLDER_* voice ids (advisory on main) |
| `L0_environments_catalog` | Env catalog |
| `L0_sprint_phases` | Sprint config |
| `L0_base_classes` | Code base class registry schema |
| `L0_zone_composition` | Zone composition contract |
| `L0_qa_catalog` | 3D model QA catalog |
| `L0_audio_qa_catalog` | BGM/VO QA catalog |
| `L0_scene_audio_map` | Scene/zone audio map |
| `L0_generation_readiness_backlog` | GR-* backlog traceability |
| `L0_workflow_integration` | Factory feature registry — hooks + doc parity |
| `L0_agent_session_telemetry` | Agent session JSONL + token backfill schema |
| `L0_factory_watchdog` | Factory stall/hang recovery config |
| `L0_factory_automations` | Automation catalog + worker dispatch wiring |
| `L0_stakeholder_report` | Product owner report + Telegram config |
| `L0_alignment_audit_catalog` | Stakeholder alignment audit catalog — management visuals: `audit_radar_spec.png`, `audit_radar_build.png` |
| `L0_candidate_tournament` | Champion/challenger config schema |
| `L0_rr_compliance` | No ship scenes on main |
| `L0_no_secrets` / `L0_ship_build_security` / `L0_player_build_protection` | Security scanners |
| `L1_python_lint` | ruff PEP 8 on `tools/*.py` |
| `L1_shellcheck` | shellcheck on `tools/*.sh` |
| `L1_json_style` | JSON format + naming (`game/data/` + config JSON) |
| `L1_typescript_lint` | ESLint/tsc on MCP Pro (SKIP when not installed) |
| `L1_markdown_style` | Docs whitespace, headings, links |
| `L1_gdshader_style` | NPR shader structure lint |
| `L1_error_handling` | No silent exceptions; `[FAIL]`→stderr |
| `L1_workflow_yaml` | actionlint on GitHub Actions YAML |
| `L1_mypy_libs` | mypy on `tools/*_lib.py` |
| `M5_asset_compliance` | License manifest |

**Not in merge CI (by design):** visual/model/audio jury, L5 E2E, L6 human — see `docs/ops/ci-cd/CI.md` §3.

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
