#!/usr/bin/env bash
# Quick automated smoke checks for fresh-rebuild dev shell.
# Full manual playtest script: docs/PLAYTEST_SCRIPT.md (re-enable after Phase 2+).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

PASS=0
FAIL=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "[PASS] $label"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
  fi
}

echo "==> Fresh-rebuild smoke checks"
echo ""

check "Story data validates" python3 tools/validate_story_data.py
check "Unit tests pass" bash tools/run_unit_tests.sh
check "Dev environment healthy" bash tools/check_dev_environment.sh
check "Boot scene loads" godot4 --headless --rendering-driver opengl3 --path game --quit-after 3

echo ""
echo "Passed: $PASS | Failed: $FAIL"
echo ""
echo "Rebuild phases: docs/IMPLEMENTATION_PLAN.md"
echo "  Phase 1: ruined_village environment vertical slice via GDAI MCP"

exit "$FAIL"
