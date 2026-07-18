#!/usr/bin/env bash
# Gate for non-PM agents — must be dispatched by PM orchestrator before work.
# Usage: bash tools/run_agent_session_gate.sh <agent_role> <issue_id>
# Authority: docs/agents/SPRINT_ORCHESTRATION.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

AGENT="${1:-}"
ISSUE_ID="${2:-}"
REPORT="${ROOT}/artifacts/pm_orchestrator_report.json"

if [[ -z "$AGENT" || -z "$ISSUE_ID" ]]; then
  echo "Usage: bash tools/run_agent_session_gate.sh <agent_role> <issue_id>"
  echo "Example: bash tools/run_agent_session_gate.sh architect P1-01"
  exit 2
fi

# Normalize agent/ prefix
AGENT="${AGENT#agent/}"

if [[ ! -f "$REPORT" ]]; then
  echo "[FAIL] No orchestrator report — PM must run: bash tools/run_pm_orchestrator.sh"
  exit 1
fi

export AGENT ISSUE_ID REPORT ROOT
python3 <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path(os.environ["ROOT"])
report_path = Path(os.environ["REPORT"])
agent = os.environ["AGENT"]
issue_id = os.environ["ISSUE_ID"]

report = json.loads(report_path.read_text(encoding="utf-8"))
dispatch = report.get("next_dispatch", [])

allowed = [
    d for d in dispatch
    if d.get("issue_id") == issue_id
    and (d.get("agent") == agent or d.get("co_agent") == agent)
]

if not allowed:
    print(f"[FAIL] Agent session gate — {agent} not dispatched for {issue_id}")
    print("PM must run: bash tools/run_pm_orchestrator.sh")
    print("Read: artifacts/pm_dispatch_packet.json")
    print("Current next_dispatch:")
    for d in dispatch:
        print(f"  - {d.get('issue_id')} → {d.get('agent')} ({d.get('action')})")
    sys.exit(1)

# Strict role — owner or co_agent only (no architect wearing builder hat)
board_path = root / "game/data/qa/sprint_board.json"
board = json.loads(board_path.read_text(encoding="utf-8"))
issue_row = next((i for i in board.get("issues", []) if i.get("id") == issue_id), None)
strict = os.environ.get("AGENT_SESSION_STRICT_ROLE", "1") != "0"
if strict and issue_row:
    owner = issue_row.get("agent_owner")
    co = issue_row.get("co_agent")
    if agent not in (owner, co):
        print(f"[FAIL] Strict role — {agent} cannot run issue owned by {owner}")
        print("Policy: one agent role per session (docs/agents/MULTI_AGENT_BRANCH_STRATEGY.md)")
        sys.exit(1)

# Mark in_progress on board if still pending
for issue in board.get("issues", []):
    if issue.get("id") == issue_id:
        if issue.get("status") == "pending":
            from datetime import datetime, timezone
            issue["status"] = "in_progress"
            issue["last_agent_session"] = datetime.now(timezone.utc).isoformat()
            board_path.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"[OK] Marked {issue_id} in_progress")
        break

print(f"[OK] Agent session gate PASS — {agent} cleared for {issue_id}")
print(f"     Gates: {', '.join(allowed[0].get('acceptance_gate_ids') or [])}")
PY

# Agent session telemetry — session start
bash tools/pm_record_agent_session.sh start --agent "$AGENT" --issue "$ISSUE_ID" 2>/dev/null || true

# Heartbeat — worker session start
bash tools/pm_record_heartbeat.sh --agent "$AGENT" --issue "$ISSUE_ID" --phase start 2>/dev/null || true
