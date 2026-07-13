# Generation brief — `tide_keeper_p1`

**Status:** M5 final boss (hero jury)  
**Authority:** `CHARACTER_BIBLE.md` §6, `BOSS_DESIGNS.md` §4, `qa_catalog.json`  
**Phase:** SC-15–16 `palace_throne_tides`

## Intent

Humanoid water form **~3.2 m** (P1–P2); blurred clock numerals in cloak (**unreadable**); phase mesh swaps; choice gate idle hold at 10% HP.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Tragic time deity — uncanny calm |
| Secondary mood | Stolen time motif — blurred, not readable clocks |
| Audience read | Final boss — awe, sorrow, moral weight |
| Static read (turntable) | Flowing water body; numeral cards blurred; not horror face |
| Motion feel (human L6) | `idle_drift` holds during choice; phase shrink feels tragic |
| Must avoid | Readable clock horror, comedy wizard, heroic final boss pose |
| Story anchor | SC-15–16 choice gate |

## Tool chain

Meshy/Blender ×3 phase meshes → UV scroll shaders → GLB per phase.

**Exports:**
- `game/assets/models/enemies/tide_keeper/tide_keeper_p1.glb`
- `game/assets/models/enemies/tide_keeper/tide_keeper_p2.glb` (cloak wave +8k)
- `game/assets/models/enemies/tide_keeper/tide_keeper_p3.glb` (~1.8 m human scale)

## Positive prompts

### Phase 1
- Translucent water shell `#1A4A5A` → `#4AE8D8` edges
- Cloak volume with **blurred** numeral cards `#D4A55A` @ 30% opacity — **not legible**
- Calm ripple UV scroll

### Phase 2
- Faster flow; higher emissive; cloak becomes tidal wave silhouette (+8k swap)

### Phase 3
- Shrinks to **1.8 m**; more opaque; tragic stillness; muted palette

## Negative prompts

readable clock face, Roman numerals sharp, European wizard, chibi, pure white body, anime hair

## Hard metrics

| Field | P1 | P2 | P3 |
|-------|----|----|-----|
| Tris | 20k–50k | +8k cloak | ~18k |
| Height | 3.2 m | 3.2 m | 1.8 m |

### Required animations (P1 GLB minimum)

| Clip | Loop | Notes |
|------|------|-------|
| `idle_drift` | Yes | Choice gate hold |
| `tidal_fingers` | No | |
| `maelstrom` | No | Phase 2 pulse |
| `death_dissolve` | No | |

## Phase swap rules

- Cross-fade **0.2 s** on mesh swap; no T-pose pop
- Numerals: blur in texture — **QA rejects readable time**

## Acceptance

- [ ] Numerals unreadable at gameplay cam (vision jury)
- [ ] `idle_drift` holds during SC-16 choice UI
- [ ] `L2_model_jury` PASS on P1
- [ ] Phase 2/3 GLBs registered before M5 ship
