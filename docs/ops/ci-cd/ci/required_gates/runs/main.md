---
id: main
type: reference
audience: [release, qa, pm]
phase: [6, 8]
status: active
authority: ci-cd
tokens_est: 440
summary: "CI — What Runs (`main`) — Authority: `game/data/qa/acceptance_criteria.json` → `docs_ci_gates.required_gates` (must match `run_docs_ci_checks.sh` 1:1 via `L0_do"
---
# CI — What Runs (`main`)

**Hub:** [`what_runs.md`](../what_runs.md)

## When to read

Use **CI — What Runs (`main`)** (roles: release, qa, pm) when you need this reference during the current task Jump to a section below instead of reading end-to-end (1 sections).



### `main` — `ci.yml` → `run_docs_ci_checks.sh`

**Authority:** `game/data/qa/acceptance_criteria.json` → `docs_ci_gates.required_gates` (must match `run_docs_ci_checks.sh` 1:1 via `L0_doc_sync`).

| Category | Gate IDs (examples) |
|----------|---------------------|
| Story / narrative / specs | `L0_story_data`, `L0_narrative_density`, `L0_spec_registry`, `L0_helpers_registry`, `L0_reference_libs` |
| Style / lint | `L1_python_lint`, `L1_shellcheck`, `L1_json_style`, `L1_typescript_lint`, `L1_markdown_style`, `L1_gdshader_style`, `L1_error_handling`, `L1_workflow_yaml`, `L1_mypy_libs` |
| Catalogs / registries | `L0_acceptance_catalog`, `L0_environments_catalog`, `L0_sprint_phases`, `L0_base_classes`, `L0_zone_*`, `L0_qa_catalog`, `L0_audio_*`, `L0_*_telemetry` |
| Factory / PM | `L0_sprint_board`, `L0_game_branch_bootstrap`, `L0_vo_casting`, `L0_factory_watchdog`, `L0_escalation_policy`, `L0_stakeholder_report`, `L0_pm_orchestrator`, `L0_workflow_integration`, `L0_candidate_tournament` |
| Security / compliance | `L0_rr_compliance`, `L0_no_secrets`, `L0_ship_build_security`, `L0_player_build_protection`, `M5_asset_compliance` |
| Docs sync | `L0_doc_sync`, `L0_alignment_audit_catalog`, `L0_main_no_ship_code`, `L0_spec_refinement_scope`, `L0_difficulty_data`, `L0_delivery_control`, `L0_generation_readiness_backlog` |

Full list: `python3 -c "import json; print('\\n'.join(json.load(open('game/data/qa/acceptance_criteria.json'))['docs_ci_gates']['required_gates']))"`
