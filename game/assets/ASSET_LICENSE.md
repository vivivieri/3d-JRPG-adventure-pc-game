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
| Poly Haven nature models (glTF subset) | CC0 1.0 | polyhaven.com (optional) |
| Noto Sans / JP / SC fonts | SIL Open Font License 1.1 | See `fonts/OFL.txt` + credits screen |
| Godot Engine | MIT | Credits screen |
| GodotSteam plugin | MIT | Credits screen (when shipped) |

3D models: Kenney via `tools/install_cc0_assets.sh` (`.asset-dl/` source packs); Poly Haven HD via `python3 tools/install_polyhaven_assets.py` (~1.6 GB, not in git).

## Verify before ship

```bash
bash tools/install_cc0_assets.sh          # Kenney low-poly fallback
python3 tools/install_polyhaven_assets.py # high-poly nature (optional, large)
python3 tools/verify_asset_licenses.py
```

Full log: `docs/LICENSES.md`
