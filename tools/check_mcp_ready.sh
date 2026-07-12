#!/usr/bin/env bash
# Verify P0 MCP stack is ready before any scene/editor work.
# Agents must exit non-zero and STOP implementation if this fails.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export GDAI_MCP_SERVER_PORT="${GDAI_MCP_SERVER_PORT:-3571}"

FAIL=0

fail() {
  echo "[FAIL] $*"
  FAIL=1
}

ok() {
  echo "[OK]   $*"
}

echo "==> MCP readiness check (P0 required before scene work)"
echo ""

command -v uv >/dev/null 2>&1 || fail "uv not installed — bash tools/install_cloud_dev.sh"
command -v godot4 >/dev/null 2>&1 || fail "godot4 not in PATH — bash tools/install_cloud_dev.sh"

PLUGIN_DIR="${ROOT}/game/addons/gdai-mcp-plugin-godot"
if [[ -d "$PLUGIN_DIR" && -f "$PLUGIN_DIR/gdai_mcp_server.py" ]]; then
  ok "GDAI plugin folder present"
else
  fail "GDAI plugin missing at game/addons/gdai-mcp-plugin-godot/ (commercial — mount via Cursor Secrets)"
fi

if [[ -d "${ROOT}/game/addons/godotiq" ]]; then
  ok "Godotiq addon present"
else
  fail "Godotiq missing — bash tools/install_godotiq.sh"
fi

if [[ -f "${ROOT}/tools/godot-mcp-pro-server/build/index.js" ]]; then
  ok "Godot MCP Pro server built"
else
  fail "Godot MCP Pro missing — bash tools/install_godot_mcp_pro.sh"
fi

if [[ -f "${ROOT}/.cursor/mcp.json" ]]; then
  ok ".cursor/mcp.json present"
else
  fail ".cursor/mcp.json missing — bash tools/write_mcp_config.sh"
fi

URL="http://127.0.0.1:${GDAI_MCP_SERVER_PORT}/tools"
if curl -sf "$URL" >/dev/null 2>&1; then
  TOOL_COUNT="$(curl -sf "$URL" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('mcp_tools',[])))")"
  ok "GDAI HTTP bridge :${GDAI_MCP_SERVER_PORT} (${TOOL_COUNT} tools)"
else
  fail "GDAI HTTP not responding on :${GDAI_MCP_SERVER_PORT} — bash tools/ensure_mcp_stack.sh"
fi

if pgrep -f "godot4.*${ROOT}/game.*--editor" >/dev/null 2>&1; then
  ok "Godot editor running with project open"
else
  fail "Godot editor not running — bash tools/start_godot_editor.sh"
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "MCP readiness: FAILED — do not hand-edit .tscn; notify user and STOP scene work"
  echo "Docs: docs/GDAI_CLOUD_SETUP.md, docs/MCP_STACK.md"
  exit 1
fi

echo "MCP readiness: PASS"
exit 0
