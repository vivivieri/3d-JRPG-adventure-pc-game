#!/usr/bin/env bash
# E2E playthrough tests (L5) — enabled Phase 6+.
# See docs/AI_DEV_WORKFLOW.md §2 and Phase 6 acceptance criteria.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> E2E playthrough tests"
echo ""
echo "[SKIP] Not implemented yet — required at Phase 6 gate."
echo "       Add game/tests/e2e/test_three_endings.gd and wire here."
echo "       See docs/AI_DEV_WORKFLOW.md §3.1 and §4 Phase 6."
echo ""
exit 0
