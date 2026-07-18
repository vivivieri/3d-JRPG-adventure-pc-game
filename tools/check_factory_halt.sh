#!/usr/bin/env bash
# Block agent work when factory halt flag is set.
# Authority: docs/agents/FACTORY_WATCHDOG.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATE="${ROOT}/artifacts/factory_state.json"

if [[ ! -f "$STATE" ]]; then
  exit 0
fi

HALTED="$(python3 -c "import json; d=json.load(open('$STATE')); print('yes' if d.get('halted') else 'no')")"
if [[ "$HALTED" != "yes" ]]; then
  exit 0
fi

REASON="$(python3 -c "import json; print(json.load(open('$STATE')).get('halt_reason','unknown'))")"
echo "[FAIL] Factory HALTED — no agent dispatch or cycle close until human clears:"
echo "       Reason: $REASON"
echo "       Fix issue, then: bash tools/run_factory_watchdog.sh --clear-halt"
echo "       Authority: docs/agents/FACTORY_WATCHDOG.md"
exit 2
