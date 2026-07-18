#!/usr/bin/env bash
# Verify agent session telemetry can auto-fetch tokens from Cursor API.
# Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
WARN=0

ok() { echo "[OK]   $1"; PASS=$((PASS + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }
warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }

echo "==> Agent session telemetry readiness (docs/qa/AGENT_SESSION_TELEMETRY.md)"

if [[ -n "${CURSOR_API_KEY:-}" || -n "${CURSOR_API_TOKEN:-}" ]]; then
  ok "CURSOR_API_KEY set (auto token fetch enabled)"
else
  fail "CURSOR_API_KEY not set — add to Cursor Secrets (docs/agents/CURSOR_SECRETS_SETUP.md §8)"
fi

if [[ -n "${CURSOR_CONVERSATION_ID:-}" ]]; then
  ok "CURSOR_CONVERSATION_ID=${CURSOR_CONVERSATION_ID} (cloud agent bcId auto-detected)"
elif [[ -n "${CURSOR_AGENT:-}" ]]; then
  warn "Cloud agent env present but CURSOR_CONVERSATION_ID missing — token auto-fetch needs bcId"
else
  warn "Not a cloud agent session — bcId must be passed explicitly for token fetch"
fi

python3 tools/validate_agent_session_telemetry_schema.py >/dev/null && ok "telemetry schema valid" || fail "schema validation failed"

if [[ -f artifacts/agent_session_telemetry/events.jsonl ]]; then
  lines=$(wc -l < artifacts/agent_session_telemetry/events.jsonl | tr -d ' ')
  ok "events.jsonl present ($lines events)"
else
  warn "no events.jsonl yet — will be created on first agent session"
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: agent telemetry ready (warnings=$WARN)"
  exit 0
fi
echo "FAIL: $FAIL blocking issue(s) — warnings=$WARN"
exit 1
