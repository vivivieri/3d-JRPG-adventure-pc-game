# License & Attribution Log

Track every third-party asset, story source, and engine dependency.

**Policy:** All shipped art and audio must be **copyright-safe for commercial release** — no unlicensed or all-rights-reserved material. See **`docs/ASSET_COMPLIANCE.md`** for the full allow/deny list.

**Machine manifest:** `docs/asset_manifest.license.json`  
**Verify before ship:** `bash tools/check_asset_compliance.sh`  
**Register new assets:** `python3 tools/register_asset.py add --help`

---

## Story source

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Urashima Tarō (folktale) | Japanese folklore | Public domain | Adapted — dark retelling in `docs/GDD.md` |

---

## Engine & plugins

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Godot Engine 4.3 | https://godotengine.org | MIT | Credits screen required |
| GodotSteam 4.15 | https://codeberg.org/godotsteam/godotsteam | MIT | `game/addons/godotsteam/` — credits screen |

---

## Fonts (bundled)

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Noto Sans (Latin) | https://github.com/notofonts/noto-fonts | OFL 1.1 | `NotoSans-*.ttf` — see `game/assets/fonts/OFL.txt` |
| Noto Sans JP | https://github.com/notofonts/noto-cjk Sans2.004 | OFL 1.1 | `NotoSansJP-*.otf` |
| Noto Sans SC | https://github.com/notofonts/noto-cjk Sans2.004 | OFL 1.1 | `NotoSansSC-*.otf` |

---

## Audio (original — no third-party samples)

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| All BGM (`bgm/*.ogg`) | `tools/generate_game_audio.py` | MIT (repo) | 2026-07 | Menu, zones, combat, boss |
| All SFX (`sfx/*.ogg`) | `tools/generate_game_audio.py` | MIT (repo) | 2026-07 | UI, combat, field |

Synthesized in code (numpy). No Freesound, stock loops, or licensed recordings.

---

## 3D models (CC0 — Kenney)

| Item | Source | License | Used for |
|------|--------|---------|----------|
| Nature Kit GLBs (`models/nature/*.glb`) | Kenney Nature Kit | CC0 1.0 | Trees, rocks, pier, cliffs, fences |
| Castle Kit OBJs (`models/castle/*.obj`) | Kenney Castle Kit | CC0 1.0 | Palace gate, pillars, banners, player knight |

Install curated subset: `bash tools/install_cc0_assets.sh` (requires `.asset-dl/` source packs).

Attribution appreciated but not required: [Kenney](https://www.kenney.nl)

---

## 3D models (CC0 — Poly Haven, high-poly)

| Item | Source | License | Used for |
|------|--------|---------|----------|
| Nature glTF (`models/polyhaven/*/`) | [Poly Haven](https://polyhaven.com) | CC0 1.0 | HD trees, cliffs, rocks, grass, shrubs |

Install curated subset: `python3 tools/install_polyhaven_assets.py` (~1.6 GB at 1k resolution).

`PropLibrary` prefers Poly Haven models when installed, falling back to Kenney low-poly.

Attribution appreciated but not required: [Poly Haven](https://polyhaven.com)

Greybox floor/wall primitives remain procedural Godot meshes.

---

## Art (original — no third-party images)

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| Zone textures (`textures/zones/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | World material albedo |
| UI panels & bars (`ui/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue, menu, HP/MP |
| Portraits (`ui/portraits/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue silhouettes |
| Icons (`ui/icons/*.png`, `ui/icon.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | App icon, combat intents |
| Main menu background | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Title screen |
| Steam capsules & screenshots | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Store page marketing |
| Steam trailer (`steam/trailer.mp4`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Slideshow + procedural BGM |

Rendered in code (Pillow). Title text uses bundled Noto (OFL) baked into PNG only.

---

## 3D models

| Status | Notes |
|--------|-------|
| **Kenney CC0 kits** | Curated Nature + Castle models in `game/assets/models/`. See `asset_manifest.json`. |
| **Poly Haven CC0** | High-poly nature glTF in `game/assets/models/polyhaven/`. See `polyhaven_manifest.json`. Not committed — run installer. |

---

## Code

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Game scripts | Original (this repo) | MIT | See repository `LICENSE` |

---

## Checklist before Steam ship

- [ ] `bash tools/check_asset_compliance.sh` passes (proof in `docs/compliance/COMPLIANCE_REPORT.md`)
- [ ] Every new asset registered in `docs/asset_manifest.license.json` + this file
- [ ] No banned licenses (NC, SA, ARR, unknown) — see `docs/ASSET_COMPLIANCE.md` §3
- [ ] Credits screen lists Godot MIT + Noto OFL + GodotSteam MIT + any CC-BY attributions
- [ ] Playtest on Windows hardware
