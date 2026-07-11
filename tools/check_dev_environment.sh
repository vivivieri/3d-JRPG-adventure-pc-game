#!/usr/bin/env bash
# Quick health check for dev environment. Exit 1 if critical items missing.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ERR=0
OK=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "[OK]   $label"
    OK=$((OK + 1))
  else
    echo "[FAIL] $label"
    ERR=$((ERR + 1))
  fi
}

echo "Dev environment check — $ROOT"
echo

check "game/project.godot exists" test -f game/project.godot
check "export preset configured" test -f game/export_presets.cfg -o -f game/export_presets.cfg.example
check "story data valid" python3 tools/validate_story_data.py
check "setup script executable" test -x tools/setup_dev_environment.sh
check "implementation plan doc" test -f docs/IMPLEMENTATION_PLAN.md
check "rendering guide" test -f docs/RENDERING_GUIDE.md
check "MCP example config" test -f .cursor/mcp.json.example

export PATH="${HOME}/.local/bin:${PATH}"
export XDG_DATA_HOME="${ROOT}/.cache/godot-data"
export XDG_CONFIG_HOME="${ROOT}/.cache/godot-config"
export XDG_CACHE_HOME="${ROOT}/.cache/godot-cache"

if command -v uv >/dev/null 2>&1; then
  echo "[OK]   uv installed"
  OK=$((OK + 1))
else
  echo "[WARN] uv not installed (needed for GDAI MCP)"
fi

if command -v godot4 >/dev/null 2>&1; then
  echo "[OK]   Godot in PATH"
  OK=$((OK + 1))
  if godot4 --headless --path game --quit-after 1 >/dev/null 2>&1; then
    echo "[OK]   Godot smoke test"
    OK=$((OK + 1))
  else
    echo "[FAIL] Godot smoke test"
    ERR=$((ERR + 1))
  fi
else
  echo "[WARN] Godot not in PATH"
fi

if [[ -d game/addons/gdai-mcp-plugin-godot ]]; then
  echo "[OK]   GDAI MCP plugin folder present"
  OK=$((OK + 1))
else
  echo "[WARN] GDAI MCP plugin not installed (dev-only)"
fi

if [[ -d game/addons/godotiq ]]; then
  echo "[OK]   Godotiq addon present"
  OK=$((OK + 1))
else
  echo "[WARN] Godotiq not installed — bash tools/install_godotiq.sh"
fi

if [[ -f tools/godot-mcp-pro-server/build/index.js ]]; then
  echo "[OK]   Godot MCP Pro server built"
  OK=$((OK + 1))
else
  echo "[WARN] Godot MCP Pro not installed — optional for L4/L5 testing"
fi

if curl -sf "http://127.0.0.1:${GDAI_MCP_SERVER_PORT:-3571}/tools" >/dev/null 2>&1; then
  echo "[OK]   GDAI HTTP bridge (:${GDAI_MCP_SERVER_PORT:-3571})"
  OK=$((OK + 1))
else
  echo "[FAIL] GDAI HTTP bridge not running — run: bash tools/ensure_gdai_mcp.sh"
  ERR=$((ERR + 1))
fi

if [[ -f .cursor/mcp.json ]]; then
  echo "[OK]   .cursor/mcp.json present"
  OK=$((OK + 1))
else
  echo "[WARN] .cursor/mcp.json missing — run: bash tools/ensure_gdai_mcp.sh"
fi

echo
echo "Passed: $OK | Failed: $ERR"
exit "$ERR"
