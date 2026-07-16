# Generation brief — `palace_sentinel`

**Status:** M5 miniboss  
**Authority:** `CHARACTER_BIBLE.md` §6, `BOSS_DESIGNS.md` §3, `qa_catalog.json`  
**Phase:** SC-14 `palace_sentinel_hall`

## Intent

Angular ryūgū-jō armor **~2.5 m** — spear + tower shield; single horizontal gold eye slit; **spear+shield silhouette at 12 m**; weak to Spirit (Yuzu).

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Sterile palace menace, obedient violence |
| Secondary mood | Lacquer perfection — soulless not heroic |
| Audience read | Miniboss — teaches Spirit weakness |
| Static read (turntable) | Angular armor; spear+shield read at distance |
| Motion feel (human L6) | Spear thrust telegraph clear; block stance reads heavy |
| Must avoid | European knight, samurai hero, bright gold parade armor |
| Story anchor | SC-14 sentinel hall |

## Tool chain

Meshy → Blender (lacquer plates, no European mail) → Mixamo → GLB.

**Export:** `game/assets/models/enemies/palace_sentinel/palace_sentinel.glb`

## Positive prompts

- Japanese palace guard armor — lacquer plates `#8B2A3A`, gold trim `#D4A55A`, void gaps `#1A1A2A`
- Single horizontal eye slit glowing gold — **only** face read
- Spear + tower shield; angular silhouette
- No European plate mail

## Negative prompts

medieval knight, European castle guard, full face helmet, chibi, PBR chrome armor

## Hard metrics

| Field | Value |
|-------|-------|
| Tris | 15,000 – 45,000 |
| Height | ~2.5 m |

### Required animations

| Clip | Loop | Duration | Notes |
|------|------|----------|-------|
| `idle` | Yes | 2.5 s | Shield ready |
| `spear_thrust` | No | 0.9 s | Telegraph ≥0.3 s |
| `shell_harden` | No | 1.5 s | Block stance |
| `hit` | No | 0.4 s | |
| `death` | No | 2.0 s | Collapse forward |

## Camera read

- Hall scale: sentinel readable at **12 m** down `palace_sentinel_hall`
- Yuzu Spirit skill VFX must read against lacquer (not same hue as hakama)

## Acceptance

- [ ] Silhouette at 12 m gameplay cam
- [ ] `L2_model_jury` PASS
- [ ] `CHARACTER_BIBLE.md` §6 boss-standard row (GR-002 ✅)
