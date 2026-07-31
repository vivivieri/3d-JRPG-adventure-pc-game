# Agent boot card — Tides of Urashima

**Load this first.** Full library map: [`docs/INDEX.yaml`](../INDEX.yaml) · Hub: [`docs/README.md`](../README.md)

---

## Session startup

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_rr_compliance.sh
bash tools/check_extended_toolchain.sh
```

| Role | First command |
|------|----------------|
| PM | `bash tools/run_pm_orchestrator.sh` |
| Worker | `bash tools/run_agent_session_gate.sh <role> <issue_id>` |

---

## STOP — do not fall back

Notify the user if any fail:

- GDAI HTTP `:3571` down (`curl http://127.0.0.1:3571/tools`)
- Cursor MCP missing `godot-mcp`, `godotiq`, `godot-mcp-pro`, or `gamelab-mcp`
- Blender missing (M5 turntable)
- `GAMELAB_API_KEY` unset

**Do not hand-edit `.tscn` when GDAI is available.** Scene edits → GDAI MCP only.

---

## Authority (conflicts)

1. `game/data/*.json` wins for runtime numbers
2. [`IMPLEMENTATION_PLAN.md`](workflow/IMPLEMENTATION_PLAN.md) — build order
3. [`TECHNICAL_DESIGN.md`](../engineering/technical/TECHNICAL_DESIGN.md) — runtime architecture
4. [`MCP_STACK.md`](agents/MCP_STACK.md) + [`.cursorrules`](../../.cursorrules) — tools

---

## Role → docs

Resolve packs with:

```bash
python3 tools/resolve_docs.py <role>
python3 tools/resolve_docs.py <role> --issue <issue_id> --budget 12000
python3 tools/resolve_docs.py <role> --task zone_lighting --phase 1
python3 tools/resolve_docs.py --list-roles
python3 tools/resolve_docs.py --list-tasks
python3 tools/docs_pack_impact.py --base origin/main
python3 tools/pm_docs_preflight.py
```

Session gate writes `artifacts/docs_pack_<issue>.txt` (kept vs deferred + tokens; deferred lines include `summary:` TL;DRs). Sprint issues may set `docs_task` or have it inferred from the title. Briefs under `docs/briefs/` auto-attach when the issue title/refs mention the asset stem.

Large bibles are split into packs (`ops/qa/testing/`, `design/art/rendering/`, `ops/workflow/implementation/`, `design/world/levels/`, …) — load the hub + one pack, not the old monolith.


| Role | Pack |
|------|------|
| builder_zone | art rendering + environment kits |
| builder_combat | combat systems + presentation |
| qa / flow | acceptance + remediation / flow QA |
| visual | art direction + automation + visual QA |
| pm | R&R + PM runbook + sprint orchestration |

---

## Branches

| Branch | Contents |
|--------|----------|
| `main` | docs + `game/data/` only |
| `game/development` | Godot implementation |

Docs land on `main` first → sync into `game/development`.

---

## Done criteria (every issue)

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit "$(git rev-parse HEAD)"
```

Cross-cutting factory features: register in `game/data/qa/workflow_integration_registry.json` before merge.
