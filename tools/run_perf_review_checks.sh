#!/usr/bin/env bash
# L2 perf catalog — validate perf_thresholds.json (CI-safe, headless).
# Runtime FPS / draw-call review is L3_perf_review (agent-local):
#   Godotiq godotiq_perf_snapshot after F5 in affected zone.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

THRESHOLDS="${ROOT}/game/data/qa/perf_thresholds.json"

echo "==> Perf review catalog (docs/RENDERING_GUIDE.md, ENVIRONMENT_KITS.md §9)"
echo ""

if [[ ! -f "$THRESHOLDS" ]]; then
  echo "[FAIL] missing $THRESHOLDS"
  exit 1
fi

python3 - <<'PY' || exit 1
import json
from pathlib import Path

p = Path("game/data/qa/perf_thresholds.json")
data = json.loads(p.read_text())

target = data.get("target") or {}
budgets = data.get("budgets") or {}
zones = data.get("zones") or []

assert target.get("min_fps_gameplay", 0) >= 30, "target.min_fps_gameplay too low"
assert budgets.get("max_materials_per_view", 0) > 0, "budgets.max_materials_per_view required"
assert zones, "perf_thresholds.json needs zones[]"

for z in zones:
    assert z.get("id"), "each zone needs id"
    assert z.get("scene_path", "").startswith("res://"), f"{z.get('id')}: scene_path must be res://"

print(f"[OK]   perf_thresholds.json — {len(zones)} zone(s), "
      f"target {target.get('min_fps_gameplay')} FPS @ {target.get('resolution')}, "
      f"≤{budgets.get('max_materials_per_view')} materials/view")
PY

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] L3_perf_review deferred — no game/project.godot yet"
else
  echo "[INFO] L3_perf_review required on scene/visual PRs — Godotiq godotiq_perf_snapshot after F5"
fi

echo "[PASS] perf catalog valid"
exit 0
