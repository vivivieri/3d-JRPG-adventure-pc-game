# Art Automation Pipeline — Quality-First, Zero Human Artists

**Version:** 1.0  
**Applies to:** M5 art rebuild and all player-facing assets on `main`  
**Authority:** When this doc conflicts with older “hand-painted / commission” language elsewhere, **this doc wins** for production tooling.

**Principle:** Ship **high-detail stylized Japanese 3D** using the **best automated tool per job**. Quality over cost — paid tools are fine when no free option matches output. **No human artists** in the art or audio production path (modeling, texturing, painting, mixing, VO performance). **Human playtest** (L6) is separate — see `docs/PLAYTEST_SCRIPT.md`.

**Cross-refs:** `docs/ART_DIRECTION.md`, `docs/MCP_STACK.md`, `docs/RENDERING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md`, `docs/ASSET_COMPLIANCE.md`, `.cursorrules` §0

---

## 1. Tier matrix (right tool, right job)

| Job | Primary (quality-first) | Free when quality ≥ paid | Post-process | Hand off to |
|-----|-------------------------|---------------------------|--------------|-------------|
| GDScript, shaders, tests | **GodotPrompter** | — | — | GDAI MCP |
| Scene graph, materials, lights | **GDAI MCP** | — | — | F5 verify |
| Debug, signal trace | **Godotiq** | — | — | GDAI if `.tscn` fix |
| L4/L5 automated tests | **Godot MCP Pro** (`--minimal`) | Headless unit tests (L0–L2) | — | — |
| **Zone NPR albedos** (wood, stone, ground) | **ComfyUI** locked stylized workflow **or** **Material Maker** | Material Maker for stone/wood; Poly Haven + toon shader for nature | **`tools/palette_remap.py`** | GDAI assigns |
| **UI frames, ink borders, icon sheets** | **GameLab MCP** | Repo procedural placeholders (dev only) | palette remap | GDAI UI scenes |
| **Hero / enemy 3D** | **Meshy / Tripo / Rodin** → GLB | Poly Haven rocks/trees (CC0 props only) | Blender decimate/UV if needed | Mixamo rig → GDAI |
| **Set-pieces** (torii, lacquer box, gate) | AI 3D + ComfyUI texture projection **or** Material Maker | Same | palette remap | GDAI placement |
| **Portraits** | ComfyUI character sheet workflow | Procedural silhouettes (`generate_procedural_portraits.py`) until M5 | palette remap | UI |
| **Zone BGM / cinematic scores** | **ACE-Step 1.5** (curated prompts) | `generate_game_audio.py` (dev placeholder) | Loudness normalize per `AUDIO_PRODUCTION_GUIDE.md` | GDAI audio buses |
| **Selective VO** (12 clips) | **ElevenLabs** | No equal free tier | Register in `LICENSES.md` | Voice bus |
| **In-game video** | Godot `CinematicDirector` | No FMV | — | — |
| **Marketing trailer** | `generate_marketing_trailer.py` + pitch PNGs | — | Optional Runway/Kling b-roll | `steam/` only |
| **Design context** | `docs/` + `game/data/` | — | JSON commits |

---

## 2. MCP requirement tiers

Not every MCP server blocks every task. Agents use this table at session startup.

