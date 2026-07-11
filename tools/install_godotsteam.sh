#!/usr/bin/env bash
# Install GodotSteam GDExtension into game/addons/godotsteam/
# GodotSteam 4.20+ required for Godot 4.7. See steam/GODOTSTEAM_SETUP.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/game/addons/godotsteam"
VERSION="${GODOTSTEAM_VERSION:-4.20}"
GODOT_MIN="${GODOTSTEAM_GODOT:-4.4}"

echo "==> GodotSteam installer"
echo "    Target: $DEST"
echo "    GodotSteam: $VERSION (Godot ${GODOT_MIN}+)"
echo ""

if [[ -f "$DEST/godotsteam.gdextension" ]]; then
  echo "[OK] GodotSteam already present at $DEST"
  exit 0
fi

mkdir -p "$DEST"

ZIP_URL="https://codeberg.org/godotsteam/godotsteam/releases/download/v${VERSION}-gde/godotsteam-${VERSION}-gdextension-plugin-${GODOT_MIN}.zip"
TMP_ZIP="$(mktemp /tmp/godotsteam-XXXXXX.zip)"

echo "==> Downloading GodotSteam ${VERSION} GDExtension (Godot ${GODOT_MIN}+)..."
if curl -fsSL -o "$TMP_ZIP" "$ZIP_URL"; then
  unzip -qo "$TMP_ZIP" -d "$DEST"
  if [[ -d "$DEST/addons/godotsteam" ]]; then
    mv "$DEST/addons/godotsteam/"* "$DEST/"
    rm -rf "$DEST/addons"
  fi
  rm -f "$TMP_ZIP"
  echo "[OK] GodotSteam installed to $DEST"
  ls "$DEST/godotsteam.gdextension"
  exit 0
fi

rm -f "$TMP_ZIP"

cat > "$DEST/README.md" <<'EOF'
# GodotSteam (manual install required)

Download **GodotSteam 4.20+** (Godot 4.7 compatible) from:
https://codeberg.org/godotsteam/godotsteam/releases

Use: `godotsteam-4.20-gdextension-plugin-4.4.zip` or newer.

Copy into this folder:
- `godotsteam.gdextension`
- platform binaries per upstream README

See `steam/GODOTSTEAM_SETUP.md` in the repo root.
EOF

echo "[INFO] Scaffold created at $DEST"
echo "[INFO] Download GodotSteam ${VERSION}+ and place in $DEST before Steam export."
