# Scenes — GDAI MCP only

**No `.tscn` files are committed in the design-phase baseline.**

Per `.cursorrules` §0 and `docs/MCP_STACK.md`:

1. **GodotPrompter** drafts GDScript, shaders, and node-tree plans.
2. **GDAI MCP** (`godot-mcp`) creates and edits all scenes in the live Godot Editor.
3. **GDAI MCP** runs F5 playtest before merge.

## First scenes to build (Phase 1–2)

| Scene | Path | Phase |
|-------|------|-------|
| Boot / main menu | `boot.tscn` or `ui/main_menu.tscn` | 2.4 |
| Ruined village | `world/ruined_village.tscn` | 1 |
| Dialogue overlay | `ui/dialogue_box.tscn` | 3.1 |

Do **not** hand-edit `.tscn` in Cursor when GDAI MCP is available.
