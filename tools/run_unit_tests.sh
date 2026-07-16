#!/usr/bin/env bash
# Run Godot headless unit tests (L1 in docs/workflow/AI_DEV_WORKFLOW.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

echo "==> Unit tests (Godot headless)"

if [[ ! -f "${ROOT}/game/project.godot" ]]; then
  echo "[SKIP] no game/project.godot — unit tests run on game/development only"
  exit 2
fi

bash "${ROOT}/tools/with_ci_godot.sh" \
  godot4 --headless --rendering-driver opengl3 --path game -s res://tests/unit/test_runner.gd
