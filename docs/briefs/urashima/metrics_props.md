---
id: metrics-props
type: how-to
audience: [visual, builder]
phase: [1, 5]
status: active
authority: briefs
tokens_est: 599
summary: "Hard metrics + props"
---
# Urashima Generation Brief — Hard metrics + props

**Hub:** [`urashima.md`](../urashima.md)

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
