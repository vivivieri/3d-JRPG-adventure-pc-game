#!/usr/bin/env bash
# Install required extended toolchain (Blender, MCP config for GameLab).
# GameLab API key + Notion OAuth must be configured by user in Cursor Secrets / Integrations.
#
# Usage: bash tools/install_extended_toolchain.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Extended toolchain install"

# --- Blender (required offline 3D pipeline) ---
if command -v blender >/dev/null 2>&1; then
  echo "==> Blender: $(blender --version 2>&1 | head -1)"
else
  echo "==> Installing Blender..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq blender
    echo "==> Blender: $(blender --version 2>&1 | head -1)"
  else
    echo "!! Install Blender manually: https://www.blender.org/download/"
    exit 1
  fi
fi

# --- Godot MCP stack (required) ---
bash "$ROOT/tools/ensure_mcp_stack.sh"

# --- GameLab MCP in .cursor/mcp.json when API key present ---
if [[ -n "${GAMELAB_API_KEY:-}" ]]; then
  echo "==> GAMELAB_API_KEY found — writing gamelab-mcp to .cursor/mcp.json"
  bash "$ROOT/tools/write_mcp_config.sh"
else
  echo "!! GAMELAB_API_KEY not set"
  echo "   1. Sign up: https://gamelabstudio.co/"
  echo "   2. Cursor → Secrets → add GAMELAB_API_KEY"
  echo "   3. Re-run: bash tools/install_extended_toolchain.sh"
fi

# --- Notion ---
if [[ -n "${NOTION_API_KEY:-}" ]]; then
  echo "==> NOTION_API_KEY present (register Notion MCP in Cursor Integrations if not connected)"
else
  echo "!! Notion MCP requires OAuth in Cursor"
  echo "   Cursor Settings → Integrations → Notion → Connect workspace"
fi

# --- ACE-Step prompt sheets ---
if [[ -f "$ROOT/game/data/audio/ace_step_prompts.json" ]]; then
  echo "==> Writing ACE-Step prompt sheets..."
  bash "$ROOT/tools/generate_ai_bgm.sh" --all-prompts 2>/dev/null || true
fi

# --- Procedural audio placeholders ---
if [[ ! -d "$ROOT/game/assets/audio/bgm" ]] || [[ -z "$(ls -A "$ROOT/game/assets/audio/bgm" 2>/dev/null || true)" ]]; then
  echo "==> Generating procedural audio placeholders..."
  python3 "$ROOT/tools/generate_game_audio.py" --all 2>/dev/null || true
fi

echo
echo "==> Extended toolchain status:"
bash "$ROOT/tools/check_extended_toolchain.sh" || true
