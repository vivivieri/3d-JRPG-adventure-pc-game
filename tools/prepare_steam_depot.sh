#!/usr/bin/env bash
# Bundle Steam depot files for local testing or upload prep.
# Usage: bash tools/prepare_steam_depot.sh [--platform windows|linux|all]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLATFORM="all"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      PLATFORM="${2:-all}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done

prepare_windows() {
  local DEPOT="$ROOT/build/steam_depot_windows"
  local EXE="$ROOT/build/TidesOfUrashima.exe"
  local STEAM_ADDON="$ROOT/game/addons/godotsteam/win64"

  echo "==> Preparing Windows Steam depot"
  echo "    Output: $DEPOT"

  if [[ ! -f "$EXE" ]]; then
    echo "[INFO] Build exe missing — running export..."
    bash "$ROOT/tools/export_windows.sh"
  fi

  if [[ ! -f "$STEAM_ADDON/steam_api64.dll" ]]; then
    echo "[WARN] GodotSteam win64 not installed — depot without Steam DLLs"
    echo "       Run: bash tools/install_godotsteam.sh"
  fi

  mkdir -p "$DEPOT"
  cp "$EXE" "$DEPOT/TidesOfUrashima.exe"
  if [[ -f "$STEAM_ADDON/steam_api64.dll" ]]; then
    cp "$STEAM_ADDON/steam_api64.dll" "$DEPOT/"
    cp "$STEAM_ADDON/libgodotsteam.windows.template_release.x86_64.dll" "$DEPOT/"
  fi
  if [[ ! -f "$DEPOT/steam_appid.txt" ]]; then
    echo "480" > "$DEPOT/steam_appid.txt"
    echo "[INFO] Created steam_appid.txt with test app id 480"
  fi
  ls -lh "$DEPOT"
}

prepare_linux() {
  local DEPOT="$ROOT/build/steam_depot_linux"
  local BIN="$ROOT/build/TidesOfUrashima.x86_64"
  local STEAM_ADDON="$ROOT/game/addons/godotsteam/linux64"

  echo "==> Preparing Linux Steam depot"
  echo "    Output: $DEPOT"

  if [[ ! -f "$BIN" ]]; then
    echo "[INFO] Linux binary missing — running export..."
    bash "$ROOT/tools/export_linux.sh"
  fi

  mkdir -p "$DEPOT"
  cp "$BIN" "$DEPOT/TidesOfUrashima.x86_64"
  chmod +x "$DEPOT/TidesOfUrashima.x86_64"
  if [[ -f "$STEAM_ADDON/libsteam_api.so" ]]; then
    cp "$STEAM_ADDON/libsteam_api.so" "$DEPOT/"
    cp "$STEAM_ADDON/libgodotsteam.linux.template_release.x86_64.so" "$DEPOT/"
  else
    echo "[WARN] GodotSteam linux64 not installed — depot without Steam libs"
  fi
  if [[ ! -f "$DEPOT/steam_appid.txt" ]]; then
    echo "480" > "$DEPOT/steam_appid.txt"
  fi
  ls -lh "$DEPOT"
}

case "$PLATFORM" in
  windows) prepare_windows ;;
  linux) prepare_linux ;;
  all)
    prepare_windows
    echo ""
    prepare_linux
    ;;
  *)
    echo "[FAIL] unknown platform: $PLATFORM (use windows|linux|all)"
    exit 1
    ;;
esac

echo ""
echo "Test Windows depot on a Windows PC with Steam client running."
echo "Test Linux depot: ./build/steam_depot_linux/TidesOfUrashima.x86_64"
