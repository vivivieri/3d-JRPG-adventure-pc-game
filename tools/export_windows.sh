#!/usr/bin/env bash
# Export Windows release build. Strips dev-only GDAI MCP autoload/plugin for the export.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

GAME="$ROOT/game"
PROJECT="$GAME/project.godot"
BACKUP="$GAME/project.godot.export-bak"
OUT_DIR="$ROOT/build"
OUT_EXE="$OUT_DIR/TidesOfUrashima.exe"
PRESET="Windows Desktop"

echo "==> Tides of Urashima — Windows export"
echo ""

if ! command -v godot4 >/dev/null 2>&1; then
  echo "[FAIL] godot4 not in PATH. Run: bash tools/install_cloud_dev.sh"
  exit 1
fi

if [[ ! -f "$GAME/export_presets.cfg" ]]; then
  if [[ -f "$GAME/export_presets.cfg.example" ]]; then
    cp "$GAME/export_presets.cfg.example" "$GAME/export_presets.cfg"
    echo "    Created export_presets.cfg from example"
  else
    echo "[FAIL] Missing $GAME/export_presets.cfg.example"
    exit 1
  fi
fi

echo "==> Pre-export checks..."
python3 tools/validate_story_data.py
bash tools/check_asset_compliance.sh || {
  echo "[WARN] Asset compliance reported issues — review before Steam upload"
}

mkdir -p "$OUT_DIR"

echo "==> Stripping dev-only GDAI MCP from project.godot..."
cp "$PROJECT" "$BACKUP"
trap 'mv -f "$BACKUP" "$PROJECT"' EXIT

python3 - "$PROJECT" <<'PY'
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
text = re.sub(r'^GDAIMCPRuntime=.*\n', '', text, flags=re.M)
text = re.sub(
    r'enabled=PackedStringArray\("res://addons/gdai-mcp-plugin-godot/plugin\.cfg"\)',
    'enabled=PackedStringArray()',
    text,
)
path.write_text(text, encoding="utf-8")
print("    Removed GDAIMCPRuntime autoload and editor plugin entry")
PY

echo "==> Exporting $PRESET -> $OUT_EXE"
godot4 --headless --path "$GAME" --export-release "$PRESET" "$OUT_EXE"

echo ""
echo "==> Export complete: $OUT_EXE"
ls -lh "$OUT_EXE"
echo ""
echo "Next: add steam_api64.dll + godotsteam.windows.dll for Steam depot (see steam/GODOTSTEAM_SETUP.md)"
