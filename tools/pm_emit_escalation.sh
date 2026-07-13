#!/usr/bin/env bash
# Emit GitHub escalation comment body when an agent is stale or blocked.
# Usage: bash tools/pm_emit_escalation.sh <issue_id> [remind|S2|S1|S0|human]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ISSUE_ID="${1:-}"
LEVEL="${2:-remind}"

if [[ -z "$ISSUE_ID" ]]; then
  echo "Usage: bash tools/pm_emit_escalation.sh <issue_id> [level]"
  exit 2
fi

export ISSUE_ID LEVEL ROOT
python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.environ["ROOT"])
issue_id = os.environ["ISSUE_ID"]
level = os.environ["LEVEL"]

board = json.loads((root / "game/data/qa/sprint_board.json").read_text(encoding="utf-8"))
issue = next((i for i in board["issues"] if i["id"] == issue_id), None)
if not issue:
    raise SystemExit(f"Unknown issue {issue_id}")

labels = {
    "remind": "status/in-progress — PM reminder",
    "S2": "severity/S2",
    "S1": "severity/S1",
    "S0": "severity/S0",
    "human": "human — escalate to project owner",
}

print(f"""## PM Escalation — {issue_id}

**Level:** {level} ({labels.get(level, level)})
**Time:** {datetime.now(timezone.utc).isoformat()}
**Agent owner:** agent/{issue.get('agent_owner')}
**Status:** {issue.get('status')}
**Blocked by:** {issue.get('depends_on')}
**Last session:** {issue.get('last_agent_session') or 'never'}

### Required action
1. Run `bash tools/run_agent_session_gate.sh {issue.get('agent_owner')} {issue_id}`
2. Complete work; cite gate IDs: {', '.join(issue.get('acceptance_gate_ids') or [])}
3. PM runs `python3 tools/pm_update_issue.py {issue_id} --status done --commit <sha>`
4. PM re-runs `bash tools/run_pm_orchestrator.sh`

**Policy:** No honor system — orchestrator must PASS before next dispatch.
""")
PY
