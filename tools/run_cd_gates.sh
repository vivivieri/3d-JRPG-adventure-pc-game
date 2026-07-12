#!/usr/bin/env bash
# Pre-export CD gates — run before artifact or Steam deploy.
# Usage: bash tools/run_cd_gates.sh [--channel rc|beta|prod]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CHANNEL="rc"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --channel) CHANNEL="${2:-rc}"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

echo "==> CD pre-export gates (channel: ${CHANNEL})"
echo ""

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[FAIL] game/project.godot missing — tag from game/development branch"
  exit 1
fi

echo "── Full game CI (L0–L2 + L4)"
bash tools/run_ci_checks.sh

echo ""
echo "── Asset compliance (ship)"
bash tools/check_asset_compliance.sh

case "$CHANNEL" in
  rc)
    echo ""
    echo "[OK]   RC channel — L5 E2E optional (run manually for beta/prod)"
    ;;
  beta|prod)
    echo ""
    echo "── L5 E2E three endings (required for ${CHANNEL})"
    REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh
    ;;
  *)
    echo "[FAIL] Unknown channel: ${CHANNEL} (use rc, beta, prod)"
    exit 2
    ;;
esac

echo ""
echo "CD gates: PASS (channel=${CHANNEL})"
echo "Next: bash tools/export_windows.sh && bash tools/prepare_steam_depot.sh"
echo "See: docs/CD.md, docs/STEAM_RELEASE_CHECKLIST.md"
