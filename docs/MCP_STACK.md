# MCP Stack — GDAI + Godotiq + Godot MCP Pro

**Version:** 1.0  
**Applies to:** `main` rebuild workflow — **Godot 4.7 stable**  
**Cross-refs:** `docs/GDAI_CLOUD_SETUP.md`, `docs/AI_DEV_WORKFLOW.md`, `docs/AI_TESTING_SPEC.md`

Three MCP servers work **together**. Each has a distinct role — agents must not use all three for the same task blindly.

---

## Role split (mandatory)

| Server | Cursor name | Primary role | Use for |
|--------|-------------|--------------|---------|
| **GDAI MCP** | `godot-mcp` | **Build** — scenes, nodes, materials, lights | All `.tscn` / editor mutations (`.cursorrules` §0) |
| **Godotiq** | `godotiq` | **Analyze** — signals, deps, validation, debug | Why combat hung, orphan signals, `read_debug_console`, `ui_map` |
| **Godot MCP Pro** | `godot-mcp-pro` | **Test** — scenarios, asserts, input replay | L4/L5 `run_test_scenario`, `assert_screen_text`, stress tests |

```
GodotPrompter (plan/code)
       │
       ├─► GDAI MCP ──────────► create/edit scenes, F5 verify
       ├─► Godotiq ───────────► trace_flow, signal_map, validate, verify_project_runs
       └─► Godot MCP Pro ─────► run_test_scenario, assert_node_state, compare_screenshots
```

### Conflict rules

| Situation | Use |
|-----------|-----|
| Create zone scene, place meshes | **GDAI only** |
| Combat state machine stuck — which signal failed? | **Godotiq** `godotiq_signal_map`, `godotiq_trace_flow` |
| Run automated JRPG menu test with assertions | **Godot MCP Pro** testing tools |
| Read Godot Output without copy-paste | **Godotiq** `godotiq_read_debug_console` |
| Screenshot game viewport during battle | **GDAI** or **Godotiq** or **MCP Pro** (any); save to `artifacts/screenshots/` |
| Edit node tree / reparent | **GDAI only** (avoid dual editors) |

**Godot MCP Pro full mode (172 tools)** overlaps GDAI for scene editing. On Cursor, use **`--minimal`** (35 tools) or **`--lite`** (81 tools) — testing + runtime + input focus. See install below.

---

## Licenses & cost

| Tool | License | Cost | In git? |
|------|---------|------|---------|
| GDAI MCP | Commercial | ~$19 | ❌ gitignored |
| Godotiq Community | MIT (pip) | Free (24 tools) | ❌ addon gitignored, `pip install` |
| Godotiq Pro | Commercial | $19 one-time | License key in env |
| Godot MCP Pro | Commercial | $15 one-time | ❌ gitignored |

**Ship builds:** disable/remove all three before Steam export.

---

## Install

### 1. GDAI MCP (required for build)

```bash
bash tools/install_gdai_plugin.sh    # from zip in game/addons/
```

See `docs/GDAI_CLOUD_SETUP.md`.

### 2. Godotiq (recommended — free tier)

```bash
bash tools/install_godotiq.sh
```

- `pip install godotiq` (or `uv pip install godotiq`)
- Copies MIT addon → `game/addons/godotiq/`
- Enable: **Project → Plugins → GodotIQ**

