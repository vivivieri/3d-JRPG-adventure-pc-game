#!/usr/bin/env bash
# Quick automated playtest smoke checks (not a full 2–3 hr manual playthrough).
# Full script: docs/PLAYTEST_SCRIPT.md
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

echo "==> Playtest smoke checks"
echo ""

check "Story data validates" python3 tools/validate_story_data.py
check "Dev environment healthy" bash tools/check_dev_environment.sh
check "Main menu loads" godot4 --headless --rendering-driver opengl3 --path game --quit-after 3
check "Beach zone loads" godot4 --headless --rendering-driver opengl3 --path game res://scenes/world/beach_shore.tscn --quit-after 2
check "Village zone loads" godot4 --headless --rendering-driver opengl3 --path game res://scenes/world/ruined_village.tscn --quit-after 2
check "Palace zone loads" godot4 --headless --rendering-driver opengl3 --path game res://scenes/world/dragon_palace_gate.tscn --quit-after 2
check "Windows exe exists" test -f build/TidesOfUrashima.exe
check "GodotSteam gdextension present" test -f game/addons/godotsteam/godotsteam.gdextension
check "Player movement works" godot4 --headless --rendering-driver opengl3 --path game res://tests/movement_smoke_test.tscn

echo ""
echo "Passed: $PASS | Failed: $FAIL"
echo ""
echo "Manual playtest (2–3 hr): see docs/PLAYTEST_SCRIPT.md"
echo "  1. F5 in Godot → New Game → play through Act I–III"
echo "  2. Test all 3 endings at SC-16"
echo "  3. Verify save at village well + Continue"

exit "$FAIL"
