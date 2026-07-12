#!/usr/bin/env bash
# Run the game (not editor) in cloud or local GUI environment.
# Requires an explicit scene — all scenes must be built via GDAI MCP first.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

SCENE="${1:-}"

if [[ -z "$SCENE" ]]; then
  echo "Usage: bash tools/run_game.sh res://scenes/<scene>.tscn"
  echo "No default scene — build scenes via GDAI MCP (see game/scenes/README.md)."
  exit 1
fi

if pgrep -f "godot4.*${ROOT}/game" >/dev/null 2>&1; then
  echo "Godot already running for this project. Close it first or use the editor."
  exit 1
fi

echo "Starting Tides of Urashima..."
echo "  Scene: $SCENE"
echo "  DISPLAY: $DISPLAY"
echo ""

exec godot4 --rendering-driver opengl3 --path "${ROOT}/game" "$SCENE"
