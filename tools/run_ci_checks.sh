#!/usr/bin/env bash
# GitHub Actions / pre-push CI — headless L0–L2 gates only.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=gate_lib.sh
source "${ROOT}/tools/gate_lib.sh"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
export CI=true

PASS=0
FAIL=0
SKIP=0

ANIM_PHASE="1"
ANIM_STRICT=""
if gate_is_game_branch; then
  ANIM_PHASE="m5"
  ANIM_STRICT="--strict"
fi

echo "==> CI checks (headless L0–L2)"
echo "    Policy: docs/CI.md, .cursorrules §0, docs/AI_DEV_WORKFLOW.md §2"

run_tri_gate "L0_rr_compliance" "R&R — no hand-built ship .tscn" \
  bash tools/check_rr_compliance.sh

run_tri_gate "L0_story_data" "Story JSON cross-references" \
  python3 tools/validate_story_data.py

run_tri_gate "L0_acceptance_catalog" "Acceptance criteria catalog" \
  python3 tools/validate_acceptance_criteria.py

run_tri_gate "L0_base_classes" "Code base class registry" \
  python3 tools/validate_base_classes.py

run_tri_gate "L1_unit_tests" "Godot headless unit tests" \
  bash tools/run_unit_tests.sh

run_tri_gate "L1_gdscript_lint" "GDScript lint on changed files" \
  bash tools/check_gdscript_changed.sh

run_tri_gate "L0_base_class_compliance" "No rogue native extends" \
  bash tools/check_base_class_compliance.sh

run_tri_gate "L2_scene_primitives" "Banned primitive meshes in ship scenes" \
  bash tools/check_scene_visuals.sh

if [[ -f game/project.godot ]]; then
  run_tri_gate "L2_zone_composition" "Zone scenes per zone_composition.json (GR-003)" \
    bash tools/run_zone_composition_checks.sh
else
  skip_gate "L2_zone_composition" "no game/project.godot"
fi

run_tri_gate "L3_gdai_built" "GDAI marker updated when scenes change" \
  bash tools/check_l3_gdai_built.sh

run_tri_gate "L2_animation_whitelist" "GLB animation whitelist + required floor" \
  python3 tools/check_animation_whitelist.py --phase "$ANIM_PHASE" $ANIM_STRICT

run_tri_gate "L2_feel_smoke" "Game feel thresholds (GAME_FEEL.md)" \
  bash tools/run_feel_smoke_checks.sh

run_tri_gate "L2_perf_catalog" "Performance thresholds catalog" \
  bash tools/run_perf_review_checks.sh

MAIN_SCENE="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
if [[ -z "$MAIN_SCENE" ]]; then
  skip_gate "L2_boot_headless" "no run/main_scene (design-phase baseline)"
else
  run_tri_gate "L2_boot_headless" "Main scene loads headless" \
    bash tools/with_ci_godot.sh \
      godot4 --headless --rendering-driver opengl3 --path game --quit-after 120
fi

if gate_is_game_branch; then
  run_tri_gate "L2_glb_import" "GLB post-import toon pipeline" \
    python3 tools/check_glb_import_scripts.py --strict
fi

if [[ -f game/project.godot ]]; then
  run_tri_gate "L2_linux_export_smoke" "Linux export + native headless run" \
    bash tools/run_linux_export_smoke.sh
  run_tri_gate "L2_windows_cross_export" "Windows cross-export (.exe build)" \
    bash tools/run_windows_cross_export.sh
else
  skip_gate "L2_linux_export_smoke" "no game/project.godot"
  skip_gate "L2_windows_cross_export" "no game/project.godot"
fi

run_tri_gate "L4_integration" "Integration tests (headless subset)" \
  bash tools/run_integration_tests.sh

if [[ -f docs/asset_manifest.license.json ]]; then
  run_tri_gate "M5_asset_compliance" "License manifest vs shipped media" \
    bash tools/check_asset_compliance.sh
else
  skip_gate "M5_asset_compliance" "no asset manifest yet"
fi

echo ""
echo "==> CI summary: PASS=${PASS} FAIL=${FAIL} SKIP=${SKIP}"
echo ""
echo "Not run in CI (agent/editor only):"
echo "  - check_mcp_ready.sh — GDAI MCP stack"
echo "  - L3_gdai_f5 full viewport verify (editor F5)"
echo "  - L2_windows_export_run — windows-latest CI (tools/run_windows_export_run.sh)"
echo "  - L3_perf_review — Godotiq perf_snapshot (FPS, draw calls)"
echo "  - L2 visual/audio/model jury (requires screenshots + API keys; use run_*_smoke_checks.sh)"
echo "  - L5 E2E three endings (REQUIRE_L5=1 for Phase 6+ / CD beta|prod)"
echo "  - L6 human playtest"
echo ""
echo "Docs: docs/CI.md"

exit "$FAIL"
