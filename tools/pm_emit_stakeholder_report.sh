#!/usr/bin/env bash
# Generate stakeholder status report + optional Telegram to product owner.
#
# Usage:
#   bash tools/pm_emit_stakeholder_report.sh --trigger agent_cycle_complete --issue P1-01 --agent architect
#   bash tools/pm_emit_stakeholder_report.sh --trigger sprint_cycle_complete --telegram
#   bash tools/pm_emit_stakeholder_report.sh --trigger pm_session
#   bash tools/pm_emit_stakeholder_report.sh --trigger phase_exit --telegram
#
# Secrets (Cursor / GitHub):
#   TELEGRAM_BOT_TOKEN — from @BotFather
#   TELEGRAM_CHAT_ID   — your chat id (message @userinfobot or getUpdates)
#
# Authority: docs/PM_STAKEHOLDER_REPORTING.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TRIGGER=""
ISSUE_ID=""
AGENT_ROLE=""
COMMIT_SHA=""
NOTE=""
SEND_TELEGRAM=""
FORCE_TELEGRAM=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --trigger) TRIGGER="$2"; shift 2 ;;
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --agent) AGENT_ROLE="$2"; shift 2 ;;
    --commit) COMMIT_SHA="$2"; shift 2 ;;
    --note) NOTE="$2"; shift 2 ;;
    --telegram) FORCE_TELEGRAM=1; shift ;;
    --no-telegram) SEND_TELEGRAM="false"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$TRIGGER" ]]; then
  echo "Usage: bash tools/pm_emit_stakeholder_report.sh --trigger <event> [options]"
  echo "Triggers: agent_cycle_complete | agent_cycle_failed | sprint_cycle_complete | phase_exit | uat_ready | pm_session | watchdog_recovery | mcp_blocked"
  exit 2
fi

export TRIGGER ISSUE_ID AGENT_ROLE COMMIT_SHA NOTE SEND_TELEGRAM FORCE_TELEGRAM ROOT
python3 <<'PY'
import json
import os
import sys
from pathlib import Path

root = Path(os.environ["ROOT"])
sys.path.insert(0, str(root / "tools"))
from pm_stakeholder_report_lib import emit_report

event_file = root / "artifacts/agent_cycle_event.json"
event_payload = None
if event_file.is_file():
    event_payload = json.loads(event_file.read_text(encoding="utf-8"))

send_flag = None
if os.environ.get("SEND_TELEGRAM") == "false":
    send_flag = False
elif os.environ.get("FORCE_TELEGRAM") == "1":
    send_flag = True

result = emit_report(
    trigger=os.environ["TRIGGER"],
    issue_id=os.environ.get("ISSUE_ID") or None,
    agent_role=os.environ.get("AGENT_ROLE") or None,
    commit_sha=os.environ.get("COMMIT_SHA") or None,
    note=os.environ.get("NOTE") or None,
    event_payload=event_payload,
    send_telegram_flag=send_flag,
)

print("==> Stakeholder report")
print(f"    Headline: {result['report'].get('headline')}")
for k, v in result["paths"].items():
    print(f"    {k}: {v}")
tg = result["telegram"]
if tg.get("sent"):
    print(f"[OK]   Telegram → product owner ({tg.get('detail')})")
else:
    print(f"[INFO] Telegram: {tg.get('detail')}")

# Write emit receipt for PM audit
receipt = root / "artifacts/stakeholder_reports/last_emit.json"
receipt.parent.mkdir(parents=True, exist_ok=True)
receipt.write_text(json.dumps({"trigger": os.environ["TRIGGER"], "telegram": tg, "paths": result["paths"]}, indent=2) + "\n", encoding="utf-8")
PY
