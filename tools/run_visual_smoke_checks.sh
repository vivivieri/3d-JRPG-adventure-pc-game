#!/usr/bin/env bash
# L2 visual smoke: palette + multi-LLM jury when ruined_village screenshots exist.
# WARN (exit 0) when screenshots or API keys missing — see docs/VISUAL_QA.md §2G.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SCREENSHOT_DIR="${ROOT}/artifacts/screenshots"
ZONE="${VISUAL_SMOKE_ZONE:-ruined_village}"
WARN=0
FAIL=0

warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }
pass() { echo "[PASS] $1"; }

find_gameplay_screenshot() {
  local candidate
  for candidate in \
    "${SCREENSHOT_DIR}/phase1_${ZONE}_gameplay.png" \
    "${SCREENSHOT_DIR}/phase1_${ZONE}_gameplay_"*.png \
    "${SCREENSHOT_DIR}/"*"${ZONE}"*gameplay*.png \
    "${SCREENSHOT_DIR}/"*"${ZONE}"*.png; do
    if [[ -f "$candidate" ]]; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

echo "==> Visual smoke checks (docs/VISUAL_QA.md)"
echo "    Zone: ${ZONE}"
echo ""

if ! SCREENSHOT="$(find_gameplay_screenshot)"; then
  warn "Visual jury skipped — no ${ZONE} screenshot in artifacts/screenshots/"
  echo "       Expected e.g. artifacts/screenshots/phase1_${ZONE}_gameplay.png"
  echo "       Capture via GDAI MCP after Phase 1 ruined_village slice."
  echo ""
  echo "Visual smoke: ${WARN} warning(s), ${FAIL} failure(s) (skipped)"
  exit 0
fi

echo "    Screenshot: ${SCREENSHOT#${ROOT}/}"
echo ""

if python3 "${ROOT}/tools/check_screenshot_palette.py" \
  --zone "$ZONE" \
  --screenshot "$SCREENSHOT"; then
  pass "Screenshot palette check (${ZONE})"
else
  fail "Screenshot palette check (${ZONE})"
fi

JURY_LOG="$(mktemp)"
set +e
python3 "${ROOT}/tools/review_screenshot_vision.py" \
  --zone "$ZONE" \
  --scene ruined_village.tscn \
  --view gameplay \
  --screenshot "$SCREENSHOT" \
  --min-pass "${VISUAL_JURY_MIN_PASS:-2}" \
  >"$JURY_LOG" 2>&1
JURY_EXIT=$?
set -e
cat "$JURY_LOG"
rm -f "$JURY_LOG"

case "$JURY_EXIT" in
  0)
    pass "Multi-LLM vision jury (>=${VISUAL_JURY_MIN_PASS:-2} models)"
    ;;
  2)
    warn "Multi-LLM vision jury skipped — no vision API keys (manual jury packet written)"
    echo "       Set OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY in Cursor Secrets,"
    echo "       or complete manual jury per artifacts/visual_reviews/*.manual.json"
    ;;
  *)
    fail "Multi-LLM vision jury consensus FAIL"
    ;;
esac

echo ""
echo "Visual smoke: ${WARN} warning(s), ${FAIL} failure(s)"
exit "$FAIL"
