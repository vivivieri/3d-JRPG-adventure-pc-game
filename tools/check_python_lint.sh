#!/usr/bin/env bash
# PEP 8 / style lint for tools/*.py — ruff (docs/technical/PYTHON_STYLE.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v ruff >/dev/null 2>&1; then
  echo "[FAIL] ruff not installed — pip install ruff or bash tools/install_ci_deps.sh"
  exit 1
fi

echo "==> Python lint (ruff) — tools/"
if ruff check tools/; then
  echo "[PASS] L1_python_lint"
  exit 0
fi

echo "[FAIL] L1_python_lint — fix with: ruff check tools/ --fix"
exit 1
