#!/usr/bin/env bash
# PM Agent / Sprint Master — mandatory session entrypoint.
# Fails non-zero if any step missed — no honor system.
# Authority: docs/PM_AGENT_RUNBOOK.md, docs/SPRINT_ORCHESTRATION.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export ROOT

# Heartbeat — PM session start (watchdog hang detection)
bash tools/pm_record_heartbeat.sh --agent pm --phase start --note "orchestrator" 2>/dev/null || true

python3 <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

root = Path(os.environ["ROOT"])
steps_path = root / "game/data/qa/pm_orchestrator_steps.json"
data = json.loads(steps_path.read_text(encoding="utf-8"))

print("==> PM Orchestrator — enforced session workflow")
print("    Authority: docs/PM_AGENT_RUNBOOK.md")
print()

for step in data.get("session_steps", []):
    if not step.get("block_on_fail", True):
        continue
    n = step["step"]
    sid = step["id"]
    cmd = step["command"]
    print(f"── Step {n}: {sid}")
    print(f"    {cmd}")
    rc = subprocess.call(cmd, shell=True, cwd=root)
    if rc != 0:
        print(f"[FAIL] Step {n} ({sid}) — PM session BLOCKED (exit {rc})")
        print()
        print("PM ORCHESTRATOR: FAILED — do not assign agents until fixed")
        print("Docs: docs/PM_AGENT_RUNBOOK.md")
        # Record fail for watchdog
        from datetime import datetime, timezone
        from pathlib import Path
        import json
        state_path = root / "artifacts/factory_state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state = {}
        if state_path.is_file():
            state = json.loads(state_path.read_text(encoding="utf-8"))
        state["last_orchestrator_result"] = "fail"
        state["last_orchestrator_at"] = datetime.now(timezone.utc).isoformat()
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        sys.exit(1)
    print(f"[PASS] Step {n} ({sid})")
    print()

print("PM ORCHESTRATOR: PASS")
# Record pass for watchdog
from datetime import datetime, timezone
from pathlib import Path
import json
state_path = root / "artifacts/factory_state.json"
state_path.parent.mkdir(parents=True, exist_ok=True)
state = {}
if state_path.is_file():
    state = json.loads(state_path.read_text(encoding="utf-8"))
state["last_orchestrator_result"] = "pass"
state["last_orchestrator_at"] = datetime.now(timezone.utc).isoformat()
state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
print()
print("Next: assign agent per artifacts/pm_orchestrator_report.json → next_dispatch")
print("After agent session: python3 tools/pm_update_issue.py <id> --status done --commit <sha>")
print("Then re-run: bash tools/run_pm_orchestrator.sh")
PY
