#!/usr/bin/env bash
# L2 perf catalog — validate perf_thresholds.json + perf_baseline.json (CI-safe, headless).
# Runtime FPS / draw-call review is L3_perf_review (agent-local):
#   Godotiq godotiq_perf_snapshot on reference_pc_gtx1060 — see docs/PERFORMANCE_BASELINE.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

THRESHOLDS="${ROOT}/game/data/qa/perf_thresholds.json"
BASELINE="${ROOT}/game/data/qa/perf_baseline.json"

echo "==> Perf review catalog (docs/PERFORMANCE_BASELINE.md)"
echo ""

if [[ ! -f "$THRESHOLDS" ]]; then
  echo "[FAIL] missing $THRESHOLDS"
  exit 1
fi

if [[ ! -f "$BASELINE" ]]; then
  echo "[FAIL] missing $BASELINE"
  exit 1
fi

python3 - <<'PY' || exit 1
import json
from pathlib import Path

thresholds = json.loads(Path("game/data/qa/perf_thresholds.json").read_text())
baseline = json.loads(Path("game/data/qa/perf_baseline.json").read_text())

target = thresholds.get("target") or {}
budgets = thresholds.get("budgets") or {}
zones = thresholds.get("zones") or []
baseline_id = thresholds.get("baseline_id")
baselines = baseline.get("baselines") or {}
primary = baseline.get("primary_baseline_id")

assert target.get("min_fps_gameplay", 0) >= 30, "target.min_fps_gameplay too low"
assert budgets.get("max_materials_per_view", 0) > 0, "budgets.max_materials_per_view required"
assert zones, "perf_thresholds.json needs zones[]"
assert baseline_id, "perf_thresholds.json needs baseline_id"
assert primary, "perf_baseline.json needs primary_baseline_id"
assert baseline_id in baselines, f"baseline_id {baseline_id!r} missing from perf_baseline.json"
assert baselines[baseline_id].get("valid_for_l3_perf_review") is True, (
    f"{baseline_id} must be valid_for_l3_perf_review"
)

for z in zones:
    assert z.get("id"), "each zone needs id"
    assert z.get("scene_path", "").startswith("res://"), f"{z.get('id')}: scene_path must be res://"

schema = baseline.get("evidence_schema") or {}
assert schema.get("required_fields"), "perf_baseline.json needs evidence_schema.required_fields"

print(
    f"[OK]   perf_thresholds.json — {len(zones)} zone(s), "
    f"baseline {baseline_id}, target {target.get('min_fps_gameplay')} FPS @ {target.get('resolution')}"
)
print(f"[OK]   perf_baseline.json — {len(baselines)} profile(s), primary {primary}")
PY

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] L3_perf_review deferred — no game/project.godot yet"
else
  echo "[INFO] L3_perf_review requires reference_pc_gtx1060 — not cloud/CI (docs/PERFORMANCE_BASELINE.md §5)"
fi

echo "[PASS] perf catalog valid"
exit 0
