#!/usr/bin/env bash
# Tri-state QA gate helpers (docs/ACCEPTANCE_CRITERIA.md global_rules).
# Exit codes for gate commands: 0=PASS, 1=FAIL, 2=SKIP (not applicable).
set -euo pipefail

GATE_EXIT_PASS=0
GATE_EXIT_FAIL=1
GATE_EXIT_SKIP=2

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

# SKIP is allowed on docs-only main; on game/development most gates must run.
gate_skip_is_fail() {
  local gate_id="${1:-}"
  gate_is_game_branch || return 1
  case "$gate_id" in
    L2_boot_headless)
      # Still allowed to skip when run/main_scene unset (early Phase 1).
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
