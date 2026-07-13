#!/usr/bin/env bash
# L2 zone composition smoke — in-scene path width / golden screenshot checks.
# Main branch: data-only validation via validate_zone_composition.py (L0).
# Game branch: set ZONE_COMPOSITION_STRICT=1 when scenes + screenshots exist.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ZONE_JSON="${ROOT}/game/data/qa/zone_composition.json"
PROJECT="${ROOT}/game/project.godot"
STRICT="${ZONE_COMPOSITION_STRICT:-0}"
WARN=0
FAIL=0

warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }
pass() { echo "[PASS] $1"; }

echo "==> Zone composition smoke (docs/GENERATION_READINESS.md §X-04)"
echo ""

if ! python3 "${ROOT}/tools/validate_zone_composition.py"; then
  fail "L0 zone composition data invalid"
  echo ""
  echo "Zone composition smoke: ${WARN} warning(s), ${FAIL} failure(s)"
  exit 1
fi
pass "L0 zone composition data"

if [[ ! -f "$PROJECT" ]]; then
  warn "No game/project.godot — skipping in-scene composition checks"
  echo ""
  echo "Zone composition smoke: ${WARN} warning(s), ${FAIL} failure(s) (skipped in-scene)"
  exit 0
fi

python3 - <<'PY' "$ZONE_JSON" "$ROOT" "$STRICT"
import json
import sys
from pathlib import Path

zone_path, root_s, strict_s = sys.argv[1:4]
root = Path(root_s)
strict = strict_s == "1"
data = json.loads(Path(zone_path).read_text(encoding="utf-8"))
fail = 0

for zone_id, zone in data.get("zones", {}).items():
    rel = zone.get("scene_path", "").replace("res://", "game/")
    scene_path = root / rel
    if not scene_path.is_file():
        msg = f"Missing scene for {zone_id}: {scene_path.relative_to(root)}"
        if strict:
            print(f"[FAIL] {msg}")
            fail += 1
        else:
            print(f"[WARN] {msg}")
        continue
    print(f"[PASS] Scene exists: {zone_id}")

    golden = zone.get("golden_screenshot")
    if golden:
        gpath = root / golden
        if not gpath.is_file():
            msg = f"Missing golden screenshot for {zone_id}: {golden}"
            if strict:
                print(f"[FAIL] {msg}")
                fail += 1
            else:
                print(f"[WARN] {msg}")
        else:
            print(f"[PASS] Golden screenshot: {zone_id}")

raise SystemExit(1 if fail else 0)
PY
SCENE_EXIT=$?
if [[ "$SCENE_EXIT" -ne 0 ]]; then
  FAIL=$((FAIL + 1))
fi

echo ""
if [[ "$FAIL" -gt 0 ]]; then
  echo "Zone composition smoke: ${WARN} warning(s), ${FAIL} failure(s)"
  exit 1
fi
echo "Zone composition smoke: ${WARN} warning(s), ${FAIL} failure(s)"
exit 0
