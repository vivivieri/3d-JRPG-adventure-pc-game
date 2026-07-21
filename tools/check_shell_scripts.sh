#!/usr/bin/env bash
# ShellCheck on tools/*.sh — docs/technical/BASH_STYLE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v shellcheck >/dev/null 2>&1; then
  echo "[FAIL] shellcheck not installed — apt install shellcheck or bash tools/install_ci_deps.sh"
  exit 1
fi

mapfile -t SCRIPTS < <(find tools -maxdepth 1 -name '*.sh' -type f | sort)
if [[ ${#SCRIPTS[@]} -eq 0 ]]; then
  echo "[SKIP] no tools/*.sh scripts found"
  exit 2
fi

echo "==> Shell lint (shellcheck) — ${#SCRIPTS[@]} script(s)"
FAIL=0
for script in "${SCRIPTS[@]}"; do
  echo "── shellcheck: ${script}"
  # SC1091: source file not found in CI sandbox (gate_lib.sh exists at runtime)
  if shellcheck -x -e SC1091 "$script"; then
    echo "[PASS] ${script}"
  else
    echo "[FAIL] ${script}"
    FAIL=1
  fi
done

if [[ "$FAIL" -eq 0 ]]; then
  echo "[PASS] L1_shellcheck"
  exit 0
fi
exit 1
