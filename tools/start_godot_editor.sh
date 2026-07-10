#!/usr/bin/env bash
# Start Godot editor with GDAI MCP project (cloud-safe, tmux-backed).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GODOT="${GODOT_BIN:-$ROOT/.godot-sdk/Godot_v4.3-stable_linux.x86_64}"
GAME="$ROOT/game"
SESSION_NAME="godot-gdai-editor"
export DISPLAY="${DISPLAY:-:1}"

if [[ ! -x "$GODOT" ]]; then
  "$ROOT/tools/install_gdai_mcp.sh" || true
fi

if [[ ! -x "$GODOT" ]]; then
  echo "Godot not found at $GODOT" >&2
  exit 1
fi

"$GODOT" --headless --path "$GAME" --import >/dev/null 2>&1 || true

if tmux -f /exec-daemon/tmux.portal.conf has-session -t "=$SESSION_NAME" 2>/dev/null; then
  echo "Godot editor session '$SESSION_NAME' already running"
else
  tmux -f /exec-daemon/tmux.portal.conf new-session -d -s "$SESSION_NAME" -c "$ROOT" -- \
    "$GODOT" --path "$GAME" --editor --rendering-driver opengl3
  echo "Started Godot editor in tmux session: $SESSION_NAME"
fi

echo "Attach: tmux -f /exec-daemon/tmux.portal.conf attach -t $SESSION_NAME"
