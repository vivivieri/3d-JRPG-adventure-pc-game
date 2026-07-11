#!/usr/bin/env bash
# Install GDAI MCP plugin from a local zip (commercial — not in git).
# Used during cloud snapshot setup or when zip is uploaded to the VM.
#
# Looks for:
#   game/addons/gdai-mcp-plugin-godot-*.zip
#   or $GDAI_PLUGIN_ZIP path
#
# Usage: bash tools/install_gdai_plugin.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${ROOT}/game/addons/gdai-mcp-plugin-godot"
ADDONS="${ROOT}/game/addons"

if [[ -d "$DEST" ]] && [[ -f "${DEST}/gdai_mcp_server.py" ]]; then
  echo "[install_gdai_plugin] Already installed at $DEST"
  exit 0
fi

ZIP="${GDAI_PLUGIN_ZIP:-}"
if [[ -z "$ZIP" ]]; then
  ZIP="$(ls -1 "${ADDONS}"/gdai-mcp-plugin-godot*.zip 2>/dev/null | head -1 || true)"
fi

if [[ -z "$ZIP" ]] || [[ ! -f "$ZIP" ]]; then
  echo "[install_gdai_plugin] FAIL: No plugin zip found."
  echo "  Place your purchase zip at: game/addons/gdai-mcp-plugin-godot-*.zip"
  echo "  Or set GDAI_PLUGIN_ZIP=/path/to/plugin.zip"
  echo "  Download: https://gdaimcp.com/"
  exit 1
fi

echo "[install_gdai_plugin] Extracting $ZIP ..."
TMP="$(mktemp -d)"
unzip -o -q "$ZIP" -d "$TMP"

# Zip may contain addons/gdai-mcp-plugin-godot/ or gdai-mcp-plugin-godot/ at root
if [[ -d "${TMP}/addons/gdai-mcp-plugin-godot" ]]; then
  SRC="${TMP}/addons/gdai-mcp-plugin-godot"
elif [[ -d "${TMP}/gdai-mcp-plugin-godot" ]]; then
  SRC="${TMP}/gdai-mcp-plugin-godot"
else
  echo "[install_gdai_plugin] FAIL: Unexpected zip layout. Expected addons/gdai-mcp-plugin-godot/"
  ls -la "$TMP"
  exit 1
fi

rm -rf "$DEST"
cp -a "$SRC" "$DEST"
rm -rf "$TMP"

if [[ ! -f "${DEST}/gdai_mcp_server.py" ]]; then
  echo "[install_gdai_plugin] FAIL: gdai_mcp_server.py missing after extract"
  exit 1
fi

echo "[install_gdai_plugin] OK → $DEST"
ls -la "$DEST" | head -5
