#!/usr/bin/env bash
# L0 — ship build security: dev plugin strip policy + optional binary scan.
# Gate: L0_ship_build_security
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CONFIG="${ROOT}/game/data/qa/ship_security.json"
PROJECT="${ROOT}/game/project.godot"

echo "==> Ship build security (docs/qa/SECURITY.md)"
echo ""

if [[ ! -f "$CONFIG" ]]; then
  echo "[FAIL] missing $CONFIG"
  exit 1
fi

python3 - <<'PY' || exit 1
import json
from pathlib import Path
p = Path("game/data/qa/ship_security.json")
data = json.loads(p.read_text())
assert data.get("forbidden_autoloads"), "forbidden_autoloads required"
assert data.get("forbidden_editor_plugin_substrings"), "forbidden_editor_plugin_substrings required"
assert data.get("export_scripts_must_call"), "export_scripts_must_call required"
print(
    f"[OK]   ship_security.json — {len(data['forbidden_autoloads'])} autoload(s), "
    f"{len(data['forbidden_editor_plugin_substrings'])} plugin pattern(s)"
)
PY

REQUIRED_CALL="$(python3 -c "import json; print(json.load(open('game/data/qa/ship_security.json'))['export_scripts_must_call'])")"
for script in tools/export_linux.sh tools/export_windows.sh; do
  if ! grep -q "$REQUIRED_CALL" "$script"; then
    echo "[FAIL] $script must call $REQUIRED_CALL"
    exit 1
  fi
done
echo "[OK]   export scripts call $REQUIRED_CALL"

if [[ -f "$PROJECT" ]]; then
  python3 tools/godot_strip_dev_plugins.py check-after-strip "$PROJECT" || exit 1
else
  echo "[SKIP] no game/project.godot — strip audit deferred"
fi

SCANNED=0
for bin in "${ROOT}/build/TidesOfUrashima.x86_64" "${ROOT}/build/TidesOfUrashima.exe"; do
  if [[ -f "$bin" ]]; then
    python3 - "$bin" <<'PY' || exit 1
import sys
from pathlib import Path

# Import from tools/ without package install
sys.path.insert(0, "tools")
from godot_strip_dev_plugins import load_config, scan_binary_forbidden

path = Path(sys.argv[1])
errs = scan_binary_forbidden(path, load_config())
if errs:
    for e in errs:
        print(f"[FAIL] {e}")
    raise SystemExit(1)
print(f"[OK]   {path.name} — no forbidden dev strings in binary")
PY
    SCANNED=1
  fi
done
if [[ "$SCANNED" -eq 0 ]]; then
  echo "[SKIP] no build/ binaries yet — binary dev-string scan on export smoke"
fi

echo "[PASS] ship build security"
exit 0
