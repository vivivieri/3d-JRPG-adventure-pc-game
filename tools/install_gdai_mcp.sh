#!/usr/bin/env bash
# Install prerequisites for GDAI MCP in cloud/local environments.
# The commercial plugin zip must be supplied by the license holder.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_DIR="$ROOT/game/addons/gdai-mcp-plugin-godot"
GODOT_SDK="${GODOT_SDK:-$ROOT/.godot-sdk}"
GODOT_BIN="${GODOT_BIN:-$GODOT_SDK/Godot_v4.3-stable_linux.x86_64}"
PLUGIN_REQUIRED="${GDAI_PLUGIN_REQUIRED:-1}"

echo "==> Installing uv (GDAI MCP dependency)"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

echo "==> Ensuring Godot 4.3 editor"
mkdir -p "$GODOT_SDK"
if [[ ! -x "$GODOT_BIN" ]]; then
  curl -L -o "$GODOT_SDK/godot.zip" \
    "https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip"
  unzip -o "$GODOT_SDK/godot.zip" -d "$GODOT_SDK"
  chmod +x "$GODOT_BIN"
fi
echo "Godot: $GODOT_BIN"

echo "==> GDAI MCP plugin"
if [[ -f "$PLUGIN_DIR/gdai_mcp_server.py" ]]; then
  echo "Plugin already present at $PLUGIN_DIR"
else
  ZIP="${GDAI_PLUGIN_ZIP:-}"
  if [[ -n "$ZIP" && -f "$ZIP" ]]; then
    echo "Extracting $ZIP ..."
    tmp="$(mktemp -d)"
    unzip -q "$ZIP" -d "$tmp"
    if [[ -d "$tmp/addons/gdai-mcp-plugin-godot" ]]; then
      mkdir -p "$ROOT/game/addons"
      cp -a "$tmp/addons/gdai-mcp-plugin-godot" "$PLUGIN_DIR"
    elif [[ -d "$tmp/gdai-mcp-plugin-godot" ]]; then
      mkdir -p "$ROOT/game/addons"
      cp -a "$tmp/gdai-mcp-plugin-godot" "$PLUGIN_DIR"
    else
      echo "Could not find gdai-mcp-plugin-godot/ inside zip" >&2
      exit 1
    fi
    rm -rf "$tmp"
  else
    cat >&2 <<EOF

GDAI MCP plugin not found.

This is a commercial plugin from https://gdaimcp.com/
It cannot be downloaded automatically in cloud CI.

Options:
  1. Purchase/download the plugin zip locally
  2. Set secret GDAI_PLUGIN_ZIP=/path/to/plugin.zip and re-run install
  3. Or manually copy to: game/addons/gdai-mcp-plugin-godot/

Then in Godot: Project -> Plugins -> enable GDAI MCP -> Start server
Register Cursor Cloud MCP (stdio): bash tools/print_gdai_mcp_config.sh

EOF
    if [[ "$PLUGIN_REQUIRED" == "1" ]]; then
      exit 1
    fi
    echo "Continuing without plugin (GDAI_PLUGIN_REQUIRED=0)."
    exit 0
  fi
fi

echo "==> MCP server path"
echo "  uv run $PLUGIN_DIR/gdai_mcp_server.py"
echo "Done."
