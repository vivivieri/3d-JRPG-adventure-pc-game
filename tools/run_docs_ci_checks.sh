#!/usr/bin/env bash
# Main-branch CI — documentation and design data only (no Godot runtime).
# Full game CI: game/development branch → bash tools/run_ci_checks.sh
# See docs/BRANCHING.md
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

echo "==> Main branch CI (docs + design data)"
echo "    Policy: docs/BRANCHING.md"

run_gate "L0_story_data" python3 tools/validate_story_data.py
run_gate "L0_acceptance_catalog" python3 tools/validate_acceptance_criteria.py
run_gate "L0_environments_catalog" python3 tools/validate_environments.py
run_gate "L0_sprint_phases" python3 tools/validate_sprint_phases.py
run_gate "L0_base_classes" python3 tools/validate_base_classes.py
run_gate "L0_zone_composition" python3 tools/validate_zone_composition.py
run_gate "L0_qa_catalog" python3 tools/validate_qa_catalog.py
run_gate "L0_audio_qa_catalog" python3 tools/validate_audio_qa_catalog.py
run_gate "L0_scene_audio_map" python3 tools/validate_scene_audio_map.py
run_gate "L0_generation_readiness_backlog" python3 tools/validate_generation_readiness_backlog.py
run_gate "L0_sprint_board" python3 tools/validate_sprint_board.py --strict
run_gate "L0_rr_compliance" bash tools/check_rr_compliance.sh
run_gate "M5_asset_compliance" bash tools/check_asset_compliance.sh

echo ""
echo "==> Main CI summary: PASS=${PASS} FAIL=${FAIL}"
echo "Game implementation CI runs on branch game/development only."
exit "$FAIL"
