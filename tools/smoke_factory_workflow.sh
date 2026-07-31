#!/usr/bin/env bash
# Smoke the PM → docs-pack → session-gate → adherence → docs-CI workflow.
# Use after docs/INDEX or resolve_docs / sprint-pack changes.
#
# Usage:
#   bash tools/smoke_factory_workflow.sh
#   bash tools/smoke_factory_workflow.sh --issue P1-01 --agent architect
#
# Exit 0 only when required steps PASS. Optional game L2 env/MCP checks are
# reported as WARN on docs-only boots (no game/project.godot or MCP down).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=factory_env.sh
source "$ROOT/tools/factory_env.sh"

ISSUE_ID="P1-01"
AGENT_ROLE="architect"
KEEP_BOARD=0
BOARD_BAK=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --agent) AGENT_ROLE="$2"; shift 2 ;;
    --keep-board) KEEP_BOARD=1; shift ;;
    -h|--help)
      sed -n '2,12p' "$0"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

AGENT_ROLE="${AGENT_ROLE#agent/}"
BOARD="$FACTORY_BOARD_PATH"
BOARD_BAK="$(mktemp)"
cp "$BOARD" "$BOARD_BAK"

# shellcheck disable=SC2317 # invoked via trap EXIT
restore_board() {
  if [[ "$KEEP_BOARD" -eq 0 && -n "$BOARD_BAK" && -f "$BOARD_BAK" ]]; then
    cp "$BOARD_BAK" "$BOARD"
    echo "[OK] restored sprint_board.json (smoke does not leave issues in_progress)"
  fi
  if [[ -n "$BOARD_BAK" && -f "$BOARD_BAK" ]]; then
    rm -f "$BOARD_BAK"
  fi
}
trap restore_board EXIT

FAIL=0
pass() { echo "[PASS] $1"; }
warn() { echo "[WARN] $1"; }
fail() { echo "[FAIL] $1"; FAIL=1; }

echo "==> Factory workflow smoke"
echo "    Issue: $ISSUE_ID · Agent: $AGENT_ROLE"
echo

echo "── 1) Sprint pack ↔ board ↔ GitHub"
if python3 tools/pm_sync_sprint_pack.py; then
  pass "pm_sync_sprint_pack"
else
  fail "pm_sync_sprint_pack"
fi
if python3 tools/validate_sprint_phases.py; then
  pass "validate_sprint_phases"
else
  fail "validate_sprint_phases"
fi
if python3 tools/validate_sprint_board.py --strict; then
  pass "validate_sprint_board"
else
  fail "validate_sprint_board"
fi
if python3 tools/pm_sync_github_issues.py --validate; then
  pass "pm_sync_github_issues"
else
  fail "pm_sync_github_issues"
fi
echo

echo "── 2) PM orchestrator"
if bash tools/run_pm_orchestrator.sh >/tmp/smoke_pm_orch.log 2>&1; then
  pass "run_pm_orchestrator"
else
  fail "run_pm_orchestrator (see /tmp/smoke_pm_orch.log)"
  tail -30 /tmp/smoke_pm_orch.log || true
fi
if python3 - <<PY
import json, os, sys
from pathlib import Path
sys.path.insert(0, "tools")
from factory_paths import ORCHESTRATOR_REPORT_PATH
r = json.loads(ORCHESTRATOR_REPORT_PATH.read_text(encoding="utf-8"))
ok = bool(r.get("orchestrator_pass"))
dispatch = r.get("next_dispatch") or []
print(f"    orchestrator_pass={ok} next_dispatch={[d.get('issue_id') for d in dispatch]}")
for d in dispatch:
    print(
        f"    - {d.get('issue_id')} → {d.get('agent')} "
        f"gh=#{d.get('github_issue')} task={d.get('docs_task')} action={d.get('action')}"
    )
sys.exit(0 if ok else 1)
PY
then
  pass "orchestrator_report"
else
  fail "orchestrator_report"
fi
echo

echo "── 3) resolve_docs matrix (roles + Phase1 issues)"
if python3 - <<'PY'
import json, os, subprocess, sys
from pathlib import Path

