---
id: bosses
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 1156
summary: "Shore Wraith, Palace Sentinel, Tide Keeper"
---
# Character Bible — Boss Enemies

**Hub:** [`enemies.md`](../enemies.md)

## When to read

Use **Character Bible — Boss Enemies** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Shore Wraith (`shore_wraith`) — BOSS](#shore-wraith-shore_wraith-boss)
- [Palace Sentinel (`palace_sentinel`) — MINIBOSS](#palace-sentinel-palace_sentinel-miniboss)
- [Tide Keeper (`tide_keeper`) — FINAL BOSS](#tide-keeper-tide_keeper-final-boss)


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

### Palace Sentinel (`palace_sentinel`) — MINIBOSS

**Combat design:** `docs/design/gameplay/BOSS_DESIGNS.md` §3.

| Spec | Detail |
|------|--------|
| **Height** | ~2.5 m (tall guard; spear+shield read at **12 m** down `palace_sentinel_hall`) |
| **Silhouette** | Angular ryūgū lacquer plates; **tower shield + spear**; single horizontal gold eye slit (only face read) |
| **Tris** | ~22k LOD0; LOD1 ~11k for intro wide shot |
| **Mesh breakdown** | (1) Torso + leg armor 10k — lacquer plates, void gaps between segments; (2) Tower shield 5k — flat profile, gold rim; (3) Spear 2k; (4) Helmet 3k — horizontal slit, emissive eye; (5) Pauldrons/greaves 2k |
| **Palette** | Lacquer `#8B2A3A`; gold trim `#D4A55A`; void gaps `#1A1A2A`; eye slit emissive `#FFD890` at ~35% intensity |
| **Materials** | Matte lacquer toon ramp; gold trim stepped highlight; **no** European plate mail, no gloss PBR chrome |
| **Weakness** | Spirit ×1.5 (`spirit_weakness` in data) — Yuzu `purify` VFX must contrast lacquer red |
| **VFX** | Eye slit pulse on `shell_harden`; single-frame spear glint on thrust — no heavy particles |
| **Animations** | `idle`, `spear_thrust`, `shell_harden`, `hit`, `death` |
| **Intro** | 3s march from hall depth (`BOSS_DESIGNS.md` §7) |
| **Arena** | `palace_sentinel_hall` — SC-14; save shrine exterior marker `palace_sentinel_hall` |
| **GLB** | `game/assets/models/enemies/palace_sentinel/palace_sentinel.glb` |
| **Portrait** | 512×512 — helmet + slit eye; shield rim visible |

**Combat:** Shield block stance; spear thrust telegraph ≥0.3 s; weak to Spirit (Yuzu)

---



### Tide Keeper (`tide_keeper`) — FINAL BOSS

**Combat design:** `docs/design/gameplay/BOSS_DESIGNS.md` §4.

| Spec | Detail |
|------|--------|
| **Height** | Phase 1–2: ~3.2 m; Phase 3: ~1.8 m (shrinks to human scale) |
| **Silhouette** | Humanoid water form; blurred clock numerals in cloak volume |
| **Tris** | ~38k LOD0 (phase 1 body); phase 2 cloak swap +8k; phase 3 mesh swap 18k |
| **Mesh breakdown** | (1) Core body 12k — translucent water shell; (2) Cloak volume 20k — sculpted wave + embedded numeral cards (blurred, not readable); (3) Crown/head 6k |
| **Palette** | Body `#1A4A5A` → `#4AE8D8` edge; cloak `#1A1A3A`; numerals `#D4A55A` at 30% opacity |
| **Phase materials** | P1: calm ripple scroll; P2: faster flow + higher emissive; P3: muted, more opaque, tragic stillness |
| **VFX** | Flowing UV scroll on body; Maelstrom phase = cloak mesh scale pulse |
| **Animations** | `idle_drift`, `tidal_fingers`, `borrowed_moment`, `gentle_pull`, `maelstrom`, `ebb_remembrance`, `phase_transition` ×2, `last_mercy`, `death_dissolve` |
| **Choice gate** | At 10% HP combat pauses; mesh holds idle_drift; UI overlay only |
| **GLB** | `game/assets/models/enemies/tide_keeper/tide_keeper_p1.glb`, `tide_keeper_p2.glb`, `tide_keeper_p3.glb` |
| **Portrait** | 768×768 — phase 1 hero; UI may swap to p3 for choice moment |

---
