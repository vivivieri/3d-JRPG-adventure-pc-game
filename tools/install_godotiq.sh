#!/usr/bin/env bash
# Install Godotiq MCP server (pip/uvx) and copy MIT addon into game/addons/godotiq/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ADDON_DEST="${ROOT}/game/addons/godotiq"

export PATH="${HOME}/.local/bin:${PATH}"

echo "==> Installing Godotiq"

if command -v uv >/dev/null 2>&1; then
  uv pip install --system godotiq 2>/dev/null || pip3 install --user godotiq
else
  pip3 install --user godotiq
fi

ADDON_SRC="$(python3 -c "import godotiq, os; print(os.path.join(os.path.dirname(godotiq.__file__), 'addon'))")"

if [[ ! -d "$ADDON_SRC" ]]; then
  echo "FAIL: godotiq pip package missing addon/ folder"
  exit 1
fi

mkdir -p "$(dirname "$ADDON_DEST")"
rm -rf "$ADDON_DEST"
cp -a "$ADDON_SRC" "$ADDON_DEST"

echo "==> Godotiq addon copied to game/addons/godotiq/"
echo "    Enable in Godot: Project → Project Settings → Plugins → GodotIQ"
echo "    MCP: uvx godotiq (configured by tools/write_mcp_config.sh)"
echo "    Pro:  set GODOTIQ_LICENSE_KEY env — https://godotiq.com/"

if command -v godotiq >/dev/null 2>&1; then
  godotiq auth status 2>/dev/null || true
fi