sys.path.insert(0, "tools")
from factory_paths import BOARD_PATH

roles = subprocess.check_output(
    ["python3", "tools/resolve_docs.py", "--list-roles"], text=True
).split()
board = json.loads(BOARD_PATH.read_text(encoding="utf-8"))
errs = []
over = []
thin = []
for role in roles:
    out = Path("/tmp/smoke_resolve.json")
    cmd = ["python3", "tools/resolve_docs.py", role, "--budget", "12000", "--report", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        errs.append((role, p.stderr or p.stdout))
        continue
    d = json.loads(out.read_text(encoding="utf-8"))
    kept = int(d.get("tokens_kept_est") or 0)
    if kept > 12000:
        over.append((role, kept))
    elif 12000 - kept < 800:
        thin.append((role, kept, 12000 - kept))
for row in board.get("issues") or []:
    owner = row.get("agent_owner")
    iid = row.get("id")
    if owner not in roles:
        continue
    out = Path("/tmp/smoke_resolve.json")
    cmd = [
        "python3", "tools/resolve_docs.py", owner, "--issue", str(iid),
        "--budget", "12000", "--remap-role", "--report", str(out),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        errs.append((f"{owner}:{iid}", p.stderr or p.stdout))
        continue
    d = json.loads(out.read_text(encoding="utf-8"))
    kept = int(d.get("tokens_kept_est") or 0)
    label = f"{owner}:{iid}"
    if kept > 12000:
        over.append((label, kept))
    elif 12000 - kept < 800:
        thin.append((label, kept, 12000 - kept))
print(f"    errors={len(errs)} over_budget={len(over)} headroom<800={len(thin)}")
for e in errs[:5]:
    print("    ERR", e[0], str(e[1])[:160])
for o in over[:5]:
    print("    OVER", o)
for t in thin[:5]:
    print("    THIN", t)
sys.exit(1 if errs or over else 0)
PY
then
  pass "resolve_docs_matrix"
else
  fail "resolve_docs_matrix"
fi
echo

echo "── 4) Session gate + adherence"
if bash tools/run_agent_session_gate.sh "$AGENT_ROLE" "$ISSUE_ID" >/tmp/smoke_gate.log 2>&1; then
  pass "run_agent_session_gate"
else
  fail "run_agent_session_gate (see /tmp/smoke_gate.log)"
  tail -25 /tmp/smoke_gate.log || true
fi
PACK="${FACTORY_ARTIFACTS_DIR}/docs_pack_${ISSUE_ID}.json"
READS="${FACTORY_ARTIFACTS_DIR}/docs_reads_${ISSUE_ID}.log"
if [[ -f "$PACK" && -f "$READS" ]]; then
  # TRIGGER verified: session gate must auto-seed must_read (no honor-system append)
  SEEDED=$(grep -cvE '^\s*(#|$)' "$READS" || true)
  if [[ "${SEEDED:-0}" -gt 0 ]]; then
    pass "docs_reads_auto_seed ($SEEDED paths)"
  else
    fail "docs_reads_auto_seed empty — session gate must call log_docs_read.py --from-pack"
  fi
  if python3 tools/check_docs_pack_adherence.py --issue "$ISSUE_ID" --strict; then
    pass "check_docs_pack_adherence"
  else
    fail "check_docs_pack_adherence"
  fi
else
  fail "docs pack/reads missing after session gate (pack=$PACK reads=$READS)"
fi
echo

echo "── 5) Post-agent cycle (failed outcome — exercises adherence without PR merge)"
# Unset live webhooks — smoke must not depend on Cursor Automation HTTP (often 400 here).
if env -u CURSOR_PM_CYCLE_WEBHOOK_URL -u CURSOR_FACTORY_ALERT_WEBHOOK_URL \
  -u CURSOR_WORKER_WEBHOOK_URL \
  bash tools/run_post_agent_cycle.sh \
  --issue "$ISSUE_ID" --agent "$AGENT_ROLE" --commit "$(git rev-parse HEAD)" \
  --outcome failed --failed-check L1_unit_tests \
  --note "smoke_factory_workflow only" >/tmp/smoke_post_cycle.log 2>&1; then
  pass "run_post_agent_cycle"
else
  fail "run_post_agent_cycle (see /tmp/smoke_post_cycle.log)"
  tail -40 /tmp/smoke_post_cycle.log || true
fi
# Ordering: adherence must appear before emit_cycle_event on the happy failed-outcome path
if awk '/docs_pack_adherence/{a=NR} /emit_cycle_event/{e=NR} END{exit !(a && e && a < e)}' /tmp/smoke_post_cycle.log; then
  pass "adherence_before_webhook"
else
  fail "adherence_before_webhook (docs_pack_adherence must run before emit_cycle_event)"
fi
# FAIL path: empty reads must refuse before board/webhook (status unchanged)
python3 - <<PY
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from factory_paths import BOARD_PATH, artifact_path
board_path = BOARD_PATH
board = json.loads(board_path.read_text(encoding="utf-8"))
issue = "$ISSUE_ID"
before = next(i for i in board["issues"] if i["id"] == issue or str(i.get("github_issue")) == issue)
status_before = before.get("status")
artifact_path(f"docs_reads_{issue}.log").write_text("# wiped for smoke ordering test\n", encoding="utf-8")
print(f"    status_before={status_before}")
PY
if env -u CURSOR_PM_CYCLE_WEBHOOK_URL -u CURSOR_FACTORY_ALERT_WEBHOOK_URL \
  -u CURSOR_WORKER_WEBHOOK_URL \
  bash tools/run_post_agent_cycle.sh \
  --issue "$ISSUE_ID" --agent "$AGENT_ROLE" --commit "$(git rev-parse HEAD)" \
  --outcome complete --skip-done \
  --note "smoke adherence fail ordering" >/tmp/smoke_adhere_fail.log 2>&1; then
  fail "adherence_blocks_close (expected FAIL on empty reads)"
else
  if grep -q "refusing board update / cycle webhook" /tmp/smoke_adhere_fail.log \
    && ! grep -q "\[PASS\] emit_cycle_event" /tmp/smoke_adhere_fail.log; then
    pass "adherence_blocks_close"
  else
    fail "adherence_blocks_close (see /tmp/smoke_adhere_fail.log)"
    tail -30 /tmp/smoke_adhere_fail.log || true
  fi
fi
python3 - <<PY
import json
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from factory_paths import BOARD_PATH
board = json.loads(BOARD_PATH.read_text(encoding="utf-8"))
issue = "$ISSUE_ID"
row = next(i for i in board["issues"] if i["id"] == issue or str(i.get("github_issue")) == issue)
# --skip-done should not mark done; empty-reads FAIL must not either
if row.get("status") == "done":
    raise SystemExit("board marked done despite adherence FAIL")
print(f"    status_after={row.get('status')} (not done — OK)")
PY
echo

echo "── 6) Factory path seam"
if python3 tools/factory_paths.py >/tmp/smoke_factory_paths.json \
  && python3 tools/validate_game_dev_factory_pack.py; then
  pass "factory_paths_and_pack"
else
  fail "factory_paths_and_pack"
fi
echo

echo "── 7) Docs CI"
if bash tools/run_docs_ci_checks.sh >/tmp/smoke_docs_ci.log 2>&1; then
  pass "run_docs_ci_checks"
else
  fail "run_docs_ci_checks (see /tmp/smoke_docs_ci.log)"
  rg -n "FAIL" /tmp/smoke_docs_ci.log | head -20 || true
fi
echo

if [[ -f game/project.godot ]]; then
  echo "── 8) Game branch note"
  warn "game/project.godot present — also run: bash tools/run_ci_checks.sh"
  warn "L2 'Dev environment healthy' needs Godot+MCP; docs-pack changes do not gate that"
  echo
fi

echo "==> Smoke summary: $([[ "$FAIL" -eq 0 ]] && echo PASS || echo FAIL)"
exit "$FAIL"
