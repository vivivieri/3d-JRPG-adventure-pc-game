#!/usr/bin/env bash
# Enforce CODE_BASE_CLASS_RULES on game/development (forbidden parallel controllers).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Base class compliance (CODE_BASE_CLASS_RULES.md)"
echo ""

python3 tools/validate_base_classes.py || exit 1

if [[ ! -d "${ROOT}/game/scripts" ]]; then
  echo "[SKIP] game/scripts/ not present yet"
  exit 0
fi

FAIL=0
ALLOWED_PLAYER="game/scripts/exploration/player_controller.gd"

while IFS= read -r -d '' gd; do
  rel="${gd#${ROOT}/}"
  if ! grep -qE 'extends[[:space:]]+CharacterBody3D' "$gd" 2>/dev/null; then
    continue
  fi
  if [[ "$rel" != "$ALLOWED_PLAYER" ]]; then
    echo "[FAIL] $rel extends CharacterBody3D — use PlayerController base ($ALLOWED_PLAYER) only"
    FAIL=1
  fi
done < <(find game/scripts game/scenes -name '*.gd' -print0 2>/dev/null)

if [[ "$FAIL" -eq 0 ]]; then
  echo "[OK]   no forbidden CharacterBody3D extensions"
fi
exit "$FAIL"
