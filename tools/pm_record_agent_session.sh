#!/usr/bin/env bash
# Record agent session telemetry event (start / progress / end).
# Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
#
# Usage:
#   bash tools/pm_record_agent_session.sh start  --agent builder --issue P1-02
#   bash tools/pm_record_agent_session.sh progress --agent builder --issue P1-02 --note "GDAI scene pass"
#   bash tools/pm_record_agent_session.sh end --agent builder --issue P1-02 --outcome complete
#   bash tools/pm_record_agent_session.sh end --agent architect --issue P1-01 --outcome failed --check L1_gdscript_lint
#
# Token self-report (optional, session end):
#   export AGENT_TOKENS_INPUT=180000 AGENT_TOKENS_OUTPUT=45000 AGENT_TOKENS_TOTAL=225000
#   bash tools/pm_record_agent_session.sh end --agent builder --issue P1-02
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ACTION="${1:-}"
shift || true

if [[ -z "$ACTION" ]]; then
  echo "Usage: bash tools/pm_record_agent_session.sh <start|progress|end> --agent <role> [--issue <id>] [options]"
  exit 2
fi

AGENT=""
ISSUE_ID=""
NOTE=""
OUTCOME="complete"
FAILED_CHECK=""
ERROR_MSG=""
GATES_PASSED=""
GATES_FAILED=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --note) NOTE="$2"; shift 2 ;;
    --outcome) OUTCOME="$2"; shift 2 ;;
    --check) FAILED_CHECK="$2"; shift 2 ;;
    --error) ERROR_MSG="$2"; shift 2 ;;
    --gates-passed) GATES_PASSED="$2"; shift 2 ;;
    --gates-failed) GATES_FAILED="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$AGENT" ]]; then
  echo "[FAIL] --agent required" >&2
  exit 2
fi

export AST_ACTION="$ACTION"
export AST_AGENT="${AGENT#agent/}"
export AST_ISSUE_ID="$ISSUE_ID"
export AST_NOTE="$NOTE"
export AST_OUTCOME="$OUTCOME"
export AST_FAILED_CHECK="$FAILED_CHECK"
export AST_ERROR_MSG="$ERROR_MSG"
export AST_GATES_PASSED="$GATES_PASSED"
export AST_GATES_FAILED="$GATES_FAILED"

python3 - <<'PY'
import json
import os
import sys

sys.path.insert(0, "tools")
from agent_session_telemetry_lib import end_session, progress_session, start_session

action = os.environ.get("AST_ACTION", "")
agent = os.environ.get("AST_AGENT", "")
issue_id = os.environ.get("AST_ISSUE_ID") or None
note = os.environ.get("AST_NOTE") or None
outcome = os.environ.get("AST_OUTCOME", "complete")
failed_check = os.environ.get("AST_FAILED_CHECK") or None
error_message = os.environ.get("AST_ERROR_MSG") or None
gates_passed_raw = os.environ.get("AST_GATES_PASSED", "")
gates_failed_raw = os.environ.get("AST_GATES_FAILED", "")
gates_passed = [g.strip() for g in gates_passed_raw.split(",") if g.strip()] or None
gates_failed = [g.strip() for g in gates_failed_raw.split(",") if g.strip()] or None

if action == "start":
    ev = start_session(agent, issue_id, note=note)
elif action == "progress":
    ev = progress_session(agent, issue_id, note=note)
    if ev is None:
        print("[WARN] No active session — starting one automatically")
        start_session(agent, issue_id)
        ev = progress_session(agent, issue_id, note=note)
elif action in ("end", "fail", "failed"):
    if action in ("fail", "failed"):
        outcome = "failed"
    ev = end_session(
        agent,
        issue_id,
        outcome=outcome,
        failed_check=failed_check,
        error_message=error_message,
        note=note,
        gates_passed=gates_passed,
        gates_failed=gates_failed,
    )
else:
    print(f"[FAIL] Unknown action: {action}", file=sys.stderr)
    sys.exit(2)

if ev:
    print(json.dumps(ev, indent=2))
    print(f"==> Logged {ev.get('event')} session_id={ev.get('session_id')}")
PY
