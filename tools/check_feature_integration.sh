#!/usr/bin/env bash
# Remind agents of workflow integration rules + verify registry parity.
# Run before committing any cross-cutting factory feature (telemetry, PM hooks, secrets).
#
# Usage:
#   bash tools/check_feature_integration.sh          # verify only
#   bash tools/check_feature_integration.sh --remind # print rules + verify
#
# Authority: docs/qa/WORKFLOW_INTEGRATION.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REMIND=0
[[ "${1:-}" == "--remind" ]] && REMIND=1

if [[ "$REMIND" -eq 1 ]]; then
  echo "==> Factory feature integration rule (agents MUST follow before merge)"
  echo "    Authority: docs/qa/WORKFLOW_INTEGRATION.md"
  echo
  echo "  When adding or changing a cross-cutting factory feature:"
  echo "  1. Register in game/data/qa/workflow_integration_registry.json"
  echo "  2. Wire script hooks (session gate, cycle events, orchestrator, watchdog)"
  echo "  3. Update authority doc + all required_doc_refs in registry"
  echo "  4. Add secrets to check_day_one_secrets.sh if needed"
  echo "  5. Run: python3 tools/validate_workflow_integration.py (must PASS)"
  echo "  6. Run: bash tools/run_docs_ci_checks.sh"
  echo
  echo "  Cross-cutting = touches PM dispatch, agent sessions, secrets, cycle events,"
  echo "  orchestrator steps, watchdog, or stakeholder reports."
  echo
fi

python3 tools/validate_workflow_integration.py
