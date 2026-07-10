#!/usr/bin/env bash
# Start Godot Editor in background for GDAI MCP (when plugin is installed).
# Detached — environment.json start command. No-op if Godot missing.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

if ! command -v godot4 >/dev/null 2>&1; then
  echo "Godot not installed — run bash tools/install_cloud_dev.sh"
  exit 0
fi

PGREP_PATTERN="godot4.*${ROOT}/game"
if pgrep -f "$PGREP_PATTERN" >/dev/null 2>&1; then
  echo "Godot editor already running for this project"
  exit 0
fi

mkdir -p "${ROOT}/.cache"
echo "Starting Godot editor (GDAI MCP: enable plugin + Start in editor panel)..."
nohup godot4 --rendering-driver opengl3 --path "${ROOT}/game" --editor >> "${ROOT}/.cache/godot-editor.log" 2>&1 &

sleep 3
PID="$(pgrep -f "$PGREP_PATTERN" | head -1 || true)"
echo "Godot editor PID: ${PID:-unknown}"
echo "Log: ${ROOT}/.cache/godot-editor.log"
