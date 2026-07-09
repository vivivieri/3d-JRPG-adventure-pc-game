#!/usr/bin/env bash
# Capture in-game screenshots without manual input (cloud-safe).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GODOT="${GODOT_BIN:-$ROOT/.godot-sdk/Godot_v4.3-stable_linux.x86_64}"
GAME="$ROOT/game"
OUT="${SCREENSHOT_DIR:-/opt/cursor/artifacts/screenshots}"
WORKSPACE_OUT="$ROOT/steam/screenshots-capture"

mkdir -p "$OUT" "$WORKSPACE_OUT"
export DISPLAY="${DISPLAY:-:1}"
export SCREENSHOT_DIR="$OUT"
export SCREENSHOT_MODE="1"

if [[ ! -x "$GODOT" ]]; then
  echo "Godot not found at $GODOT"
  exit 1
fi

echo "Importing assets..."
"$GODOT" --headless --path "$GAME" --import >/dev/null 2>&1 || true

echo "Capturing screenshots to $OUT ..."
"$GODOT" --path "$GAME" \
  --resolution 1280x720 \
  --rendering-driver opengl3 \
  --audio-driver Dummy \
  -s res://scripts/debug/screenshot_capture.gd

cp -f "$OUT"/*.png "$WORKSPACE_OUT/" 2>/dev/null || true
echo "Done. Files:"
ls -la "$OUT"/*.png
