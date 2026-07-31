---
id: golden-rules
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 359
summary: "1. **GodotPrompter writes code** → **GDAI MCP builds scenes** → **QA proves gates** — never skip a handoff."
---
# R&R Cheat Sheet — Golden rules

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## Golden rules

1. **GodotPrompter writes code** → **GDAI MCP builds scenes** → **QA proves gates** — never skip a handoff.
2. **Only GDAI MCP** may create/edit `.tscn`, nodes, materials, lights, inspector values.
3. **Never hand-edit `.tscn` in Cursor** when GDAI is available (`L0_rr_compliance`).
4. **Scene diff → update `.gdai_built`** in the same PR (`L3_gdai_built` in CI).
5. **P0 MCP required:** `godot-mcp`, `godotiq`, `godot-mcp-pro` — if missing, **STOP and notify user**.
6. **One writer per `.tscn`** — never parallel two agents on the same scene file.
7. **`docs/` + `game/data/`** are design truth — not sprint backlog reprioritization.
8. **Cross-cutting factory features** — register in `workflow_integration_registry.json`; run `bash tools/check_feature_integration.sh --remind` before merge (`docs/ops/qa/WORKFLOW_INTEGRATION.md`).
9. **Open PRs with the role template** — `game_development` or `docs_main` checklist (`docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`).
10. **Extend base classes only** — no new `CharacterBody3D` stacks (`docs/engineering/technical/CODE_BASE_CLASS_RULES.md`).

---
