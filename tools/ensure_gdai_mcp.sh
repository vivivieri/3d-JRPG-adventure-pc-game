#!/usr/bin/env bash
# Bootstrap GDAI MCP bridge for Cursor agents.
# 1) Godot Editor running with project open
# 2) GDAI plugin HTTP server listening (default :3571)
# 3) .cursor/mcp.json points uv at gdai_mcp_server.py
#
# Usage: bash tools/ensure_gdai_mcp.sh [--wait SECONDS]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WAIT="${1:-90}"
if [[ "${1:-}" == "--wait" ]]; then
  WAIT="${2:-90}"
fi

export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"
export GDAI_MCP_SERVER_PORT="${GDAI_MCP_SERVER_PORT:-3571}"

PLUGIN_DIR="${ROOT}/game/addons/gdai-mcp-plugin-godot"
SERVER_PY="${PLUGIN_DIR}/gdai_mcp_server.py"
MCP_JSON="${ROOT}/.cursor/mcp.json"
LOG="${ROOT}/.cache/ensure-gdai-mcp.log"
mkdir -p "${ROOT}/.cache"

log() { echo "[ensure_gdai_mcp] $*" | tee -a "$LOG"; }

fail() {
  log "FAIL: $*"
  echo ""
  echo "=== GDAI MCP NOT READY ==="
  echo "$*"
  echo ""
  echo "Required steps:"
  echo "  1. bash tools/install_cloud_dev.sh"
  echo "  2. bash tools/ensure_gdai_mcp.sh"
  echo "  3. Desktop: Cursor Settings → Tools & MCP → add godot-mcp from .cursor/mcp.json"
  echo "     Cloud:  https://cursor.com/agents → register godot-mcp custom MCP server"
  echo "  4. In Godot Editor: GDAI MCP panel → Start (if HTTP :${GDAI_MCP_SERVER_PORT} not up)"
  echo "  5. Restart Cursor / cloud agent after MCP shows connected"
  echo ""
  echo "Docs: docs/GDAI_CLOUD_SETUP.md"
  exit 1
}

log "Checking prerequisites..."

command -v uv >/dev/null 2>&1 || fail "uv not installed. Run: bash tools/install_cloud_dev.sh"
command -v godot4 >/dev/null 2>&1 || fail "godot4 not in PATH. Run: bash tools/install_cloud_dev.sh"
[[ -d "$PLUGIN_DIR" ]] || fail "GDAI plugin missing at game/addons/gdai-mcp-plugin-godot/"
[[ -f "$SERVER_PY" ]] || fail "gdai_mcp_server.py missing in plugin folder"

# Write MCP config for all installed servers
bash "${ROOT}/tools/write_mcp_config.sh"
log "MCP config updated"

# Kill headless Godot processes that steal GDAI runtime port
for pid in $(pgrep -f "godot4.*--headless.*${ROOT}/game" 2>/dev/null || true); do
  log "Stopping headless Godot PID $pid (conflicts with editor GDAI bridge)"
  kill "$pid" 2>/dev/null || true
done
sleep 1

# Start editor if not running
PGREP_PATTERN="godot4.*${ROOT}/game.*--editor"
if ! pgrep -f "$PGREP_PATTERN" >/dev/null 2>&1; then
  log "Starting Godot editor..."
  bash "${ROOT}/tools/start_godot_editor.sh" >>"$LOG" 2>&1 || true
  sleep 5
fi

if ! pgrep -f "$PGREP_PATTERN" >/dev/null 2>&1; then
  fail "Godot editor failed to start. See ${ROOT}/.cache/godot-editor.log"
fi
log "Godot editor running"

# Wait for GDAI HTTP /tools endpoint
URL="http://127.0.0.1:${GDAI_MCP_SERVER_PORT}/tools"
log "Waiting up to ${WAIT}s for GDAI HTTP at ${URL}..."

deadline=$((SECONDS + WAIT))
ready=0
while [[ $SECONDS -lt $deadline ]]; do
  if curl -sf "$URL" >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done

if [[ $ready -ne 1 ]]; then
  fail "GDAI HTTP server not responding on :${GDAI_MCP_SERVER_PORT}. Open Godot → GDAI MCP panel → Start."
fi

TOOLS_JSON="$(curl -sf "$URL")"
TOOL_COUNT="$(python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('mcp_tools',[])))" <<<"$TOOLS_JSON")"
log "GDAI HTTP OK — ${TOOL_COUNT} tools on :${GDAI_MCP_SERVER_PORT}"

# Verify stdio bridge can import
if ! timeout 8 uv run "$SERVER_PY" </dev/null >/dev/null 2>&1; then
  log "WARN: stdio bridge slow to start (uv deps); HTTP bridge is up"
fi

# Godotiq + Godot MCP Pro — required — see docs/MCP_STACK.md
STACK_OK=1
if [[ -d "${ROOT}/game/addons/godotiq" ]]; then
  log "Godotiq addon present"
  if ss -tln 2>/dev/null | grep -q ':6007 ' || netstat -tln 2>/dev/null | grep -q ':6007 '; then
    log "Godotiq WebSocket OK on :6007"
  else
    log "FAIL: Godotiq :6007 not listening — enable GodotIQ plugin in Project → Plugins"
    STACK_OK=0
  fi
else
  log "FAIL: Godotiq not installed — bash tools/install_godotiq.sh"
  STACK_OK=0
fi

if [[ -f "${ROOT}/tools/godot-mcp-pro-server/build/index.js" ]]; then
  log "Godot MCP Pro server built"
else
  log "FAIL: Godot MCP Pro not installed — bash tools/install_godot_mcp_pro.sh"
  STACK_OK=0
fi

if [[ $STACK_OK -eq 0 ]]; then
  fail "Required MCP stack incomplete (Godotiq and/or MCP Pro). See docs/MCP_STACK.md"
fi

echo ""
echo "=== MCP STACK STATUS ==="
echo "  GDAI (build):     HTTP :${GDAI_MCP_SERVER_PORT} — ${TOOL_COUNT} tools"
if [[ -d "${ROOT}/game/addons/godotiq" ]]; then
  echo "  Godotiq (analyze): addon installed — enable GodotIQ plugin"
else
  echo "  Godotiq (analyze): not installed"
fi
if [[ -f "${ROOT}/tools/godot-mcp-pro-server/build/index.js" ]]; then
  echo "  MCP Pro (test):   server ready (${GODOT_MCP_PRO_MODE:---minimal})"
else
  echo "  MCP Pro (test):   not installed"
fi
echo "  MCP cfg: ${MCP_JSON}"
echo ""
echo "NEXT: Register P0 in Cursor MCP: godot-mcp, godotiq, godot-mcp-pro"
echo "      Optional: gamelab-mcp (UI art), notion (design index)"
echo "      Offline: ComfyUI/Material Maker, Meshy/Blender, ACE-Step 1.5"
echo "      Docs: docs/MCP_STACK.md"
echo ""
exit 0
