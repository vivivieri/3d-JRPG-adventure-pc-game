#!/usr/bin/env bash
# Enforce GodotPrompter + GDAI MCP role rules (.cursorrules §0, docs/agents/MCP_STACK.md).
# Fails if hand-edited ship scenes are committed or main_scene lacks GDAI verification.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCENES_DIR="${ROOT}/game/scenes"
PROJECT_GODOT="${ROOT}/game/project.godot"
GDAI_MARKER="${SCENES_DIR}/.gdai_built"

FAIL=0

fail() {
  echo "[FAIL] $*"
  FAIL=1
}

ok() {
  echo "[OK]   $*"
}

marker_verified() {
  [[ -f "$GDAI_MARKER" ]] || return 1
  grep -qE '^verified_f5=true' "$GDAI_MARKER" 2>/dev/null
}

is_allowed_scene_path() {
  local rel="$1"
  [[ "$rel" == *"/greybox/"* ]] && return 0
  [[ "$rel" == *"/_dev/"* ]] && return 0
  [[ "$rel" == *".greybox.tscn" ]] && return 0
  return 1
}

echo "==> R&R compliance check (.cursorrules §0 — GDAI builds scenes)"
echo ""

if [[ ! -d "$SCENES_DIR" ]]; then
  fail "Missing ${SCENES_DIR}"
  echo ""
  echo "R&R compliance: FAILED"
  exit 1
fi

# --- 1. Ship .tscn require valid GDAI marker ---
SHIP_TSCN=()
while IFS= read -r -d '' tscn; do
  rel="${tscn#${ROOT}/}"
  if is_allowed_scene_path "$rel"; then
    echo "[SKIP] greybox/dev: $rel"
    continue
  fi
  SHIP_TSCN+=("$rel")
done < <(find "$SCENES_DIR" -name '*.tscn' -print0 2>/dev/null)

if [[ ${#SHIP_TSCN[@]} -gt 0 ]]; then
  if ! marker_verified; then
    for rel in "${SHIP_TSCN[@]}"; do
      fail "Ship scene without GDAI verification: $rel (missing or incomplete ${GDAI_MARKER#${ROOT}/})"
    done
  else
    for rel in "${SHIP_TSCN[@]}"; do
      ok "GDAI-verified ship scene: $rel"
    done
  fi
fi

# --- 2. main_scene must match .gdai_built when set ---
MAIN_SCENE=""
if [[ -f "$PROJECT_GODOT" ]]; then
  MAIN_SCENE="$(grep -E '^run/main_scene=' "$PROJECT_GODOT" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
fi

if [[ -n "$MAIN_SCENE" ]]; then
  if ! marker_verified; then
    fail "project.godot sets run/main_scene=$MAIN_SCENE but ${GDAI_MARKER#${ROOT}/} is missing or unverified"
  else
    MARKED_SCENE="$(grep -E '^main_scene=' "$GDAI_MARKER" 2>/dev/null | head -1 | cut -d= -f2- || true)"
    if [[ -z "$MARKED_SCENE" ]]; then
      fail "${GDAI_MARKER#${ROOT}/} missing main_scene= line"
    elif [[ "$MARKED_SCENE" != "$MAIN_SCENE" ]]; then
      fail "main_scene mismatch: project.godot=$MAIN_SCENE vs .gdai_built=$MARKED_SCENE"
    else
      ok "main_scene verified by GDAI marker: $MAIN_SCENE"
    fi
  fi
else
  ok "No run/main_scene set (design-phase baseline)"
fi

# --- 3. Marker without scenes is suspicious but allowed during transition ---
if marker_verified && [[ ${#SHIP_TSCN[@]} -eq 0 && -z "$MAIN_SCENE" ]]; then
  echo "[WARN] .gdai_built exists but no ship .tscn / main_scene — remove stale marker"
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "R&R compliance: FAILED"
  echo ""
  echo "Remediation:"
  echo "  1. bash tools/ensure_mcp_stack.sh"
  echo "  2. Build scenes in Godot via GDAI MCP (godot-mcp) — not Cursor file edits"
  echo "  3. F5 playtest in editor"
  echo "  4. Write game/scenes/.gdai_built (see game/scenes/README.md)"
  echo "Docs: .cursorrules §0, docs/agents/MCP_STACK.md, docs/agents/GDAI_CLOUD_SETUP.md"
  exit 1
fi

echo "R&R compliance: PASS"
exit 0
