#!/usr/bin/env bash
# Verify plugin compatibility with the pinned Godot version (see tools/install_cloud_dev.sh).
# Usage: bash tools/check_plugin_compatibility.sh [--with-editor]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WITH_EDITOR=0
if [[ "${1:-}" == "--with-editor" ]]; then
  WITH_EDITOR=1
fi

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
export DISPLAY="${DISPLAY:-:1}"
GDAI_PORT="${GDAI_MCP_SERVER_PORT:-3571}"
GODOTIQ_PORT="${GODOTIQ_PORT:-6007}"

PASS=0
WARN=0
FAIL=0
SKIP=0

ok()   { echo "[PASS] $*"; PASS=$((PASS + 1)); }
warn() { echo "[WARN] $*"; WARN=$((WARN + 1)); }
fail() { echo "[FAIL] $*"; FAIL=$((FAIL + 1)); }
skip() { echo "[SKIP] $*"; SKIP=$((SKIP + 1)); }

plugin_version() {
  local cfg="$1"
  if [[ -f "$cfg" ]]; then
    awk -F= '/^version=/ { gsub(/"/, "", $2); print $2; exit }' "$cfg"
  fi
}

echo "==> Plugin compatibility audit — $(date -u +%Y-%m-%dT%H:%MZ)"
echo "    Project: $ROOT/game"
echo ""

# --- Engine ---
if command -v godot4 >/dev/null 2>&1; then
  GODOT_VER="$(godot4 --version 2>/dev/null | head -1)"
  ok "Godot engine: $GODOT_VER"
else
  fail "Godot not in PATH — run: bash tools/install_cloud_dev.sh"
  GODOT_VER="unknown"
fi

# --- Headless project load ---
if command -v godot4 >/dev/null 2>&1; then
  if OUT="$(godot4 --headless --path game --quit-after 1 2>&1)"; then
    if echo "$OUT" | grep -qiE 'SCRIPT ERROR|Parse Error|Failed to load'; then
      fail "Headless project load — script/parse errors"
      echo "$OUT" | tail -10
    else
      ok "Headless project load (boot + autoloads)"
    fi
    if echo "$OUT" | grep -q 'Capture not registered: .gdaimcp'; then
      warn "GDAI runtime capture unregister noise on headless quit (known, non-blocking)"
    fi
  else
    fail "Headless project load crashed"
    echo "$OUT" | tail -15
  fi
fi

# --- GDAI MCP ---
GDAI_DIR="game/addons/gdai-mcp-plugin-godot"
if [[ -d "$GDAI_DIR" ]]; then
  GDAI_VER="$(plugin_version "$GDAI_DIR/plugin.cfg")"
  ok "GDAI MCP addon present (v${GDAI_VER:-?})"
  [[ -f "$GDAI_DIR/gdai_mcp_server.py" ]] && ok "GDAI MCP server script present" || fail "gdai_mcp_server.py missing"

  if grep -q 'gdai-mcp-plugin-godot/plugin.cfg' game/project.godot 2>/dev/null; then
    ok "GDAI MCP enabled in project.godot"
  else
    fail "GDAI MCP not enabled — Project → Plugins → GDAI MCP"
  fi

  if curl -sf "http://127.0.0.1:${GDAI_PORT}/tools" >/dev/null 2>&1; then
    TOOL_COUNT="$(curl -sf "http://127.0.0.1:${GDAI_PORT}/tools" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('mcp_tools',[])))")"
    ok "GDAI HTTP bridge :${GDAI_PORT} (${TOOL_COUNT} tools)"
  elif [[ $WITH_EDITOR -eq 1 ]]; then
    bash tools/ensure_gdai_mcp.sh --wait 90 >/dev/null 2>&1 || true
    if curl -sf "http://127.0.0.1:${GDAI_PORT}/tools" >/dev/null 2>&1; then
      ok "GDAI HTTP bridge :${GDAI_PORT} (after ensure_gdai_mcp)"
    else
      warn "GDAI HTTP bridge offline — open editor → GDAI panel → Start"
    fi
  else
    warn "GDAI HTTP bridge offline (run: bash tools/ensure_gdai_mcp.sh --wait 90)"
  fi
else
  skip "GDAI MCP not installed"
fi