Optional Pro: set `GODOTIQ_LICENSE_KEY` in MCP env (purchase at https://godotiq.com/).

### 3. Godot MCP Pro (recommended for L4/L5 testing)

```bash
# Place purchased zip: game/addons/godot-mcp-pro*.zip
bash tools/install_godot_mcp_pro.sh
```

- Extracts addon → `game/addons/godot_mcp/`
- Extracts Node server → `tools/godot-mcp-pro-server/`
- Runs `npm install && npm run build`
- Enable: **Project → Plugins → Godot MCP Pro**

Requires **Node.js 18+** (`node --version`).

### 4. Bootstrap all

```bash
bash tools/ensure_mcp_stack.sh
```

Writes `.cursor/mcp.json`, starts Godot editor, checks bridges.

---

## Cursor / cloud MCP registration

`tools/write_mcp_config.sh` generates `.cursor/mcp.json` with every **installed** server.

**Desktop:** Settings → Tools & MCP → sync from project config.

**Cloud:** [cursor.com/agents](https://cursor.com/agents) → add each server (`godot-mcp`, `godotiq`, `godot-mcp-pro`). Restart agent after save.

Example (all three installed):

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "uv",
      "args": ["run", "/workspace/game/addons/gdai-mcp-plugin-godot/gdai_mcp_server.py"]
    },
    "godotiq": {
      "command": "uvx",
      "args": ["godotiq"],
      "env": {
        "GODOTIQ_PROJECT_ROOT": "/workspace/game"
      }
    },
    "godot-mcp-pro": {
      "command": "node",
      "args": [
        "/workspace/tools/godot-mcp-pro-server/build/index.js",
        "--minimal"
      ],
      "env": {
        "GODOT_MCP_PORT": "6505"
      }
    }
  }
}
```

Godotiq Pro: add `"GODOTIQ_LICENSE_KEY": "your-key"` inside `godotiq.env`.

---

## Ports (defaults)

| Server | Port | Check |
|--------|------|-------|
| GDAI HTTP | 3571 | `curl -sf http://127.0.0.1:3571/tools` |
| Godotiq WebSocket | 6007 | GodotIQ plugin auto-connects |
| Godot MCP Pro | 6505 | Plugin panel in editor |

If ports conflict, adjust in each plugin’s settings and MCP env vars.

---

## Godot editor plugins

Enable all installed plugins in **Project → Project Settings → Plugins**:

| Plugin | Required for |
|--------|----------------|
| GDAI MCP | Build (`godot-mcp`) |
| GodotIQ | Bridge tools (`godotiq` runtime/editor) |
| Godot MCP Pro | Test tools (`godot-mcp-pro`) |

Start **GDAI MCP** panel → **Start** after editor opens.

---

## Testing workflow with full stack

See `docs/AI_TESTING_SPEC.md` §11. Summary:

| Layer | Tools |
|-------|-------|
| L0–L2 | Shell scripts (no MCP) |
| L3 | GDAI F5 + screenshot; Godotiq `godotiq_ui_map` for menus |
| L4 | Godot MCP Pro `run_test_scenario`; Godotiq `godotiq_verify_project_runs` |
| L5 | Godot MCP Pro input replay + `assert_screen_text`; Godotiq `godotiq_trace_flow` on failure |
| L6 | Human — **after** L5 |

### Example prompts

**Debug hung turn (Godotiq):**

```
Use godotiq_signal_map and godotiq_trace_flow on CombatManager.
Why did enemy turn not advance after SC-05? Read debug console.
```

**Automated combat menu (Godot MCP Pro):**

```
Using godot-mcp-pro: run_test_scenario for SC-05 tutorial.
Assert battle menu text visible. compare_screenshots against baseline.
```

**Build fix (GDAI only):**

```
Using godot-mcp only: fix dialogue_box.tscn layout per UI_UX_FLOW.md.
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Too many MCP tools in Cursor | Godot MCP Pro: use `--minimal` in mcp.json args |
| GDAI + MCP Pro both edit scene | **Rule:** GDAI builds; MCP Pro tests only |
| Godotiq bridge offline | Enable GodotIQ plugin; wait 5s auto-reconnect |
| `node` not found | Install Node 18+ for Godot MCP Pro |
| godotiq not in MCP catalog | Register `godotiq` in cloud dashboard separately |

---

## Related

- `game/.godotiq.json` — project conventions for Godotiq linter  
- `game/addons/README.md` — addon policy  
- `.cursor/mcp.json.example` — template  
