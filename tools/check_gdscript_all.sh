#!/usr/bin/env bash
# Full-tree gdlint on game/scripts + game/tests — docs/technical/GDSCRIPT_STYLE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot — full GDScript lint runs on game/development only"
  exit 2
fi

export PATH="${HOME}/.local/bin:${PATH}"

mapfile -t DIRS < <(
  {
    [[ -d game/scripts ]] && echo game/scripts
    [[ -d game/tests ]] && echo game/tests
    [[ -d tools/godot_templates ]] && echo tools/godot_templates
  } | sort -u
)

if [[ ${#DIRS[@]} -eq 0 ]]; then
  echo "[SKIP] no game/scripts or game/tests tree"
  exit 2
fi

mapfile -t FILES < <(find "${DIRS[@]}" -name '*.gd' -type f 2>/dev/null | sort)
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[SKIP] no .gd files under game/scripts or game/tests"
  exit 2
fi

echo "==> GDScript full-tree lint (${#FILES[@]} file(s))"

if command -v gdlint >/dev/null 2>&1; then
  if gdlint "${DIRS[@]}"; then
    echo "[PASS] L1_gdscript_lint_all"
    exit 0
  fi
  echo "[FAIL] L1_gdscript_lint_all"
  exit 1
fi

if [[ "${CI:-}" == "true" ]]; then
  echo "[FAIL] gdtoolkit not installed — run bash tools/install_ci_deps.sh"
  exit 1
fi

echo "[WARN] gdtoolkit not installed — skipping gdlint"
exit 2
