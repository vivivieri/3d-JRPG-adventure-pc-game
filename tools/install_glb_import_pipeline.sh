#!/usr/bin/env bash
# Copy GLB post-import + toon shader into game project (game/development).
# See docs/art/MODEL_QA.md §M2b
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_POST="${ROOT}/tools/godot_templates/editor/glb_toon_post_import.gd"
SRC_SHADER="${ROOT}/tools/godot_templates/shaders/toon_base.gdshader"
DEST_EDITOR="${ROOT}/game/scripts/editor"
DEST_SHADER="${ROOT}/game/assets/shaders"
POST_IMPORT_GD="${DEST_EDITOR}/glb_toon_post_import.gd"
TOON_SHADER="${DEST_SHADER}/toon_base.gdshader"
POST_IMPORT_RES="res://scripts/editor/glb_toon_post_import.gd"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] game/project.godot missing — run on game/development branch"
  echo "       Templates stay under tools/godot_templates/"
  exit 2
fi

mkdir -p "$DEST_EDITOR" "$DEST_SHADER"
cp "$SRC_POST" "$POST_IMPORT_GD"
cp "$SRC_SHADER" "$TOON_SHADER"
echo "[OK] Installed ${POST_IMPORT_GD}"
echo "[OK] Installed ${TOON_SHADER}"

# Patch .import sidecars for existing GLBs
patched=0
while IFS= read -r -d '' glb; do
  import_file="${glb}.import"
  [[ -f "$import_file" ]] || continue
  if grep -q 'post_import_script=' "$import_file" 2>/dev/null; then
    sed -i "s|^post_import_script=.*|post_import_script=\"${POST_IMPORT_RES}\"|" "$import_file"
  else
    printf '\npost_import_script="%s"\n' "$POST_IMPORT_RES" >>"$import_file"
  fi
  patched=$((patched + 1))
done < <(find "${ROOT}/game/assets/models" -name '*.glb' -print0 2>/dev/null)

echo ""
echo "[OK] Patched post_import_script on ${patched} .import file(s)"
echo "Reimport GLBs in Godot if materials look stale (Project → Reload Current Project)."
echo "Verify: python3 tools/check_glb_import_scripts.py --strict"
