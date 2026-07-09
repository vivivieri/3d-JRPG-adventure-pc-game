# Asset license summary — Tides of Urashima

**Commercial use:** All shipped art and audio are safe to distribute on Steam.

## Original (no third-party copyright)

| Category | Generator | License |
|----------|-----------|---------|
| BGM & SFX | `tools/generate_game_audio.py` | MIT (this repository) |
| Textures, UI, portraits | `tools/generate_game_art.py` | MIT (this repository) |
| Steam capsules, screenshots, trailer | `tools/generate_game_art.py` | MIT (this repository) |

These files are **synthesized in code** (numpy/Pillow). No samples, stock photos, or downloaded loops are used.

## Third-party (permissive licenses — attribution required)

| Asset | License | Attribution |
|-------|---------|-------------|
| Noto Sans / JP / SC fonts | SIL Open Font License 1.1 | See `fonts/OFL.txt` + credits screen |
| Godot Engine | MIT | Credits screen |
| GodotSteam plugin | MIT | Credits screen (when shipped) |

## Not included

No Kenney, Quaternius, Freesound, OpenGameArt, Mixamo, or other external art/audio packs are imported into this project.

## Verify before ship

```bash
python3 tools/verify_asset_licenses.py
```

Full log: `docs/LICENSES.md`
