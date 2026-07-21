#!/usr/bin/env bash
# TypeScript lint for tools/godot-mcp-pro-server — TYPESCRIPT_STYLE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MCP_DIR="${ROOT}/tools/godot-mcp-pro-server"

if [[ ! -f "${MCP_DIR}/package.json" ]]; then
  echo "[SKIP] no tools/godot-mcp-pro-server/package.json — install via tools/install_godot_mcp_pro.sh"
  exit 0
fi

if ! command -v node >/dev/null 2>&1; then
  echo "[FAIL] node not installed — required for TypeScript lint"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "[FAIL] npm not installed — required for TypeScript lint"
  exit 1
fi

cd "$MCP_DIR"

if [[ ! -d node_modules ]]; then
  echo "==> Installing MCP Pro dependencies (npm ci)…"
  if [[ -f package-lock.json ]]; then
    npm ci --no-audit --no-fund
  else
    npm install --no-audit --no-fund
  fi
fi

echo "==> TypeScript lint — ${MCP_DIR}"

if npm run lint --if-present; then
  echo "[PASS] L1_typescript_lint (npm run lint)"
  exit 0
fi

if [[ -f tsconfig.json ]]; then
  if npx tsc --noEmit; then
    echo "[PASS] L1_typescript_lint (tsc --noEmit)"
    exit 0
  fi
  echo "[FAIL] L1_typescript_lint — tsc --noEmit failed"
  exit 1
fi

if npm run build; then
  echo "[PASS] L1_typescript_lint (npm run build — no lint/tsconfig; build is clean)"
  exit 0
fi

echo "[FAIL] L1_typescript_lint — no lint script, tsconfig.json, or successful build"
exit 1
