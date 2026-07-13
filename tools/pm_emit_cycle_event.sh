#!/usr/bin/env bash
# Emit agent cycle completion event — triggers PM Cloud Agent via webhook (event-driven).
# Usage:
#   bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-01 --agent architect --commit <sha>
#   bash tools/pm_emit_cycle_event.sh sprint_cycle_complete --sprint Phase1-Sprint1 --next-sprint 2
#   bash tools/pm_emit_cycle_event.sh uat_ready --tag v0.9.0-rc1 --commit <sha>
#
# Requires (one of):
#   CURSOR_PM_CYCLE_WEBHOOK_URL — Cursor Automation webhook URL (Secrets)
#   GH workflow: gh workflow run agent-cycle-pm.yml (uses repository_dispatch)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

EVENT="${1:-}"
shift || true

if [[ -z "$EVENT" ]]; then
  echo "Usage: bash tools/pm_emit_cycle_event.sh <event> [options]"
  echo "Events: agent_cycle_complete | sprint_cycle_complete | ci_cycle_complete | uat_ready | mcp_blocked | watchdog_recovery | factory_halt"
  exit 2
fi

ISSUE_ID=""
AGENT_ROLE=""
COMMIT_SHA=""
SPRINT_ID=""
BRANCH="game/development"
NEXT_SPRINT=""
TAG=""
FAILED_CHECK=""
NOTES=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --agent) AGENT_ROLE="$2"; shift 2 ;;
    --commit) COMMIT_SHA="$2"; shift 2 ;;
    --sprint) SPRINT_ID="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --next-sprint) NEXT_SPRINT="$2"; shift 2 ;;
    --tag) TAG="$2"; shift 2 ;;
    --check) FAILED_CHECK="$2"; shift 2 ;;
    --note) NOTES="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

# Defaults from sprint board
if [[ -f game/data/qa/sprint_board.json ]]; then
  SPRINT_ID="${SPRINT_ID:-$(python3 -c "import json; print(json.load(open('game/data/qa/sprint_board.json'))['active_sprint']['id'])")}"
fi
COMMIT_SHA="${COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null || echo unknown)}"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ARTIFACT_DIR="${ROOT}/artifacts"
mkdir -p "$ARTIFACT_DIR"
EVENT_FILE="${ARTIFACT_DIR}/agent_cycle_event.json"

python3 - <<PY
import json
from pathlib import Path

payload = {
    "event": "${EVENT}",
    "timestamp": "${TS}",
    "issue_id": "${ISSUE_ID}" or None,
    "agent_role": "${AGENT_ROLE}" or None,
    "commit_sha": "${COMMIT_SHA}",
    "sprint_id": "${SPRINT_ID}" or None,
    "branch": "${BRANCH}",
    "next_sprint_number": int("${NEXT_SPRINT}") if "${NEXT_SPRINT}".isdigit() else None,
    "tag": "${TAG}" or None,
    "failed_check": "${FAILED_CHECK}" or None,
    "note": "${NOTES}" or None,
    "repo": "vivivieri/3d-JRPG-adventure-pc-game",
    "pm_command": "bash tools/run_pm_orchestrator.sh",
}
Path("${EVENT_FILE}").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload))
PY

echo ""
echo "==> Cycle event written: ${EVENT_FILE}"

# Append to cycle log for watchdog stall detection
python3 - <<'LOGPY'
import json
from pathlib import Path
src = Path("artifacts/agent_cycle_event.json")
log = Path("artifacts/factory_cycle_log.jsonl")
if src.is_file():
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        fh.write(src.read_text(encoding="utf-8").strip() + "\n")
LOGPY

# Marker for optional CI secondary trigger (avoid naked CI→PM loops)
if [[ "$EVENT" == "agent_cycle_complete" || "$EVENT" == "sprint_cycle_complete" || "$EVENT" == "watchdog_recovery" ]]; then
  echo "cycle_pending=${EVENT} commit=${COMMIT_SHA}" > "${ARTIFACT_DIR}/.cycle_pending"
fi

DISPATCHED=0

if [[ -n "${CURSOR_PM_CYCLE_WEBHOOK_URL:-}" ]]; then
  echo "==> POST Cursor PM cycle webhook"
  HTTP_CODE="$(curl -sS -o /tmp/cursor_webhook_resp.txt -w '%{http_code}' \
    -X POST "${CURSOR_PM_CYCLE_WEBHOOK_URL}" \
    -H "Content-Type: application/json" \
    -d @"${EVENT_FILE}")"
  if [[ "$HTTP_CODE" =~ ^2 ]]; then
    echo "[OK]   Cursor webhook HTTP ${HTTP_CODE}"
    DISPATCHED=1
  else
    echo "[FAIL] Cursor webhook HTTP ${HTTP_CODE}" >&2
    cat /tmp/cursor_webhook_resp.txt >&2 || true
    exit 1
  fi
fi

if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "==> repository_dispatch agent-cycle-pm"
  if gh api repos/:owner/:repo/dispatches \
    -f event_type="agent-cycle" \
    -f "client_payload[event]=${EVENT}" \
    -f "client_payload[commit_sha]=${COMMIT_SHA}" \
    -f "client_payload[issue_id]=${ISSUE_ID}" \
    -f "client_payload[sprint_id]=${SPRINT_ID}" 2>/dev/null; then
    echo "[OK]   GitHub repository_dispatch sent"
    DISPATCHED=1
  fi
fi

if [[ "$DISPATCHED" -eq 0 ]]; then
  echo "[WARN] No webhook configured — set CURSOR_PM_CYCLE_WEBHOOK_URL in Cursor Secrets"
  echo "       or configure GitHub dispatch. Event saved locally for manual PM trigger."
  echo "       Manual: start PM Cloud Agent with prompt referencing ${EVENT_FILE}"
  exit 0
fi

echo "==> PM cycle event dispatched — expect PM Automation to start next orchestrator run"
exit 0
