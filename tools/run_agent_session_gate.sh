#!/usr/bin/env bash
# Gate for non-PM agents — must be dispatched by PM orchestrator before work.
# Usage: bash tools/run_agent_session_gate.sh <agent_role> <issue_id>
# Authority: docs/ops/agents/SPRINT_ORCHESTRATION.md
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

# Factory halt — block all worker sessions
if ! bash tools/check_factory_halt.sh; then
  exit 2
fi

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
        print("Policy: one agent role per session (docs/ops/agents/MULTI_AGENT_BRANCH_STRATEGY.md)")
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

# Progressive disclosure — role ∪ task ∪ issue handoff_refs ∪ briefs (budgeted)
# Specialty remap: builder + zone_lighting → builder_zone (tools/docs_role_map.py)
DOCS_TASK="${AGENT_DOCS_TASK:-}"
if [[ -z "$DOCS_TASK" ]]; then
  DOCS_TASK="$(python3 - <<PY
import json
from pathlib import Path
board = json.loads(Path("game/data/qa/sprint_board.json").read_text(encoding="utf-8"))
for issue in board.get("issues") or []:
    if str(issue.get("id") or "") == "$ISSUE_ID" or str(issue.get("github_issue") or "") == "$ISSUE_ID":
        print(issue.get("docs_task") or "")
        break
PY
)"
fi
DOCS_ROLE="$(python3 tools/docs_role_map.py "$AGENT" "${DOCS_TASK:-}")"
DOCS_BUDGET="${AGENT_DOCS_BUDGET:-12000}"
mkdir -p "$ROOT/artifacts"
DOCS_REPORT="$ROOT/artifacts/docs_pack_${ISSUE_ID}.txt"
# Reads log — session gate auto-seeds must_read; post-cycle enforces --strict
export DOCS_READ_LOG="${DOCS_READ_LOG:-$ROOT/artifacts/docs_reads_${ISSUE_ID}.log}"
: > "$DOCS_READ_LOG"
echo "# Auto-seeded must_read by session gate; extras: python3 tools/log_docs_read.py --issue $ISSUE_ID <path>" >> "$DOCS_READ_LOG"
echo "# Session gate initialized $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$DOCS_READ_LOG"
RESOLVE_ARGS=("$DOCS_ROLE" --issue "$ISSUE_ID" --budget "$DOCS_BUDGET" --report "$DOCS_REPORT" --remap-role)
if [[ -n "$DOCS_TASK" ]]; then
  RESOLVE_ARGS+=(--task "$DOCS_TASK")
fi
echo ""
echo "[DOCS] Role pack ($DOCS_ROLE${DOCS_TASK:+ / task=$DOCS_TASK}) + issue $ISSUE_ID (budget≈${DOCS_BUDGET}; report=$DOCS_REPORT):"
echo "       Reads log: $DOCS_READ_LOG (auto-seed must_read; strict check at post-cycle)"
if python3 tools/resolve_docs.py "${RESOLVE_ARGS[@]}" --check \
  >/tmp/resolve_docs_check.txt 2>&1; then
  python3 tools/resolve_docs.py "${RESOLVE_ARGS[@]}" | sed 's/^/       /'
  echo "       [OK] wrote $DOCS_REPORT (+ ${DOCS_REPORT%.txt}.json)"
else
  echo "[FAIL] resolve_docs.py failed for role=$DOCS_ROLE issue=$ISSUE_ID — refusing BOOT-only fallback"
  sed 's/^/       /' /tmp/resolve_docs_check.txt || true
  echo "       Fix INDEX paths / handoff_refs, then re-run session gate."
  exit 1
fi
# TRIGGER: seed must_read into reads log (follower = post-cycle --strict)
if ! python3 tools/log_docs_read.py --issue "$ISSUE_ID" --from-pack --log "$DOCS_READ_LOG"; then
  echo "[FAIL] log_docs_read.py --from-pack — cannot enforce docs pack adherence"
  exit 1
fi

# Agent session telemetry — session start (warn once if API key missing)
if [[ -z "${CURSOR_API_KEY:-}" && -z "${CURSOR_API_TOKEN:-}" ]]; then
  echo "[WARN] CURSOR_API_KEY not set — tokens will not auto-log (docs/ops/agents/CURSOR_SECRETS_SETUP.md §8)"
fi
bash tools/pm_record_agent_session.sh start --agent "$AGENT" --issue "$ISSUE_ID" 2>/dev/null || true

# Heartbeat — worker session start
bash tools/pm_record_heartbeat.sh --agent "$AGENT" --issue "$ISSUE_ID" --phase start 2>/dev/null || true

echo ""
echo "[RULE] End every worker session (mandatory — enforced script):"
echo "       bash tools/run_post_agent_cycle.sh --issue $ISSUE_ID --agent $AGENT --commit \$(git rev-parse HEAD)"
echo "[RULE] Cross-cutting factory features → workflow_integration_registry.json"
echo "       bash tools/check_feature_integration.sh --remind · docs/ops/qa/WORKFLOW_INTEGRATION.md"