# --- Godotiq ---
GODOTIQ_DIR="game/addons/godotiq"
if [[ -d "$GODOTIQ_DIR" ]]; then
  GIQ_VER="$(plugin_version "$GODOTIQ_DIR/plugin.cfg")"
  ok "Godotiq addon present (v${GIQ_VER:-?})"

  if python3 -c "import godotiq" 2>/dev/null; then
    PIP_VER="$(pip3 show godotiq 2>/dev/null | awk '/^Version:/ {print $2}')"
    ok "Godotiq pip package (v${PIP_VER:-?})"
  else
    warn "Godotiq pip not installed — bash tools/install_godotiq.sh"
  fi

  if grep -q 'godotiq/plugin.cfg' game/project.godot 2>/dev/null; then
    ok "GodotIQ enabled in project.godot"
  else
    fail "GodotIQ not enabled — Project → Plugins → GodotIQ"
  fi

  if ss -tln 2>/dev/null | grep -q ":${GODOTIQ_PORT} " || netstat -tln 2>/dev/null | grep -q ":${GODOTIQ_PORT} "; then
    ok "Godotiq WebSocket bridge :${GODOTIQ_PORT}"
  elif [[ $WITH_EDITOR -eq 1 ]]; then
  warn "Godotiq WebSocket :${GODOTIQ_PORT} not listening — enable GodotIQ plugin and wait ~5s"
  else
    warn "Godotiq WebSocket offline (needs editor + GodotIQ plugin enabled)"
  fi
else
  skip "Godotiq not installed"
fi

# --- Godot MCP Pro ---
if [[ -f tools/godot-mcp-pro-server/build/index.js ]]; then
  MCP_VER="$(plugin_version game/addons/godot_mcp/plugin.cfg 2>/dev/null || true)"
  ok "Godot MCP Pro server built (addon v${MCP_VER:-?})"
  if command -v node >/dev/null 2>&1; then
    NODE_VER="$(node --version)"
    ok "Node.js for MCP Pro ($NODE_VER)"
  else
    fail "Node.js missing — required for Godot MCP Pro"
  fi
  if grep -q 'godot_mcp/plugin.cfg' game/project.godot 2>/dev/null; then
    ok "Godot MCP Pro enabled in project.godot"
  else
    warn "Godot MCP Pro not enabled in project.godot"
  fi
else
  skip "Godot MCP Pro not installed (commercial zip required)"
fi

# --- GodotSteam ---
STEAM_EXT="game/addons/godotsteam/godotsteam.gdextension"
if [[ -f "$STEAM_EXT" ]]; then
  if grep -q 'Version 4.15' game/addons/godotsteam/readme.md 2>/dev/null; then
    INSTALLED_STEAM="4.15"
  else
    INSTALLED_STEAM="unknown"
  fi
  warn "GodotSteam ${INSTALLED_STEAM} present — requires 4.20+ for Godot 4.7 (bash tools/install_godotsteam.sh)"
  STEAM_TEST="$(mktemp /tmp/steam_test_XXXXXX.gd)"
  cat >"$STEAM_TEST" <<'EOF'
extends SceneTree
func _initialize() -> void:
	if ClassDB.class_exists("Steam"):
		print("STEAM_CLASS_OK")
	else:
		print("STEAM_CLASS_MISSING")
	quit()
EOF
  if OUT="$(godot4 --headless --path game --script "$STEAM_TEST" 2>&1)"; then
    if echo "$OUT" | grep -q STEAM_CLASS_OK; then
      if [[ "$INSTALLED_STEAM" == "4.15" ]]; then
        warn "GodotSteam 4.15 registers Steam class on ${GODOT_VER} — vendor still requires 4.20+ before ship"
      else
        ok "GodotSteam GDExtension loads on ${GODOT_VER}"
      fi
    else
      fail "GodotSteam GDExtension does not register Steam class on ${GODOT_VER} — run: bash tools/install_godotsteam.sh"
    fi
  else
    fail "GodotSteam load test crashed"
    echo "$OUT" | tail -8
  fi
  rm -f "$STEAM_TEST"
else
  skip "GodotSteam not installed (Phase 8)"
fi

echo ""
echo "=== Summary ==="
echo "Pass: $PASS | Warn: $WARN | Fail: $FAIL | Skip: $SKIP"
echo "Matrix: docs/PLUGIN_COMPATIBILITY.md"
echo ""

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
exit 0
