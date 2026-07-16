# Tides of Urashima — Art Direction Bible

**Version:** 1.1 (Pre-build pivot)  
**Visual target:** **High-detail stylized Japanese 3D** — automated stylized albedo, readable silhouettes, authored environments. Not anime-realistic or photoreal PBR — closer to *Ni no Kuni* environmental richness and *Eastward* clarity with Japanese coastal motifs.

**Production policy:** Quality-first **automated** pipeline — no human artists in art/audio production. See `docs/art/ART_AUTOMATION_PIPELINE.md`.

**Audience note (men 20–30):** Muted palette, emotional weight, no chibi comedy. Beauty with decay.

**Related docs:** `docs/art/CHARACTER_BIBLE.md`, `docs/world/ENVIRONMENT_KITS.md`, `docs/ui/CINEMATICS.md`, `docs/art/ITEMS_3D_MODEL_GUIDE.md`, `docs/art/RENDERING_GUIDE.md`

### Ship rule (v1)

**No primitive placeholders** (`BoxMesh`, `CapsuleMesh`, Kenney knight, procedural spheres) in player-facing builds. Greybox may exist in editor-only layers during development.

---

## 1. Color palette

### Hub — Ruined Village
| Role | Hex | Usage |
|------|-----|-------|
| Fog grey | `#8B9DAF` | Sky, distance |
| Weathered wood | `#5C4A3A` | Buildings, pier |
| Seaweed green | `#3D5C4A` | Moss, decay |
| Rust accent | `#8B3A2A` | Banners, warning |
| Pale sand | `#C9B89A` | Ground, beach |

### Dungeon — Tidal Caves
| Role | Hex | Usage |
|------|-----|-------|
| Deep teal | `#1A4A5A` | Water, shadows |
| Biolume cyan | `#4AE8D8` | Algae, interactables |
| Wet stone | `#3A3A45` | Walls, floor |

### Dungeon — Dragon Palace Gate
| Role | Hex | Usage |
|------|-----|-------|
| Coral gold | `#D4A55A` | Trim, pillars |
| Palace crimson | `#8B2A3A` | Banners, accents |
| Ethereal white | `#E8E4DC` | Marble, glow |
| Void blue | `#1A1A3A` | Sky, void gaps |

---

## 2. Character silhouettes

Readable at gameplay camera distance. Exaggerate head-to-body ratio slightly (1:5, not chibi 1:3). Full model sheets: `docs/art/CHARACTER_BIBLE.md`.

### Urashima
- Long coat over traditional fisherman's tunic
- Lacquer box on hip (glowing faintly in palace zones)
- Slouched posture → straightens through story

### Yuzu
- Shrine maiden hakama, torn hem
- Semi-transparent lower body (spirit)
- Twin braids, fox-bell accessory

### Roku
- Bulky dive suit, patched
- Harpoon on back
- Wide stance (tank read)

### Enemies
- **Salt Crab:** Low wide silhouette
- **Tide Wraith:** Tall, dripping, no legs
- **Shore Wraith:** Massive draped form
- **Palace Sentinel:** Angular armor, single eye slit
- **Tide Keeper:** Humanoid tide, flowing water cloak

---

## 3. Environment style rules

1. **Modular kits first** — 80% reused pieces (walls, floors, rocks, props); see `docs/world/ENVIRONMENT_KITS.md`
2. **Poly budget** — Modules 500–3k tris; hero set-pieces (torii, palace gate) 8k–20k
3. **Automated stylized albedo** (ComfyUI/Material Maker + `palette_remap.py`) + light normal maps OK; single toon ramp across scene
4. **No PBR realism** — avoid glossy skin, HDR reflections
5. **Fog always on** in hub (draw distance mask)
6. **Water** is stylized (sculpted basins + foam decals, not simulation)
7. **Lighting:** One dominant directional + colored fill per zone
8. **Japanese coastal / ryūgū motifs only** — no European castle or medieval fantasy props

---

## 4. UI style

- **Font:** Noto Serif JP (headings) + Noto Sans (body) — OFL license
- **Menu frames:** Ink-wash border texture (subtle)
- **HP bars:** Horizontal, deep red fill, dark frame
- **Combat intent icons:** Simple pictograms (sword, skull, shield, sparkles)
- **Dialogue box:** Lower third, semi-transparent `#1A1A2ECC`, white text

---

## 5. Poly budgets

