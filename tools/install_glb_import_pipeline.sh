#!/usr/bin/env bash
# Copy GLB post-import script into game project (game/development).
# See docs/MODEL_QA.md §M2b, tools/godot_templates/editor/glb_toon_post_import.gd
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/tools/godot_templates/editor/glb_toon_post_import.gd"
DEST_DIR="${ROOT}/game/scripts/editor"
DEST="${DEST_DIR}/glb_toon_post_import.gd"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] game/project.godot missing — run on game/development branch"
  echo "       Template stays at tools/godot_templates/editor/glb_toon_post_import.gd"
  exit 0
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST"
echo "[OK] Installed ${DEST}"
echo ""
echo "Next in Godot Editor:"
echo "  1. Select a .glb under game/assets/models/"
echo "  2. Import dock → Scene tab → Advanced"
echo "  3. Post Import Script → res://scripts/editor/glb_toon_post_import.gd"
echo "  4. Reimport"
