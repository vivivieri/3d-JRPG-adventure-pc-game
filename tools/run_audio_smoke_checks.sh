#!/usr/bin/env bash
# L2 audio smoke: catalog + technical + optional LLM jury when bgm_village.ogg exists.
# WARN (exit 0) when gate track missing or dev placeholders — docs/AUDIO_QA.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GATE_TRACK="${AUDIO_SMOKE_GATE_TRACK:-bgm_village}"
GATE_PATH="${ROOT}/game/assets/audio/bgm/${GATE_TRACK}.ogg"
PHASE="${AUDIO_SMOKE_PHASE:-1}"
WARN=0
FAIL=0

warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }
pass() { echo "[PASS] $1"; }

echo "==> Audio smoke checks (docs/AUDIO_QA.md)"
echo "    Gate track: ${GATE_TRACK}"
echo ""

if [[ ! -f "$GATE_PATH" ]]; then
  warn "Audio smoke skipped — ${GATE_PATH#${ROOT}/} not found"
  echo "       Generate via: bash tools/generate_ai_bgm.sh --track ${GATE_TRACK}"
  echo ""
  echo "Audio smoke: ${WARN} warning(s), ${FAIL} failure(s) (skipped)"
  exit 0
fi

echo "    Gate file: ${GATE_PATH#${ROOT}/}"
echo ""

if python3 "${ROOT}/tools/check_audio_catalog.py" --phase "$PHASE"; then
  pass "Audio catalog (phase ${PHASE})"
else
  fail "Audio catalog (phase ${PHASE})"
fi

TECH_LOG="$(mktemp)"
set +e
python3 "${ROOT}/tools/check_audio_technical.py" --track "$GATE_TRACK" >"$TECH_LOG" 2>&1
TECH_EXIT=$?
set -e
cat "$TECH_LOG"
if [[ "$TECH_EXIT" -eq 0 ]]; then
  if grep -q '^\s*\[WARN\]' "$TECH_LOG" || grep -q 'WARN:' "$TECH_LOG"; then
    warn "Technical check (${GATE_TRACK}) — dev placeholders or loudness drift"
  else
    pass "Technical check (${GATE_TRACK})"
  fi
else
  fail "Technical check (${GATE_TRACK})"
  bash "${ROOT}/tools/qa_emit_remediation.sh" audio-tech "$GATE_TRACK" || true
fi
rm -f "$TECH_LOG"

JURY_LOG="$(mktemp)"
set +e
python3 "${ROOT}/tools/review_audio_vision.py" \
  --track "$GATE_TRACK" \
  --min-pass "${AUDIO_JURY_MIN_PASS:-2}" \
  >"$JURY_LOG" 2>&1
JURY_EXIT=$?
set -e
cat "$JURY_LOG"
case "$JURY_EXIT" in
  0) pass "Audio LLM jury (${GATE_TRACK}, >=${AUDIO_JURY_MIN_PASS:-2} models)" ;;
  2)
    warn "Audio LLM jury skipped — no OPENAI/GEMINI keys or manual packet written"
    echo "       Set API keys in Cursor Secrets or complete artifacts/audio_reviews/*.manual.json"
    ;;
  *)
    fail "Audio LLM jury consensus FAIL (${GATE_TRACK})"
    bash "${ROOT}/tools/qa_emit_remediation.sh" \
      audio-jury "${ROOT}/artifacts/audio_reviews/${GATE_TRACK}.jury.json" \
      "$GATE_TRACK" || true
    ;;
esac
rm -f "$JURY_LOG"

echo ""
echo "Audio smoke: ${WARN} warning(s), ${FAIL} failure(s)"
exit "$FAIL"
