#!/usr/bin/env bash
# Export Linux x86_64 release build. Strips dev-only GDAI MCP autoload/plugin for export.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=export_lib.sh
source "${ROOT}/tools/export_lib.sh"

GAME="$ROOT/game"
PROJECT="$GAME/project.godot"
BACKUP="$GAME/project.godot.export-bak"
PRESETS_BAK="$GAME/export_presets.cfg.export-bak"
OUT_DIR="$ROOT/build"
OUT_BIN="$OUT_DIR/TidesOfUrashima.x86_64"
PRESET="Linux"

echo "==> Tides of Urashima — Linux export"
echo ""

export_godot_env "$ROOT"
export_require_godot

if [[ ! -f "$PROJECT" ]]; then
  echo "[FAIL] missing $PROJECT — bootstrap on game/development first (P1-00)"
  exit 1
fi

export_ensure_presets "$GAME"
export_pre_checks
mkdir -p "$OUT_DIR"

export_strip_dev_plugins_begin "$PROJECT" "$BACKUP"
export_ship_protection_begin "$GAME" "$PROJECT" "$PRESETS_BAK"
trap 'export_ship_protection_restore "$GAME" "$PRESETS_BAK"; export_strip_dev_plugins_restore "$PROJECT" "$BACKUP"' EXIT

echo "==> Exporting $PRESET -> $OUT_BIN"
godot4 --headless --path "$GAME" --export-release "$PRESET" "$OUT_BIN"

chmod +x "$OUT_BIN"
echo ""
echo "==> Export complete: $OUT_BIN"
ls -lh "$OUT_BIN"
echo ""
echo "Next: bash tools/prepare_steam_depot.sh --platform linux"
