#!/usr/bin/env bash
# Install GodotSteam 4.15 GDExtension (Godot 4.1–4.3) into game/addons/godotsteam/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GAME="$ROOT/game"
ADDON="$GAME/addons/godotsteam"
URL="https://codeberg.org/godotsteam/godotsteam/releases/download/v4.15-gde/godotsteam-4.15-gdextension-plugin-4.1-4.3.zip"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading GodotSteam 4.15 (Godot 4.1–4.3)..."
curl -L -o "$TMP/godotsteam.zip" "$URL"

mkdir -p "$ADDON"
unzip -o "$TMP/godotsteam.zip" -d "$GAME"

echo "Installed to $ADDON"
echo "Platforms: linux64, win64, osx (+ 32-bit variants)"
echo "Dev App ID: $(cat "$GAME/steam_appid.txt" 2>/dev/null || echo '480 (create steam_appid.txt)')"
echo "Replace steam_appid.txt with your Steam App ID when your Steamworks app is ready."
