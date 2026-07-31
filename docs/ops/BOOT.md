---
id: boot
type: tutorial
audience: [pm, architect, builder, qa, flow, visual, release, narrative, audio]
phase: [0, 1]
status: active
authority: ops
tokens_est: 450
summary: "Session boot — MCP stack, STOP conditions, resolve_docs pack only"
---
# Agent boot card

**Router:** [`docs/INDEX.yaml`](../INDEX.yaml) · **Discovery:** [`docs/llms.txt`](../llms.txt) · **Cloud pointer:** [`AGENTS.md`](../../AGENTS.md)

## Session startup

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_extended_toolchain.sh
bash tools/run_agent_session_gate.sh <role> <issue_id>
```

Load **only** the pack printed by the gate (`python3 tools/resolve_docs.py <role> --issue <id> --budget 12000`). Hub + one pack — never the full library. Pack-split policy: [`DOC_LIBRARY_ADR.md`](../_meta/DOC_LIBRARY_ADR.md) § Amendment — Docs pack thinning (no bulk thinning; named packs only).

## STOP — do not fall back

If GDAI `:3571`, Cursor MCP servers (`godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`), or Blender (M5) are missing → **STOP and notify**. Do not hand-edit `.tscn`.

## Authority (conflicts)

1. `docs/ops/workflow/IMPLEMENTATION_PLAN.md`
2. `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md` / `BRANCHING.md`
3. `docs/engineering/technical/TECHNICAL_DESIGN.md`
4. `game/data/` JSON (runtime numbers win)

## Role → docs

```bash
python3 tools/resolve_docs.py --list-roles
python3 tools/resolve_docs.py --list-tasks
python3 tools/resolve_docs.py <role> --issue <id> --budget 12000 --report artifacts/docs_pack_<id>.txt
```

Specialty remap: `builder` + `zone_lighting` → `builder_zone` (`tools/docs_role_map.py`).

After docs/INDEX or pack-router changes, smoke the PM→gate→adherence path:

```bash
bash tools/smoke_factory_workflow.sh --issue P1-01 --agent architect
```

**Docs pack adherence (no honor system):**

| Step | Script | Role |
|------|--------|------|
| Trigger | `run_agent_session_gate.sh` → `log_docs_read.py --from-pack` | Auto-seeds `must_read` into `artifacts/docs_reads_<id>.log` |
| Follower | `run_post_agent_cycle.sh` → `check_docs_pack_adherence.py --strict` | FAIL if log missing/empty or reads outside pack∪deferred |

Extras beyond the pack: `python3 tools/log_docs_read.py --issue <id> docs/path.md` (still must be in pack∪deferred). Debug-only: `DOCS_PACK_ADHERENCE_STRICT=0`.

## Branches

| Branch | Contents |
|--------|----------|
| `main` | Docs, `game/data/`, tooling |
| `game/development` | Godot project, scenes, assets |

Docs land on `main` first, then sync → `game/development`.

## Done criteria

`bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit "$(git rev-parse HEAD)"`
Cross-cutting features → `workflow_integration_registry.json` · `bash tools/check_feature_integration.sh --remind`
