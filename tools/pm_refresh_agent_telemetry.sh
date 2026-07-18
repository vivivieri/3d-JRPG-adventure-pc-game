#!/usr/bin/env bash
# Backfill pending token usage and regenerate analysis reports (non-blocking).
# Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

REPORT_DIR="${ROOT}/artifacts/agent_session_reports"
EVENTS="${ROOT}/artifacts/agent_session_telemetry/events.jsonl"

echo "==> Agent telemetry refresh"

if [[ -z "${CURSOR_API_KEY:-}" && -z "${CURSOR_API_TOKEN:-}" ]]; then
  echo "[WARN] CURSOR_API_KEY not set — token backfill skipped (docs/agents/CURSOR_SECRETS_SETUP.md §8)"
else
  python3 tools/pm_sync_agent_session_tokens.py 2>/dev/null || echo "[WARN] token sync incomplete (API may lag)"
fi

if [[ ! -f "$EVENTS" ]]; then
  echo "[SKIP] No events.jsonl yet — first agent session will create it"
  exit 0
fi

mkdir -p "$REPORT_DIR"
python3 tools/analyze_agent_session_telemetry.py \
  --json "$REPORT_DIR/latest.json" \
  --csv "$REPORT_DIR/sessions.csv" \
  --markdown "$REPORT_DIR/latest.md" \
  2>/dev/null || echo "[WARN] telemetry analysis skipped"

echo "[OK] Telemetry refresh complete → $REPORT_DIR"
