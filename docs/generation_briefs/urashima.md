# Generation brief — `urashima`

**Status:** P0 · Phase 1 vertical slice  
**Authority:** `docs/CHARACTER_BIBLE.md` §2, `game/data/models/qa_catalog.json`  
**Cross-refs:** `docs/GENERATION_READINESS.md`, `docs/ART_AUTOMATION_PIPELINE.md` §5

---

## Intent (one sentence)

Weathered late-20s Japanese fisherman, adult **1:5** proportions (~1.7 m), dark indigo coat and cream tunic — **lacquer box on left hip readable at 8 m gameplay camera** in `ruined_village`.

---

## Tool chain

| Step | Tool | Output |
|------|------|--------|
| 1 | **Meshy** or **Tripo** | Base mesh + albedo (stylized, not PBR glossy) |
| 2 | **Blender** | Decimate to tri budget, UV unwrap, separate lacquer box mesh, export GLB |
| 3 | **ComfyUI** or **Material Maker** | Stylized albedo touch-up / projection if needed |
| 4 | `palette_remap.py` | Zone-neutral character palette compliance |
| 5 | **Mixamo** | Humanoid rig + animation clips (rename to whitelist) |
| 6 | `install_glb_import_pipeline.sh` | NPR post-import + toon shader on import |
| 7 | **GDAI MCP** | Place in `ruined_village.tscn`, F5 verify |

**Export path:** `game/assets/models/characters/urashima/urashima.glb`

---

## Positive prompt anchors

### Style
- Stylized Japanese coastal NPR — muted, emotional weight, beauty with decay
- Reference mood: *Eastward* clarity + *Ni no Kuni* material richness — **not** bright Ghibli fantasy, not photoreal PBR, not chibi

### Silhouette (must read at distance)
- Long **dark indigo coat** (`#2A3A4A`) open at front, wind-reactive hem (2 bone chains max)
- **Cream fisherman tunic** (`#D8C8A8`) with salt stains, rolled trousers
- **Straw sandals**, rope belt / obi
- **Lacquer box** on **left hip** — separate mesh; dormant red seam glow (`#8B2A3A` at 15%)
- Hair tied back (`#1A1A1A`); weathered face; slightly hunched Act I posture

### Palette (hard hex)

| Part | Hex |
|------|-----|
| Coat | `#2A3A4A` |
| Tunic | `#D8C8A8` |
| Skin | `#C8A888` |
| Hair | `#1A1A1A` |
| Box lacquer | `#6B1A1A` |
| Box clasp | `#C8A040` |

### Proportions & scale
- Head-to-body **1:5** (adult — no oversized anime head)
- **Height:** 1.7 m in Godot (1 unit = 1 m)
- Shoulder width ~0.45 m; coat hem ~mid-calf

---

## Negative prompt (required)

```
chibi, big anime eyes, cel-shaded glossy skin, PBR metallic, European medieval,
Kenney, low-poly blockout, T-pose shipped, cape superhero, fantasy armor,
bright saturated Ghibli colors, photoreal face, beard, western cowboy,
floating accessories, symmetrical perfect clean clothes
```

---

## Hard metrics (`qa_catalog.json`)

| Field | Value |
|-------|-------|
| Tris | 8,000 – 22,000 |
| Textures | ≥ 1 embedded |
| Rig | `mixamo_humanoid` |
| Category | `hero` |
| Hero jury | Yes |

### Required animations (CI floor — P0 ship)

| Clip | Loop | Target duration | Root motion | Notes |
|------|------|-----------------|-------------|-------|
| `idle` | Yes | 2.0–3.0 s | No | Subtle weight shift; box visible on hip |
| `walk` | Yes | 1.0–1.2 s/cycle | Yes (forward) | Exhausted fisherman gait Act I; ~1.4 m/s field speed |
| `interact` | No | 1.2–1.8 s | No | Reach / examine — banner, well, torii |
| `attack_light` | No | 0.5–0.7 s | No | Short katana draw from hip |
| `hit` | No | 0.3–0.5 s | No | Stagger without ragdoll |

### Allowed animations (ship when ready)

`run`, `attack_heavy`, `skill_cast`, `defeat`, `ending_dissolve`, `ending_stand`, `ending_row`

**Mixamo retarget notes (1:5 proportions):**
- Use **Mixamo auto-rigger** on decimated mesh; verify **wrist–hip–ankle** alignment before batch download
- If head reads too large post-rig: scale head bone **0.92–0.95** in Blender before export — do **not** shrink entire mesh below 1.65 m
- Rename all clips to lowercase snake_case matching table above (Mixamo defaults like `Walking` → `walk`)
- Coat hem: max **2** skirt bones; test `walk` for clipping through sandals at 45° camera

---

## Lacquer box (attached prop)

| State | When | Emission |
|-------|------|----------|
| Dormant | Hub, caves | `#8B2A3A` seam @ 15% |
| Awakened | Palace | Pulse 40–60% + motes |
| Choice | SC-16 | Full bloom + UI sync |

- Box is **separate mesh** parented to `hip_L` (or equivalent)
- Hip attach offset: ~0.12 m left, 0.08 m forward from pelvis — tune in GDAI so box edge shows in portrait framing

---

## Camera-distance readability (X-02)

| Check | Target |
|-------|--------|
| Gameplay camera | Third-person follow; ~8 m behind player; FOV ~65° (tune in `PlayerController`) |
| Face read | Brow + coat silhouette identifiable at 8 m — not photoreal detail, but **not** grey blob |
| Box read | Red lacquer mass visible on left hip at 8 m |
| Golden screenshot | `artifacts/screenshots/phase1_ruined_village_gameplay.png` with Urashima on main path |

---

## Costume layers (model order)

1. Body + face  
2. Tunic + trousers  
3. Coat (open front)  
4. Obi + rope belt  
5. Sandals  
6. Lacquer box (separate mesh)

---

## Acceptance evidence

- [ ] Turntable 4-view PNG (`artifacts/models/urashima_turntable.png`)
- [ ] Gameplay-distance screenshot — Urashima on village path at 8 m
- [ ] `python3 tools/check_model_technical.py --model urashima` — PASS
- [ ] `python3 tools/check_animation_whitelist.py --phase 1 --strict` — PASS (required floor)
- [ ] `L2_model_jury` — PASS (2-of-3 when API keys set)
- [ ] `L2_visual_jury` — PASS in `ruined_village` placement
- [ ] Portrait `game/assets/ui/portraits/urashima.png` — chest up, box edge visible (512×512 min)
- [ ] Registered: `python3 tools/register_asset.py add ...` + `LICENSES.md` entry

---

## Forbidden

- `CapsuleMesh` / `BoxMesh` placeholder in ship build
- T-pose in any shipped scene
- Clip names outside `allowed_animations` in catalog
- PBR glossy skin or metallic workflow materials
