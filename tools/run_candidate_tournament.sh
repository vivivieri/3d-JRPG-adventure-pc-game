#!/usr/bin/env bash
# Champion/challenger tournament runner — L2.5 pre-merge (non-ship).
#
# Usage:
#   bash tools/run_candidate_tournament.sh --challenger artifacts/candidates/P1-02/challenger_run2.json
#   bash tools/run_candidate_tournament.sh --challenger ... --promote
#
# Authority: docs/qa/CANDIDATE_TOURNAMENT.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

CHALLENGER=""
SCOPE=""
PROMOTE=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --challenger) CHALLENGER="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --promote) PROMOTE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help)
      sed -n '3,10p' "$0"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$CHALLENGER" ]]; then
  echo "Usage: bash tools/run_candidate_tournament.sh --challenger <manifest.json> [--scope <id>] [--promote]" >&2
  exit 2
fi

echo "==> Candidate tournament (L2.5 — pre-merge, non-ship)"
echo "    Authority: docs/qa/CANDIDATE_TOURNAMENT.md"
echo "    Challenger: $CHALLENGER"
echo

COMPARE_ARGS=(python3 tools/compare_champion_challenger.py --challenger "$CHALLENGER" --write --json)
[[ -n "$SCOPE" ]] && COMPARE_ARGS+=(--scope "$SCOPE")

COMPARISON_JSON="$(mktemp)"
if ! "${COMPARE_ARGS[@]}" > "$COMPARISON_JSON"; then
  RC=$?
  cat "$COMPARISON_JSON"
  rm -f "$COMPARISON_JSON"
  echo "[FAIL] L2_candidate_select — challenger did not win or hard gates/harness failed"
  exit "$RC"
fi

ARTIFACT="$(python3 -c "import json; print(json.load(open('$COMPARISON_JSON')).get('artifact_path',''))")"
cat "$COMPARISON_JSON"
rm -f "$COMPARISON_JSON"

if [[ -z "$ARTIFACT" || ! -f "$ARTIFACT" ]]; then
  echo "[FAIL] comparison artifact missing" >&2
  exit 1
fi

echo
echo "[PASS] L2_candidate_select comparison: $ARTIFACT"

if [[ "$PROMOTE" -eq 1 ]]; then
  PROMOTE_ARGS=(python3 tools/promote_champion_candidate.py --comparison "$ARTIFACT" --challenger "$CHALLENGER")
  [[ "$DRY_RUN" -eq 1 ]] && PROMOTE_ARGS+=(--dry-run)
  "${PROMOTE_ARGS[@]}"
  echo "[OK] Champion registry updated (one winner per scope)"
fi

echo
echo "Next: merge ONLY this challenger commit to game/development, then run full run_ci_checks.sh (L0–L6 unchanged)"
exit 0
