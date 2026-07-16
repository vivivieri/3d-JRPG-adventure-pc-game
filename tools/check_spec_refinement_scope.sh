#!/usr/bin/env bash
# Spec refinement mode — block ship implementation paths on main during design/spec work.
# See docs/SPEC_FIRST_DEVELOPMENT.md §10
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0
fail() { echo "[FAIL] $*"; FAIL=1; }
ok() { echo "[OK]   $*"; }

echo "==> Spec refinement scope check (main branch policy)"
echo ""

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [[ "$BRANCH" != "main" && "${CI_FORCE_SPEC_SCOPE:-0}" != "1" ]]; then
  ok "skipped — branch=$BRANCH (main-only gate; set CI_FORCE_SPEC_SCOPE=1 to force)"
  exit 0
fi

is_allowed_game_path() {
  local rel="$1"
  [[ "$rel" == "game/README.md" ]] && return 0
  [[ "$rel" == game/data/* ]] && return 0
  [[ "$rel" == game/locale/* ]] && return 0
  return 1
}

is_allowed_tools_gd() {
  local rel="$1"
  [[ "$rel" == tools/godot_templates/* ]] && return 0
  return 1
}

FORBIDDEN_GAME_PREFIXES=(
  "game/project.godot"
  "game/scripts/"
  "game/scenes/"
  "game/shaders/"
  "game/assets/"
  "game/tests/"
  "game/addons/"
)

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  if is_allowed_game_path "$rel"; then
    continue
  fi
  for prefix in "${FORBIDDEN_GAME_PREFIXES[@]}"; do
    if [[ "$rel" == "$prefix" || "$rel" == ${prefix}* ]]; then
      fail "main spec refinement: forbidden tracked path $rel"
      continue 2
    fi
  done
  if [[ "$rel" == game/* ]]; then
    fail "main spec refinement: forbidden path $rel (ship implementation belongs on game/development)"
  fi
done < <(git ls-files 'game/')

if [[ "$FAIL" -eq 0 ]]; then
  ok "tracked game/ paths are spec/data only (data/, locale/, README)"
fi

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  if is_allowed_tools_gd "$rel"; then
    continue
  fi
  fail "main spec refinement: GDScript in tools/ not allowed ($rel)"
done < <(git ls-files 'tools/*.gd' 'tools/**/*.gd')

if [[ "$FAIL" -eq 0 ]]; then
  ok "tools/ GDScript limited to godot_templates/ reference"
fi

echo ""
if [[ "$FAIL" -ne 0 ]]; then
  echo "Spec refinement scope: FAILED"
  echo "During design/spec work on main, change only:"
  echo "  docs/, game/data/, game/locale/, tools/*.py (validators + *_lib.py reference)"
  echo "Implementation: PR to game/development after PM dispatch + run_agent_session_gate.sh"
  echo "Policy: docs/SPEC_FIRST_DEVELOPMENT.md §10"
  exit 1
fi

echo "Spec refinement scope: PASSED"
exit 0
