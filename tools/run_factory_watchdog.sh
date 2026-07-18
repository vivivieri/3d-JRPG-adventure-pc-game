#!/usr/bin/env bash
# Factory watchdog — stall/hang detection and exception recovery.
#
# Normal PM dispatch stays event-driven (pm_emit_cycle_event.sh).
# This script is the EXCEPTION layer when the factory is idle too long or hung.
#
# Usage:
#   bash tools/run_factory_watchdog.sh              # analyze only
#   bash tools/run_factory_watchdog.sh --recover    # emit watchdog_recovery if needed
#   bash tools/run_factory_watchdog.sh --halt "reason"
#   bash tools/run_factory_watchdog.sh --clear-halt   # human operator only
#
# Authority: docs/agents/FACTORY_WATCHDOG.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

MODE="analyze"
HALT_REASON=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --recover) MODE="recover"; shift ;;
    --halt) MODE="halt"; HALT_REASON="${2:-operator halt}"; shift 2 ;;
    --clear-halt) MODE="clear_halt"; shift ;;
    --json) MODE="json"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

export ROOT MODE HALT_REASON
python3 <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(os.environ["ROOT"])
mode = os.environ["MODE"]
halt_reason = os.environ.get("HALT_REASON", "")

sys.path.insert(0, str(root / "tools"))
from factory_watchdog_lib import (  # noqa: E402
    analyze_health,
    clear_halt,
    load_factory_state,
    record_recovery,
    set_halt,
    write_health_report,
)

if mode == "halt":
    state = load_factory_state()
    set_halt(state, halt_reason or "operator halt")
    print(f"[HALT] Factory halted: {halt_reason}")
    sys.exit(2)

if mode == "clear_halt":
    state = load_factory_state()
    clear_halt(state)
    print("[OK] Factory halt cleared — resume with pm_emit_cycle_event or watchdog --recover")
    sys.exit(0)

report = analyze_health()
report_path = write_health_report(report)

if mode == "json":
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["status"] in ("healthy", "idle_ok") else 1)

print("==> Factory Watchdog")
print(f"    Status: {report['status']}")
print(f"    Sprint: {report.get('sprint_id')}")
print(f"    Incomplete: {report.get('incomplete')}")
print(f"    Recommended: {report.get('recommended_action')}")
if report.get("findings"):
    print("\nFindings:")
    for f in report["findings"]:
        print(f"  - [{f.get('severity')}] {f.get('code')}: {json.dumps(f, default=str)[:200]}")
print(f"\nReport: {report_path.relative_to(root)}")

if report["status"] in ("healthy", "idle_ok"):
    print("\n[WATCHDOG] HEALTHY — no recovery needed")
    sys.exit(0)

if report["status"] == "halted":
    print("\n[WATCHDOG] HALTED — human must clear with: bash tools/run_factory_watchdog.sh --clear-halt")
    sys.exit(2)

if mode != "recover":
    print("\n[WATCHDOG] UNHEALTHY — run with --recover to trigger PM recovery (if allowed)")
    sys.exit(1)

action = report.get("recommended_action")
if action not in ("watchdog_recovery", "escalate_and_recover", "halt_and_human"):
    print(f"\n[WATCHDOG] No automatic recovery for action={action}")
    sys.exit(1)

if not report.get("can_recover"):
    reason = report.get("recover_block_reason", "blocked")
    state = load_factory_state()
    set_halt(state, f"recovery exhausted: {reason}")
    print(f"\n[CRITICAL] Recovery blocked — factory halted: {reason}")
    # Human alert webhook optional
    alert_url = os.environ.get("CURSOR_FACTORY_ALERT_WEBHOOK_URL", "")
    if alert_url:
        payload = {
            "event": "factory_halt",
            "reason": reason,
            "report": report,
        }
        subprocess.run(
            ["curl", "-sf", "-X", "POST", alert_url, "-H", "Content-Type: application/json", "-d", json.dumps(payload)],
            check=False,
        )
    sys.exit(2)

issue_id = report.get("recovery_issue_id") or ""
state = load_factory_state()
record_recovery(state, issue_id or None, report["status"])

# Escalate stale agents before recovery
for finding in report.get("findings", []):
    if finding.get("code") == "stale_agent":
        for stale in finding.get("issues", []):
            sid = stale.get("issue_id")
            if sid:
                esc = subprocess.run(
                    ["bash", "tools/pm_emit_escalation.sh", sid, "S2"],
                    cwd=root,
                    capture_output=True,
                    text=True,
                )
                print(f"\n==> Escalation body for {sid} (post to GitHub issue):")
                print(esc.stdout)

print("\n==> Emitting watchdog_recovery event")
cmd = [
    "bash", "tools/pm_emit_cycle_event.sh", "watchdog_recovery",
    "--issue", issue_id,
    "--agent", "watchdog",
    "--note", f"status={report['status']} action={action}",
]
rc = subprocess.call(cmd, cwd=root)
if rc != 0:
    print("[FAIL] watchdog_recovery dispatch failed", file=sys.stderr)
    sys.exit(rc)

print("\n[WATCHDOG] Recovery dispatched — PM Automation should start orchestrator")
sys.exit(0)
PY

# Non-blocking: backfill token usage + refresh efficiency reports
bash tools/pm_refresh_agent_telemetry.sh 2>/dev/null || true
