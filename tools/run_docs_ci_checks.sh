#!/usr/bin/env bash
# Main-branch CI — documentation and design data only (no Godot runtime).
# Full game CI: game/development branch → bash tools/run_ci_checks.sh
# See docs/workflow/BRANCHING.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

run_gate() {
  local gate_id="$1"
  shift
  echo ""
  echo "── ${gate_id}"
  if "$@"; then
    echo "[PASS] ${gate_id}"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] ${gate_id}"
    FAIL=$((FAIL + 1))
  fi
}

BRANCH="$(bash "$(dirname "$0")/git_branch_name.sh")"
echo "==> Main branch CI (docs + design data)"
echo "    Policy: docs/workflow/BRANCHING.md"
if [[ "$BRANCH" == "game/development" ]]; then
  echo "    Note: checked out ${BRANCH} — ship-code gates skip via branch-aware scripts"
fi

run_gate "L0_story_data" python3 tools/validate_story_data.py
run_gate "L0_narrative_density" python3 tools/validate_narrative_density.py
run_gate "L0_spec_registry" python3 tools/validate_spec_registry.py
run_gate "L0_helpers_registry" python3 tools/validate_helpers_registry.py
run_gate "L0_reference_libs" python3 tools/test_reference_libs.py
run_gate "L1_python_lint" bash tools/check_python_lint.sh
run_gate "L1_shellcheck" bash tools/check_shell_scripts.sh
run_gate "L1_json_style" python3 tools/check_json_style.py
run_gate "L1_typescript_lint" bash tools/check_typescript_lint.sh
run_gate "L1_markdown_style" python3 tools/check_markdown_style.py
run_gate "L1_gdshader_style" python3 tools/check_gdshader_style.py
run_gate "L1_error_handling" bash tools/check_error_handling.sh
run_gate "L1_workflow_yaml" bash tools/check_workflow_yaml.sh
run_gate "L1_mypy_libs" bash tools/check_mypy_libs.sh
run_gate "L0_main_no_ship_code" bash tools/check_main_no_ship_code.sh
run_gate "L0_spec_refinement_scope" bash tools/check_spec_refinement_scope.sh
run_gate "L0_difficulty_data" python3 tools/validate_difficulty_data.py
run_gate "L0_acceptance_catalog" python3 tools/validate_acceptance_criteria.py
run_gate "L0_environments_catalog" python3 tools/validate_environments.py
run_gate "L0_sprint_phases" python3 tools/validate_sprint_phases.py
run_gate "L0_base_classes" python3 tools/validate_base_classes.py
run_gate "L0_zone_visuals_contract" python3 tools/validate_zone_visuals_contract.py
run_gate "L0_scene_registry" python3 tools/validate_scene_registry.py
run_gate "L0_zone_composition" python3 tools/validate_zone_composition.py
run_gate "L0_qa_catalog" python3 tools/validate_qa_catalog.py
run_gate "L0_audio_qa_catalog" python3 tools/validate_audio_qa_catalog.py
run_gate "L0_scene_audio_map" python3 tools/validate_scene_audio_map.py
run_gate "L0_playtest_telemetry" python3 tools/validate_playtest_telemetry_schema.py
run_gate "L0_agent_session_telemetry" python3 tools/validate_agent_session_telemetry_schema.py
run_gate "L0_delivery_control" python3 tools/validate_delivery_control.py
run_gate "L0_generation_readiness_backlog" python3 tools/validate_generation_readiness_backlog.py
run_gate "L0_sprint_board" python3 tools/validate_sprint_board.py --strict
run_gate "L0_game_branch_bootstrap" bash tools/check_game_branch_bootstrap.sh
run_gate "L0_vo_casting" python3 tools/validate_vo_casting.py
run_gate "L0_factory_watchdog" python3 tools/validate_factory_watchdog.py
run_gate "L0_escalation_policy" python3 tools/validate_escalation_policy.py
run_gate "L0_stakeholder_report" python3 tools/validate_stakeholder_report_config.py
run_gate "L0_pm_orchestrator" python3 tools/validate_pm_orchestrator_steps.py
run_gate "L0_rr_compliance" bash tools/check_rr_compliance.sh
run_gate "L0_no_secrets" bash tools/check_no_secrets.sh
run_gate "L0_ship_build_security" bash tools/check_ship_build_security.sh
run_gate "L0_player_build_protection" bash tools/check_player_build_protection.sh
run_gate "L0_doc_sync" python3 tools/check_doc_sync.py
run_gate "L0_alignment_audit_catalog" python3 tools/validate_alignment_audit_catalog.py
run_gate "L0_workflow_integration" python3 tools/validate_workflow_integration.py
run_gate "L0_candidate_tournament" python3 tools/validate_candidate_tournament.py
run_gate "M5_asset_compliance" bash tools/check_asset_compliance.sh

echo ""
echo "==> Main CI summary: PASS=${PASS} FAIL=${FAIL}"
echo "Game implementation CI runs on branch game/development only."
exit "$FAIL"
