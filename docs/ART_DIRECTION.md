# Tides of Urashima — Art Direction Bible

**Visual target:** Stylized low-poly 3D with painted-texture accents. Not anime-realistic — closer to *Rime*, *Sable*, or *Eastward* mood with Japanese coastal motifs.

**Audience note (men 20–30):** Muted palette, emotional weight, no chibi comedy. Beauty with decay.

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

Readable at low-poly distance. Exaggerate head-to-body ratio slightly (1:5, not chibi 1:3).

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

1. **Modular kits first** — 80% reused pieces (walls, floors, rocks, props)
2. **Vertex color** for variation before unique textures
3. **No PBR realism** — flat or hand-painted albedo, minimal roughness variation
4. **Fog always on** in hub (draw distance mask)
5. **Water** is stylized (flat color + foam line, not simulation)
6. **Lighting:** One dominant directional + colored fill per zone

---

## 4. UI style

- **Font:** Noto Serif JP (headings) + Noto Sans (body) — OFL license
- **Menu frames:** Ink-wash border texture (subtle)
- **HP bars:** Horizontal, deep red fill, dark frame
- **Combat intent icons:** Simple pictograms (sword, skull, shield, sparkles)
- **Dialogue box:** Lower third, semi-transparent `#1A1A2ECC`, white text

---

## 5. Free asset sourcing plan

| Need | Source | License |
|------|--------|---------|
| Modular ruins | Kenney.nl Nature / Building kits | CC0 |
| Low-poly characters base | Quaternius Universal Base | CC0 |
| Rocks, caves | Quaternius Nature Pack | CC0 |
| Textures | ambientCG, Poly Haven | CC0 |
| Animations | Mixamo (humanoid rig) | Mixamo ToS (free commercial) |
| UI icons | Kenney Game Icons | CC0 |
| SFX | Freesound (filter CC0) | CC0 |
| Music | OpenGameArt (curated) | Per-track license |

**Rule:** Log every download in `docs/LICENSES.md` before import.

---

## 6. Blender → Godot pipeline

1. Model in Blender (low poly, &lt; 5k tris per character)
2. UV unwrap → paint or flat color
3. Export as `.glb` (embedded textures)
4. Import to `game/assets/models/`
5. Rig humanoids via Mixamo if needed
6. Materials: Godot StandardMaterial3D, unshaded or toon for spirits

---

## 7. Reference mood board (keywords)

- Grey overcast Japanese fishing coast
- Submerged torii gates (real-world photography)
- Dragon Palace — Takato Yamamoto woodblock intensity (tone only, not art theft)
- Combat UI — Persona 5 clarity (without copying layout)
- Boss scale — Shadow of the Colossus (emotional, not technical)

---

## 8. What to avoid

- Bright candy colors in hub
- Overly sexualized character designs
- Generic fantasy medieval props (stay Japanese coastal)
- Mixing realistic and toon shaders in same scene
- Asset Store "office worker" models retextured as fishermen
