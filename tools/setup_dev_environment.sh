#!/usr/bin/env bash
# Create Godot project folder structure and verify dev tools.
# Run from repo root: bash tools/setup_dev_environment.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Tides of Urashima — dev environment setup"
echo "    Root: $ROOT"
echo

# --- Directory layout (docs/ENVIRONMENT_KITS.md, docs/ART_DIRECTION.md) ---
DIRS=(
  game/assets/fonts
  game/assets/models/characters
  game/assets/models/environment/shared
  game/assets/models/environment/beach_shore
  game/assets/models/environment/ruined_village
  game/assets/models/environment/tidal_caves
  game/assets/models/environment/dragon_palace_gate
  game/assets/models/items
  game/assets/shaders
  game/assets/textures/zones
  game/assets/ui
  game/addons
  game/locale
  game/scenes/world
  game/scenes/ui
  game/scenes/combat
  game/scripts/core
  game/scripts/combat
  game/scripts/narrative
  game/scripts/player
  game/scripts/ui
  game/scripts/world
  game/scripts/shaders
  game/environments
  build
  .cursor
)

for d in "${DIRS[@]}"; do
  mkdir -p "$d"
done

# Place .gitkeep only in empty leaf dirs (skip if dir already has files)
while IFS= read -r -d '' d; do
  if [[ -z "$(find "$d" -mindepth 1 -maxdepth 1 ! -name '.gitkeep' -print -quit)" ]]; then
    touch "$d/.gitkeep"
  fi
done < <(find game/assets game/scenes game/scripts game/environments game/locale game/addons -type d -print0 2>/dev/null)

echo "==> Created project directories"

# --- uv (GDAI MCP bridge) ---
if command -v uv >/dev/null 2>&1; then
  echo "==> uv: $(uv --version)"
else
  echo "!! uv not found — required for GDAI MCP"
  echo "   Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# --- Godot 4.3+ ---
GODOT=""
for cmd in godot4 godot Godot; do
  if command -v "$cmd" >/dev/null 2>&1; then
    GODOT="$cmd"
    break
  fi
done

if [[ -n "$GODOT" ]]; then
  echo "==> Godot: $($GODOT --version 2>&1 | head -1)"
else
  echo "!! Godot 4.3+ not in PATH"
  echo "   Download: https://godotengine.org/download"
  echo "   Open: $ROOT/game/project.godot"
fi

# --- Python validators (already on main) ---
if command -v python3 >/dev/null 2>&1; then
  echo "==> Validating story data..."
  python3 tools/validate_story_data.py
else
  echo "!! python3 not found"
fi

# --- MCP config template ---
if [[ ! -f .cursor/mcp.json ]] && [[ -f .cursor/mcp.json.example ]]; then
  echo "==> MCP: copy .cursor/mcp.json.example → .cursor/mcp.json and set gdai path"
else
  echo "==> MCP: see .cursor/mcp.json.example"
fi

# --- GDAI plugin reminder ---
if [[ ! -d game/addons/gdai-mcp-plugin-godot ]]; then
  echo "!! GDAI MCP plugin not installed (dev-only, gitignored)"
  echo "   See: game/addons/README.md + docs/GDAI_CLOUD_SETUP.md"
fi

# --- Export preset (gitignored locally; copy from example) ---
if [[ ! -f game/export_presets.cfg ]] && [[ -f game/export_presets.cfg.example ]]; then
  cp game/export_presets.cfg.example game/export_presets.cfg
  echo "==> Created game/export_presets.cfg from example"
fi

echo
echo "==> Setup complete."
echo "    1. Install Godot 4.3+ and open game/project.godot"
echo "    2. Install GDAI MCP plugin → game/addons/gdai-mcp-plugin-godot/"
echo "    3. Configure .cursor/mcp.json from .cursor/mcp.json.example"
echo "    4. Ship build: bash tools/export_windows.sh"
echo "    5. Workflow: GodotPrompter (plan) → GDAI MCP (editor) per .cursorrules"
