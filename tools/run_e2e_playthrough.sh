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

# Pre-Phase-6 dev runs may tolerate SKIP (exit 2). Gate runners treat SKIP as FAIL on
# game branch unless ALLOW_L5_SKIP=1. Phase 6+ / CD must set REQUIRE_L5=1.
if [[ "${REQUIRE_L5:-0}" == "1" ]]; then
  echo "[FAIL] REQUIRE_L5=1 — L5 gate requires a real E2E run, SKIP is not PASS."
  exit 1
fi

if [[ "${ALLOW_L5_SKIP:-0}" == "1" ]]; then
  echo "[SKIP] ALLOW_L5_SKIP=1 — pre-Phase-6 development only"
  exit 2
fi

echo "[FAIL] L5 not implemented — set ALLOW_L5_SKIP=1 only for pre-Phase-6 dev"
exit 1
