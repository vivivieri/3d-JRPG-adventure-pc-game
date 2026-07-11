#!/usr/bin/env bash
# Write .cursor/mcp.json for required Godot MCP servers + GameLab when API key is set.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MCP_JSON="${ROOT}/.cursor/mcp.json"
GAME_ROOT="${ROOT}/game"

mkdir -p "${ROOT}/.cursor"

GDAI_SERVER="${ROOT}/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"
MCP_PRO_SERVER="${ROOT}/tools/godot-mcp-pro-server/build/index.js"
MCP_PRO_MODE="${GODOT_MCP_PRO_MODE:---minimal}"

python3 <<PY
import json
import os

root = ${ROOT@Q}
game = ${GAME_ROOT@Q}
mcp_path = ${MCP_JSON@Q}
gdai = ${GDAI_SERVER@Q}
mcp_pro = ${MCP_PRO_SERVER@Q}
mcp_pro_mode = ${MCP_PRO_MODE@Q}

servers = {}

if os.path.isfile(gdai):
    servers["godot-mcp"] = {
        "command": "uv",
        "args": ["run", gdai],
    }

# Godotiq — free via uvx when pip package available
if os.system("command -v uvx >/dev/null 2>&1") == 0:
    env = {"GODOTIQ_PROJECT_ROOT": game}
    key = os.environ.get("GODOTIQ_LICENSE_KEY", "").strip()
    if key:
        env["GODOTIQ_LICENSE_KEY"] = key
    servers["godotiq"] = {
        "command": "uvx",
        "args": ["godotiq"],
        "env": env,
    }

if os.path.isfile(mcp_pro):
    servers["godot-mcp-pro"] = {
        "command": "node",
        "args": [mcp_pro, mcp_pro_mode],
        "env": {"GODOT_MCP_PORT": os.environ.get("GODOT_MCP_PORT", "6505")},
    }

gamelab_key = os.environ.get("GAMELAB_API_KEY", "").strip()
if gamelab_key:
    servers["gamelab-mcp"] = {
        "type": "sse",
        "url": "http://api.gamelabstudio.co:8765/sse",
        "headers": {"X-API-Key": gamelab_key},
    }

with open(mcp_path, "w", encoding="utf-8") as f:
    json.dump({"mcpServers": servers}, f, indent=2)
    f.write("\n")

print(f"Wrote {mcp_path} with servers: {', '.join(servers.keys()) or '(none)'}")
PY
