---
id: part-a
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 354
summary: "Character Bible — Enemy Bosses (A)"
---
# Character Bible — Enemy Bosses — Character Bible — Enemy Bosses (A)

**Hub:** [`part_b.md`](../part_b.md)

### Shore Wraith (`shore_wraith`) — BOSS

**Combat design:** `docs/design/gameplay/BOSS_DESIGNS.md` §2.

| Spec | Detail |
|------|--------|
| **Height** | ~4.0 m (colossal; camera looks up in arena) |
| **Silhouette** | Draped monolith; no legs; cloth pools at base |
| **Tris** | ~32k (LOD0); LOD1 ~15k for intro cinematic wide shot |
| **Mesh breakdown** | (1) Outer drape 18k — sculpted folds, no cloth sim; (2) Inner face cluster 6k — 5–7 embedded villager faces; (3) Arm tendrils 4k; (4) Base mist cards 4k |
| **Palette** | Drape `#2A3A4A`; wet highlights `#4AE8D8`; faces `#C8A888` desaturated |
| **Materials** | Matte cloth toon; faces slightly glossy (unsettling); additive drip particles |
| **VFX** | Water drip particles from hem; phase 2 whisper overlay on faces |
| **Animations** | `idle_float`, `drowned_grasp`, `regret_aura`, `heavy_slam`, `phase_transition`, `summon_wraith`, `death_collapse` |
| **Intro** | Emerges from pool — 5s; mesh rises from water plane with alpha fade on lower drape |
| **GLB** | `game/assets/models/enemies/shore_wraith/shore_wraith.glb` |
| **Portrait** | 512×512 — draped form + single visible face |

---
