---
id: part-a
type: reference
phase: [0, 1]
audience: [pm, qa, release]
status: active
authority: ops
tokens_est: 643
summary: "Controls — Gates by Branch (A)"
---
# Controls — Gates by Branch — Controls — Gates by Branch (A)

**Hub:** [`gates_by_branch.md`](../gates_by_branch.md)

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
