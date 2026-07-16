#!/usr/bin/env bash
# L2 — Cross-export Windows .exe from Linux CI (build only, no run).
# Gate: L2_windows_cross_export
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=export_lib.sh
source "${ROOT}/tools/export_lib.sh"

export_godot_env "$ROOT"

echo "==> Windows cross-export smoke (build only — run on windows-latest CI)"
echo ""

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot"
  exit 2
fi

if is_windows_host; then
  echo "[INFO] Windows host — use run_windows_export_run.sh for export + run"
  exec bash "${ROOT}/tools/run_windows_export_run.sh"
fi

if ! export_require_godot; then
  exit 1
fi

bash "${ROOT}/tools/export_windows.sh"

EXE="${ROOT}/build/TidesOfUrashima.exe"
if [[ ! -f "$EXE" ]]; then
  echo "[FAIL] Windows exe missing after cross-export: $EXE"
  exit 1
fi

# PE signature check (MZ header)
HEADER="$(head -c 2 "$EXE" | od -An -tx1 | tr -d ' \n')"
if [[ "$HEADER" != "4d5a" ]]; then
  echo "[FAIL] $EXE does not look like a Windows PE binary (missing MZ)"
  exit 1
fi

ls -lh "$EXE"
echo "[PASS] Windows cross-export smoke — .exe built (run verified on windows-latest CI)"
exit 0
