#!/usr/bin/env bash
# GitHub Actions workflow lint — actionlint on .github/workflows/*.yml
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WORKFLOW_DIR="${ROOT}/.github/workflows"
if [[ ! -d "$WORKFLOW_DIR" ]]; then
  echo "[SKIP] no .github/workflows directory"
  exit 0
fi

mapfile -t FILES < <(find "$WORKFLOW_DIR" -maxdepth 1 -name '*.yml' -o -name '*.yaml' | sort)
if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "[SKIP] no workflow YAML files"
  exit 0
fi

if ! command -v actionlint >/dev/null 2>&1; then
  ACTIONLINT_BIN="${HOME}/.local/bin/actionlint"
  if [[ ! -x "$ACTIONLINT_BIN" ]]; then
    echo "==> Installing actionlint to ${ACTIONLINT_BIN}…"
    mkdir -p "${HOME}/.local/bin"
    TMPDIR_ACTIONLINT="$(mktemp -d)"
    curl -fsSL -o "${TMPDIR_ACTIONLINT}/actionlint.tar.gz" \
      "https://github.com/rhysd/actionlint/releases/download/v1.7.7/actionlint_1.7.7_linux_amd64.tar.gz"
    tar -xzf "${TMPDIR_ACTIONLINT}/actionlint.tar.gz" -C "${TMPDIR_ACTIONLINT}"
    install -m 0755 "${TMPDIR_ACTIONLINT}/actionlint" "$ACTIONLINT_BIN"
    rm -rf "$TMPDIR_ACTIONLINT"
  fi
  export PATH="${HOME}/.local/bin:${PATH}"
fi

if ! command -v actionlint >/dev/null 2>&1; then
  echo "[FAIL] actionlint not installed — bash tools/install_ci_deps.sh"
  exit 1
fi

echo "==> Workflow lint (actionlint) — ${#FILES[@]} file(s)"
if actionlint "${FILES[@]}"; then
  echo "[PASS] L1_workflow_yaml"
  exit 0
fi

echo "[FAIL] L1_workflow_yaml — fix actionlint findings above"
exit 1
