#!/usr/bin/env bash
# Static Godot scene style lint — docs/technical/SCENE_STYLE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCENES_DIR="${ROOT}/game/scenes"

if [[ ! -d "$SCENES_DIR" ]]; then
  echo "[SKIP] no game/scenes — scene style runs on game/development only"
  exit 0
fi

FAIL=0
CHECKED=0

fail() {
  echo "[FAIL] $*"
  FAIL=1
}

is_greybox_path() {
  local path="$1"
  [[ "$path" == *"/greybox/"* ]] && return 0
  [[ "$path" == *"/_dev/"* ]] && return 0
  [[ "$path" == *".greybox.tscn" ]] && return 0
  return 1
}

echo "==> Scene style lint (docs/technical/SCENE_STYLE.md)"
echo "    Scanning: ${SCENES_DIR}"
echo ""

while IFS= read -r -d '' tscn; do
  rel="${tscn#"${ROOT}"/}"
  if is_greybox_path "$rel"; then
    echo "[SKIP] greybox: $rel"
    continue
  fi

  base="$(basename "$tscn")"
  if [[ ! "$base" =~ ^[a-z][a-z0-9_]*\.tscn$ ]]; then
    fail "$rel — file name must be snake_case.tscn"
  fi

  if ! head -n 1 "$tscn" | grep -q '^\[gd_scene'; then
    fail "$rel — must start with [gd_scene …] header"
  fi

  if grep -qE 'res://.*/(home|Users|workspace)/' "$tscn" 2>/dev/null; then
    fail "$rel — absolute filesystem path in scene resource"
  fi

  CHECKED=$((CHECKED + 1))
done < <(find "$SCENES_DIR" -name '*.tscn' -print0)

if [[ "$CHECKED" -eq 0 ]]; then
  echo "[WARN] No ship .tscn files under game/scenes/ (greybox-only?)"
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "[FAIL] L1_scene_style — fix scene naming/format issues"
  exit 1
fi

echo "[PASS] L1_scene_style ($CHECKED scene(s) checked)"
exit 0
