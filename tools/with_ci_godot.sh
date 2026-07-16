#!/usr/bin/env bash
# Run a command with MCP autoloads stripped from project.godot when addons are absent.
# Restores project.godot on exit. No-op when all MCP addons are installed.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${ROOT}/game/project.godot"
BACKUP="${PROJECT}.ci.bak"
STRIPPED=0

restore_project() {
  if [[ "$STRIPPED" -eq 1 && -f "$BACKUP" ]]; then
    mv -f "$BACKUP" "$PROJECT"
    STRIPPED=0
  fi
}

trap restore_project EXIT

MCP_PRESENT=1
[[ -f "${ROOT}/game/addons/gdai-mcp-plugin-godot/gdai_mcp_runtime.gd" ]] || MCP_PRESENT=0
[[ -f "${ROOT}/game/addons/godot_mcp/mcp_screenshot_service.gd" ]] || MCP_PRESENT=0

if [[ "$MCP_PRESENT" -eq 0 && -f "$PROJECT" ]]; then
  cp "$PROJECT" "$BACKUP"
  python3 "${ROOT}/tools/godot_strip_dev_plugins.py" strip "$PROJECT"
  STRIPPED=1
  echo "[OK]   Stripped MCP autoloads for CI (addons absent)"
fi

if [[ $# -eq 0 ]]; then
  echo "Usage: with_ci_godot.sh <command> [args...]"
  exit 1
fi

"$@"
