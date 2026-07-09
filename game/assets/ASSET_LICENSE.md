# Asset license summary — Tides of Urashima

**Commercial use:** All shipped art and audio are safe to distribute on Steam.

## Original (no third-party copyright)

| Category | Generator | License |
|----------|-----------|---------|
| BGM & SFX | `tools/generate_game_audio.py` | MIT (this repository) |
| Textures, UI, portraits | `tools/generate_game_art.py` | MIT (this repository) |
| Steam capsules, screenshots, trailer | `tools/generate_game_art.py` | MIT (this repository) |

These files are **synthesized in code** (numpy/Pillow). No samples, stock photos, or downloaded loops are used.

## Third-party (permissive licenses)

| Asset | License | Attribution |
|-------|---------|-------------|
| Kenney Nature Kit (GLB subset) | CC0 1.0 | Kenney / www.kenney.nl (optional) |
| Kenney Castle Kit (OBJ subset) | CC0 1.0 | Kenney / www.kenney.nl (optional) |
| Noto Sans / JP / SC fonts | SIL Open Font License 1.1 | See `fonts/OFL.txt` + credits screen |
| Godot Engine | MIT | Credits screen |
| GodotSteam plugin | MIT | Credits screen (when shipped) |

3D models are installed via `tools/install_cc0_assets.sh` from source packs in `.asset-dl/`.

## Verify before ship

```bash
bash tools/install_cc0_assets.sh   # if models not yet copied
python3 tools/verify_asset_licenses.py
```

Full log: `docs/LICENSES.md`
