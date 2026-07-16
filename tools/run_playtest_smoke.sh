#!/usr/bin/env bash
# Quick automated smoke checks for fresh-rebuild dev shell.
# Full manual playtest script: docs/qa/PLAYTEST_SCRIPT.md (re-enable after Phase 2+).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

PASS=0
FAIL=0
WARN=0

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

check_story_data() {
  local label="Story data validates"
  local log
  log="$(mktemp)"
  set +e
  python3 tools/validate_story_data.py >"$log" 2>&1
  local rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    cat "$log"
    echo "[PASS] $label"
    PASS=$((PASS + 1))
  else
    cat "$log"
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
    bash tools/qa_emit_remediation.sh data-story || true
    python3 tools/qa_write_gate_result.py --gate L0_story_data --status fail \
      --message "validate_story_data failed" 2>/dev/null || true
  fi
  rm -f "$log"
}

check_scene_visuals() {
  local label="Scene visual lint (no primitives)"
  local log
  log="$(mktemp)"
  set +e
  bash tools/check_scene_visuals.sh >"$log" 2>&1
  local rc=$?
  set -e
  cat "$log"
  if [[ "$rc" -eq 0 ]]; then
    echo "[PASS] $label"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
    bash tools/qa_emit_remediation.sh scene-primitives || true
  fi
  rm -f "$log"
}

check_visual_smoke() {
  local label="Visual smoke (palette + LLM jury when screenshot exists)"
  local log
  log="$(mktemp)"
  set +e
  bash tools/run_visual_smoke_checks.sh >"$log" 2>&1
  local rc=$?
  set -e
  cat "$log"
  if [[ "$rc" -eq 0 ]]; then
    if grep -q '^\[WARN\]' "$log"; then
      echo "[WARN] $label (see above)"
      WARN=$((WARN + 1))
    else
      echo "[PASS] $label"
      PASS=$((PASS + 1))
    fi
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
  fi
  rm -f "$log"
}

check_audio_smoke() {
  local label="Audio smoke (catalog + technical + jury when bgm_village exists)"
  local log
  log="$(mktemp)"
  set +e
  bash tools/run_audio_smoke_checks.sh >"$log" 2>&1
  local rc=$?
  set -e
  cat "$log"
  if [[ "$rc" -eq 0 ]]; then
    if grep -q '^\[WARN\]' "$log"; then
      echo "[WARN] $label (see above)"
      WARN=$((WARN + 1))
    else
      echo "[PASS] $label"
      PASS=$((PASS + 1))
    fi
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
  fi
  rm -f "$log"
}

check_model_smoke() {
  local label="Model smoke (GLB lint + turntable jury when urashima exists)"
  local log
  log="$(mktemp)"
  set +e
  bash tools/run_model_smoke_checks.sh >"$log" 2>&1
  local rc=$?
  set -e
  cat "$log"
  if [[ "$rc" -eq 0 ]]; then
    if grep -q '^\[WARN\]' "$log"; then
      echo "[WARN] $label (see above)"
      WARN=$((WARN + 1))
    else
      echo "[PASS] $label"
      PASS=$((PASS + 1))
    fi
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
  fi
  rm -f "$log"
}

check_optional() {
  local label="$1"
  shift
  set +e
  "$@" >/dev/null 2>&1
  local rc=$?
  set -e
  case "$rc" in
    0) echo "[PASS] $label"; PASS=$((PASS + 1)) ;;
    2) echo "[SKIP] $label"; WARN=$((WARN + 1)) ;;
    *) echo "[FAIL] $label"; FAIL=$((FAIL + 1)) ;;
  esac
}

echo "==> Fresh-rebuild smoke checks"
echo ""

check "R&R compliance (no hand-built scenes)" bash tools/check_rr_compliance.sh
check_story_data
check_optional "Base class registry" python3 tools/validate_base_classes.py
check_optional "Base class compliance" bash tools/check_base_class_compliance.sh
check_optional "GDScript lint (changed)" bash tools/check_gdscript_changed.sh
check_optional "Animation whitelist" python3 tools/check_animation_whitelist.py --phase 1
check_optional "Feel smoke" bash tools/run_feel_smoke_checks.sh
check_scene_visuals
check "Unit tests pass" bash tools/run_unit_tests.sh
check "Dev environment healthy" bash tools/check_dev_environment.sh
check "Acceptance criteria catalog valid" python3 tools/validate_acceptance_criteria.py
MAIN_SCENE="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | cut -d= -f2- | tr -d '"' || true)"
if [[ -z "$MAIN_SCENE" ]]; then
  echo "[SKIP] Boot scene loads — no run/main_scene until GDAI MCP builds first scene"
  WARN=$((WARN + 1))
else
  check "Boot scene loads" godot4 --headless --rendering-driver opengl3 --path game --quit-after 3
fi
check_visual_smoke
check_audio_smoke
check_model_smoke

echo ""
echo "Passed: $PASS | Failed: $FAIL | Warnings: $WARN"
echo ""
echo "Rebuild phases: docs/workflow/IMPLEMENTATION_PLAN.md"
echo "  Phase 1: ruined_village environment vertical slice via GDAI MCP"

exit "$FAIL"
