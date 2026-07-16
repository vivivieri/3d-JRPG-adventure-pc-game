#!/usr/bin/env bash
# L0 — player build protection policy (PCK encryption path, save HMAC spec, Steam DRM).
# Gate: L0_player_build_protection
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Player build protection (docs/qa/SECURITY.md §9)"
echo ""

python3 - <<'PY' || exit 1
import json
from pathlib import Path

root = Path(".")
sec = json.loads((root / "game/data/qa/ship_security.json").read_text())
pb = sec.get("player_build_protection")
if not pb:
    raise SystemExit("[FAIL] ship_security.json missing player_build_protection")
for key in ("pck_encryption", "save_integrity", "steam_drm"):
    if key not in pb:
        raise SystemExit(f"[FAIL] player_build_protection missing {key}")
print("[OK]   ship_security.json player_build_protection block")
PY

python3 tools/validate_save_integrity_spec.py || exit 1

for script in tools/export_linux.sh tools/export_windows.sh; do
  if ! grep -q "export_ship_protection_begin" "$script"; then
    echo "[FAIL] $script must call export_ship_protection_begin"
    exit 1
  fi
done
echo "[OK]   export scripts call export_ship_protection_begin"

for tool in \
  tools/export_apply_pck_encryption.py \
  tools/generate_ship_protection_keys.sh \
  tools/build_godot_export_templates_encrypted.sh; do
  if [[ ! -f "$tool" ]]; then
    echo "[FAIL] missing $tool"
    exit 1
  fi
done
echo "[OK]   ship protection tooling present"

DRM="$(python3 -c "import json; print(json.load(open('game/data/qa/ship_security.json'))['player_build_protection']['steam_drm']['policy'])")"
echo "[OK]   Steam DRM policy: ${DRM}"

if [[ "${SHIP_RELEASE:-0}" == "1" ]]; then
  for var in GODOT_SCRIPT_ENCRYPTION_KEY GODOT_SAVE_HMAC_KEY; do
    if [[ -z "${!var:-}" ]]; then
      echo "[FAIL] SHIP_RELEASE=1 requires $var"
      exit 1
    fi
  done
  if [[ -z "${GODOT_CUSTOM_TEMPLATE_LINUX:-}" && -z "${GODOT_CUSTOM_TEMPLATE_WINDOWS:-}" ]]; then
    echo "[FAIL] SHIP_RELEASE=1 requires custom encrypted export template path(s)"
    exit 1
  fi
  echo "[OK]   SHIP_RELEASE secrets and template paths configured"
else
  echo "[SKIP] SHIP_RELEASE not set — RC key/template enforcement deferred"
fi

echo "[PASS] player build protection"
exit 0
