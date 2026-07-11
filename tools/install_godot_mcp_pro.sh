#!/usr/bin/env bash
# Install Godot MCP Pro from purchased zip (commercial — not in git).
#
# Place zip at: game/addons/godot-mcp-pro*.zip  OR  set GODOT_MCP_PRO_ZIP=/path/to.zip
# Extracts:
#   game/addons/godot_mcp/          — Godot editor plugin
#   tools/godot-mcp-pro-server/     — Node.js MCP server (npm build)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ADDON_DEST="${ROOT}/game/addons/godot_mcp"
SERVER_DEST="${ROOT}/tools/godot-mcp-pro-server"

ZIP="${GODOT_MCP_PRO_ZIP:-}"
if [[ -z "$ZIP" ]]; then
  # Prefer full package zip (contains server/) over addon-only archives
  ZIP="$(ls -1 "${ROOT}/game/addons"/godot-mcp-pro*.zip 2>/dev/null | head -1 || true)"
fi
if [[ -z "$ZIP" ]]; then
  ZIP="$(ls -1 "${ROOT}/game/addons"/godot_mcp_pro*.zip 2>/dev/null | head -1 || true)"
fi

if [[ -z "$ZIP" || ! -f "$ZIP" ]]; then
  echo "Godot MCP Pro zip not found."
  echo "  Purchase: https://godot-mcp.abyo.net/"
  echo "  Place zip in game/addons/ then re-run: bash tools/install_godot_mcp_pro.sh"
  exit 1
fi

command -v unzip >/dev/null 2>&1 || { echo "unzip required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js 18+ required for MCP Pro server"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm required"; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "==> Extracting $(basename "$ZIP")..."
unzip -q -o "$ZIP" -d "$TMP"

# Find addon folder (addons/godot_mcp or godot_mcp)
ADDON_SRC=""
for candidate in \
  "$TMP/addons/godot_mcp" \
  "$TMP/godot_mcp" \
  "$TMP/addons/godot-mcp-pro" \
  "$(find "$TMP" -maxdepth 3 -type d -name 'godot_mcp' 2>/dev/null | head -1)"; do
  if [[ -n "$candidate" && -f "$candidate/plugin.cfg" ]]; then
    ADDON_SRC="$candidate"
    break
  fi
done

if [[ -z "$ADDON_SRC" ]]; then
  echo "FAIL: could not find godot_mcp plugin.cfg in zip"
  exit 1
fi

rm -rf "$ADDON_DEST"
mkdir -p "$(dirname "$ADDON_DEST")"
cp -a "$ADDON_SRC" "$ADDON_DEST"
echo "==> Addon: $ADDON_DEST"

# Find server/ directory
SERVER_SRC=""
for candidate in "$TMP/server" "$(find "$TMP" -maxdepth 2 -type d -name server 2>/dev/null | head -1)"; do
  if [[ -n "$candidate" && -f "$candidate/package.json" ]]; then
    SERVER_SRC="$candidate"
    break
  fi
done

if [[ -z "$SERVER_SRC" ]]; then
  echo "FAIL: server/ with package.json not found in zip (need full paid package)"
  exit 1
fi

rm -rf "$SERVER_DEST"
cp -a "$SERVER_SRC" "$SERVER_DEST"
echo "==> Building Node MCP server..."
(cd "$SERVER_DEST" && npm install && npm run build)

if [[ ! -f "$SERVER_DEST/build/index.js" ]]; then
  echo "FAIL: build/index.js missing after npm run build"
  exit 1
fi

echo "==> Godot MCP Pro installed"
echo "    Enable plugin: Project → Plugins → Godot MCP Pro"
echo "    MCP mode: ${GODOT_MCP_PRO_MODE:---minimal} (set GODOT_MCP_PRO_MODE=--lite for more tools)"
echo "    Run: bash tools/ensure_mcp_stack.sh"
