#!/usr/bin/env bash
# Build Godot 4.7 export templates with PCK encryption key baked in (M6).
# Requires: SCRIPT_AES256_ENCRYPTION_KEY (same value as GODOT_SCRIPT_ENCRYPTION_KEY).
# See docs/SECURITY.md §9 and Godot compiling_with_script_encryption_key.html
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GODOT_TAG="${GODOT_SOURCE_TAG:-4.7-stable}"
BUILD_ROOT="${GODOT_TEMPLATE_BUILD_ROOT:-${ROOT}/.cache/godot-template-build}"
SOURCE_DIR="${BUILD_ROOT}/godot"
KEY="${SCRIPT_AES256_ENCRYPTION_KEY:-${GODOT_SCRIPT_ENCRYPTION_KEY:-}}"

echo "==> Encrypted Godot export templates (M6 ship hardening)"
echo ""

if [[ -z "$KEY" ]]; then
  echo "[FAIL] Set SCRIPT_AES256_ENCRYPTION_KEY or GODOT_SCRIPT_ENCRYPTION_KEY (64 hex chars)"
  echo "       Generate: bash tools/generate_ship_protection_keys.sh"
  exit 1
fi

if ! [[ "$KEY" =~ ^[0-9a-fA-F]{64}$ ]]; then
  echo "[FAIL] Encryption key must be 64 hex characters (256-bit AES)"
  exit 1
fi

export SCRIPT_AES256_ENCRYPTION_KEY="$KEY"

for dep in git python3 scons; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    echo "[FAIL] missing build dependency: $dep"
    echo "       Linux: sudo apt install git python3 scons build-essential pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl1-mesa-dev libxi-dev libasound2-dev"
    exit 1
  fi
done

mkdir -p "$BUILD_ROOT"
if [[ ! -d "$SOURCE_DIR/.git" ]]; then
  echo "==> Cloning godotengine/godot tag ${GODOT_TAG}..."
  git clone --depth 1 --branch "$GODOT_TAG" https://github.com/godotengine/godot.git "$SOURCE_DIR"
fi

cd "$SOURCE_DIR"
echo "==> Building Linux release export template (this may take 30–90 minutes)..."
scons platform=linuxbsd target=template_release arch=x86_64 -j"$(nproc)"

LINUX_BIN="${SOURCE_DIR}/bin/godot.linuxbsd.template_release.x86_64"
if [[ ! -f "$LINUX_BIN" ]]; then
  echo "[FAIL] Linux template binary not found after build"
  exit 1
fi

OUT_LINUX="${ROOT}/build/godot-templates/linux_encrypted.template_release.x86_64"
mkdir -p "$(dirname "$OUT_LINUX")"
cp "$LINUX_BIN" "$OUT_LINUX"
chmod +x "$OUT_LINUX"

echo ""
echo "[OK]   Linux encrypted template: $OUT_LINUX"
echo ""
echo "Set before ship export:"
echo "  export GODOT_CUSTOM_TEMPLATE_LINUX=\"$OUT_LINUX\""
echo ""
echo "Windows template: build on Windows or cross-compile per Godot docs, then set:"
echo "  export GODOT_CUSTOM_TEMPLATE_WINDOWS=\"/path/to/godot.windows.template_release.x86_64.exe\""
echo ""
echo "Then export with keys in environment:"
echo "  export GODOT_SCRIPT_ENCRYPTION_KEY=\"\$SCRIPT_AES256_ENCRYPTION_KEY\""
echo "  export GODOT_SAVE_HMAC_KEY=\"<from generate_ship_protection_keys.sh>\""
echo "  export SHIP_RELEASE=1"
echo "  bash tools/export_linux.sh"
