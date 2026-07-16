#!/usr/bin/env bash
# Verify day-one Cursor / runtime secrets are set (values not printed).
# Authority: docs/agents/CURSOR_SECRETS_SETUP.md
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REQUIRED=(
  CURSOR_PM_CYCLE_WEBHOOK_URL
  CURSOR_FACTORY_ALERT_WEBHOOK_URL
  GAMELAB_API_KEY
  GH_TOKEN
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID
  ELEVENLABS_API_KEY
)

PASS=0
FAIL=0

check_secret() {
  local name="$1"
  local val="${!name:-}"
  if [[ -n "$val" ]]; then
    echo "[OK]   $name set"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $name not set — see docs/agents/CURSOR_SECRETS_SETUP.md"
    FAIL=$((FAIL + 1))
  fi
}

echo "==> Day-one secrets (docs/agents/CURSOR_SECRETS_SETUP.md)"
for name in "${REQUIRED[@]}"; do
  check_secret "$name"
done

if command -v gh >/dev/null 2>&1 && [[ -n "${GH_TOKEN:-}" ]]; then
  if gh auth status >/dev/null 2>&1; then
    echo "[OK]   gh authenticated"
  else
    echo "[WARN] GH_TOKEN set but gh auth status failed"
  fi
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "PASS: all ${#REQUIRED[@]} day-one secrets present"
  exit 0
fi

echo "FAIL: $FAIL missing — configure in Cursor Secrets (Personal + Runtime Secret)"
exit 1
