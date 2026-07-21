#!/usr/bin/env bash
# Tri-state QA gate helpers (docs/qa/ACCEPTANCE_CRITERIA.md global_rules).
# Exit codes for gate commands: 0=PASS, 1=FAIL, 2=SKIP (not applicable).
set -euo pipefail

export GATE_EXIT_PASS=0
export GATE_EXIT_FAIL=1
export GATE_EXIT_SKIP=2

gate_root() {
  if [[ -z "${ROOT:-}" ]]; then
    ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  fi
  printf '%s' "$ROOT"
}

gate_is_game_branch() {
  local root
  root="$(gate_root)"
  [[ -f "${root}/game/project.godot" ]]
}

gate_active_phase() {
  local root phases_file
  root="$(gate_root)"
  phases_file="${root}/game/data/qa/sprint_phases.json"
  if [[ ! -f "$phases_file" ]]; then
    echo "0"
    return
  fi
  python3 - <<PY 2>/dev/null || echo "0"
import json
from pathlib import Path
print(json.loads(Path("${phases_file}").read_text(encoding="utf-8")).get("active_phase", 0))
PY
}

gate_main_scene_set() {
  local root pg ms
  root="$(gate_root)"
  pg="${root}/game/project.godot"
  [[ -f "$pg" ]] || return 1
  ms="$(grep -E '^run/main_scene=' "$pg" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
  [[ -n "$ms" ]]
}

# Hero GLB art assets present yet? The M5 art pipeline lands character/prop GLBs
# under game/assets/models/. Strict GLB-import + animation-whitelist gates only
# make sense once those exist; before then they SKIP (acceptance_criteria.issue_bootstrap).
gate_hero_glbs_present() {
  local root
  root="$(gate_root)"
  [[ -d "${root}/game/assets/models" ]] || return 1
  [[ -n "$(find "${root}/game/assets/models" -type f -name '*.glb' 2>/dev/null | head -1)" ]]
}

# Phase 1 before M5 art: project.godot exists (P1-00 boot shell) but no hero GLBs
# yet, so art/animation gates cannot pass. Distinct from gate_is_phase1_bootstrap,
# which flips off once any run/main_scene (even the boot placeholder) is set.
gate_is_phase1_pre_art() {
  gate_is_game_branch || return 1
  [[ "$(gate_active_phase)" == "1" ]] || return 1
  gate_hero_glbs_present && return 1
  return 0
}

# Phase 1 bootstrap: project.godot exists but no playable main_scene yet (P1-00 / pre-P1-02).
# Set PHASE1_BOOTSTRAP_CI=1 to force bootstrap skip policy (tools/run_bootstrap_ci_checks.sh).
gate_is_phase1_bootstrap() {
  if [[ "${PHASE1_BOOTSTRAP_CI:-}" == "1" ]]; then
    return 0
  fi
  gate_is_game_branch || return 1
  [[ "$(gate_active_phase)" == "1" ]] || return 1
  if gate_main_scene_set; then
    return 1
  fi
  return 0
}

# SKIP is allowed on docs-only main; on game/development most gates must run.
# During phase 1 bootstrap, art/export gates may SKIP (see acceptance_criteria.issue_bootstrap).
gate_skip_is_fail() {
  local gate_id="${1:-}"
  gate_is_game_branch || return 1

  if gate_is_phase1_bootstrap; then
    case "$gate_id" in
      L1_gdscript_lint|L2_glb_import|L2_animation_whitelist|L2_linux_export_smoke|L2_windows_cross_export|L2_boot_headless|L4_integration)
        return 1
        ;;
    esac
  fi

  # Phase 1 with a boot main_scene but no hero GLBs yet: the changed-files
  # gdscript lint is fully covered by the required L1_gdscript_lint_all gate, and
  # the GLB import / animation-whitelist gates need art that has not landed. Allow
  # these to SKIP until M5 art arrives, then they enforce automatically.
  if gate_is_phase1_pre_art; then
    case "$gate_id" in
      L1_gdscript_lint|L2_glb_import|L2_animation_whitelist)
        return 1
        ;;
    esac
  fi

  case "$gate_id" in
    L2_boot_headless)
      # Allowed to skip when run/main_scene unset (early Phase 1).
      return 1
      ;;
    L2_windows_cross_export|L2_linux_export_smoke)
      return 1
      ;;
    L4_integration)
      return 0
      ;;
    *)
      return 0
      ;;
  esac
}

run_tri_gate() {
  local gate_id="$1"
  local label="$2"
  shift 2
  echo ""
  echo "── ${gate_id}: ${label}"
  set +e
  "$@"
  local rc=$?
  set -e
  case "$rc" in
    0)
      echo "[PASS] ${gate_id}"
      PASS=$((PASS + 1))
      ;;
    2)
      if gate_skip_is_fail "$gate_id"; then
        echo "[FAIL] ${gate_id} — SKIP not allowed on game branch (global_rules.skip_is_not_pass)"
        FAIL=$((FAIL + 1))
      else
        echo "[SKIP] ${gate_id} — ${label}"
        SKIP=$((SKIP + 1))
      fi
      ;;
    *)
      echo "[FAIL] ${gate_id}"
      FAIL=$((FAIL + 1))
      ;;
  esac
}

skip_gate() {
  local gate_id="$1"
  local reason="$2"
  echo ""
  if gate_skip_is_fail "$gate_id"; then
    echo "[FAIL] ${gate_id} — SKIP not allowed on game branch: ${reason}"
    FAIL=$((FAIL + 1))
  else
    echo "[SKIP] ${gate_id} — ${reason}"
    SKIP=$((SKIP + 1))
  fi
}
