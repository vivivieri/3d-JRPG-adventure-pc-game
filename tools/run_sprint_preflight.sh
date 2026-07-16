#!/usr/bin/env bash
# Sprint preflight — MCP + toolchain before worker dispatch.
# Emits mcp_blocked + factory halt on failure.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Sprint preflight (MCP + extended toolchain)"

if [[ ! -f game/project.godot ]] && [[ "${SPRINT_PREFLIGHT_MODE:-auto}" == "auto" ]]; then
  echo "[SKIP] MCP preflight — game/project.godot absent (bootstrap / docs-only sprint)"
  echo "[PASS] Sprint preflight (bootstrap mode)"
  exit 0
fi

FAIL=0
for cmd in "bash tools/check_mcp_ready.sh" "bash tools/check_extended_toolchain.sh"; do
  echo "── $cmd"
  if $cmd; then
    echo "[PASS] $cmd"
  else
    echo "[FAIL] $cmd"
    FAIL=1
  fi
done

if [[ "$FAIL" -ne 0 ]]; then
  echo ""
  echo "[BLOCK] Preflight failed — dispatch blocked"
  bash tools/pm_emit_cycle_event.sh mcp_blocked --check "sprint_preflight" --note "MCP or toolchain check failed" 2>/dev/null || true
  bash tools/run_factory_watchdog.sh --halt "mcp_blocked: sprint preflight failed" 2>/dev/null || true
  exit 1
fi

echo ""
echo "[PASS] Sprint preflight"
exit 0
