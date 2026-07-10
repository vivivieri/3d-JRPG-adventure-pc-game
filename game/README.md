# Godot project — Tides of Urashima

Fresh implementation branch. **Design docs on `main` are source of truth.**

## Quick start

```bash
# From repo root
bash tools/setup_dev_environment.sh
bash tools/check_dev_environment.sh

# Open in Godot 4.3+ (Forward+)
# File → Open Project → game/project.godot
```

Press **F5** — you should see the dev boot screen and no missing-data errors in the Output panel.

## Dev toolchain (use together)

| Tool | Role |
|------|------|
| **GodotPrompter** | Plan shaders, GDScript, architecture |
| **GDAI MCP** | Build scenes in the live Godot Editor |
| **`.cursorrules`** | Project workflow + stylized rendering rules |

See `docs/GDAI_CLOUD_SETUP.md` and `docs/IMPLEMENTATION_PLAN.md`.

## Folder layout

```
game/
  project.godot          # Godot 4.3+ Forward+
  data/                  # Story JSON (from main — do not duplicate)
  assets/
    models/environment/  # Per-zone kits (beach, village, caves, palace)
    shaders/             # Toon ramp, water, spirit materials
    textures/zones/      # Hand-painted tileables
    fonts/               # Noto OFL bundle (see fonts/README.md)
  scenes/world/          # Zone scenes
  scenes/ui/             # Dialogue, combat HUD
  scripts/               # GDScript systems
  environments/          # WorldEnvironment .tres presets per zone
  addons/                # Dev plugins (see addons/README.md)
```

## Data loading

```gdscript
# Future GameManager API — data lives at res://data/
var scenes = JSON.parse_string(FileAccess.get_file_as_string("res://data/story/scenes.json"))
```

Validate data from repo root:

```bash
python3 tools/validate_story_data.py
```

## Rendering

Follow `docs/RENDERING_GUIDE.md` — Filmic/ACES tonemap, zone fog, toon materials, muted coastal palette.

## Related docs

- `docs/IMPLEMENTATION_PLAN.md` — build phases
- `docs/ENVIRONMENT_KITS.md` — modular assets per zone
- `docs/ART_DIRECTION.md` — palette & style rules
- `docs/DATA_ARCHITECTURE.md` — JSON schema
