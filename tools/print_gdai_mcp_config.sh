#!/usr/bin/env bash
# Print stdio MCP JSON for Cursor Cloud Agents dashboard registration.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER_PY="$ROOT/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"

if [[ ! -f "$SERVER_PY" ]]; then
  echo "GDAI plugin not installed. Run: GDAI_PLUGIN_ZIP=/path/to.zip bash tools/install_gdai_mcp.sh" >&2
  exit 1
fi

cat <<EOF
Register at https://cursor.com/agents → MCP → Add stdio server:

{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": [
        "run",
        "$SERVER_PY"
      ],
      "env": {
        "PATH": "$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
EOF
