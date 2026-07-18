#!/usr/bin/env bash
# Record agent session heartbeat for factory hang detection.
# Usage:
#   bash tools/pm_record_heartbeat.sh --agent pm --issue P1-00 --phase start
#   bash tools/pm_record_heartbeat.sh --agent architect --issue P1-01 --phase progress --note "shader draft"
#   bash tools/pm_record_heartbeat.sh --agent builder --issue P1-02 --phase end
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

AGENT=""
ISSUE_ID=""
PHASE="progress"
NOTE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --phase) PHASE="$2"; shift 2 ;;
    --note) NOTE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$AGENT" ]]; then
  echo "Usage: bash tools/pm_record_heartbeat.sh --agent <role> [--issue <id>] [--phase start|progress|end] [--note text]"
  exit 2
fi

AGENT="${AGENT#agent/}"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ARTIFACT_DIR="${ROOT}/artifacts"
mkdir -p "$ARTIFACT_DIR"
HB_FILE="${ARTIFACT_DIR}/factory_heartbeat.json"

python3 - <<PY
import json
from pathlib import Path

payload = {
    "timestamp": "${TS}",
    "agent_role": "${AGENT}",
    "issue_id": "${ISSUE_ID}" or None,
    "phase": "${PHASE}",
    "note": "${NOTE}" or None,
}
path = Path("${HB_FILE}")
path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload))
PY

# Append to agent session telemetry JSONL (analysis-friendly history)
if [[ -n "${ISSUE_ID}" ]]; then
  bash tools/pm_record_agent_session.sh progress --agent "$AGENT" --issue "$ISSUE_ID" --note "${NOTE:-heartbeat}" 2>/dev/null || true
fi

echo "==> Heartbeat recorded: ${HB_FILE}"