| Tier | Servers | If missing |
|------|---------|------------|
| **P0 — block** | `godot-mcp`, `godotiq`, `godot-mcp-pro` | **STOP** — notify user |
| **P1 — UI art** | `gamelab-mcp` + `GAMELAB_API_KEY` | **WARN** — procedural UI placeholders |
| **Offline** | ComfyUI, Blender, ACE-Step GPU | **WARN** per task — document fallback used |

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_dev_environment.sh
bash tools/check_extended_toolchain.sh   # GameLab = WARN if absent; P0 MCP = FAIL
```

---

## 3. Zone texture workflow (not GameLab-first)

GameLab is **UI-focused**. Zone albedos use ComfyUI or Material Maker.

### 3.1 ComfyUI batch (heroes, unique surfaces)

```
1. READ  docs/ART_DIRECTION.md §1 palette for zone
2. ComfyUI — locked workflow: stylized NPR tileable, muted coastal decay
3. Export PNG → game/assets/textures/zones/<zone>/
4. python3 tools/palette_remap.py --zone <zone> --input <path>   # enforce §1 hex
5. python3 tools/register_asset.py + docs/LICENSES.md
6. GodotPrompter — tune toon_base.gdshader if needed
7. GDAI MCP — assign in zone .tscn, F5 verify
8. bash tools/check_asset_compliance.sh
```

### 3.2 Material Maker (stone, wood, ground — free path)

```
1. Material Maker — procedural weathered wood #5C4A3A, wet stone #3A3A45
2. Export seamless PNG → game/assets/textures/zones/<zone>/
3. palette_remap.py → register → GDAI assign
```

### 3.3 Nature meshes (rocks, trees)

- **Poly Haven** CC0 meshes + project **toon ramp** — no photoreal PBR in player scenes.
- Kenney Nature: **dev greybox only** — not ship art (`docs/LICENSES.md`).

---

## 4. UI art workflow (GameLab-primary)

```
1. READ  docs/ART_DIRECTION.md §4 UI style
2. GameLab MCP — ink-wash frame, combat icon sheet, menu border (muted, not candy-bright)
3. palette_remap.py on full-color gens
4. Save → game/assets/textures/ui/
5. GDAI MCP — assign to Control themes / TextureRects in UI scenes
```

**Dev fallback:** `generate_procedural_portraits.py` and flat-color UI placeholders until GameLab key is set.

---

## 5. 3D character & prop workflow

```
1. READ  docs/CHARACTER_BIBLE.md poly budgets
2. Meshy / Tripo / Rodin — text prompt from bible silhouettes (Japanese coastal, not chibi)
3. Blender — decimate to budget, UV unwrap, export GLB
4. ComfyUI or Material Maker — stylized albedo bake / projection
5. palette_remap.py on texture sheets
6. Mixamo — humanoid rig + walk/idle/combat clips (Mixamo ToS)
7. Import → game/assets/models/characters/ or environment/
8. GodotPrompter — toon shader + emission states (lacquer box)
9. GDAI MCP — place in scene, F5 verify
10. `docs/MODEL_QA.md` — GLB lint + turntable jury before import; `docs/VISUAL_QA.md` after in-scene
```

**No commission path.** Rights = service ToS + `register_asset.py` + `LICENSES.md`.

---

## 6. Palette compliance (`palette_remap.py`)

All **2D generated** art (ComfyUI, GameLab, Material Maker exports) must pass palette remap before ship.

```bash
python3 tools/palette_remap.py --zone ruined_village --input game/assets/textures/zones/ruined_village/wood_planks.png
python3 tools/palette_remap.py --help
```

Maps dominant hues toward zone rows in `docs/ART_DIRECTION.md` §1. Agents run this **after every external gen**, before `register_asset.py`.

---

## 7. Audio automation (no human mix)

| Stage | Tool | Ship rule |
|-------|------|-----------|
| Dev placeholder | `generate_game_audio.py` | Replace before M5 |
| Zone + hero BGM | ACE-Step 1.5 via `generate_ai_bgm.sh` | **Curated prompt sheet** — normalize to -16 LUFS; register MIT |
| Selective VO | ElevenLabs via `generate_ai_vo.sh` | 12 lines only — `docs/VO_HIT_LIST.md` |
| SFX layers | Freesound **CC0-only** + procedural | Register each file |

**No human mix pass or commission** on the ship path. Quality gate = `docs/AUDIO_QA.md` (technical + optional hero jury) + L6 listen.

**On any art/audio/model QA FAIL:** `docs/QA_REMEDIATION_LOOP.md` — brief + one lever change before rebuild (max 3 attempts).

---

## 8. Quality gates (M5)

Before marking M5 complete (`docs/MILESTONES.md`):

- [ ] `bash tools/check_scene_visuals.sh` passes (no primitives in ship `.tscn`)
- [ ] All zone albedos pass `palette_remap.py` + gameplay-camera palette check (ART_DIRECTION §10)
- [ ] Single toon ramp family (`RENDERING_GUIDE.md`)
- [ ] Every external asset in `LICENSES.md` + `asset_manifest.license.json`
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] 60 FPS @ 1080p on GTX 1060 — SC-02 first
- [ ] No FMV in `game/` — cinematics are Godot-only (`docs/CINEMATICS.md`)

---

## 9. Pay vs free decision rule

```
IF free_tool_output >= paid_tool_output on blind review (same prompt, same zone):
    USE free
ELSE:
    USE paid (document cost in LICENSES.md / team notes)
```

Examples where **paid typically wins:** GameLab UI sheets, ElevenLabs VO, Meshy hero characters.  
Examples where **free typically wins:** Material Maker stone/wood, Poly Haven rocks, procedural dev audio.

---

## 10. Explicitly rejected

| Approach | Reason |
|----------|--------|
| Human commission / hand-paint ship path | Policy — fully automated pipeline |
| GameLab for **all** zone textures | UI-primary; zone path uses ComfyUI / Material Maker |
| Kenney kits in ship builds | European/wrong read — greybox only |
| Random web images / unknown license | `ASSET_COMPLIANCE.md` |
| FMV in-game | Godot cinematics only |
| Full-script VO | 12 selective clips only |

---

## Related

- `docs/MCP_STACK.md` — MCP R&R map (tiered requirements)
- `docs/ART_DIRECTION.md` — palette, silhouettes, poly budgets
- `tools/palette_remap.py` — post-gen palette enforcement
- `tools/check_extended_toolchain.sh` — GameLab WARN vs P0 FAIL
