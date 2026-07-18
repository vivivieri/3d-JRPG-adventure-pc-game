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
  echo "Events: agent_cycle_complete | agent_cycle_failed | sprint_cycle_complete | ci_cycle_complete | uat_ready | mcp_blocked | watchdog_recovery | factory_halt"
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

# Cycle log + health snapshot (committed path for remote watchdog)
python3 - <<'SNAPPY'
import os
import sys
sys.path.insert(0, "tools")
from pm_event_lib import append_cycle_log, write_health_snapshot

payload_path = __import__("pathlib").Path("artifacts/agent_cycle_event.json")
if payload_path.is_file():
    import json
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    append_cycle_log(payload)
    status = "halted" if payload.get("event") in ("mcp_blocked", "factory_halt") else "active"
    write_health_snapshot(
        event=payload.get("event"),
        issue_id=payload.get("issue_id"),
        agent_role=payload.get("agent_role"),
        commit_sha=payload.get("commit_sha"),
        sprint_id=payload.get("sprint_id"),
        status=status,
        note=payload.get("note"),
    )
    print("==> Health snapshot: game/data/qa/factory_health_snapshot.json")
SNAPPY

# Agent session telemetry — close session on cycle complete/fail
if [[ "$EVENT" == "agent_cycle_complete" || "$EVENT" == "agent_cycle_failed" ]]; then
  OUTCOME="complete"
  [[ "$EVENT" == "agent_cycle_failed" ]] && OUTCOME="failed"
  END_ARGS=(end --agent "$AGENT_ROLE" --outcome "$OUTCOME")
  [[ -n "$ISSUE_ID" ]] && END_ARGS+=(--issue "$ISSUE_ID")
  [[ -n "$FAILED_CHECK" ]] && END_ARGS+=(--check "$FAILED_CHECK")
  [[ -n "$NOTES" ]] && END_ARGS+=(--note "$NOTES")
  bash tools/pm_record_agent_session.sh "${END_ARGS[@]}" 2>/dev/null || true
  # Backfill tokens + refresh analysis reports (non-blocking)
  bash tools/pm_refresh_agent_telemetry.sh 2>/dev/null || true
  # Enrich webhook payload with session telemetry (PM + stakeholder reports)
  python3 - <<'TELEMETRY_ENRICH'
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from agent_session_telemetry_lib import read_events

event_path = Path("artifacts/agent_cycle_event.json")
if not event_path.is_file():
    sys.exit(0)

payload = json.loads(event_path.read_text(encoding="utf-8"))
issue_id = payload.get("issue_id")
agent_role = payload.get("agent_role")
if not issue_id and not agent_role:
    sys.exit(0)

terminal = None
for ev in reversed(read_events()):
    if ev.get("event") not in ("session_end", "session_failed", "session_token_backfill"):
        continue
    if issue_id and ev.get("issue_id") != issue_id:
        continue
    if agent_role and ev.get("agent_role") != agent_role:
        continue
    terminal = ev
    break

if not terminal:
    sys.exit(0)

for key in (
    "session_id",
    "duration_seconds",
    "task_category",
    "tokens_total",
    "tokens_input",
    "tokens_output",
    "model_name",
    "cursor_bc_id",
    "tokens_source",
    "tokens_fetch_status",
):
    if terminal.get(key) is not None:
        payload[key] = terminal[key]

event_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print("==> Cycle event enriched with agent session telemetry")
TELEMETRY_ENRICH
fi

# mcp_blocked / factory_halt → stop automatic recovery
if [[ "$EVENT" == "mcp_blocked" || "$EVENT" == "factory_halt" ]]; then
  bash tools/run_factory_watchdog.sh --halt "${NOTES:-$EVENT}" 2>/dev/null || true
  ALERT_URL="${CURSOR_FACTORY_ALERT_WEBHOOK_URL:-}"
  if [[ -n "$ALERT_URL" ]]; then
    curl -sf -X POST "$ALERT_URL" -H "Content-Type: application/json" -d @"${EVENT_FILE}" || true
  fi
fi

# Stakeholder status report → product owner (Telegram when TELEGRAM_* secrets set)
echo "==> Stakeholder report for product owner"
bash tools/pm_emit_stakeholder_report.sh \
  --trigger "$EVENT" \
  ${ISSUE_ID:+--issue "$ISSUE_ID"} \
  ${AGENT_ROLE:+--agent "$AGENT_ROLE"} \
  ${COMMIT_SHA:+--commit "$COMMIT_SHA"} \
  ${NOTES:+--note "$NOTES"} \
  || echo "[WARN] Stakeholder report failed (non-blocking)"

# If last issue closed the sprint, also send sprint-cycle summary
if [[ "$EVENT" == "agent_cycle_complete" ]]; then
  SPRINT_DONE="$(python3 -c "
import json
b=json.load(open('game/data/qa/sprint_board.json'))
issues=b.get('issues',[])
done=sum(1 for i in issues if i.get('status')=='done')
print('yes' if issues and done==len(issues) else 'no')
" 2>/dev/null || echo no)"
  if [[ "$SPRINT_DONE" == "yes" ]]; then
    bash tools/pm_emit_stakeholder_report.sh --trigger sprint_cycle_complete \
      ${ISSUE_ID:+--issue "$ISSUE_ID"} \
      ${COMMIT_SHA:+--commit "$COMMIT_SHA"} \
      || true
  fi
fi

# agent_cycle_failed → PM webhook (remediation, not next issue)
if [[ "$EVENT" == "agent_cycle_failed" ]]; then
  echo "cycle_pending=${EVENT} commit=${COMMIT_SHA}" > "${ARTIFACT_DIR}/.cycle_pending"
fi

# Marker for optional CI secondary trigger (avoid naked CI→PM loops)
if [[ "$EVENT" == "agent_cycle_complete" || "$EVENT" == "sprint_cycle_complete" || "$EVENT" == "watchdog_recovery" || "$EVENT" == "agent_cycle_failed" ]]; then
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
