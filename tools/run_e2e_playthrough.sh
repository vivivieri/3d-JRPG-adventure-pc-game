#!/usr/bin/env bash
# E2E playthrough tests (L5) — required before human QA.
# See docs/AI_TESTING_SPEC.md §7 and docs/AI_DEV_WORKFLOW.md Phase 6 / Phase 8.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> E2E playthrough tests (L5)"
echo ""
echo "[SKIP] Not implemented yet — required at Phase 6 gate."
echo ""
echo "BLOCKS: Human QA (L6) cannot start until this script exits 0 (not SKIP)."
echo "IMPLEMENT: game/tests/e2e/test_three_endings.gd"
echo "SPEC:     docs/AI_TESTING_SPEC.md §7"
echo ""

# SKIP is never PASS at a gate (acceptance_criteria.json: skip_allowed=false for
# L5_e2e_three_endings). Gate runners (Phase 6+) must set REQUIRE_L5=1 so this
# stub fails loudly; pre-Phase-6 per-commit runs tolerate the SKIP with exit 0.
if [[ "${REQUIRE_L5:-0}" == "1" ]]; then
  echo "[FAIL] REQUIRE_L5=1 — L5 gate requires a real E2E run, SKIP is not PASS."
  exit 1
fi
exit 0
