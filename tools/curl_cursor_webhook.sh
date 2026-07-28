#!/usr/bin/env bash
# POST JSON to a Cursor automation webhook with optional auth header.
#
# Usage:
#   bash tools/curl_cursor_webhook.sh pm    @artifacts/agent_cycle_event.json
#   bash tools/curl_cursor_webhook.sh alert @artifacts/agent_cycle_event.json
#   bash tools/curl_cursor_webhook.sh worker @artifacts/worker_dispatch_event.json
#   bash tools/curl_cursor_webhook.sh --url "$URL" --auth "$AUTH" --data @file.json
#
# Auth secret format (from automation → Generate auth header):
#   - "Bearer <token>"  (recommended)
#   - "<token>"         (Bearer prefix added automatically)
#   - "Authorization: Bearer <token>" (used as-is)
set -euo pipefail

format_auth_header() {
  local auth="${1:-}"
  [[ -z "$auth" ]] && return 0
  if [[ "$auth" == Authorization:* ]]; then
    printf '%s' "$auth"
  elif [[ "$auth" == Bearer\ * ]]; then
    printf 'Authorization: %s' "$auth"
  else
    printf 'Authorization: Bearer %s' "$auth"
  fi
}

URL=""
AUTH=""
DATA_FILE=""
KIND=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    pm|alert|worker)
      KIND="$1"
      shift
      ;;
    --url)
      URL="$2"
      shift 2
      ;;
    --auth)
      AUTH="$2"
      shift 2
      ;;
    --data)
      DATA_FILE="$2"
      shift 2
      ;;
    @*)
      DATA_FILE="${1#@}"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

case "$KIND" in
  pm)
    URL="${URL:-${CURSOR_PM_CYCLE_WEBHOOK_URL:-}}"
    AUTH="${AUTH:-${CURSOR_PM_WEBHOOK_AUTH:-}}"
    ;;
  alert)
    URL="${URL:-${CURSOR_FACTORY_ALERT_WEBHOOK_URL:-}}"
    AUTH="${AUTH:-${CURSOR_ALERT_WEBHOOK_AUTH:-}}"
    ;;
  worker)
    URL="${URL:-${CURSOR_WORKER_WEBHOOK_URL:-}}"
    AUTH="${AUTH:-${CURSOR_WORKER_WEBHOOK_AUTH:-}}"
    ;;
esac

if [[ -z "$URL" ]]; then
  echo "[FAIL] webhook URL not set" >&2
  exit 1
fi

if [[ -z "$DATA_FILE" || ! -f "$DATA_FILE" ]]; then
  echo "[FAIL] data file required and must exist: ${DATA_FILE:-<missing>}" >&2
  exit 1
fi

if [[ -z "$AUTH" ]]; then
  echo "[WARN] webhook auth not set — POST may return HTTP 401" >&2
fi

HDR="$(format_auth_header "$AUTH")"
ARGS=(-sS -w '%{http_code}' -o /tmp/cursor_webhook_resp.txt -X POST "$URL" -H "Content-Type: application/json" --data-binary "@${DATA_FILE}")
if [[ -n "$HDR" ]]; then
  ARGS+=(-H "$HDR")
fi

HTTP_CODE="$(curl "${ARGS[@]}")"
if [[ "$HTTP_CODE" =~ ^2 ]]; then
  echo "[OK]   Cursor webhook HTTP ${HTTP_CODE}"
  exit 0
fi

echo "[FAIL] Cursor webhook HTTP ${HTTP_CODE}" >&2
cat /tmp/cursor_webhook_resp.txt >&2 || true
exit 1
