---
id: tiers-requirements
type: how-to
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 793
summary: "Art Automation Pipeline — Tier matrix & MCP requirements — All listed servers and offline tools are required for the project. Agents use this table at session s"
---
# Art Automation Pipeline — Tier matrix & MCP requirements

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## When to read

Use **Art Automation Pipeline — Tier matrix & MCP requirements** (roles: visual, builder) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Tier matrix (right tool, right job)](#1-tier-matrix-right-tool-right-job)
- [2. MCP and toolchain requirement tiers](#2-mcp-and-toolchain-requirement-tiers)


## 1. Tier matrix (right tool, right job)

| Job | Primary (quality-first) | Free when quality ≥ paid | Post-process | Hand off to |
|-----|-------------------------|---------------------------|--------------|-------------|
| GDScript, shaders, tests | **GodotPrompter** | — | — | GDAI MCP |
| Scene graph, materials, lights | **GDAI MCP** | — | — | F5 verify |
| Debug, signal trace | **Godotiq** | — | — | GDAI if `.tscn` fix |
| L4/L5 automated tests | **Godot MCP Pro** (`--minimal`) | Headless unit tests (L0–L2) | — | — |
| **Zone NPR albedos** (wood, stone, ground) | **ComfyUI** locked stylized workflow **or** **Material Maker** | Material Maker for stone/wood; Poly Haven + toon shader for nature | **`tools/palette_remap.py`** | GDAI assigns |
| **UI frames, ink borders, icon sheets** | **GameLab MCP** | Repo procedural placeholders (dev asset output only) | palette remap | GDAI UI scenes |
| **Hero / enemy 3D** | **Meshy / Tripo / Rodin** → GLB | Poly Haven rocks/trees (CC0 props only) | Blender decimate/UV if needed | Mixamo rig → GDAI |
| **Set-pieces** (torii, lacquer box, gate) | AI 3D + ComfyUI texture projection **or** Material Maker | Same | palette remap | GDAI placement |
| **Portraits** | ComfyUI character sheet workflow | Procedural silhouettes (`generate_procedural_portraits.py`) until M5 | palette remap | UI |
| **Zone BGM / cinematic scores** | **ACE-Step 1.5** (curated prompts) | `generate_game_audio.py` (dev placeholder) | Loudness normalize per `AUDIO_PRODUCTION_GUIDE.md` | GDAI audio buses |
| **Selective VO** (12 clips) | **ElevenLabs** | No equal free tier | Register in `LICENSES.md` | Voice bus |
| **In-game video** | Godot `CinematicDirector` | No FMV | — | — |
| **Marketing trailer** | `generate_marketing_trailer.py` + pitch PNGs | — | Optional Runway/Kling b-roll | `steam/` only |
| **Design context** | `docs/` + `game/data/` | — | JSON commits |

---


## 2. MCP and toolchain requirement tiers

All listed servers and offline tools are **required** for the project. Agents use this table at session startup.

| Tier | Servers / tools | If missing |
|------|-----------------|------------|
| **MCP — block** | `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp` + `GAMELAB_API_KEY` | **STOP** — notify user |
| **Offline — block** | **Blender** (M5 turntable QA) | **STOP** — `bash tools/install_extended_toolchain.sh` |
| **Offline — per task** | ComfyUI, Material Maker, ACE-Step GPU | Document fallback used; quality-first per §1 |

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_dev_environment.sh
bash tools/check_extended_toolchain.sh   # GameLab + Blender = FAIL if absent
```

---
