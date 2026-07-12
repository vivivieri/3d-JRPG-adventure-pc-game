#!/usr/bin/env bash
# Run a command with MCP autoloads stripped from project.godot when addons are absent.
# Restores project.godot on exit. No-op when all MCP addons are installed.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT="${ROOT}/game/project.godot"
BACKUP="${PROJECT}.ci.bak"
STRIPPED=0

restore_project() {
  if [[ "$STRIPPED" -eq 1 && -f "$BACKUP" ]]; then
    mv -f "$BACKUP" "$PROJECT"
    STRIPPED=0
  fi
}

trap restore_project EXIT

MCP_PRESENT=1
[[ -f "${ROOT}/game/addons/gdai-mcp-plugin-godot/gdai_mcp_runtime.gd" ]] || MCP_PRESENT=0
[[ -f "${ROOT}/game/addons/godot_mcp/mcp_screenshot_service.gd" ]] || MCP_PRESENT=0

if [[ "$MCP_PRESENT" -eq 0 && -f "$PROJECT" ]]; then
  cp "$PROJECT" "$BACKUP"
  python3 - "$PROJECT" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
strip_keys = {"GDAIMCPRuntime", "GodotIQRuntime", "MCPScreenshot", "MCPInputService", "MCPGameInspector"}
strip_plugin_substrings = ("gdai-mcp-plugin-godot", "godot_mcp", "godotiq")
lines = text.splitlines(keepends=True)
out: list[str] = []
section = ""
for line in lines:
    stripped = line.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        section = stripped[1:-1]
        out.append(line)
        continue
    if section == "autoload":
        key = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
        if key in strip_keys:
            continue
    if section == "editor_plugins" and stripped.startswith("enabled="):
        m = re.search(r'PackedStringArray\((.*)\)', stripped)
        if m:
            parts = [p.strip().strip('"') for p in m.group(1).split(",") if p.strip()]
            kept = [p for p in parts if not any(s in p for s in strip_plugin_substrings)]
            quoted = ", ".join(f'"{p}"' for p in kept)
            out.append(f'enabled=PackedStringArray({quoted})\n')
            continue
    out.append(line)
path.write_text("".join(out), encoding="utf-8")
PY
  STRIPPED=1
  echo "[OK]   Stripped MCP autoloads for CI (addons absent)"
fi

if [[ $# -eq 0 ]]; then
  echo "Usage: with_ci_godot.sh <command> [args...]"
  exit 1
fi

"$@"
