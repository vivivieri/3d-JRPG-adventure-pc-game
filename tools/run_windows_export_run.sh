#!/usr/bin/env bash
# L2 — Windows export + native run smoke (windows-latest CI or reference_pc_gtx1060).
# Gate: L2_windows_export_run
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=export_lib.sh
source "${ROOT}/tools/export_lib.sh"

export_godot_env "$ROOT"

echo "==> Windows export + run smoke (docs/qa/PLATFORM_SUPPORT.md)"
echo ""

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot"
  exit 2
fi

# shellcheck source=gate_lib.sh
source "${ROOT}/tools/gate_lib.sh"
if gate_is_phase1_bootstrap; then
  echo "[SKIP] phase 1 bootstrap — export deferred until main_scene set"
  exit 2
fi

if ! is_windows_host; then
  echo "[SKIP] not a Windows host — run on GitHub Actions windows-latest or reference_pc_gtx1060"
  echo "       Linux CI uses: bash tools/run_windows_cross_export.sh (build only)"
  exit 2
fi

if ! export_require_godot; then
  exit 1
fi

bash "${ROOT}/tools/export_windows.sh"

EXE="${ROOT}/build/TidesOfUrashima.exe"
if [[ ! -f "$EXE" ]]; then
  echo "[FAIL] Windows exe missing after export: $EXE"
  exit 1
fi

echo "==> Running exported Windows build (headless, quit-after 120)..."
set +e
timeout 120 "$EXE" --headless --audio-driver Dummy --quit-after 120 2>&1
RC=$?
set -e

if [[ "$RC" -eq 0 ]]; then
  echo "==> Post-export ship security scan..."
  bash "${ROOT}/tools/check_ship_build_security.sh" || exit 1
  echo "[PASS] Windows export run smoke — .exe ran headless"
  exit 0
fi

echo "[FAIL] Windows export run smoke — exit $RC"
exit 1
