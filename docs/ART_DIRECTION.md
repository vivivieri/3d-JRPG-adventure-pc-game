# Tides of Urashima — Art Direction Bible

**Version:** 1.1 (Pre-build pivot)  
**Visual target:** **High-detail stylized Japanese 3D** — hand-painted albedo, readable silhouettes, authored environments. Not anime-realistic or photoreal PBR — closer to *Ni no Kuni* environmental richness and *Eastward* clarity with Japanese coastal motifs.

**Audience note (men 20–30):** Muted palette, emotional weight, no chibi comedy. Beauty with decay.

**Related docs:** `docs/CHARACTER_BIBLE.md`, `docs/ENVIRONMENT_KITS.md`, `docs/CINEMATICS.md`, `docs/ITEMS_3D_MODEL_GUIDE.md`, `docs/RENDERING_GUIDE.md`

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

Readable at gameplay camera distance. Exaggerate head-to-body ratio slightly (1:5, not chibi 1:3). Full model sheets: `docs/CHARACTER_BIBLE.md`.

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

1. **Modular kits first** — 80% reused pieces (walls, floors, rocks, props); see `docs/ENVIRONMENT_KITS.md`
2. **Poly budget** — Modules 500–3k tris; hero set-pieces (torii, palace gate) 8k–20k
3. **Hand-painted albedo** + light normal maps OK; single toon ramp across scene
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

## 6. Asset sourcing plan (revised)

**Priority:** Custom or commissioned for heroes + set-pieces; curated Japanese-environment packs for modular fill.

| Need | Approach | License |
|------|----------|---------|
| Characters (Urashima, Yuzu, Roku, bosses) | **Custom Blender** or commission | Own / contract |
| Japanese ruins / coastal kits | Curated packs (itch.io, Sketchfab CC0) + custom trim | CC0 / own |
| Rocks, cliffs (shared) | Custom + Poly Haven / ambientCG | CC0 |
| Textures | Hand-painted tileables; ambientCG base | CC0 |
| Animations | Mixamo (humanoid rig) | Mixamo ToS |
| UI icons | Kenney Game Icons or custom ink-wash | CC0 / own |
| SFX | Freesound (filter CC0) | CC0 |
| Music | OpenGameArt or commissioned short score | Per-track |

**Deprecated for ship builds:** Kenney Castle kit (European read), Quaternius as final character base, procedural primitive placeholders.

**Rule:** Log every download in `docs/LICENSES.md` before import. **Run `bash tools/check_asset_compliance.sh` before commit.**

**Copyright policy:** Only ship-safe licenses (CC0, MIT, OFL, public domain, commissioned with rights). **Banned:** all-rights-reserved, CC-BY-NC, CC-BY-SA, unknown sources. Full list: `docs/ASSET_COMPLIANCE.md`.

---

## 7. Blender → Godot pipeline

1. Model in Blender per `docs/CHARACTER_BIBLE.md` poly budgets
2. Items & props per `docs/ITEMS_3D_MODEL_GUIDE.md`
3. UV unwrap → hand-paint albedo (4K heroes, 2K modules, 1K weapons)
4. Export as `.glb` (embedded textures)
5. Import to `game/assets/models/characters/`, `environment/`, or `items/`
6. Rig humanoids via Mixamo if needed
7. Materials: Godot toon shader family; spirits use alpha on lower body

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

Before full production, **SC-02 Ruined Village** must pass:

- [ ] Urashima authored model + walk/idle
- [ ] Hero torii + shack + well (no primitives)
- [ ] Palette matches §1 hex values at gameplay camera distance
- [ ] 60 FPS @ 1080p on target hardware
