#!/usr/bin/env bash
# CI dependencies on Windows (GitHub Actions windows-latest). Godot editor + export templates.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export CI=true
GODOT_VERSION="${GODOT_VERSION:-4.7-stable}"
GODOT_INSTALL_DIR="${GODOT_INSTALL_DIR:-${RUNNER_TEMP:-/tmp}/godot}"
GODOT_ZIP_NAME="Godot_v${GODOT_VERSION}_win64.exe.zip"
GODOT_EXE_NAME="Godot_v${GODOT_VERSION}_win64.exe"
GODOT_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/${GODOT_ZIP_NAME}"
TEMPLATES_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/Godot_v${GODOT_VERSION}_export_templates.tpz"
TEMPLATE_VER="${GODOT_VERSION/-/.}"

echo "==> Windows CI dependency install (Godot ${GODOT_VERSION})"
echo ""

mkdir -p "$GODOT_INSTALL_DIR" "${HOME}/.local/bin"

if [[ ! -f "${GODOT_INSTALL_DIR}/${GODOT_EXE_NAME}" ]]; then
  echo "==> Downloading Godot Windows editor..."
  TMPZIP="$(mktemp /tmp/godot-win.XXXXXX.zip)"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$TMPZIP" "$GODOT_URL"
  else
    wget -q -O "$TMPZIP" "$GODOT_URL"
  fi
  unzip -o -q "$TMPZIP" -d "$GODOT_INSTALL_DIR"
  rm -f "$TMPZIP"
fi

chmod +x "${GODOT_INSTALL_DIR}/${GODOT_EXE_NAME}" 2>/dev/null || true
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_EXE_NAME}" "${HOME}/.local/bin/godot4"
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_EXE_NAME}" "${HOME}/.local/bin/godot"
export PATH="${HOME}/.local/bin:${PATH}"

GODOT_VER_OUT="$(godot4 --version 2>&1 | head -1)"
echo "==> Godot: ${GODOT_VER_OUT}"

APPDATA_GODOT="${APPDATA:-${HOME}/AppData/Roaming}/Godot"
mkdir -p "${APPDATA_GODOT}/export_templates/${TEMPLATE_VER}"
if [[ ! -f "${APPDATA_GODOT}/export_templates/${TEMPLATE_VER}/version" ]]; then
  echo "==> Installing export templates to ${APPDATA_GODOT}/export_templates/${TEMPLATE_VER}"
  TMPTPZ="$(mktemp /tmp/godot-templates.XXXXXX.tpz)"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$TMPTPZ" "$TEMPLATES_URL"
  else
    wget -q -O "$TMPTPZ" "$TEMPLATES_URL"
  fi
  TMPDIR_TPL="$(mktemp -d /tmp/godot-tpl.XXXXXX)"
  unzip -o -q "$TMPTPZ" -d "$TMPDIR_TPL"
  cp -a "$TMPDIR_TPL"/templates/* "${APPDATA_GODOT}/export_templates/${TEMPLATE_VER}/"
  rm -rf "$TMPDIR_TPL" "$TMPTPZ"
fi

export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"

if [[ -f "${ROOT}/tools/requirements-ci.txt" ]]; then
  pip3 install -q -r "${ROOT}/tools/requirements-ci.txt" 2>/dev/null || true
fi

echo "==> Windows CI deps ready"
