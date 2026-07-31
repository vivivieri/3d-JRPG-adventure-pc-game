---
id: art-code-ship
type: reference
phase: [1, 5]
audience: [visual, release, audio]
status: active
authority: art
tokens_est: 758
summary: "Art, ship status, code, M6 checklist"
---
# Licenses — Art, ship status, code, M6 checklist

**Hub:** [`LICENSES.md`](../LICENSES.md)

## Art (original — no third-party images)

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| Zone textures (`textures/zones/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | World material albedo |
| UI panels & bars (`ui/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue, menu, HP/MP |
| Portraits (`ui/portraits/*.png`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Dialogue silhouettes |
| Icons (`ui/icons/*.png`, `ui/icon.png`, `ui/icon.svg`) | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | App icon (PNG + SVG), combat intents |
| Main menu background | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Title screen |
| Steam capsules & screenshots | `tools/generate_game_art.py` | MIT (repo) | 2026-07 | Store page marketing |
| Pitch illustrations (`docs/archive/pitch/illustrations/**/*.png`) | Cursor AI image generation | Pitch/marketing use | 2026-07 | Storyboard set — replace with 3D for ship |
| Marketing trailer (`steam/trailer.mp4`, `trailer_ja.mp4`, `trailer_zh.mp4`, `trailer_zh-Hant.mp4`) | `tools/generate_marketing_trailer.py` | MIT (repo) + pitch art above | 2026-07 | ~75s; procedural or ACE-Step BGM (`steam/trailer_bgm.ogg`) |
| AI video b-roll (optional) | Runway / Kling / similar | Per vendor ToS | — | **Marketing trailer only** — log in manifest; never in-game |

Rendered in code (Pillow). Title text uses bundled Noto (OFL) baked into PNG only.

---


## 3D models — ship status

| Status | Notes |
|--------|-------|
| **Kenney CC0 kits** | Dev greybox in `game/assets/models/` — **replace before M5 ship** for palace/hero props |
| **Poly Haven CC0** | High-poly nature glTF in `game/assets/models/polyhaven/`. Not committed — run installer |
| **Hero meshes** | AI 3D + automated NPR albedo per `docs/design/art/CHARACTER_BIBLE.md` — M5 deliverable |

---


## Code

| Item | Source | License | Notes |
|------|--------|---------|-------|
| Game scripts | Original (this repo) | MIT | See repository `LICENSE` |

---


## Checklist before Steam ship (M6)

- [ ] `bash tools/check_asset_compliance.sh` passes (proof in `docs/archive/compliance/COMPLIANCE_REPORT.md`)
- [ ] Every new asset registered in `docs/asset_manifest.license.json` + this file
- [ ] No banned licenses (NC, SA, ARR, unknown) — see `docs/design/art/ASSET_COMPLIANCE.md` §3
- [ ] No Kenney Castle kit or primitive placeholders in player-facing scenes (M5 art pass)
- [ ] Curated BGM/VO — no dev-only procedural audio in ship build
- [ ] GodotSteam **4.20+** installed for Godot 4.7 export
- [ ] Credits screen lists Godot MIT + Noto OFL + GodotSteam MIT + ACE-Step/ElevenLabs if used + any CC-BY attributions
- [ ] Playtest on Windows hardware
