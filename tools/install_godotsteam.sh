#!/usr/bin/env bash
# Install GodotSteam GDExtension into game/addons/godotsteam/
# Run once before Steam-enabled exports. See steam/GODOTSTEAM_SETUP.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/game/addons/godotsteam"
VERSION="${GODOTSTEAM_VERSION:-4.15}"

echo "==> GodotSteam installer"
echo "    Target: $DEST"
echo "    Version: $VERSION (override with GODOTSTEAM_VERSION)"
echo ""

if [[ -f "$DEST/godotsteam.gdextension" ]]; then
  echo "[OK] GodotSteam already present at $DEST"
  exit 0
fi

mkdir -p "$DEST"

cat > "$DEST/README.md" <<'EOF'
# GodotSteam (manual install required)

Download the **Godot 4.x Windows** release from:
https://codeberg.org/godotsteam/godotsteam/releases

Copy into this folder:
- `godotsteam.gdextension`
- `win64/godotsteam.windows.dll` (and related binaries per upstream README)

Then register the plugin in Project Settings if required by your GodotSteam version.

See `steam/GODOTSTEAM_SETUP.md` in the repo root.
EOF

echo "[INFO] Scaffold created at $DEST"
echo "[INFO] Download GodotSteam $VERSION binaries and place them in $DEST before Steam export."
echo "[INFO] SteamManager autoload will no-op until GodotSteam is installed."
