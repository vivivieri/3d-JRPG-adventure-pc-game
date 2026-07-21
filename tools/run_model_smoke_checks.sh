#!/usr/bin/env bash
# L2 model smoke: catalog + GLB technical + turntable jury when urashima.glb exists.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GATE_MODEL="${MODEL_SMOKE_GATE:-urashima}"
PHASE="${MODEL_SMOKE_PHASE:-1}"
WARN=0
FAIL=0

warn() { echo "[WARN] $1"; WARN=$((WARN + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }
pass() { echo "[PASS] $1"; }

echo "==> Model smoke checks (docs/art/MODEL_QA.md)"
echo "    Gate model: ${GATE_MODEL}"
echo ""

GATE_PATH="${ROOT}/game/assets/models/characters/${GATE_MODEL}/${GATE_MODEL}.glb"
if [[ ! -f "$GATE_PATH" ]]; then
  warn "Model smoke skipped — ${GATE_PATH#"${ROOT}"/} not found"
  echo "       Generate via Meshy/Blender pipeline per docs/art/ART_AUTOMATION_PIPELINE.md §5"
  echo ""
  echo "Model smoke: ${WARN} warning(s), ${FAIL} failure(s) (skipped)"
  exit 0
fi

echo "    Gate file: ${GATE_PATH#"${ROOT}"/}"
echo ""

if python3 "${ROOT}/tools/check_model_catalog.py" --phase "$PHASE"; then
  pass "Model catalog (phase ${PHASE})"
else
  fail "Model catalog (phase ${PHASE})"
fi

TECH_LOG="$(mktemp)"
set +e
python3 "${ROOT}/tools/check_model_technical.py" --model "$GATE_MODEL" >"$TECH_LOG" 2>&1
TECH_EXIT=$?
set -e
cat "$TECH_LOG"
if [[ "$TECH_EXIT" -eq 0 ]]; then
  if grep -q 'WARN:' "$TECH_LOG"; then
    warn "Technical GLB check (${GATE_MODEL})"
  else
    pass "Technical GLB check (${GATE_MODEL})"
  fi
else
  fail "Technical GLB check (${GATE_MODEL})"
  bash "${ROOT}/tools/qa_emit_remediation.sh" model-tech "$GATE_MODEL" || true
  python3 "${ROOT}/tools/qa_write_gate_result.py" --gate L2_model_technical --status fail \
    --message "technical lint failed for ${GATE_MODEL}" 2>/dev/null || true
fi
rm -f "$TECH_LOG"

if command -v blender >/dev/null 2>&1; then
  if python3 "${ROOT}/tools/render_model_turntable.py" --model "$GATE_MODEL"; then
    pass "Turntable render (${GATE_MODEL})"
    JURY_LOG="$(mktemp)"
    AGENT_DIR="${ROOT}/artifacts/model_reviews/${GATE_MODEL}.agent"
    set +e
    if compgen -G "${AGENT_DIR}/*.json" >/dev/null 2>&1; then
      # Agent-driven jury: verdicts from Cursor LLM subagents, no external API keys.
      # See docs/qa/AGENT_JURY.md
      python3 "${ROOT}/tools/ingest_agent_jury.py" \
        --domain model \
        --asset "$GATE_PATH" \
        --reviews-dir "$AGENT_DIR" \
        --out "${ROOT}/artifacts/model_reviews/${GATE_MODEL}.model_jury.json" \
        --min-pass "${MODEL_JURY_MIN_PASS:-2}" \
        >"$JURY_LOG" 2>&1
    else
      python3 "${ROOT}/tools/review_model_vision.py" \
        --model "$GATE_MODEL" \
        --min-pass "${MODEL_JURY_MIN_PASS:-2}" \
        >"$JURY_LOG" 2>&1
    fi
    JURY_EXIT=$?
    set -e
    cat "$JURY_LOG"
    case "$JURY_EXIT" in
      0) pass "Model vision jury (${GATE_MODEL})" ;;
      2)
        warn "Model vision jury skipped — no API keys"
        ;;
      *)
        fail "Model vision jury FAIL (${GATE_MODEL})"
        bash "${ROOT}/tools/qa_emit_remediation.sh" \
          model-jury "${ROOT}/artifacts/model_reviews/${GATE_MODEL}.model_jury.json" \
          "$GATE_MODEL" || true
        ;;
    esac
    rm -f "$JURY_LOG"
  else
    warn "Turntable render failed — check Blender GLB import"
  fi
else
  warn "Blender not installed — skip turntable + model jury"
fi

echo ""
echo "Model smoke: ${WARN} warning(s), ${FAIL} failure(s)"
exit "$FAIL"
