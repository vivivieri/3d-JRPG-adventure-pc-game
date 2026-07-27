#!/usr/bin/env bash
# Verify this Cloud Agent booted from the game/development snapshot (not JIT web boot).
# Repo-controlled — runs even when you cannot edit cursor.com/automations.
#
# Usage:
#   bash tools/check_snapshot_boot.sh           # fail if implementation stack missing
#   bash tools/check_snapshot_boot.sh --pm        # warn only (PM docs/orchestrator sessions)
#   bash tools/check_snapshot_boot.sh --report    # print diagnostics, exit 0
#
# Authority: docs/agents/CLOUD_SNAPSHOT_LAUNCH.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="strict"
if [[ "${1:-}" == "--pm" ]]; then
  MODE="pm"
elif [[ "${1:-}" == "--report" ]]; then
  MODE="report"
fi

EXPECTED_SNAPSHOT=""
if [[ -f .cursor/environment.json ]]; then
  EXPECTED_SNAPSHOT="$(python3 -c "import json; print(json.load(open('.cursor/environment.json')).get('snapshot',''))" 2>/dev/null || true)"
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
BOOT_KIND="unknown"
FAILURES=()
WARNINGS=()

# Heuristic: snapshot boot leaves commercial addons on disk; JIT web boot usually does not.
if [[ -f game/project.godot ]]; then
  if [[ -d game/addons/gdai-mcp-plugin-godot ]] && [[ -f game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py ]]; then
    BOOT_KIND="snapshot_or_repaired"
  elif command -v godot4 >/dev/null 2>&1; then
    BOOT_KIND="jit_partial"
    FAILURES+=("GDAI plugin missing at game/addons/gdai-mcp-plugin-godot/ (typical JIT web boot)")
  else
    BOOT_KIND="bootstrap"
    WARNINGS+=("Godot not in PATH — bootstrap or docs-only session")
  fi
else
  BOOT_KIND="docs_only"
  WARNINGS+=("game/project.godot absent — snapshot not required for docs/data work")
fi

if [[ -f game/project.godot ]]; then
  if ! curl -sf http://127.0.0.1:3571/tools >/dev/null 2>&1; then
    if [[ "$BOOT_KIND" == "jit_partial" ]]; then
      FAILURES+=("GDAI HTTP :3571 not responding")
    else
      WARNINGS+=("GDAI HTTP :3571 not responding (run: bash tools/ensure_mcp_stack.sh)")
    fi
  fi
  if [[ ! -d game/addons/godotiq ]]; then
    WARNINGS+=("Godotiq addon missing")
  fi
  if [[ ! -f tools/godot-mcp-pro-server/build/index.js ]]; then
    WARNINGS+=("Godot MCP Pro server not built")
  fi
fi

echo "==> Snapshot boot check"
echo "    Branch: ${BRANCH}"
echo "    Mode: ${MODE}"
echo "    Boot kind (heuristic): ${BOOT_KIND}"
if [[ -n "$EXPECTED_SNAPSHOT" ]]; then
  echo "    Pinned snapshot (environment.json): ${EXPECTED_SNAPSHOT}"
else
  echo "    Pinned snapshot: (none — main/docs boot)"
fi
echo ""
echo "    Signals:"
echo "      - build.snapshotId in cursor-cloud environment-info = definitive PASS"
echo "      - build null + source web + missing GDAI = JIT boot (this pod)"
echo ""
echo "    Who controls launch path (not in git):"
echo "      - Cursor team owner: cursor.com/automations + Cloud Agents → Environments"
echo "      - You (repo): .cursor/environment.json + preflight gates below"
echo ""

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  for w in "${WARNINGS[@]}"; do
    echo "[WARN] $w"
  done
  echo ""
fi

if [[ ${#FAILURES[@]} -gt 0 ]]; then
  for f in "${FAILURES[@]}"; do
    echo "[FAIL] $f"
  done
  echo ""
  echo "Remediation (pick one):"
  echo "  1. Team owner: launch from Cloud Agents → Environments (game/development), not ad-hoc web/GitHub agent"
  echo "  2. Setup Agent: bash tools/rebuild_cloud_snapshot.sh → save snapshot → update .cursor/environment.json"
  echo "  3. JIT workaround: upload GDAI zip to game/addons/ → bash tools/install_gdai_plugin.sh"
  echo "Docs: docs/agents/CLOUD_SNAPSHOT_LAUNCH.md"
  if [[ "$MODE" == "pm" ]]; then
    echo ""
    echo "[WARN] PM mode — continuing, but do NOT dispatch Builder/Architect until snapshot PASS"
    exit 0
  fi
  if [[ "$MODE" == "report" ]]; then
    exit 0
  fi
  exit 1
fi

echo "[PASS] Snapshot boot check (filesystem signals OK)"
if [[ "$BOOT_KIND" == "docs_only" ]]; then
  echo "       Docs/data session — full MCP stack not required"
fi
exit 0
