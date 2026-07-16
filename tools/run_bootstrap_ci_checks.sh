#!/usr/bin/env bash
# P1-00 bootstrap CI — same runner as game CI with phase-1 bootstrap skip policy.
# See game/data/qa/acceptance_criteria.json → issue_bootstrap.P1-00
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PHASE1_BOOTSTRAP_CI=1

echo "==> Bootstrap CI (P1-00 profile)"
echo "    Policy: acceptance_criteria.json → issue_bootstrap.P1-00"
echo "    Deferred until main_scene + GDAI scenes: export, GLB import, strict animation"
echo ""

exec bash tools/run_ci_checks.sh
