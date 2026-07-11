# Plugin install guide — Godotiq & Godot MCP Pro

**Applies to:** Godot **4.7 stable**, Cursor desktop + Cloud Agents  
**Cross-refs:** `docs/MCP_STACK.md` (roles), `docs/PLUGIN_COMPATIBILITY.md` (4.7 matrix), `docs/GDAI_CLOUD_SETUP.md` (GDAI)

Step-by-step instructions for providing and installing the **analyze** and **test** MCP plugins. GDAI MCP (build) is covered in `docs/GDAI_CLOUD_SETUP.md`.

---

## Overview

| Plugin | Cost | You provide | Cursor MCP name | Role |
|--------|------|-------------|-----------------|------|
| **Godotiq** | Free (Pro optional) | Nothing — installs from pip | `godotiq` | Analyze, debug, signals |
| **Godot MCP Pro** | $15 one-time | Purchased zip | `godot-mcp-pro` | L4/L5 automated tests |

Neither plugin is committed to git. Install locally or bake into a **cloud snapshot**.

---

## Godotiq

### What you need

| Piece | How you get it |
|-------|----------------|
| Python package | `pip install godotiq` (script does this) |
| Godot addon | Copied to `game/addons/godotiq/` by install script |
| Cursor bridge | `uvx godotiq` |
| Editor bridge | WebSocket on `127.0.0.1:6007` when GodotIQ plugin is enabled |

**Purchase (optional Pro):** https://godotiq.com/ — set `GODOTIQ_LICENSE_KEY` in MCP env for extra tools.

### Local install

```bash
# From repo root
bash tools/install_godotiq.sh
```

Then in Godot:

1. Open `game/project.godot`
2. **Project → Project Settings → Plugins**
3. Enable **GodotIQ**
4. Confirm in Output: `GodotIQ: WebSocket server listening on 127.0.0.1:6007`

Regenerate MCP config and bootstrap:

```bash
bash tools/write_mcp_config.sh
bash tools/ensure_gdai_mcp.sh
```

### Cursor — desktop

After `write_mcp_config.sh`, `.cursor/mcp.json` should include:

```json
"godotiq": {
  "command": "uvx",
  "args": ["godotiq"],
  "env": {
    "GODOTIQ_PROJECT_ROOT": "/absolute/path/to/game"
  }
}
```

1. **Cursor Settings → Tools & MCP** — add or sync `godotiq`
2. Restart Cursor
3. Keep Godot editor open with **GodotIQ** enabled

**Pro license (optional):**

```json
"env": {
  "GODOTIQ_PROJECT_ROOT": "/absolute/path/to/game",
  "GODOTIQ_LICENSE_KEY": "your-key"
}
```

### Cursor — Cloud Agents

Godotiq installs from the network (no zip upload).

1. In the setup agent terminal:

```bash
bash tools/install_godotiq.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_plugin_compatibility.sh
```

