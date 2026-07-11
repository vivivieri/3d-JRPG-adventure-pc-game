#!/usr/bin/env bash
# Report status of full required toolchain (Godot MCP + extended tools).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERR=0
OK=0

check_ok() { echo "[OK]   $1"; OK=$((OK + 1)); }
check_fail() { echo "[FAIL] $1"; ERR=$((ERR + 1)); }

echo "Extended toolchain check — $ROOT"
echo

# Godot MCP plugins (delegate)
bash "$ROOT/tools/check_dev_environment.sh" || ERR=$((ERR + 1))

echo "--- Extended layers ---"

if command -v blender >/dev/null 2>&1; then
  check_ok "Blender installed ($(blender --version 2>&1 | head -1))"
else
  check_fail "Blender not installed — bash tools/install_extended_toolchain.sh"
fi

if [[ -n "${GAMELAB_API_KEY:-}" ]]; then
  check_ok "GAMELAB_API_KEY secret set"
else
  check_fail "GAMELAB_API_KEY not set — https://gamelabstudio.co/ → Cursor Secrets"
fi

if grep -q '"gamelab-mcp"' "$ROOT/.cursor/mcp.json" 2>/dev/null; then
  check_ok "gamelab-mcp in .cursor/mcp.json"
else
  check_fail "gamelab-mcp missing from .cursor/mcp.json (set GAMELAB_API_KEY and re-run install)"
fi

# Notion — cannot verify OAuth from shell; check env or instruct
if [[ -n "${NOTION_API_KEY:-}" ]]; then
  check_ok "NOTION_API_KEY secret set"
else
  check_fail "Notion MCP — connect in Cursor Integrations (OAuth)"
fi

if [[ -f "$ROOT/game/assets/audio/bgm/menu_theme.ogg" ]] 2>/dev/null || \
   ls "$ROOT/game/assets/audio/bgm/"*.ogg >/dev/null 2>&1; then
  check_ok "Procedural audio placeholders present"
else
  check_fail "Audio placeholders missing — python3 tools/generate_game_audio.py --all"
fi

echo
echo "  ACE-Step 1.5 — bash tools/install_ace_step.sh (local GPU, MIT)"
echo "  Free cloud mood preview only: AIVA free tier (non-commercial, do not ship)"
echo "  Blender AI Render addon — install inside Blender (free OSS)"

echo
echo "Passed: $OK | Failed: $ERR"
exit "$ERR"
