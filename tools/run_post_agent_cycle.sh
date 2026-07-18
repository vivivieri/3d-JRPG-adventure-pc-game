#!/usr/bin/env bash
# Enforced worker/PM cycle close — replaces honor-system post_agent_steps.
#
# Usage:
#   bash tools/run_post_agent_cycle.sh --issue P1-02 --agent builder --commit <sha>
#   bash tools/run_post_agent_cycle.sh --issue P1-02 --agent qa --commit <sha> --gate L2_scene_primitives --artifact artifacts/...
#   bash tools/run_post_agent_cycle.sh --issue P1-00 --agent pm --commit <sha> --run-orchestrator --alignment-audit
#   bash tools/run_post_agent_cycle.sh --issue P1-02 --agent builder --outcome failed --failed-check L1_unit_tests
#
# Authority: docs/agents/PM_AGENT_RUNBOOK.md · game/data/qa/pm_orchestrator_steps.json
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ISSUE_ID=""
AGENT_ROLE=""
COMMIT_SHA=""
OUTCOME="complete"
FAILED_CHECK=""
NOTE=""
GATE_ID=""
ARTIFACT=""
RUN_ORCHESTRATOR=0
ALIGNMENT_AUDIT=0
SKIP_DONE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue) ISSUE_ID="$2"; shift 2 ;;
    --agent) AGENT_ROLE="$2"; shift 2 ;;
    --commit) COMMIT_SHA="$2"; shift 2 ;;
    --outcome) OUTCOME="$2"; shift 2 ;;
    --failed-check|--check) FAILED_CHECK="$2"; shift 2 ;;
    --note) NOTE="$2"; shift 2 ;;
    --gate) GATE_ID="$2"; shift 2 ;;
    --artifact) ARTIFACT="$2"; shift 2 ;;
    --run-orchestrator) RUN_ORCHESTRATOR=1; shift ;;
    --alignment-audit) ALIGNMENT_AUDIT=1; shift ;;
    --skip-done) SKIP_DONE=1; shift ;;
    -h|--help)
      sed -n '3,12p' "$0"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

AGENT_ROLE="${AGENT_ROLE#agent/}"

if [[ -z "$ISSUE_ID" || -z "$AGENT_ROLE" ]]; then
  echo "Usage: bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> [--commit <sha>] [options]" >&2
  exit 2
fi

COMMIT_SHA="${COMMIT_SHA:-$(git rev-parse HEAD 2>/dev/null || echo unknown)}"

echo "==> Post-agent cycle (enforced — docs/qa/WORKFLOW_INTEGRATION.md)"
echo "    Issue: $ISSUE_ID · Agent: $AGENT_ROLE · Outcome: $OUTCOME · Commit: $COMMIT_SHA"
echo

FAIL=0

run_step() {
  local id="$1"
  local desc="$2"
  shift 2
  echo "── Step: $id — $desc"
  if "$@"; then
    echo "[PASS] $id"
  else
    echo "[FAIL] $id"
    FAIL=1
    return 1
  fi
  echo
}

# 0. Factory halt guard
run_step "factory_halt" "block when factory halted" \
  bash tools/check_factory_halt.sh || exit 2

# 1. Done criteria (success only)
if [[ "$OUTCOME" == "complete" && "$SKIP_DONE" -eq 0 ]]; then
  run_step "check_done_criteria" "verify pr_merged / ci_green / push_only" \
    python3 tools/pm_check_done_criteria.py "$ISSUE_ID" --commit "$COMMIT_SHA" || true
  [[ "$FAIL" -eq 0 ]] || exit 1
fi

# 2. Update board (before cycle event so PM webhook sees done status)
if [[ "$OUTCOME" == "complete" && "$SKIP_DONE" -eq 0 ]]; then
  UPDATE_ARGS=(python3 tools/pm_update_issue.py "$ISSUE_ID" --status done --commit "$COMMIT_SHA" --agent "$AGENT_ROLE")
  run_step "update_board" "mark issue done on sprint board" \
    "${UPDATE_ARGS[@]}" || exit 1
fi

# 3. Cycle event (closes telemetry, stakeholder report, PM webhook — writes session_*.json rollup)
EVENT="agent_cycle_complete"
[[ "$OUTCOME" == "failed" ]] && EVENT="agent_cycle_failed"
CYCLE_ARGS=(bash tools/pm_emit_cycle_event.sh "$EVENT" --issue "$ISSUE_ID" --agent "$AGENT_ROLE" --commit "$COMMIT_SHA")
[[ -n "$FAILED_CHECK" ]] && CYCLE_ARGS+=(--check "$FAILED_CHECK")
[[ -n "$NOTE" ]] && CYCLE_ARGS+=(--note "$NOTE")
run_step "emit_cycle_event" "dispatch PM webhook + close session telemetry" \
  "${CYCLE_ARGS[@]}" || exit 1

# 4. Evidence bundle (after cycle event — session rollup lands in sprint_evidence/<issue>/)
if [[ -n "$GATE_ID" && -n "$ARTIFACT" ]]; then
  run_step "bundle_evidence" "attach gate evidence + session rollup" \
    python3 tools/pm_bundle_evidence.py "$ISSUE_ID" --gate "$GATE_ID" --artifact "$ARTIFACT" || true
  [[ "$FAIL" -eq 0 ]] || exit 1
else
  echo "── Step: bundle_evidence — auto-link session telemetry rollup"
  if python3 tools/pm_bundle_evidence.py "$ISSUE_ID" 2>/dev/null; then
    echo "[PASS] bundle_evidence"
  else
    echo "[WARN] evidence bundle skipped (no session rollup yet — non-blocking)"
  fi
  echo
fi

# 5. Workflow integration registry
run_step "check_feature_integration" "factory workflow registry parity" \
  bash tools/check_feature_integration.sh || true
[[ "$FAIL" -eq 0 ]] || exit 1

# 6. PM-only: alignment audit (non-blocking)
if [[ "$ALIGNMENT_AUDIT" -eq 1 ]]; then
  echo "── Step: alignment_audit — stakeholder alignment snapshot (non-blocking)"
  bash tools/run_alignment_audit.sh --trigger post_merge --note "post_agent_cycle issue=$ISSUE_ID" 2>/dev/null || echo "[WARN] alignment audit skipped"
  echo
fi

# 7. PM-only: re-run orchestrator (same session — e.g. PM closed own issue)
if [[ "$RUN_ORCHESTRATOR" -eq 1 ]]; then
  run_step "re_run_orchestrator" "PM dispatch next agent" \
    bash tools/run_pm_orchestrator.sh || exit 1
fi

echo "==> Post-agent cycle PASS"
echo "    Next: PM Automation should wake from webhook (unless --run-orchestrator already ran)"
exit 0
