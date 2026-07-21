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
echo "── Asset compliance (ship — strict: missing manifest files FAIL)"
bash tools/check_asset_compliance.sh --strict

echo ""
echo "── VO casting (ship — no PLACEHOLDER_* voice ids)"
VO_CASTING_REQUIRED=1 python3 tools/validate_vo_casting.py

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

if [[ "$CHANNEL" == "prod" ]]; then
  echo ""
  echo "── L6 human playtest sign-off (required for prod)"
  L6_REPORT="${ROOT}/artifacts/qa_reports/L6_human_playtest.json"
  if [[ ! -f "$L6_REPORT" ]]; then
    echo "[FAIL] Missing ${L6_REPORT#"${ROOT}"/}"
    echo "       Run docs/qa/PLAYTEST_SCRIPT.md with min 5 testers; write gate result:"
    echo "       python3 tools/qa_write_gate_result.py --gate L6_human_playtest --status pass \\"
    echo "         --metric completion_percent=80 --metric testers=5 --evidence artifacts/qa_reports/L6_human_playtest.json"
    exit 1
  fi
  python3 - <<'PY' || exit 1
import json
from pathlib import Path
p = Path("artifacts/qa_reports/L6_human_playtest.json")
data = json.loads(p.read_text())
if data.get("status") != "pass" or not data.get("valid_pass"):
    raise SystemExit(f"[FAIL] L6 report status must be pass (got {data.get('status')})")
metrics = data.get("metrics", {})
testers = int(metrics.get("testers", 0) or 0)
if testers < 5:
    raise SystemExit(f"[FAIL] L6 requires min 5 testers (got {testers})")
print(f"[OK]   L6 human playtest signed off ({testers} testers)")
PY
fi

echo ""
echo "CD gates: PASS (channel=${CHANNEL})"
echo "Next: bash tools/export_windows.sh && bash tools/prepare_steam_depot.sh"
echo "See: docs/ci-cd/CD.md, docs/ci-cd/STEAM_RELEASE_CHECKLIST.md"
