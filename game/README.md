# Godot project — Tides of Urashima (fresh rebuild)

**Design docs on `main` and `game/data/` JSON are the source of truth.**  
All gameplay scenes and systems were removed for a clean rebuild under the GDAI MCP workflow.

## Quick start

```bash
# From repo root
bash tools/setup_dev_environment.sh
bash tools/ensure_gdai_mcp.sh          # GDAI MCP + Godot editor HTTP bridge
bash tools/check_dev_environment.sh
```

Open `game/project.godot` in Godot 4.3+ (Forward+) and press **F5**. You should see the dev boot screen with no missing-data errors in Output.

## Dev toolchain (required)

| Tool | Role |
|------|------|
| **GodotPrompter** | Plan shaders, GDScript, architecture |
| **GDAI MCP** | Build scenes in the live Godot Editor — **no manual `.tscn` edits** |
| **`.cursorrules`** | Project workflow + stylized rendering rules |

See `docs/GDAI_CLOUD_SETUP.md`, `docs/AI_DEV_WORKFLOW.md`, and `docs/AI_TESTING_SPEC.md`.

## What exists today

```
game/
  project.godot              # Main scene: scenes/boot.tscn
  scenes/boot.tscn           # Dev boot UI
  scripts/core/
    boot_scene.gd            # Boot screen
    game_bootstrap.gd        # Validates required data paths at startup
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

**Phase 1** — Environment foundation: `ruined_village` vertical slice per `docs/RENDERING_GUIDE.md`.  
Use GodotPrompter for shaders/scripts → GDAI MCP for scene assembly.

## Related docs

- `docs/IMPLEMENTATION_PLAN.md` — build phases
- `docs/ENVIRONMENT_KITS.md` — modular assets per zone
- `docs/ART_DIRECTION.md` — palette & style rules
- `docs/DATA_ARCHITECTURE.md` — JSON schema
