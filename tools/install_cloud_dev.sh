#!/usr/bin/env bash
# Idempotent cloud dev environment installer for Tides of Urashima.
# Used by .cursor/environment.json and manual setup.
#
# Installs: uv, Godot 4.7 editor + export templates, Python deps, project dirs.
# Does NOT install GDAI MCP (commercial — user must add game/addons/gdai-mcp-plugin-godot/).
#
# Usage: bash tools/install_cloud_dev.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GODOT_VERSION="${GODOT_VERSION:-4.7-stable}"
GODOT_INSTALL_DIR="${GODOT_INSTALL_DIR:-/opt/godot}"
GODOT_BIN_NAME="Godot_v${GODOT_VERSION}_linux.x86_64"
GODOT_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/${GODOT_BIN_NAME}.zip"
TEMPLATES_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}/Godot_v${GODOT_VERSION}_export_templates.tpz"

export PATH="${HOME}/.local/bin:${PATH}"

echo "==> Tides of Urashima — cloud dev install"
echo "    Root: $ROOT"
echo "    Godot: $GODOT_VERSION"
echo

# --- System packages (idempotent) ---
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    curl wget unzip ca-certificates \
    libgl1-mesa-dri libglx-mesa0 libvulkan1 xvfb \
    >/dev/null 2>&1 || true
fi

# --- uv (GDAI MCP bridge) ---
if ! command -v uv >/dev/null 2>&1; then
  echo "==> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
fi
echo "==> uv: $(uv --version)"

# --- Godot editor ---
sudo mkdir -p "$GODOT_INSTALL_DIR"
if [[ ! -x "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" ]]; then
  echo "==> Downloading Godot ${GODOT_VERSION}..."
  TMPZIP="$(mktemp /tmp/godot.XXXXXX.zip)"
  wget -q -O "$TMPZIP" "$GODOT_URL"
  sudo unzip -o -q "$TMPZIP" -d "$GODOT_INSTALL_DIR"
  sudo chmod +x "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}"
  rm -f "$TMPZIP"
fi

# Symlink godot4 + godot into user local bin
mkdir -p "${HOME}/.local/bin"
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" "${HOME}/.local/bin/godot4"
ln -sf "${GODOT_INSTALL_DIR}/${GODOT_BIN_NAME}" "${HOME}/.local/bin/godot"
echo "==> Godot: $(${HOME}/.local/bin/godot4 --version 2>&1 | head -1)"

# --- Export templates (headless export / validation) ---
# Export template folder: 4.7-stable → 4.7.stable
TEMPLATE_VER="${GODOT_VERSION/-/.}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
mkdir -p "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}"

