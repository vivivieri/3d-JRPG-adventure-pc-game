---
id: audio-models
type: reference
phase: [1, 5]
audience: [visual, release, audio]
status: active
authority: art
tokens_est: 747
summary: "Licenses — Audio + 3D models — Third-party audio samples: Do not import random web loops. Filtered CC0 from documented sources (e.g. Freesound CC0-only) is allo"
---
# Licenses — Audio + 3D models

**Hub:** [`LICENSES.md`](../LICENSES.md)

## When to read

Use **Licenses — Audio + 3D models** (roles: visual, release, audio) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Audio](#audio)
- [3D models (CC0 — Kenney) — **dev greybox only**](#3d-models-cc0-kenney-dev-greybox-only)
- [3D models (CC0 — Poly Haven, high-poly)](#3d-models-cc0-poly-haven-high-poly)


## Audio

| Item | Source | License | Date | Used for |
|------|--------|---------|------|----------|
| Procedural BGM/SFX (`bgm/*.ogg`, `sfx/*.ogg`) | `tools/generate_game_audio.py` | MIT (repo) | 2026-07 | **Dev placeholder** — replace before M5 ship |
| ACE-Step ship tracks | ACE-Step 1.5 via `tools/generate_ai_bgm.py` | MIT (ACE-Step) | 2026-07 | Zone + cinematic hero BGM — curated prompts + loudness normalize |
| Selective VO (12 clips) | ElevenLabs via `tools/generate_ai_vo.py` | Commercial AI — verify ToS | 2026-07 | `game/assets/audio/voice/{locale}/*.ogg` — log each clip |
| Marketing trailer BGM | `tools/generate_marketing_trailer.py` or ACE-Step stitch | MIT / ACE-Step | 2026-07 | `steam/trailer_bgm.ogg` — marketing only |

**Third-party audio samples:** Do not import random web loops. Filtered CC0 from documented sources (e.g. Freesound CC0-only) is allowed **only** when registered here and in `asset_manifest.license.json` per `docs/design/art/ASSET_COMPLIANCE.md`. Default pipeline: procedural + ACE-Step + ElevenLabs.

---


## 3D models (CC0 — Kenney) — **dev greybox only**

| Item | Source | License | Used for |
|------|--------|---------|----------|
| Nature Kit GLBs (`models/nature/*.glb`) | Kenney Nature Kit | CC0 1.0 | **Phase 1–6 greybox** — trees, rocks, pier |
| Castle Kit OBJs (`models/castle/*.obj`) | Kenney Castle Kit | CC0 1.0 | **Phase 1–6 greybox** — blockout only |

Install curated subset: `bash tools/install_cc0_assets.sh` (requires `.asset-dl/` source packs).

**Ship rule (M5):** Replace Kenney Castle/European kit pieces in **player-facing builds** per `docs/design/art/ART_DIRECTION.md`. Nature kit pieces may remain only if art-reviewed and logged. Kenney Castle kit is **deprecated for ship** — do not ship palace gate from Castle kit.

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