| Asset | Tris (target) |
|-------|---------------|
| Urashima (hero) | 12k–18k |
| Party members | 10k–15k each |
| Standard enemy | 5k–10k |
| Boss | 25k–40k |
| Environment module | 500–3k |
| Handheld item / pickup | 200–1.2k |
| Equipped weapon | 800–2.5k |
| Key story prop (lacquer box) | 1k–3k |
| Hero set-piece (torii, gate) | 8k–20k |

---

## 6. Asset sourcing plan (automated)

**Priority:** AI-generated heroes + set-pieces; curated CC0 Japanese-environment packs for modular fill. **No commission or hand-paint ship path.**

| Need | Approach | License |
|------|----------|---------|
| Characters (Urashima, Yuzu, Roku, bosses) | **Meshy / Tripo / Rodin** + Mixamo rig | Service ToS + register |
| Japanese ruins / coastal kits | Curated packs (itch.io, Sketchfab CC0) + AI trim | CC0 / documented |
| Rocks, cliffs (shared) | Poly Haven + toon shader | CC0 |
| Zone textures | **ComfyUI** or **Material Maker** + `palette_remap.py` | Workflow output |
| UI frames / icons | **GameLab MCP** or ComfyUI UI workflow | Per tool ToS |
| Animations | Mixamo (humanoid rig) | Mixamo ToS |
| UI icons (fallback) | Procedural / GameLab ink-wash | CC0 / own |
| SFX | Freesound (filter CC0) + procedural | CC0 |
| Music | **ACE-Step 1.5** curated prompts | MIT (ACE-Step) |

**Deprecated for ship builds (M5):** Kenney Castle kit (European read), Quaternius as final character base, procedural primitive placeholders. Kenney Nature may remain only if art-reviewed — see `docs/art/LICENSES.md` §Kenney (dev greybox only).

**Rule:** Log every download in `docs/art/LICENSES.md` before import. **Run `bash tools/check_asset_compliance.sh` before commit.**

**Copyright policy:** Only ship-safe licenses (CC0, MIT, OFL, public domain, documented AI service ToS). **Banned:** all-rights-reserved, CC-BY-NC, CC-BY-SA, unknown sources. Full list: `docs/art/ASSET_COMPLIANCE.md`.

---

## 7. AI 3D → Godot pipeline

1. Generate mesh via Meshy/Tripo/Rodin per `docs/art/CHARACTER_BIBLE.md` poly budgets
2. Items & props per `docs/art/ITEMS_3D_MODEL_GUIDE.md`
3. Blender — decimate, UV unwrap; ComfyUI/Material Maker albedo (4K heroes, 2K modules, 1K weapons)
4. `python3 tools/palette_remap.py` on texture sheets
5. Export as `.glb` (embedded textures)
6. Import to `game/assets/models/characters/`, `environment/`, or `items/`
7. Rig humanoids via Mixamo if needed
8. Materials: Godot toon shader family; spirits use alpha on lower body

Full workflow: `docs/art/ART_AUTOMATION_PIPELINE.md` §5.

---

## 8. Reference mood board (keywords)

- Grey overcast Japanese fishing coast
- Submerged torii gates (real-world photography)
- Dragon Palace — Takato Yamamoto woodblock intensity (tone only, not art theft)
- Combat UI — Persona 5 clarity (without copying layout)
- Boss scale — Shadow of the Colossus (emotional, not technical)

---

## 9. What to avoid

- Bright candy colors in hub
- Overly sexualized character designs
- Generic fantasy medieval props (stay Japanese coastal)
- Mixing realistic and toon shaders in same scene
- Asset Store "office worker" models retextured as fishermen
- **BoxMesh / primitive placeholders in shipped scenes**
- Low-poly CC0 kitbash as final art (prototype only)

---

## 10. Vertical slice gate

**SC-02 Ruined Village** is gated twice — greybox first, final art later:

### Phase 1 gate (greybox slice — rendering foundation)

- [ ] Palette matches §1 hex values at gameplay camera distance (lights, fog, sky)
- [ ] Filmic/ACES tonemap + zone fog per `RENDERING_GUIDE.md` (no default grey)
- [ ] Toon ramp shader on ground/blockout meshes
- [ ] 60 FPS @ 1080p on target hardware
- Greybox/primitive meshes **allowed** at this gate (dev only — `LEVEL_DESIGN.md` §1)

### M5 / Phase 7 gate (final art — before ship)

- [ ] Urashima authored model + walk/idle
- [ ] Hero torii + shack + well (no primitives)
- [ ] Zero primitive/greybox meshes in player-facing scenes
- [ ] 60 FPS @ 1080p maintained after art pass
