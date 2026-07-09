#!/usr/bin/env bash
# Export Tides of Urashima Windows desktop build (Linux host + Godot 4.3).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GODOT_DIR="${GODOT_DIR:-$ROOT/.godot-sdk}"
GODOT_BIN="${GODOT_BIN:-$GODOT_DIR/Godot_v4.3-stable_linux.x86_64}"
TEMPLATE_DIR="$HOME/.local/share/godot/export_templates/4.3.stable"
BUILD_DIR="$ROOT/build"
PRESET_FILE="$ROOT/game/export_presets.cfg"

mkdir -p "$BUILD_DIR" "$GODOT_DIR" "$(dirname "$TEMPLATE_DIR")"

if [[ ! -x "$GODOT_BIN" ]]; then
  echo "Downloading Godot 4.3..."
  TMP="$(mktemp -d)"
  curl -L -o "$TMP/godot.zip" "https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_linux.x86_64.zip"
  unzip -q "$TMP/godot.zip" -d "$GODOT_DIR"
  chmod +x "$GODOT_DIR"/Godot_v*
  GODOT_BIN="$(find "$GODOT_DIR" -maxdepth 1 -name 'Godot_v4.3-stable_linux.x86_64' | head -1)"
  rm -rf "$TMP"
fi

if [[ ! -f "$TEMPLATE_DIR/version.txt" ]]; then
  echo "Downloading export templates..."
  TMP="$(mktemp -d)"
  curl -L -o "$TMP/templates.tpz" "https://github.com/godotengine/godot/releases/download/4.3-stable/Godot_v4.3-stable_export_templates.tpz"
  mkdir -p "$TEMPLATE_DIR"
  unzip -q "$TMP/templates.tpz" -d "$TMP/ex"
  mv "$TMP/ex"/templates/* "$TEMPLATE_DIR/"
  rm -rf "$TMP"
fi

if [[ ! -f "$PRESET_FILE" ]]; then
  cp "$ROOT/steam/godot_export_notes.txt" "$PRESET_FILE" 2>/dev/null || true
fi

if [[ ! -f "$PRESET_FILE" ]]; then
  cat > "$PRESET_FILE" <<'EOF'
[preset.0]
name="Windows Desktop"
platform="Windows Desktop"
runnable=true
export_filter="all_resources"
export_path="../build/TidesOfUrashima.exe"
binary_format/embed_pck=true
binary_format/architecture="x86_64"
texture_format/s3tc_bptc=true
application/icon="res://assets/ui/icon.svg"
application/file_version="0.1.0.0"
application/product_version="0.1.0.0"
application/company_name="Tides of Urashima"
application/product_name="Tides of Urashima"
application/file_description="A short 3D JRPG adventure adapted from Japanese folklore."
EOF
fi

echo "Exporting Windows build..."
cd "$ROOT/game"
"$GODOT_BIN" --headless --path . --export-release "Windows Desktop" "$BUILD_DIR/TidesOfUrashima.exe"
echo "Done: $BUILD_DIR/TidesOfUrashima.exe"
ls -lh "$BUILD_DIR/TidesOfUrashima.exe"
