#!/usr/bin/env bash
# Report status of full toolchain (Godot MCP P0 + extended art/audio layers).
# GameLab and Notion are WARN (not FAIL) — see docs/ART_AUTOMATION_PIPELINE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERR=0
WARN=0
OK=0

check_ok() { echo "[OK]   $1"; OK=$((OK + 1)); }
check_warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }
check_fail() { echo "[FAIL] $1"; ERR=$((ERR + 1)); }

echo "Extended toolchain check — $ROOT"
echo

# Godot MCP plugins (delegate) — P0 failures exit non-zero from child
bash "$ROOT/tools/check_dev_environment.sh" || ERR=$((ERR + 1))

echo "--- Extended layers (tiered) ---"

if command -v blender >/dev/null 2>&1; then
  check_ok "Blender installed ($(blender --version 2>&1 | head -1))"
else
  check_warn "Blender not installed — bash tools/install_extended_toolchain.sh (hero 3D pipeline)"
fi

if [[ -n "${GAMELAB_API_KEY:-}" ]]; then
  check_ok "GAMELAB_API_KEY secret set"
else
  check_warn "GAMELAB_API_KEY not set — UI art via GameLab unavailable; use ComfyUI/procedural fallbacks"
fi

if grep -q '"gamelab-mcp"' "$ROOT/.cursor/mcp.json" 2>/dev/null; then
  check_ok "gamelab-mcp in .cursor/mcp.json"
else
  check_warn "gamelab-mcp missing — zone path: ComfyUI/Material Maker; UI: procedural placeholders"
fi

# Notion — optional
if [[ -n "${NOTION_API_KEY:-}" ]]; then
  check_ok "NOTION_API_KEY secret set"
else
  check_warn "Notion MCP optional — use docs/ + game/data/ if not connected"
fi

if [[ -f "$ROOT/tools/palette_remap.py" ]]; then
  check_ok "palette_remap.py present"
else
  check_warn "palette_remap.py missing — post-gen palette enforcement unavailable"
fi

if [[ -f "$ROOT/game/assets/audio/bgm/menu_theme.ogg" ]] 2>/dev/null || \
   ls "$ROOT/game/assets/audio/bgm/"*.ogg >/dev/null 2>&1; then
  check_ok "Procedural audio placeholders present"
else
  check_fail "Audio placeholders missing — python3 tools/generate_game_audio.py --all"
fi

echo
echo "  ACE-Step 1.5 — bash tools/install_ace_step.sh (local GPU, MIT)"
echo "  ComfyUI / Material Maker — zone NPR albedos (offline)"
echo "  Meshy / Tripo / Rodin — hero 3D (service ToS)"

echo
echo "Passed: $OK | Warnings: $WARN | Failed: $ERR"
exit "$ERR"
