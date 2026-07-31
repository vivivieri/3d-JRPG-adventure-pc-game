---
id: session-loop
type: how-to
audience: [pm, architect, builder]
status: active
authority: workflow
tokens_est: 675
summary: "Session startup + loop + forbids"
---
# AI Dev — Build Policy — Session startup + loop + forbids

**Hub:** [`build_policy.md`](../build_policy.md)

### 1.2 Session startup (every agent run)

```bash
bash tools/ensure_mcp_stack.sh   # full stack — wraps ensure_gdai_mcp.sh
```

**Sprint workers** (after PM dispatch) also run:

```bash
bash tools/run_agent_session_gate.sh <role> <issue_id>   # opens session telemetry
```

**End every worker session** (closes telemetry + triggers PM):

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
```

Factory telemetry policy: `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` §9. One-time secret: `CURSOR_API_KEY` (`docs/ops/agents/CURSOR_SECRETS_SETUP.md` §8).

**Cross-cutting factory features (register before merge):**

```bash
bash tools/check_feature_integration.sh --remind   # docs/ops/qa/WORKFLOW_INTEGRATION.md
```

**Factory stack scripts** (event-driven PM):

Authority: `docs/ops/agents/FACTORY_SETUP_GUIDE.md`

| Script | Role |
|--------|------|
| `run_factory_watchdog.sh` | Stall detection + PM recovery |
| `pm_emit_stakeholder_report.sh` | Product owner status on cycle events |
| `run_alignment_audit.sh` | Spec/data alignment audit at post-merge — management visuals: `audit_radar_spec.png`, `audit_radar_build.png` |

All must be true before implementation (`.cursorrules` §0 / `MCP_STACK.md`):

| Check | How |
|-------|-----|
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Cursor MCP servers | `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`, `notion` all connected |
| Godot Editor | Running with `game/project.godot` open |

If any server is missing → **stop and notify the user** (`godot-mcp-pro` hard-blocks L4/L5 gates;
others block their respective roles — see `MCP_STACK.md`).


### 1.3 Build loop (per task)

```
1. Read design doc section for the task
2. GodotPrompter — draft GDScript / shaders / unit tests
3. GDAI MCP — apply scenes, nodes, materials in live editor
4. GDAI MCP — F5 run scene; read Output / debugger; fix until clean
5. Run automated tests (§3)
6. Confirm acceptance criteria for current phase (§4)
7. Commit + push
```


### 1.4 What AI agents must not do

- Import unknown-license art, audio, or models from the web
- Hand-edit `.tscn` when GDAI MCP is available
- Ship with GDAI MCP plugin enabled (dev-only; remove before export)
- Mark a phase complete without passing its acceptance criteria
- Add new `CharacterBody3D` / `Area3D` interaction stacks outside `base_classes.json` registry

---
