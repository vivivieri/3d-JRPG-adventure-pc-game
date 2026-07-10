# Art assets

Original procedural textures, UI art, and portraits. MIT license (this repo).

Regenerate:

```bash
./tools/generate_assets.sh
# or
python3 tools/generate_game_art.py
```

## Layout

| Path | Usage |
|------|-------|
| `textures/zones/` | Tileable ground/structure maps per zone |
| `ui/panel_*.png` | Dialogue and menu panel backgrounds |
| `ui/bar_*.png` | HP/MP progress bar styles |
| `ui/portraits/` | Character/boss dialogue silhouettes |
| `ui/main_menu_bg.png` | Title screen background |
| `ui/icon.png` | Application icon |

Palette follows `docs/ART_DIRECTION.md`.
