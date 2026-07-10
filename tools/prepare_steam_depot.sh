#!/usr/bin/env bash
# Bundle Windows Steam depot files for local testing or upload prep.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEPOT="$ROOT/build/steam_depot"
EXE="$ROOT/build/TidesOfUrashima.exe"
STEAM_ADDON="$ROOT/game/addons/godotsteam/win64"

echo "==> Preparing Steam depot layout"
echo "    Output: $DEPOT"
echo ""

if [[ ! -f "$EXE" ]]; then
  echo "[INFO] Build exe missing — running export..."
  bash "$ROOT/tools/export_windows.sh"
fi

if [[ ! -f "$STEAM_ADDON/steam_api64.dll" ]]; then
  echo "[FAIL] GodotSteam win64 not installed. Run: bash tools/install_godotsteam.sh"
  echo "       Then download/extract GodotSteam 4.15 for Godot 4.3."
  exit 1
fi

mkdir -p "$DEPOT"
cp "$EXE" "$DEPOT/TidesOfUrashima.exe"
cp "$STEAM_ADDON/steam_api64.dll" "$DEPOT/"
cp "$STEAM_ADDON/libgodotsteam.windows.template_release.x86_64.dll" "$DEPOT/"

# Optional dev file — remove before production depot upload
if [[ ! -f "$DEPOT/steam_appid.txt" ]]; then
  echo "480" > "$DEPOT/steam_appid.txt"
  echo "[INFO] Created steam_appid.txt with Spacewar test app id 480 (replace with your Steam App ID)"
fi

echo ""
echo "==> Depot ready:"
ls -lh "$DEPOT"
echo ""
echo "Copy $DEPOT/ to a Windows PC to test with Steam client running."
echo "Replace steam_appid.txt with your real App ID before Steam upload."
