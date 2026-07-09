#!/usr/bin/env bash
# Run Tides of Urashima in the cloud environment (OpenGL software renderer).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GODOT="${GODOT_BIN:-$ROOT/.godot-sdk/Godot_v4.3-stable_linux.x86_64}"
GAME="$ROOT/game"

if [[ ! -x "$GODOT" ]]; then
  echo "Godot not found. Run ./tools/export_windows.sh first to download Godot 4.3."
  exit 1
fi

export DISPLAY="${DISPLAY:-:1}"

echo "Importing assets (if needed)..."
"$GODOT" --headless --path "$GAME" --import >/dev/null 2>&1 || true

echo "Starting Tides of Urashima (OpenGL, 1280x720)..."
echo "Controls: WASD move, E interact, Tab menu, Enter confirm, Esc cancel"
exec "$GODOT" --path "$GAME" --resolution 1280x720 --rendering-driver opengl3 "$@"
