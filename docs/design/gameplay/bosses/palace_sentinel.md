---
id: palace-sentinel
type: reference
audience: [builder, builder_combat, qa]
phase: [3, 5]
status: active
authority: gameplay
tokens_est: 615
summary: "Location: Dragon Palace Gate — sentinel hall"
---
# Boss Designs — Palace Sentinel

**Hub:** [`BOSS_DESIGNS.md`](../BOSS_DESIGNS.md)

## When to read

Use **Boss Designs — Palace Sentinel** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [3. Palace Sentinel (`palace_sentinel`)](#3-palace-sentinel-palace_sentinel)
- [Visual](#visual)
- [Stats (Normal) — from `enemies.json`](#stats-normal-from-enemiesjson)
- [Skill kit (data IDs)](#skill-kit-data-ids)
- [Phase 1 — Guardian (100% → 0% HP, single phase)](#phase-1-guardian-100-0-hp-single-phase)
- [Hard mode deltas](#hard-mode-deltas)
- [Rewards — from `enemies.json`](#rewards-from-enemiesjson)


## 3. Palace Sentinel (`palace_sentinel`)

**Storyboard:** SC-14
**Location:** Dragon Palace Gate — sentinel hall
**Role:** Miniboss; teaches Spirit weakness (Yuzu)
**Element:** Physical (armor); weak to Spirit
**Recommended party level:** 6–7

### Visual

- Angular ryūgū-jō armor; single horizontal eye slit glowing gold
- Tall (~2.5m); spear + tower shield
- No European plate mail — lacquer plates only

**3D production:** Full mesh breakdown, poly budgets, GLB paths, arena scale — `docs/design/art/CHARACTER_BIBLE.md` §6 (`palace_sentinel`).

### Stats (Normal) — from `enemies.json`

| Stat | Value |
|------|-------|
| HP | 250 |
| ATK | 16 |
| DEF | 14 |
| MAG | 6 |
| RES | 10 |
| SPD | 8 |

### Skill kit (data IDs)

| Data skill ID | Flavor name | Intent | Effect (see `skills.json`) |
|---------------|-------------|--------|-----------------------------|
| `sentinel_cleave` | Spear Thrust | Sword | Single target, ATK ×1.6 physical |
| `shell_harden` | Oath of Stillness | Shield | Self Def Up +4, 2 turns |

### Phase 1 — Guardian (100% → 0% HP, single phase)

**Behavior:** Heavy single-target pressure; hardens when low.
**AI weights (data):** `sentinel_cleave` 75 / `shell_harden` 25 (only below 40% HP).

**Spirit weakness:** `spirit_weakness: 1.5` in data — Spirit-element damage (Yuzu `purify`, Urashima `box_unbound`) deals **×1.5**. UI hint after first `shell_harden`: *"Spirit arts pierce the lacquer."*

### Hard mode deltas

- Global Hard multipliers (HP ×1.15, ATK ×1.10)
- Intent shown same-turn in second half of fight

### Rewards — from `enemies.json`

| Drop | Rate |
|------|------|
| XP | 100 |
| Shell coins | 60 |
| Item | `palace_edge` (100% — best Urashima weapon), `palace_fragment` (50%) |

---