2. Register at [cursor.com/agents](https://cursor.com/agents) → **Integrations & MCP**:

```json
{
  "command": "uvx",
  "args": ["godotiq"],
  "env": {
    "GODOTIQ_PROJECT_ROOT": "/workspace/game"
  }
}
```

3. Restart the cloud agent
4. **Save snapshot** so `game/addons/godotiq/` is pre-installed for future runs

### Verify Godotiq

```bash
ss -tln | grep 6007          # WebSocket listening
bash tools/check_plugin_compatibility.sh
```

---

## Godot MCP Pro

### What you need

| Piece | How you get it |
|-------|----------------|
| Purchased zip | https://godot-mcp.abyo.net/ or https://y1uda.itch.io/godot-mcp-pro |
| Godot addon | `game/addons/godot_mcp/` (from zip) |
| Node MCP server | `tools/godot-mcp-pro-server/` (from zip, `npm run build`) |
| Node.js | 18+ (`node --version`) |
| Editor bridge | WebSocket on `127.0.0.1:6505` (default) |

Use **`--minimal`** mode in Cursor (35 tools) so MCP Pro does not overlap GDAI for scene editing. See `docs/MCP_STACK.md`.

### Step 1 — Obtain the zip

1. Purchase at https://godot-mcp.abyo.net/ ($15, lifetime updates)
2. Download the **full package** (must include `addons/godot_mcp/` and `server/` with `package.json`)
3. Place in the repo (any matching name):

```
game/addons/godot-mcp-pro.zip
```

Accepted patterns: `godot-mcp-pro*.zip`, `godot_mcp_pro*.zip`

Or set an explicit path:

```bash
export GODOT_MCP_PRO_ZIP=/path/to/your/godot-mcp-pro.zip
```

### Step 2 — Install

```bash
bash tools/install_godot_mcp_pro.sh
```

This extracts:

- `game/addons/godot_mcp/` — Godot editor plugin
- `tools/godot-mcp-pro-server/` — Node server (`npm install && npm run build`)

Success marker: `tools/godot-mcp-pro-server/build/index.js` exists.

### Step 3 — Enable in Godot

1. Open `game/project.godot`
2. **Project → Project Settings → Plugins**
3. Enable **Godot MCP Pro**
4. Check the MCP Pro panel — connection to port **6505**

Add to `project.godot` `editor_plugins` if not already present:

```ini
"res://addons/godot_mcp/plugin.cfg"
```

### Step 4 — Cursor MCP config

```bash
bash tools/write_mcp_config.sh
```

Expected entry:

```json
"godot-mcp-pro": {
  "command": "node",
  "args": [
    "/absolute/path/to/tools/godot-mcp-pro-server/build/index.js",
    "--minimal"
  ],
  "env": {
    "GODOT_MCP_PORT": "6505"
  }
}
```

**Mode options** (set via `GODOT_MCP_PRO_MODE` before `write_mcp_config.sh`):

| Mode | Flag | Tools | Use when |
|------|------|-------|----------|
| Minimal | `--minimal` | 35 | Cursor (recommended — testing focus) |
| Lite | `--lite` | 84 | Windsurf, 100-tool limits |
| Full | (none) | 175 | Claude Code, no overlap concern |

### Cursor — desktop

1. **Cursor Settings → Tools & MCP** — add `godot-mcp-pro`
2. Restart Cursor
3. Godot editor open + **Godot MCP Pro** plugin enabled

### Cursor — Cloud Agents

The zip is **not in git**. You must upload it once, then save a snapshot.

1. [cursor.com/agents](https://cursor.com/agents) → **Start Setup Agent**
2. Upload zip to:

```
/workspace/game/addons/godot-mcp-pro.zip
```

3. Run:

```bash
bash tools/install_godot_mcp_pro.sh
bash tools/write_mcp_config.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_plugin_compatibility.sh
```

4. Register **godot-mcp-pro** in **Integrations & MCP**:

```json
{
  "command": "node",
  "args": [
    "/workspace/tools/godot-mcp-pro-server/build/index.js",
    "--minimal"
  ],
  "env": {
    "GODOT_MCP_PORT": "6505"
  }
}
```

5. **Save snapshot** (addon + built server persist for future agents)
6. Restart the cloud agent

**Tip:** Leave the zip in `game/addons/` inside the snapshot so a future `install_godot_mcp_pro.sh` can re-run on boot if needed (same pattern as GDAI).

### Verify Godot MCP Pro

```bash
test -f tools/godot-mcp-pro-server/build/index.js && echo "server OK"
node --version    # must be 18+
ss -tln | grep 6505
bash tools/check_plugin_compatibility.sh --with-editor
```

---

## Install everything (full MCP stack)

```bash
# GDAI — see docs/GDAI_CLOUD_SETUP.md (commercial zip)
bash tools/install_gdai_plugin.sh

# Godotiq — free, from network
bash tools/install_godotiq.sh

# Godot MCP Pro — commercial zip required first
bash tools/install_godot_mcp_pro.sh

# Bootstrap editor + write .cursor/mcp.json
bash tools/ensure_mcp_stack.sh

# Audit
bash tools/check_plugin_compatibility.sh --with-editor
```

### Bridge ports (defaults)

| Server | Port | Quick check |
|--------|------|-------------|
| GDAI MCP | 3571 | `curl -sf http://127.0.0.1:3571/tools` |
| Godotiq | 6007 | `ss -tln \| grep 6007` |
| Godot MCP Pro | 6505 | Plugin panel in editor |

### Editor plugins to enable

**Project → Project Settings → Plugins:**

| Plugin | Required for |
|--------|----------------|
| GDAI MCP | Build (`godot-mcp`) |
| GodotIQ | Analyze (`godotiq`) |
| Godot MCP Pro | Test (`godot-mcp-pro`) |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `godotiq` not in MCP tool list (cloud) | Register in [cursor.com/agents](https://cursor.com/agents) dashboard, not only `.cursor/mcp.json` |
| Godotiq :6007 not listening | Enable **GodotIQ** plugin; wait ~5s; restart editor |
| `install_godot_mcp_pro.sh` — zip not found | Place zip in `game/addons/` or set `GODOT_MCP_PRO_ZIP` |
| `node` not found | Install Node 18+; cloud: `bash tools/install_cloud_dev.sh` |
| MCP Pro build fails | `cd tools/godot-mcp-pro-server && npm install && npm run build` |
| Too many MCP tools in Cursor | Use `--minimal` for MCP Pro |
| GDAI + MCP Pro both edit scenes | **Rule:** GDAI builds; MCP Pro tests only (`docs/MCP_STACK.md`) |

---

## Ship builds

Before Steam export: **disable and remove** all MCP dev plugins (GDAI, Godotiq, MCP Pro). Only **GodotSteam** ships. See `game/addons/README.md`.

---

## Related

- `docs/MCP_STACK.md` — which tool to use when
- `docs/PLUGIN_COMPATIBILITY.md` — Godot 4.7 verification matrix
- `docs/GDAI_CLOUD_SETUP.md` — GDAI install + cloud snapshot
- `game/addons/README.md` — addon policy
- `.cursor/mcp.json.example` — template paths
