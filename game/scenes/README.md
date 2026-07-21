# Scenes — GDAI MCP policy

**Branch:** `game/development` only. No ship `.tscn` on `main`.

## Rules

1. **Build scenes in Godot via GDAI MCP** (`godot-mcp`) — not Cursor hand-edits.
2. After F5 verify, update `game/scenes/.gdai_built`:
   - `verified_f5=true`
   - `main_scene=` (when `run/main_scene` is set)
   - `scenes_touched=` list of `res://` paths
3. Greybox paths (`greybox/`, `_dev/`, `*.greybox.tscn`) are exempt from the marker until promoted.

## Docs

- `docs/agents/MCP_STACK.md`
- `.cursorrules` §0
- `tools/check_rr_compliance.sh`
