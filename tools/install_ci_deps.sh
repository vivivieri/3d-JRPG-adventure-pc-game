#!/usr/bin/env bash
# Minimal CI dependencies — Godot + Python validators. No GDAI/MCP stack.
# Used by .github/workflows/ci.yml and local pre-push checks.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export CI=true
export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

GODOT_VERSION="${GODOT_VERSION:-4.7-stable}"
GODOT_INSTALL_DIR="${GODOT_INSTALL_DIR:-/opt/godot}"
GODOT_BIN_NAME="Godot_v${GODOT_VERSION}_linux.x86_64"
GODOT_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/${GODOT_BIN_NAME}.zip"
TEMPLATES_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/Godot_v${GODOT_VERSION}_export_templates.tpz"

echo "==> CI dependency install (no MCP stack)"
echo "    Godot: ${GODOT_VERSION}"
echo ""

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    curl wget unzip ca-certificates python3 python3-pip ripgrep shellcheck \
    libgl1-mesa-dri libglx-mesa0 libvulkan1 xvfb
fi

sudo mkdir -p "$GODOT_INSTALL_DIR"
if [[ ! -x "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" ]]; then
  echo "==> Downloading Godot ${GODOT_VERSION}..."
  TMPZIP="$(mktemp /tmp/godot.XXXXXX.zip)"
  wget -q -O "$TMPZIP" "$GODOT_URL"
  sudo unzip -o -q "$TMPZIP" -d "$GODOT_INSTALL_DIR"
  sudo chmod +x "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}"
  rm -f "$TMPZIP"
fi

mkdir -p "${HOME}/.local/bin"
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" "${HOME}/.local/bin/godot4"
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" "${HOME}/.local/bin/godot"
GODOT_VER_OUT="$(godot4 --version 2>&1 | head -1)"
echo "==> Godot: ${GODOT_VER_OUT}"
if ! grep -q "${GODOT_VERSION/-/.}" <<<"${GODOT_VER_OUT}"; then
  echo "[FAIL] Godot version mismatch: expected ${GODOT_VERSION}, got ${GODOT_VER_OUT}"
  exit 1
fi

TEMPLATE_VER="${GODOT_VERSION/-/.}"
mkdir -p "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}"
if [[ ! -f "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}/version" ]]; then
  echo "==> Installing export templates..."
  TMPTPZ="$(mktemp /tmp/godot-templates.XXXXXX.tpz)"
  wget -q -O "$TMPTPZ" "$TEMPLATES_URL"
  TMPDIR_TPL="$(mktemp -d /tmp/godot-tpl.XXXXXX)"
  unzip -o -q "$TMPTPZ" -d "$TMPDIR_TPL"
  cp -a "$TMPDIR_TPL"/templates/* "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}/"
  rm -rf "$TMPDIR_TPL" "$TMPTPZ"
fi

if [[ -f "${ROOT}/tools/requirements-ci.txt" ]]; then
  pip3 install --user -q -r "${ROOT}/tools/requirements-ci.txt" 2>/dev/null || \
    pip3 install -q -r "${ROOT}/tools/requirements-ci.txt" 2>/dev/null || true
fi

if [[ -f "${ROOT}/requirements.txt" ]]; then
  pip3 install --user -q -r "${ROOT}/requirements.txt" 2>/dev/null || \
    pip3 install -q -r "${ROOT}/requirements.txt" 2>/dev/null || true
fi

bash "${ROOT}/tools/setup_dev_environment.sh" >/dev/null 2>&1 || true

bash "${ROOT}/tools/install_git_lfs.sh" >/dev/null 2>&1 || true

echo "==> CI deps ready"
