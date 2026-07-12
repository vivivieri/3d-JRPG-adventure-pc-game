# Godot project — Tides of Urashima (fresh rebuild)

**Design docs on `main` and `game/data/` JSON are the source of truth.**  
Gameplay **scenes** are built only via **GDAI MCP** in the live editor — see `game/scenes/README.md`.

## Quick start

```bash
# From repo root
bash tools/setup_dev_environment.sh
bash tools/ensure_mcp_stack.sh          # GDAI MCP + Godot editor HTTP bridge — REQUIRED
bash tools/check_dev_environment.sh
```

Open `game/project.godot` in Godot 4.7 (Forward+). **No main scene is set** until GDAI MCP builds the first menu/boot scene (Phase 2.4).

## Dev toolchain (required)

| Tool | Role |
|------|------|
| **GodotPrompter** | Plan shaders, GDScript, architecture, unit tests |
| **GDAI MCP** | Build scenes in the live Godot Editor — **no manual `.tscn` edits** |
| **`.cursorrules`** | Project workflow + stylized rendering rules |

See `docs/MCP_STACK.md`, `docs/GDAI_CLOUD_SETUP.md`, and `docs/AI_TESTING_SPEC.md`.

## What exists today

```
game/
  project.godot              # Autoloads only — no run/main_scene until GDAI builds UI
  scenes/README.md           # Scene build policy (no committed .tscn)
  scripts/core/
    game_bootstrap.gd        # Validates required data paths at startup
  scripts/story/
    cinematic_director.gd    # Cinematic hook registry (partial)
    story_data.gd            # JSON helpers
    voice_line_player.gd     # VO path resolver (spec; clips Phase 7)
  locale/translations.csv    # UI/skills/combat i18n keys (data)
  data/                      # Story JSON (do not duplicate in docs)
  assets/                    # Placeholder folders for Phase 1+ assets
  addons/                    # GDAI MCP plugin (commercial — see addons/README.md)
```

## Data loading

```gdscript
var scenes = JSON.parse_string(FileAccess.get_file_as_string("res://data/story/scenes.json"))
```

Validate from repo root:

```bash
python3 tools/validate_story_data.py
bash tools/run_unit_tests.sh
```

## Next build step

**Phase 1** — GodotPrompter plans shaders/`zone_visuals.gd` → **GDAI MCP** builds `ruined_village.tscn` per `docs/RENDERING_GUIDE.md`.

## Related docs

- `docs/IMPLEMENTATION_PLAN.md` — build phases
- `docs/ENVIRONMENT_KITS.md` — modular assets per zone
- `docs/ART_DIRECTION.md` — palette & style rules
- `docs/DATA_ARCHITECTURE.md` — JSON schema