if [[ ! -f "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}/version" ]]; then
  echo "==> Installing Godot export templates..."
  TMPTPZ="$(mktemp /tmp/godot-templates.XXXXXX.tpz)"
  wget -q -O "$TMPTPZ" "$TEMPLATES_URL"
  TMPDIR_TPL="$(mktemp -d /tmp/godot-tpl.XXXXXX)"
  unzip -o -q "$TMPTPZ" -d "$TMPDIR_TPL"
  cp -a "$TMPDIR_TPL"/templates/* "${XDG_DATA_HOME}/godot/export_templates/${TEMPLATE_VER}/"
  rm -rf "$TMPDIR_TPL" "$TMPTPZ"
fi

# --- Python tooling (validators + trailer generator) ---
echo "==> Python dependencies..."
if command -v uv >/dev/null 2>&1; then
  uv pip install --system numpy 2>/dev/null || pip3 install --user numpy 2>/dev/null || true
else
  pip3 install --user numpy 2>/dev/null || true
fi

# --- Project structure ---
bash "$ROOT/tools/setup_dev_environment.sh"

# --- GDAI MCP plugin (commercial zip — not in git) ---
if [[ -d "$ROOT/game/addons/gdai-mcp-plugin-godot" ]]; then
  echo "==> GDAI MCP plugin already installed"
elif ls "$ROOT/game/addons"/gdai-mcp-plugin-godot*.zip >/dev/null 2>&1 || [[ -n "${GDAI_PLUGIN_ZIP:-}" ]]; then
  echo "==> Installing GDAI MCP from zip..."
  bash "$ROOT/tools/install_gdai_plugin.sh"
else
  echo "!! GDAI MCP plugin not installed (commercial — https://gdaimcp.com/)"
  echo "   For cloud: upload zip to game/addons/ during Setup Agent, then rebuild snapshot"
  echo "   Or: cp plugin zip → game/addons/gdai-mcp-plugin-godot-*.zip and re-run install"
fi

# --- Persist Godot XDG paths for agent shells ---
PROFILE_SNIPPET="# Tides of Urashima — Godot cloud paths
export PATH=\"\${HOME}/.local/bin:\${PATH}\"
export XDG_DATA_HOME=\"${ROOT}/.cache/godot-data\"
export XDG_CONFIG_HOME=\"${ROOT}/.cache/godot-config\"
export XDG_CACHE_HOME=\"${ROOT}/.cache/godot-cache\"
"
for f in "${HOME}/.bashrc" "${HOME}/.profile"; do
  if [[ -f "$f" ]] && ! grep -q "Tides of Urashima — Godot cloud paths" "$f" 2>/dev/null; then
    echo "$PROFILE_SNIPPET" >> "$f"
  fi
done

# --- Headless project smoke test ---
echo "==> Godot headless smoke test..."
export PATH="${HOME}/.local/bin:${PATH}"
if godot4 --headless --path "$ROOT/game" --quit-after 2 2>&1 | tail -5; then
  echo "==> Godot project loads OK"
else
  echo "!! Godot smoke test had warnings (check output above)"
fi

# --- Godotiq (required — analyze/debug MCP) ---
if [[ -d "$ROOT/game/addons/godotiq" ]]; then
  echo "==> Godotiq addon already installed"
else
  echo "==> Installing Godotiq..."
  bash "$ROOT/tools/install_godotiq.sh"
fi

# --- Godot MCP Pro (required) ---
if [[ -f "$ROOT/tools/godot-mcp-pro-server/build/index.js" ]]; then
  echo "==> Godot MCP Pro server already built"
elif ls "$ROOT/game/addons"/godot-mcp-pro*.zip >/dev/null 2>&1; then
  echo "==> Installing Godot MCP Pro from zip..."
  bash "$ROOT/tools/install_godot_mcp_pro.sh"
else
  echo "!! Godot MCP Pro not installed — place godot-mcp-pro.zip in game/addons/"
fi

# --- Extended toolchain (Blender, GameLab config, audio placeholders) ---
if [[ -f "$ROOT/tools/install_extended_toolchain.sh" ]]; then
  bash "$ROOT/tools/install_extended_toolchain.sh" || echo "!! install_extended_toolchain.sh had failures — see output"
fi

# --- MCP config ---
if [[ -f "$ROOT/tools/write_mcp_config.sh" ]]; then
  bash "$ROOT/tools/write_mcp_config.sh" || true
fi

# --- GDAI MCP (manual) ---
if [[ -d "$ROOT/game/addons/gdai-mcp-plugin-godot" ]]; then
  echo "==> GDAI MCP plugin found"
  if [[ ! -f "$ROOT/.cursor/mcp.json" ]] && [[ -f "$ROOT/.cursor/mcp.json.example" ]]; then
    SERVER="$ROOT/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
    if [[ -f "$SERVER" ]]; then
      cat > "$ROOT/.cursor/mcp.json" <<EOF
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "$SERVER"]
    }
  }
}
EOF
      echo "==> Wrote .cursor/mcp.json (gitignored)"
    fi
  fi
else
  echo "!! GDAI MCP plugin not installed (commercial — https://gdaimcp.com/)"
  echo "   Copy to: game/addons/gdai-mcp-plugin-godot/"
  echo "   Then re-run this script or configure Cursor MCP manually."
fi

echo
echo "==> Cloud dev install complete."
bash "$ROOT/tools/check_dev_environment.sh" || true

if [[ "${SKIP_MCP_BOOTSTRAP:-0}" == "1" ]]; then
  echo "==> SKIP_MCP_BOOTSTRAP=1 — deferring MCP stack to tools/rebuild_cloud_snapshot.sh"
else
  echo
  echo "==> Bootstrapping MCP stack (required — blocks install on failure)..."
  bash "$ROOT/tools/ensure_mcp_stack.sh"
  bash "$ROOT/tools/check_mcp_ready.sh"
fi

echo
echo "Required Cursor Secrets (day one — see docs/agents/CURSOR_SECRETS_SETUP.md):"
echo "  CURSOR_PM_CYCLE_WEBHOOK_URL, CURSOR_FACTORY_ALERT_WEBHOOK_URL"
echo "  GAMELAB_API_KEY, GH_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ELEVENLABS_API_KEY"
echo "  Verify: bash tools/check_day_one_secrets.sh"
echo "Register in Cursor: godot-mcp, godotiq, godot-mcp-pro, gamelab-mcp (all required)"
echo "Blender: required for M5 turntable QA — bash tools/install_extended_toolchain.sh"
echo "See: docs/agents/MCP_STACK.md"
