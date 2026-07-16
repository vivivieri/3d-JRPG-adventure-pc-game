#!/usr/bin/env bash
# L2 feel smoke — validate GAME_FEEL thresholds against implementation constants when present.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

THRESHOLDS="${ROOT}/game/data/qa/feel_thresholds.json"
PLAYER="${ROOT}/game/scripts/exploration/player_controller.gd"

echo "==> Feel smoke checks (docs/GAME_FEEL.md)"
echo ""

if [[ ! -f "$THRESHOLDS" ]]; then
  echo "[FAIL] missing $THRESHOLDS"
  exit 1
fi

python3 - <<'PY' || exit 1
import json
from pathlib import Path
p = Path("game/data/qa/feel_thresholds.json")
data = json.loads(p.read_text())
assert data.get("scenarios"), "feel_thresholds.json needs scenarios[]"
print(f"[OK]   feel_thresholds.json — {len(data['scenarios'])} scenario(s)")
PY

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot — feel constant audit runs on game/development"
  exit 2
fi

FAIL=0
if [[ -f "$PLAYER" ]]; then
  if grep -qE 'INPUT_LATENCY|input_latency|MAX_INPUT_MS' "$PLAYER" 2>/dev/null; then
    echo "[OK]   player_controller defines input latency constant"
  else
    echo "[WARN] player_controller.gd missing INPUT_LATENCY constant (GAME_FEEL §3)"
    if [[ "${FEEL_SMOKE_STRICT:-}" == "1" ]]; then
      FAIL=1
    fi
  fi
else
  echo "[WARN] $PLAYER not present yet — Architect must add before Phase 2"
  if [[ "${FEEL_SMOKE_STRICT:-}" == "1" ]]; then
    FAIL=1
  fi
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "[PASS] feel smoke (catalog + optional constant audit)"
  exit 0
fi
echo "[FAIL] feel smoke strict mode"
exit 1
