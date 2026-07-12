# Scenes — GDAI MCP only

**No ship `.tscn` files are committed in the design-phase baseline.**

Per `.cursorrules` §0 and `docs/MCP_STACK.md`:

1. **GodotPrompter** drafts GDScript, shaders, and node-tree plans.
2. **GDAI MCP** (`godot-mcp`) creates and edits all scenes in the live Godot Editor.
3. **GDAI MCP** runs F5 playtest before merge.
4. **`tools/check_rr_compliance.sh`** must pass before commit/merge.

## First scenes to build (Phase 1–2)

| Scene | Path | Phase |
|-------|------|-------|
| Boot / main menu | `boot.tscn` or `ui/main_menu.tscn` | 2.4 |
| Ruined village | `world/ruined_village.tscn` | 1 |
| Dialogue overlay | `ui/dialogue_box.tscn` | 3.1 |

Do **not** hand-edit ship `.tscn` in Cursor when GDAI MCP is available.

**Allowed without GDAI marker:** paths under `greybox/`, `_dev/`, or `*.greybox.tscn` only.

## After GDAI builds a scene (required for merge)

Create or update `game/scenes/.gdai_built`:

```ini
main_scene=res://scenes/ui/main_menu.tscn
built_by=gdai-mcp
verified_f5=true
verified_at=2026-07-12T12:00:00Z
agent_note=Optional one-line note
```

Rules:

- `main_scene` must match `run/main_scene` in `game/project.godot`
- `verified_f5=true` only after GDAI MCP F5 playtest with no errors
- Run `bash tools/check_rr_compliance.sh` before push

## Agent startup (mandatory)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
```

If either fails → **STOP** scene work; docs/data-only tasks OK.
