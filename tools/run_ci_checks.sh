#!/usr/bin/env bash
# GitHub Actions / pre-push CI — headless L0–L2 gates only.
# Does NOT require GDAI MCP, editor, or jury API keys.
# See docs/CI.md and game/data/qa/acceptance_criteria.json → ci_gates.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
export CI=true

PASS=0
FAIL=0
SKIP=0

run_gate() {
  local gate_id="$1"
  local label="$2"
  shift 2
  echo ""
  echo "── ${gate_id}: ${label}"
  if "$@"; then
    echo "[PASS] ${gate_id}"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] ${gate_id}"
    FAIL=$((FAIL + 1))
  fi
}

skip_gate() {
  local gate_id="$1"
  local reason="$2"
  echo ""
  echo "── ${gate_id}: SKIP — ${reason}"
  SKIP=$((SKIP + 1))
}

echo "==> CI checks (headless L0–L2)"
echo "    Policy: docs/CI.md, .cursorrules §0, docs/AI_DEV_WORKFLOW.md §2"

run_gate "L0_rr_compliance" "R&R — no hand-built ship .tscn" \
  bash tools/check_rr_compliance.sh

run_gate "L0_story_data" "Story JSON cross-references" \
  python3 tools/validate_story_data.py

run_gate "L0_acceptance_catalog" "Acceptance criteria catalog" \
  python3 tools/validate_acceptance_criteria.py

run_gate "L1_unit_tests" "Godot headless unit tests" \
  bash tools/run_unit_tests.sh

run_gate "L2_scene_primitives" "Banned primitive meshes in ship scenes" \
  bash tools/check_scene_visuals.sh

MAIN_SCENE="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
if [[ -z "$MAIN_SCENE" ]]; then
  skip_gate "L2_boot_headless" "no run/main_scene (design-phase baseline; GDAI builds first scene)"
else
  run_gate "L2_boot_headless" "Main scene loads headless" \
    bash tools/with_ci_godot.sh \
      godot4 --headless --rendering-driver opengl3 --path game --quit-after 3
fi

run_gate "L4_integration" "Integration tests (headless subset)" \
  bash tools/run_integration_tests.sh

if [[ -f docs/asset_manifest.license.json ]]; then
  run_gate "M5_asset_compliance" "License manifest vs shipped media" \
    bash tools/check_asset_compliance.sh
else
  skip_gate "M5_asset_compliance" "no asset manifest yet"
fi

echo ""
echo "==> CI summary: PASS=${PASS} FAIL=${FAIL} SKIP=${SKIP}"
echo ""
echo "Not run in CI (agent/editor only):"
echo "  - check_mcp_ready.sh — GDAI MCP stack (Cursor cloud / local dev)"
echo "  - L3 GDAI F5 viewport verify"
echo "  - L2 visual/audio/model jury (requires screenshots + API keys)"
echo "  - L5 E2E three endings (requires Godot MCP Pro + playable build)"
echo "  - L6 human playtest"
echo ""
echo "Docs: docs/CI.md"

exit "$FAIL"
