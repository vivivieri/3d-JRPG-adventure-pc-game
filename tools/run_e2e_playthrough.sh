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
# NOTE: exit non-zero while unimplemented. Per docs/ACCEPTANCE_CRITERIA.md
# ("skip_is_not_pass") a SKIP must never be indistinguishable from a PASS to
# exit-code-only automation. Change this to `exit 0` only once the real L5
# scenario runner is implemented and actually passes.
exit 1
