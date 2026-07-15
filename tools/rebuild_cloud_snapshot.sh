#!/usr/bin/env bash
# Orchestrate cloud snapshot rebuild for game/development.
# Run inside a Setup Agent after uploading commercial plugin zips.
#
# Usage:
#   bash tools/rebuild_cloud_snapshot.sh           # full rebuild
#   bash tools/rebuild_cloud_snapshot.sh --preflight  # checks only (no install)
#
# Required zips (not in git):
#   game/addons/gdai-mcp-plugin-godot-*.zip
#   game/addons/godot-mcp-pro*.zip  (or godot_mcp_pro*.zip)
#
# After PASS: save snapshot in dashboard, update .cursor/environment.json snapshot id.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PREFLIGHT_ONLY=0
if [[ "${1:-}" == "--preflight" ]]; then
  PREFLIGHT_ONLY=1
fi

export PATH="${HOME}/.local/bin:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

step() { echo; echo "════════════════════════════════════════"; echo "  $*"; echo "════════════════════════════════════════"; }
ok() { echo "[OK]   $*"; }
fail() { echo "[FAIL] $*"; exit 1; }
warn() { echo "[WARN] $*"; }

step "Phase 0 — Preflight"

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [[ "$BRANCH" != "game/development" ]]; then
  warn "Branch is '$BRANCH' (expected game/development for snapshot save)"
else
  ok "Branch: game/development"
fi

GDAI_ZIP="$(ls -1 "${ROOT}/game/addons"/gdai-mcp-plugin-godot*.zip 2>/dev/null | head -1 || true)"
MCP_PRO_ZIP="$(ls -1 "${ROOT}/game/addons"/godot-mcp-pro*.zip "${ROOT}/game/addons"/godot_mcp_pro*.zip 2>/dev/null | head -1 || true)"

if [[ -d "${ROOT}/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py" ]]; then
  ok "GDAI plugin already extracted"
elif [[ -n "$GDAI_ZIP" ]]; then
  ok "GDAI zip found: $(basename "$GDAI_ZIP")"
else
  fail "GDAI zip missing. Upload to game/addons/gdai-mcp-plugin-godot-*.zip (https://gdaimcp.com/)"
fi

if [[ -f "${ROOT}/tools/godot-mcp-pro-server/build/index.js" ]]; then
  ok "Godot MCP Pro server already built"
elif [[ -n "$MCP_PRO_ZIP" ]]; then
  ok "MCP Pro zip found: $(basename "$MCP_PRO_ZIP")"
else
  fail "MCP Pro zip missing. Upload to game/addons/godot-mcp-pro*.zip (https://godot-mcp.abyo.net/)"
fi

if [[ $PREFLIGHT_ONLY -eq 1 ]]; then
  echo
  echo "Preflight PASS — upload zips present (or plugins already installed)."
  echo "Run without --preflight to execute full bootstrap."
  exit 0
fi

step "Phase 1 — Extract commercial plugins"
bash "${ROOT}/tools/install_gdai_plugin.sh"
bash "${ROOT}/tools/install_godot_mcp_pro.sh"

step "Phase 2 — Core toolchain (Godot, uv, Godotiq, Blender)"
SKIP_MCP_BOOTSTRAP=1 bash "${ROOT}/tools/install_cloud_dev.sh"

step "Phase 3 — MCP stack bootstrap"
bash "${ROOT}/tools/ensure_mcp_stack.sh" --wait 120

step "Phase 4 — Verification"
bash "${ROOT}/tools/check_mcp_ready.sh"
bash "${ROOT}/tools/check_extended_toolchain.sh" || warn "Extended toolchain had warnings (GameLab key optional)"

if curl -sf http://127.0.0.1:3571/tools >/dev/null 2>&1; then
  TOOL_COUNT="$(curl -sf http://127.0.0.1:3571/tools | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('mcp_tools',[])))")"
  ok "GDAI HTTP bridge :3571 — ${TOOL_COUNT} tools"
else
  fail "GDAI HTTP :3571 not responding after bootstrap"
fi

step "Phase 5 — SAVE SNAPSHOT (manual — dashboard)"
echo
echo "Bootstrap PASS. Complete these dashboard steps:"
echo
echo "  1. Open: https://cursor.com/dashboard/cloud-agents/environments/r/github.com/vivivieri/3d-jrpg-adventure-pc-game"
echo "  2. Click **Save snapshot** (or equivalent) in the Setup Agent UI"
echo "  3. Copy the new snapshot id (snapshot-YYYYMMDD-...)"
echo "  4. Update .cursor/environment.json on game/development:"
echo '       "snapshot": "snapshot-NEW-ID-HERE"'
echo "  5. Commit and push game/development"
echo "  6. Register MCP servers in Dashboard → Integrations & MCP:"
echo "       godot-mcp  → uv run ${ROOT}/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
echo "       godotiq    → uvx godotiq"
echo "       godot-mcp-pro → node ${ROOT}/tools/godot-mcp-pro-server/build/index.js --minimal"
echo
echo "Verify next agent boot: cursor-cloud environment-info → build should NOT be null"
echo "Docs: docs/CLOUD_SNAPSHOT_LAUNCH.md"
