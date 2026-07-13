#!/usr/bin/env bash
# Emit remediation brief after smoke/integration FAIL (docs/QA_REMEDIATION_LOOP.md, docs/FLOW_QA.md).
# Usage:
#   bash tools/qa_emit_remediation.sh model-tech <model_id>
#   bash tools/qa_emit_remediation.sh model-jury <jury.json> [asset_id]
#   bash tools/qa_emit_remediation.sh audio-tech <track_id>
#   bash tools/qa_emit_remediation.sh audio-jury <jury.json> [track_id]
#   bash tools/qa_emit_remediation.sh vo-tech <clip_id>
#   bash tools/qa_emit_remediation.sh vo-jury <jury.json> [clip_id]
#   bash tools/qa_emit_remediation.sh visual-palette <zone> [asset_id]
#   bash tools/qa_emit_remediation.sh visual-jury <jury.json> [asset_id]
#   bash tools/qa_emit_remediation.sh data-story
#   bash tools/qa_emit_remediation.sh flow-scenario <INT-ID>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRIEF="${ROOT}/tools/qa_remediation_brief.py"

header() {
  echo ""
  echo "========== QA REMEDIATION BRIEF (read before next build) =========="
}

footer() {
  echo "==================================================================="
  echo "Policy: docs/QA_REMEDIATION_LOOP.md | Flow: docs/FLOW_QA.md"
  echo "Change ONE lever this attempt. Max 3 tries → escalate."
  echo ""
}

kind="${1:-}"
shift || true

case "$kind" in
  model-tech)
    id="${1:?model id}"
    header
    python3 "$BRIEF" --technical-model "$id" || true
    footer
    ;;
  model-jury)
    jury="${1:?jury json path}"
    id="${2:-}"
    header
    if [[ -n "$id" ]]; then
      python3 "$BRIEF" --jury "$jury" --asset-id "$id" || true
    else
      python3 "$BRIEF" --jury "$jury" || true
    fi
    footer
    ;;
  audio-tech)
    track="${1:?track id}"
    header
    python3 "$BRIEF" --technical-audio "$track" || true
    footer
    ;;
  audio-jury)
    jury="${1:?jury json path}"
    track="${2:-}"
    header
    if [[ -n "$track" ]]; then
      python3 "$BRIEF" --jury "$jury" --asset-id "$track" || true
    else
      python3 "$BRIEF" --jury "$jury" || true
    fi
    footer
    ;;
  vo-tech)
    clip="${1:?clip id}"
    header
    python3 "$BRIEF" --technical-vo "$clip" || true
    footer
    ;;
  vo-jury)
    jury="${1:?jury json path}"
    clip="${2:-}"
    header
    if [[ -n "$clip" ]]; then
      python3 "$BRIEF" --jury "$jury" --asset-id "$clip" || true
    else
      python3 "$BRIEF" --jury "$jury" || true
    fi
    footer
    ;;
  visual-palette)
    zone="${1:?zone}"
    asset="${2:-$zone}"
    header
    python3 "$BRIEF" --visual-palette --zone "$zone" --asset-id "$asset" || true
    footer
    ;;
  visual-jury)
    jury="${1:?jury json path}"
    asset="${2:-}"
    header
    if [[ -n "$asset" ]]; then
      python3 "$BRIEF" --jury "$jury" --asset-id "$asset" || true
    else
      python3 "$BRIEF" --jury "$jury" || true
    fi
    footer
    ;;
  data-story)
    header
    python3 "$BRIEF" --validate-story || true
    footer
    ;;
  flow-scenario)
    sid="${1:?scenario id e.g. INT-QUEST-01}"
    header
    python3 "$BRIEF" --flow-scenario "$sid" || true
    footer
    ;;
  scene-primitives)
    header
    python3 "$BRIEF" --scene-primitives || true
    footer
    ;;
  *)
    echo "Unknown kind: ${kind:-<missing>}" >&2
    echo "Run: bash tools/qa_emit_remediation.sh model-tech urashima" >&2
    exit 2
    ;;
esac
