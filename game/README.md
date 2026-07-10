# GDAI regeneration branch — `game/`

Minimal Godot 4.3 scaffold for **GDAI MCP only** (no GodotPrompter).

## Quick start

1. Read `docs/GDAI_REGEN_PLAN.md` (build phases)
2. Install GDAI plugin → `addons/gdai-mcp-plugin-godot/` (see `docs/GDAI_CLOUD_SETUP.md`)
3. Open this folder in Godot 4.3+ → enable GDAI MCP → start server
4. Press **F5** — New Game starts at `beach_shore.tscn` (SC-01)

## Zones (greybox → build with GDAI)

| Scene | Story |
|-------|-------|
| `scenes/world/beach_shore.tscn` | SC-01 arrival |
| `scenes/world/ruined_village.tscn` | SC-02–05 hub |
| `scenes/world/tidal_caves.tscn` | SC-06–08 dungeon |
| `scenes/world/dragon_palace_gate.tscn` | SC-09+ palace |

**Do not move** gameplay marker nodes documented in `docs/GDAI_REGEN_PLAN.md`.

## Design docs (on `main`)

- `docs/GDD.md`
- `docs/STORYBOARD.md`
- `docs/ART_DIRECTION.md`
