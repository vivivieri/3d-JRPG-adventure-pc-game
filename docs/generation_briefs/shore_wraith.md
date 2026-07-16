# Generation brief — `shore_wraith`

**Status:** M5 · first boss (hero jury)  
**Authority:** `CHARACTER_BIBLE.md` §6, `BOSS_DESIGNS.md` §2, `qa_catalog.json`  
**Phase:** SC-09 `cave_boss_arena_ring`

## Intent

Colossal **4.0 m** draped monolith — pooled cloth base, 5–7 embedded villager faces; `heavy_slam` telegraph readable; emerges from pool (5 s intro).

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Colossal communal guilt, drowned grief |
| Secondary mood | Faces under folds — unsettling not splatter horror |
| Audience read | First boss — awe and dread |
| Static read (turntable) | Draped monolith pools at base; faces glimpsed in folds |
| Motion feel (human L6) | `heavy_slam` telegraph readable; emerge from pool feels inevitable |
| Must avoid | Jump-scare horror, European reaper, anime villain pose |
| Story anchor | SC-09 boss — village sins rise |

## Tool chain

Meshy/Blender hero sculpt → particle drip cards → Mixamo/custom rig → GLB.

**Export:** `game/assets/models/enemies/shore_wraith/shore_wraith.glb`

## Positive prompts

- Draped monolith, no legs; cloth pools at base
- Outer drape `#2A3A4A`; wet highlights `#4AE8D8`; faces `#C8A888` desaturated
- 5–7 embedded villager faces under folds (unsettling, not gore)
- Matte cloth toon; faces slightly glossy

## Negative prompts

European reaper, skeleton, anime villain, cloth simulation runtime, chibi, readable single hero face only

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 20,000 – 50,000 (LOD0 ~32k) |
| Height | **4.0 m** |
| Category | `boss` |

### Mesh breakdown

1. Outer drape ~18k  
2. Face cluster ~6k  
3. Arm tendrils ~4k  
4. Base mist cards ~4k  

### Required animations

| Clip | Loop | Duration | Notes |
|------|------|----------|-------|
| `idle_float` | Yes | 3.0 s | Subtle hover |
| `drowned_grasp` | No | 1.2 s | Reach |
| `heavy_slam` | No | **1.5–2.0 s** | **Telegraph ≥0.5 s** |
| `death_collapse` | No | 2.5 s | Pool sink |

## Arena / camera

- Arena: `cave_boss_arena_ring` — boss centered, camera looks **up**
- Golden shot: `artifacts/screenshots/phase5_shore_wraith_boss.png`
- Intro: rise from water, alpha fade lower drape 5 s

## Acceptance

- [ ] `heavy_slam` telegraph at 8 m boss cam
- [ ] `L2_model_jury` PASS (hero jury)
- [ ] Phase transition hook for `regret_aura` (P1)
