#!/usr/bin/env bash
# L2 — Linux export + native headless run (cloud / ubuntu CI).
# Gate: L2_linux_export_smoke
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=export_lib.sh
source "${ROOT}/tools/export_lib.sh"

export_godot_env "$ROOT"

echo "==> Linux export + run smoke (docs/qa/PLATFORM_SUPPORT.md)"
echo ""

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot"
  exit 2
fi

if ! export_require_godot; then
  exit 1
fi

bash "${ROOT}/tools/export_linux.sh"

BIN="${ROOT}/build/TidesOfUrashima.x86_64"
if [[ ! -x "$BIN" ]]; then
  chmod +x "$BIN" 2>/dev/null || true
fi
if [[ ! -f "$BIN" ]]; then
  echo "[FAIL] Linux binary missing after export: $BIN"
  exit 1
fi

echo "==> Running exported Linux build (headless, quit-after 120)..."
set +e
if command -v xvfb-run >/dev/null 2>&1; then
  timeout 90 xvfb-run -a "$BIN" --headless --audio-driver Dummy --quit-after 120 2>&1
else
  timeout 90 "$BIN" --headless --audio-driver Dummy --quit-after 120 2>&1
fi
RC=$?
set -e

if [[ "$RC" -eq 0 ]]; then
  echo "==> Post-export ship security scan..."
  bash "${ROOT}/tools/check_ship_build_security.sh" || exit 1
  echo "[PASS] Linux export smoke — binary ran headless"
  exit 0
fi

echo "[FAIL] Linux export smoke — exit $RC"
exit 1
