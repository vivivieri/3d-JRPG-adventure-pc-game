#!/usr/bin/env bash
# L3 gate (CI): if ship scenes or run/main_scene change in the diff, .gdai_built must update too.
# Full L3 F5 viewport verify remains agent-local (editor + GDAI MCP).
# See docs/ci-cd/CI.md, docs/cheat-sheets/CONTROLS_CHEATSHEET.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCENES_DIR="${ROOT}/game/scenes"
MARKER="${SCENES_DIR}/.gdai_built"
FAIL=0

fail() {
  echo "[FAIL] $*"
  FAIL=1
}

ok() {
  echo "[OK]   $*"
}

is_allowed_scene_path() {
  local rel="$1"
  [[ "$rel" == *"/greybox/"* ]] && return 0
  [[ "$rel" == *"/_dev/"* ]] && return 0
  [[ "$rel" == *".greybox.tscn" ]] && return 0
  return 1
}

resolve_diff_range() {
  DIFF_BASE=""
  DIFF_HEAD="HEAD"

  if [[ -n "${GITHUB_EVENT_NAME:-}" ]]; then
    case "$GITHUB_EVENT_NAME" in
      pull_request)
        DIFF_BASE="${GITHUB_BASE_SHA:-}"
        DIFF_HEAD="${GITHUB_SHA:-HEAD}"
        ;;
      push)
        DIFF_BASE="${GITHUB_EVENT_BEFORE:-}"
        DIFF_HEAD="${GITHUB_SHA:-HEAD}"
        if [[ "$DIFF_BASE" == "0000000000000000000000000000000000000000" ]]; then
          DIFF_BASE=""
        fi
        ;;
    esac
  fi

  if [[ -z "$DIFF_BASE" ]]; then
    if git rev-parse origin/game/development >/dev/null 2>&1; then
      DIFF_BASE="$(git merge-base HEAD origin/game/development 2>/dev/null || true)"
    fi
    if [[ -z "$DIFF_BASE" ]]; then
      if git rev-parse HEAD~1 >/dev/null 2>&1; then
        DIFF_BASE="HEAD~1"
      else
        DIFF_BASE=""
      fi
    fi
  fi
}

echo "==> L3 GDAI built marker check (CI subset)"
echo ""

if [[ ! -d "$SCENES_DIR" ]]; then
  ok "No game/scenes/ — skip (docs-only baseline)"
  exit 0
fi

resolve_diff_range

if [[ -z "$DIFF_BASE" ]]; then
  ok "No diff base — first commit or shallow clone; skip L3 diff gate"
  exit 0
fi

if ! git diff --name-only "$DIFF_BASE" "$DIFF_HEAD" >/dev/null 2>&1; then
  fail "Cannot diff ${DIFF_BASE}..${DIFF_HEAD}"
  echo ""
  exit 1
fi

SCENE_CHANGED=0
MARKER_CHANGED=0
MAIN_SCENE_CHANGED=0

while IFS= read -r path; do
  [[ -z "$path" ]] && continue
  if [[ "$path" == "game/scenes/.gdai_built" ]]; then
    MARKER_CHANGED=1
    continue
  fi
  if [[ "$path" == "game/project.godot" ]]; then
    if git diff "$DIFF_BASE" "$DIFF_HEAD" -- "$path" | grep -qE '^\+.*run/main_scene='; then
      MAIN_SCENE_NOW="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
      if [[ -n "$MAIN_SCENE_NOW" ]]; then
        MAIN_SCENE_CHANGED=1
      fi
    fi
    continue
  fi
  if [[ "$path" == game/scenes/* ]] && [[ "$path" == *.tscn ]]; then
    if is_allowed_scene_path "$path"; then
      echo "[SKIP] greybox/dev change: $path"
    else
      SCENE_CHANGED=1
      echo "[DIFF] ship scene: $path"
    fi
  fi
done < <(git diff --name-only "$DIFF_BASE" "$DIFF_HEAD")

echo ""
echo "Diff range: ${DIFF_BASE}..${DIFF_HEAD}"

if [[ "$SCENE_CHANGED" -eq 0 && "$MAIN_SCENE_CHANGED" -eq 0 ]]; then
  ok "No ship scene or main_scene changes — L3 marker diff not required"
  exit 0
fi

if [[ "$MARKER_CHANGED" -eq 0 ]]; then
  fail "Ship scene or main_scene changed but game/scenes/.gdai_built was not updated"
  fail "Builder must run GDAI F5 and refresh .gdai_built (see game/scenes/README.md)"
else
  ok ".gdai_built updated in same diff"
fi

if [[ ! -f "$MARKER" ]]; then
  fail "Missing game/scenes/.gdai_built after scene change"
else
  if ! grep -qE '^verified_f5=true' "$MARKER" 2>/dev/null; then
    fail "game/scenes/.gdai_built must include verified_f5=true after GDAI F5"
  else
    ok "verified_f5=true present"
  fi
  if ! grep -qE '^verified_at=' "$MARKER" 2>/dev/null; then
    fail "game/scenes/.gdai_built must include verified_at= timestamp"
  else
    ok "verified_at present"
  fi
  MAIN_SCENE="$(grep -E '^run/main_scene=' game/project.godot 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
  if [[ -n "$MAIN_SCENE" ]]; then
    MARKED_SCENE="$(grep -E '^main_scene=' "$MARKER" 2>/dev/null | head -1 | cut -d= -f2- || true)"
    if [[ "$MARKED_SCENE" != "$MAIN_SCENE" ]]; then
      fail "main_scene mismatch: project.godot=$MAIN_SCENE vs .gdai_built=$MARKED_SCENE"
    else
      ok "main_scene matches project.godot"
    fi
  fi
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "L3_gdai_built: FAILED"
  echo ""
  echo "Remediation:"
  echo "  1. bash tools/ensure_mcp_stack.sh && bash tools/check_mcp_ready.sh"
  echo "  2. Build/edit scenes via GDAI MCP — F5 verify"
  echo "  3. Update game/scenes/.gdai_built (verified_f5=true, verified_at, main_scene)"
  exit 1
fi

echo "L3_gdai_built: PASS"
exit 0
