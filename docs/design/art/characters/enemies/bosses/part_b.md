---
id: part-b
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 798
summary: "Character Bible — Enemy Bosses (B)"
---
# Character Bible — Enemy Bosses — Character Bible — Enemy Bosses (B)

**Hub:** [`part_b.md`](../part_b.md)

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
