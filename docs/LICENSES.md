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
| Godot Engine 4.7 | https://godotengine.org | MIT | Credits screen required |
| GodotSteam **4.20+** | https://codeberg.org/godotsteam/godotsteam | MIT | `game/addons/godotsteam/` — **required for Godot 4.7 ship**; install via `bash tools/install_godotsteam.sh` |

---

## Fonts (bundled)

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Noto Sans (Latin) | https://github.com/notofonts/noto-fonts | OFL 1.1 | `NotoSans-*.ttf` — see `game/assets/fonts/OFL.txt` |
| Noto Sans JP | https://github.com/notofonts/noto-cjk Sans2.004 | OFL 1.1 | `NotoSansJP-*.otf` |
| Noto Sans SC | https://github.com/notofonts/noto-cjk Sans2.004 | OFL 1.1 | `NotoSansSC-*.otf` |

---

## Audio

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| Procedural BGM/SFX (`bgm/*.ogg`, `sfx/*.ogg`) | `tools/generate_game_audio.py` | MIT (repo) | 2026-07 | **Dev placeholder** — replace before M5 ship |
| ACE-Step ship tracks | ACE-Step 1.5 via `tools/generate_ai_bgm.py` | MIT (ACE-Step) | 2026-07 | Zone + cinematic hero BGM — curated prompts + loudness normalize |
| Selective VO (12 clips) | ElevenLabs via `tools/generate_ai_vo.py` | Commercial AI — verify ToS | 2026-07 | `game/assets/audio/voice/{locale}/*.ogg` — log each clip |
| Marketing trailer BGM | `tools/generate_marketing_trailer.py` or ACE-Step stitch | MIT / ACE-Step | 2026-07 | `steam/trailer_bgm.ogg` — marketing only |

**Third-party audio samples:** Do not import random web loops. Filtered CC0 from documented sources (e.g. Freesound CC0-only) is allowed **only** when registered here and in `asset_manifest.license.json` per `docs/ASSET_COMPLIANCE.md`. Default pipeline: procedural + ACE-Step + ElevenLabs.

---

## 3D models (CC0 — Kenney) — **dev greybox only**

| Item | Source | License | Used for |
|------|--------|---------|----------|
| Nature Kit GLBs (`models/nature/*.glb`) | Kenney Nature Kit | CC0 1.0 | **Phase 1–6 greybox** — trees, rocks, pier |
| Castle Kit OBJs (`models/castle/*.obj`) | Kenney Castle Kit | CC0 1.0 | **Phase 1–6 greybox** — blockout only |

Install curated subset: `bash tools/install_cc0_assets.sh` (requires `.asset-dl/` source packs).

**Ship rule (M5):** Replace Kenney Castle/European kit pieces in **player-facing builds** per `docs/ART_DIRECTION.md`. Nature kit pieces may remain only if art-reviewed and logged. Kenney Castle kit is **deprecated for ship** — do not ship palace gate from Castle kit.

Attribution appreciated but not required: [Kenney](https://www.kenney.nl)

---

## 3D models (CC0 — Poly Haven, high-poly)

| Item | Source | License | Used for |
|------|--------|---------|----------|
| Nature glTF (`models/polyhaven/*/`) | [Poly Haven](https://polyhaven.com) | CC0 1.0 | HD trees, cliffs, rocks, grass, shrubs |

Install curated subset: `python3 tools/install_polyhaven_assets.py` (~1.6 GB at 1k resolution).

`PropLibrary` prefers Poly Haven models when installed, falling back to Kenney low-poly during greybox.

Attribution appreciated but not required: [Poly Haven](https://polyhaven.com)

Greybox floor/wall primitives remain procedural Godot meshes — replace before M5 ship.

---

## Art (original — no third-party images)

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| Zone textures (`textures/zones/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | World material albedo |
| UI panels & bars (`ui/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue, menu, HP/MP |
| Portraits (`ui/portraits/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue silhouettes |
| Icons (`ui/icons/*.png`, `ui/icon.png`, `ui/icon.svg`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | App icon (PNG + SVG), combat intents |
| Main menu background | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Title screen |
| Steam capsules & screenshots | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Store page marketing |
| Pitch illustrations (`docs/pitch/illustrations/**/*.png`) | Cursor AI image generation | Pitch/marketing use | 2026-07 | Storyboard set — replace with 3D for ship |
| Marketing trailer (`steam/trailer.mp4`, `trailer_ja.mp4`, `trailer_zh.mp4`, `trailer_zh-Hant.mp4`) | `tools/generate_marketing_trailer.py` | MIT (repo) + pitch art above | 2026-07 | ~75s; procedural or ACE-Step BGM (`steam/trailer_bgm.ogg`) |
| AI video b-roll (optional) | Runway / Kling / similar | Per vendor ToS | — | **Marketing trailer only** — log in manifest; never in-game |

Rendered in code (Pillow). Title text uses bundled Noto (OFL) baked into PNG only.

---

## 3D models — ship status

| Status | Notes |
|--------|-------|
| **Kenney CC0 kits** | Dev greybox in `game/assets/models/` — **replace before M5 ship** for palace/hero props |
| **Poly Haven CC0** | High-poly nature glTF in `game/assets/models/polyhaven/`. Not committed — run installer |
| **Hero meshes** | AI 3D + automated NPR albedo per `docs/CHARACTER_BIBLE.md` — M5 deliverable |

---

## Code

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Game scripts | Original (this repo) | MIT | See repository `LICENSE` |

---

## Checklist before Steam ship (M6)

- [ ] `bash tools/check_asset_compliance.sh` passes (proof in `docs/compliance/COMPLIANCE_REPORT.md`)
- [ ] Every new asset registered in `docs/asset_manifest.license.json` + this file
- [ ] No banned licenses (NC, SA, ARR, unknown) — see `docs/ASSET_COMPLIANCE.md` §3
- [ ] No Kenney Castle kit or primitive placeholders in player-facing scenes (M5 art pass)
- [ ] Curated BGM/VO — no dev-only procedural audio in ship build
- [ ] GodotSteam **4.20+** installed for Godot 4.7 export
- [ ] Credits screen lists Godot MIT + Noto OFL + GodotSteam MIT + ACE-Step/ElevenLabs if used + any CC-BY attributions
- [ ] Playtest on Windows hardware
