---
id: shore-wraith
type: reference
audience: [builder, builder_combat, qa]
phase: [2]
status: active
authority: gameplay
tokens_est: 631
summary: "Tidal Caves — boss arena"
---
# Boss Designs — Shore Wraith

**Hub:** [`BOSS_DESIGNS.md`](../BOSS_DESIGNS.md)

## 2. Shore Wraith (`shore_wraith`)

**Storyboard:** SC-09
**Location:** Tidal Caves — boss arena
**Role:** First boss; teaches intent UI + phase change
**Element:** Spirit
**Recommended party level:** 4

### Visual

- Colossal draped form (~4m tall); cloth simulated as static sculpt + particle drips
- Multiple villager faces visible under folds
- Emerges from pool (intro cinematic 5s)

**3D production:** Full mesh breakdown, poly budgets, GLB paths — `docs/design/art/CHARACTER_BIBLE.md` §6 (`shore_wraith`).

### Stats (Normal) — from `enemies.json`

| Stat | Value |
|------|-------|
| HP | 320 (tuned for **solo Urashima** — Yuzu joins after SC-09) |
| ATK | 13 |
| DEF | 10 |
| MAG | 16 |
| RES | 12 |
| SPD | 10 |

### Skill kit (data IDs)

| Data skill ID | Flavor name | Intent | Effect (see `skills.json`) |
|---------------|-------------|--------|-----------------------------|
| `drown_touch` | Drowned Grasp | Skull | Single target, MAG ×1.1 water; 40% Poison 3t |
| `regret_surge` | Regret Aura | Waves | All party, MAG ×1.3 spirit; 60% Def Down 2t |

### Phase 1 — Accusation (100% → 50% HP)

**Behavior:** Slow, heavy hits; punishes idle healing.
**AI weights (data):** `drown_touch` 70 / `regret_surge` 30.

**Player teach moment:** Use Defend when Skull intent shows; cure Poison with `coral_antidote`.

### Phase 2 — Collective (50% → 0% HP)

**Trigger:** Banner "The drowned rise with me!" (`phases[0].hp_threshold: 0.5`)

**AI weights (data):** `regret_surge` 60 / `drown_touch` 40 — pressure shifts to AoE.

> **Cut for v1:** the earlier "Summon Tide Wraith" add mechanic is **not** in
> `enemies.json` and is not implemented. If reinstated post-v1, add a summon skill
> to `skills.json` and an `adds` block to the boss entry first.

### Hard mode deltas

- Intent icons appear **same turn** (no preview) in phase 2
- Global Hard multipliers apply (HP ×1.15, ATK ×1.10 — `PROGRESSION_TUNING.md` §6)

### Rewards — from `enemies.json`

| Drop | Rate |
|------|------|
| XP | 120 |
| Shell coins | 45 |
| Item | `wraith_pearl` ×1 (100% — key item, opens palace gate) |

### Audio / VFX

- Intro: low choir + water surge
- Phase 2: overlapping whisper SFX (drowned voices)
- Death: cloth collapses into pool; silence 2s before Yuzu scene

---
