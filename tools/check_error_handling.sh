#!/usr/bin/env bash
# Error-handling lint — docs/technical/ERROR_HANDLING.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v ruff >/dev/null 2>&1; then
  echo "[FAIL] ruff not installed — pip install ruff or bash tools/install_ci_deps.sh"
  exit 1
fi

exec python3 tools/check_error_handling.py
