#!/usr/bin/env bash
# Optional static typing on tools/*_lib.py — docs/technical/PYTHON_STYLE.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"

mapfile -t LIBS < <(find tools -maxdepth 1 -name '*_lib.py' -type f | sort)
if [[ ${#LIBS[@]} -eq 0 ]]; then
  echo "[SKIP] no tools/*_lib.py files"
  exit 0
fi

if ! command -v mypy >/dev/null 2>&1; then
  echo "[FAIL] mypy not installed — pip install mypy or bash tools/install_ci_deps.sh"
  exit 1
fi

echo "==> mypy — ${#LIBS[@]} library file(s)"
if mypy --config-file "${ROOT}/pyproject.toml" "${LIBS[@]}"; then
  echo "[PASS] L1_mypy_libs"
  exit 0
fi

echo "[FAIL] L1_mypy_libs — fix mypy findings above"
exit 1
