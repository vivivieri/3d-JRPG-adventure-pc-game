#!/usr/bin/env bash
# Integration tests (L4) — expand as phases land.
# See docs/AI_DEV_WORKFLOW.md §2 and §4.
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
    if [[ "$label" == *"Boot scene"* ]]; then
      bash "${ROOT}/tools/qa_emit_remediation.sh" flow-scenario INT-BOOT-01 || true
    fi
  fi
}

echo "==> Integration tests"
echo ""

check "Boot scene loads headless" \
  godot4 --headless --rendering-driver opengl3 --path game --quit-after 3

# Phase 2+: add zone transition, save/load, combat round scripts here.

echo ""
echo "Passed: $PASS | Failed: $FAIL"
echo "See docs/AI_DEV_WORKFLOW.md for phase acceptance criteria."

exit "$FAIL"
