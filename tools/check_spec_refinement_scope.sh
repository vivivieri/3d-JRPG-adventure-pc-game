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

# Paths allowed under game/ on main (spec + data only)
is_allowed_game_path() {
  local rel="$1"
  [[ "$rel" == "game/README.md" ]] && return 0
  [[ "$rel" == game/data/* ]] && return 0
  [[ "$rel" == game/locale/* ]] && return 0
  return 1
}

# Scan tracked files under game/ — anything outside allowlist is a violation
while IFS= read -r -d '' f; do
  rel="${f#${ROOT}/}"
  if is_allowed_game_path "$rel"; then
    continue
  fi
  fail "main spec refinement: forbidden path $rel (ship implementation belongs on game/development)"
done < <(find "${ROOT}/game" -type f ! -path '*/.git/*' -print0 2>/dev/null)

# Explicit forbidden roots even if empty
for forbidden in \
  "${ROOT}/game/project.godot" \
  "${ROOT}/game/scripts" \
  "${ROOT}/game/scenes" \
  "${ROOT}/game/shaders" \
  "${ROOT}/game/assets" \
  "${ROOT}/game/tests" \
  "${ROOT}/game/addons"
do
  if [[ -e "$forbidden" ]]; then
    rel="${forbidden#${ROOT}/}"
    fail "main spec refinement: $rel must not exist on main"
  fi
done

if [[ "$FAIL" -eq 0 ]]; then
  ok "game/ contains only spec/data paths (data/, locale/, README)"
fi

# tools/ — allow validators + reference libs; forbid ship GDScript
while IFS= read -r -d '' f; do
  rel="${f#${ROOT}/}"
  if [[ "$rel" == *.gd ]]; then
    fail "main spec refinement: GDScript in tools/ not allowed ($rel)"
  fi
done < <(find "${ROOT}/tools" -name '*.gd' -print0 2>/dev/null)

if [[ "$FAIL" -eq 0 ]]; then
  ok "tools/ has no .gd files"
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
