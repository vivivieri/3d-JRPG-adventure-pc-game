#!/usr/bin/env bash
# Static visual lint: banned primitive meshes and ship-forbidden assets in .tscn.
# See docs/VISUAL_QA.md — catches BoxMesh placeholders before they spread.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCENES_DIR="${ROOT}/game/scenes"
FAIL=0
CHECKED=0

# Primitive mesh types banned in player-facing ship scenes.
BANNED_MESH_RE='BoxMesh|CapsuleMesh|CylinderMesh|SphereMesh|PrismMesh|QuadMesh'
# Kenney castle kit — European read; dev greybox only.
BANNED_ASSET_RE='models/castle/|kenney.*castle|Castle Kit'

is_greybox_path() {
  local path="$1"
  [[ "$path" == *"/greybox/"* ]] && return 0
  [[ "$path" == *"/_dev/"* ]] && return 0
  [[ "$path" == *".greybox.tscn" ]] && return 0
  return 1
}

echo "==> Scene visual lint (docs/VISUAL_QA.md)"
echo "    Scanning: ${SCENES_DIR}"
echo ""

if [[ ! -d "$SCENES_DIR" ]]; then
  echo "[FAIL] Missing ${SCENES_DIR}"
  exit 1
fi

while IFS= read -r -d '' tscn; do
  rel="${tscn#${ROOT}/}"
  if is_greybox_path "$rel"; then
    echo "[SKIP] greybox: $rel"
    continue
  fi
  CHECKED=$((CHECKED + 1))
  if rg -n -i "$BANNED_MESH_RE" "$tscn" >/tmp/scene_visual_lint.txt 2>/dev/null; then
    echo "[FAIL] $rel — banned primitive mesh:"
    sed 's/^/         /' /tmp/scene_visual_lint.txt
    FAIL=$((FAIL + 1))
  fi
  if rg -n -i "$BANNED_ASSET_RE" "$tscn" >/tmp/scene_visual_lint.txt 2>/dev/null; then
    echo "[FAIL] $rel — banned Kenney castle / European kit reference:"
    sed 's/^/         /' /tmp/scene_visual_lint.txt
    FAIL=$((FAIL + 1))
  fi
done < <(find "$SCENES_DIR" -name '*.tscn' -print0)

if [[ "$CHECKED" -eq 0 ]]; then
  echo "[WARN] No ship .tscn files found under game/scenes/ (greybox-only?)"
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "Scene visual lint: FAILED ($FAIL issue(s) in $CHECKED scene(s))"
  echo "Fix: replace primitives with NPR meshes per docs/ART_AUTOMATION_PIPELINE.md"
  exit 1
fi

echo "Scene visual lint: PASS ($CHECKED scene(s) checked)"
exit 0
