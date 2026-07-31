---
id: stack-troubleshoot
type: how-to
phase: [0, 1]
audience: [builder, pm]
status: active
authority: ops
tokens_est: 692
summary: "Plugin Install Guide — Full stack, troubleshoot, ship — bash tools/install_gdai_plugin.sh"
---
# Plugin Install Guide — Full stack, troubleshoot, ship

**Hub:** [`PLUGIN_INSTALL_GUIDE.md`](../PLUGIN_INSTALL_GUIDE.md)

## When to read

Use **Plugin Install Guide — Full stack, troubleshoot, ship** (roles: builder, pm) when executing this procedure Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [Install everything (full MCP stack)](#install-everything-full-mcp-stack)
- [Bridge ports (defaults)](#bridge-ports-defaults)
- [Editor plugins to enable](#editor-plugins-to-enable)
- [Troubleshooting](#troubleshooting)
- [Ship builds](#ship-builds)
- [Related](#related)


## Install everything (full MCP stack)

```bash
# GDAI — see docs/ops/agents/GDAI_CLOUD_SETUP.md (commercial zip)
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
| GDAI + MCP Pro both edit scenes | **Rule:** GDAI builds; MCP Pro tests only (`docs/ops/agents/MCP_STACK.md`) |

---


## Ship builds

Before Steam export: **disable and remove** all MCP dev plugins (GDAI, Godotiq, MCP Pro). Only **GodotSteam** ships. See `game/addons/README.md`.

---


## Related

- `docs/ops/agents/MCP_STACK.md` — which tool to use when
- `docs/engineering/technical/PLUGIN_COMPATIBILITY.md` — Godot 4.7 verification matrix
- `docs/ops/agents/GDAI_CLOUD_SETUP.md` — GDAI install + cloud snapshot
- `game/addons/README.md` — addon policy
- `.cursor/mcp.json.example` — template paths
