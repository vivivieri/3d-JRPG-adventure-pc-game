#!/usr/bin/env bash
# Bootstrap full MCP stack: GDAI + Godotiq + Godot MCP Pro.
# Usage: bash tools/ensure_mcp_stack.sh [--wait SECONDS]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "${ROOT}/tools/ensure_gdai_mcp.sh" "$@"
