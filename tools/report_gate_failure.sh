#!/usr/bin/env bash
# Format a GitHub Issue body for gate failures (agents + CI).
# Usage: bash tools/report_gate_failure.sh --gate L0_story_data --env qa --commit abc1234 [--log-file path]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GATE=""
ENV="qa"
COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
LOG_FILE=""
WORKFLOW_URL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gate) GATE="${2:-}"; shift 2 ;;
    --env) ENV="${2:-}"; shift 2 ;;
    --commit) COMMIT="${2:-}"; shift 2 ;;
    --log-file) LOG_FILE="${2:-}"; shift 2 ;;
    --workflow-url) WORKFLOW_URL="${2:-}"; shift 2 ;;
    *) echo "Unknown: $1"; exit 2 ;;
  esac
done

if [[ -z "$GATE" ]]; then
  echo "Usage: report_gate_failure.sh --gate <gate_id> [--env qa] [--commit SHA] [--log-file path]"
  exit 2
fi

echo "## Gate failure report"
echo ""
echo "| Field | Value |"
echo "|-------|-------|"
echo "| Gate ID | \`${GATE}\` |"
echo "| Environment | \`${ENV}\` |"
echo "| Commit | \`${COMMIT}\` |"
[[ -n "$WORKFLOW_URL" ]] && echo "| Actions run | ${WORKFLOW_URL} |"
echo ""
echo "### Log excerpt"
echo '```'
if [[ -n "$LOG_FILE" && -f "$LOG_FILE" ]]; then
  tail -n 40 "$LOG_FILE"
else
  echo "(no log file — paste CI output)"
fi
echo '```'
echo ""
echo "### Remediation"
echo "Run: \`bash tools/qa_emit_remediation.sh <brief-id>\`"
echo ""
echo "### Labels"
echo "\`env/${ENV}\` \`gate/${GATE}\` \`agent/qa\` \`status/in-progress\`"
