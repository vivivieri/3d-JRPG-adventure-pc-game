#!/usr/bin/env bash
# Integration tests (L4) — expand as phases land.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=gate_lib.sh
source "${ROOT}/tools/gate_lib.sh"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

PASS=0
FAIL=0
SKIP=0

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

echo "==> Integration tests (L4)"
echo ""

check "R&R compliance" bash tools/check_rr_compliance.sh

MAIN_SCENE="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | cut -d= -f2- | tr -d '"' || true)"
if [[ -z "$MAIN_SCENE" ]]; then
  echo "[SKIP] Boot scene loads headless — no run/main_scene until GDAI MCP builds first scene"
  SKIP=$((SKIP + 1))
else
  check "INT-BOOT-01 Boot scene loads headless" \
    godot4 --headless --rendering-driver opengl3 --path game --quit-after 120
fi

# Fail if game branch requires unimplemented scenarios for current phase
if [[ -f "${ROOT}/game/data/qa/integration_scenarios.json" ]]; then
  python3 - <<'PY' || FAIL=$((FAIL + 1))
import json
import sys
from pathlib import Path

root = Path(".")
catalog = json.loads((root / "game/data/qa/integration_scenarios.json").read_text())
game = (root / "game/project.godot").is_file()
missing = []
for s in catalog.get("scenarios", []):
    if not s.get("implemented") and s.get("required_on_game_branch") and game:
        missing.append(s["id"])
if missing:
    print(f"[FAIL] L4 required scenarios not implemented: {', '.join(missing)}")
    sys.exit(1)
unimpl = [s["id"] for s in catalog["scenarios"] if not s.get("implemented")]
print(f"[OK]   L4 catalog — implemented: INT-BOOT-01; pending: {', '.join(unimpl[1:]) or 'none'}")
PY
fi

echo ""
echo "Passed: $PASS | Failed: $FAIL | Skipped: $SKIP"
echo "See docs/qa/AI_TESTING_SPEC.md §6 for full INT-* catalog."

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
if [[ "$PASS" -eq 0 && "$SKIP" -gt 0 ]]; then
  exit 2
fi
exit 0
