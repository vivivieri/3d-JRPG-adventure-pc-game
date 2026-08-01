#!/usr/bin/env bash
# Cloud Environment start router — MCP stack only when Godot project is present.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "${CLOUD_DOCS_ONLY:-}" == "1" ]]; then
  echo "==> CLOUD_DOCS_ONLY=1 — skip MCP stack start"
  exit 0
fi

if [[ ! -f game/project.godot ]]; then
  echo "==> bootstrap_cloud_start: no game/project.godot — run install first"
  exit 0
fi

bash tools/ensure_xvfb_display.sh
exec bash tools/ensure_mcp_stack.sh --wait "${GDAI_MCP_WAIT:-180}"
