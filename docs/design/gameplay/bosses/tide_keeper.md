---
id: tide-keeper
type: reference
audience: [builder, builder_combat, qa]
phase: [5]
status: active
authority: gameplay
tokens_est: 926
summary: "Final boss; 3 phases + choice gate at 10% HP"
---
# Boss Designs — Tide Keeper

**Hub:** [`BOSS_DESIGNS.md`](../BOSS_DESIGNS.md)

## When to read

Use **Boss Designs — Tide Keeper** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (10 sections).

## Jump to

- [4. Tide Keeper (`tide_keeper`)](#4-tide-keeper-tide_keeper)
- [Visual](#visual)
- [Stats (Normal) — from `enemies.json`](#stats-normal-from-enemiesjson)
- [Skill kit (data IDs)](#skill-kit-data-ids)
- [Phase 1 — Calm (100% → 66% HP)](#phase-1-calm-100-66-hp)
- [Phase 2 — Surge (66% → 33% HP)](#phase-2-surge-66-33-hp)
- [Phase 3 — Ebb (33% → 10% HP)](#phase-3-ebb-33-10-hp)
- [Choice gate (10% HP)](#choice-gate-10-hp)
- [Hard mode deltas](#hard-mode-deltas)
- [Rewards — from `enemies.json`](#rewards-from-enemiesjson)


## 4. Tide Keeper (`tide_keeper`)

**Storyboard:** SC-15, SC-16
**Location:** Throne of tides
**Role:** Final boss; 3 phases + choice gate at 10% HP
**Element:** Water / Time
**Recommended party level:** 8–10

### Visual

- Humanoid figure of flowing water; stolen **clock motifs** embedded in cloak (Roman numerals blurred — not literal clocks)
- Phase 2: cloak becomes tidal wave silhouette
- Phase 3: shrinks to human scale; calmer, more tragic

**3D production:** Phase mesh swaps, materials, animations — `docs/design/art/CHARACTER_BIBLE.md` §6 (`tide_keeper`).

### Stats (Normal) — from `enemies.json`

| Stat | Value |
|------|-------|
| HP | 580 |
| ATK | 15 |
| DEF | 12 |
| MAG | 20 |
| RES | 14 |
| SPD | 11 |

### Skill kit (data IDs)

| Data skill ID | Flavor name | Intent | Effect (see `skills.json`) |
|---------------|-------------|--------|-----------------------------|
| `drown_touch` | Gentle Pull | Sword | Single target, MAG ×1.1 water; 40% Poison 3t |
| `tide_lament` | Tidal Fingers / Maelstrom | Waves | All party, MAG ×1.5 water; 25% Stun 1t |
| `regret_surge` | Borrowed Moment | Clock | All party, MAG ×1.3 spirit; 60% Def Down 2t |

### Phase 1 — Calm (100% → 66% HP)

**Tone:** "Paradise is mercy."
**AI weights (data):** `drown_touch` 50 / `tide_lament` 50.

### Phase 2 — Surge (66% → 33% HP)

**Trigger:** Banner "The tide rises..." (`phases[0].hp_threshold: 0.66`)
**Camera:** Slow orbit during phase (see `CINEMATICS.md`)
**AI weights (data):** `regret_surge` 40 / `tide_lament` 60 — AoE pressure peaks.

### Phase 3 — Ebb (33% → 10% HP)

**Trigger:** Banner "Time fractures." (`phases[1].hp_threshold: 0.33`)
**AI weights (data):** `tide_lament` 100. Dialogue barks shorter; more pauses.

### Choice gate (10% HP)

**Trigger:** `phases[2].hp_threshold: 0.1` with `triggers_choice: true` → banner "Choose." →
**combat freezes** and combat logic sets flag **`tide_keeper_phase3`**. No timer.

| UI | Options |
|----|---------|
| Choice overlay | **Rewind** / **Anchor** / **Drift** |
| Dialogue | Tide Keeper: "Return what was taken — or become the tide." |

**After choice:** SC-16 dialogue choice sets **`ending_chosen`** (`rewind` \| `anchor` \| `drift`) →
scripted `Last Mercy` beat (cosmetic 1 turn, cinematic — not a data skill) → scripted defeat sets
**`tide_keeper_defeated`** → ending scene SC-17a/b/c.

**Technical:** Flag sequence is `tide_keeper_phase3` (at 10% HP) → `ending_chosen` (SC-16 choice)
→ `tide_keeper_defeated` (scripted resolution). No attack input during the prompt.

### Hard mode deltas

- Global Hard multipliers (HP ×1.15 → ~667, ATK ×1.10)
- `tide_lament` in phase 2+ has **no** intent preview
- Choice gate at 15% HP (less room for error)

### Rewards — from `enemies.json`

| Drop | Rate |
|------|------|
| XP | 250 |
| Shell coins | 100 |
| Item | `palace_fragment` (100%) — story reward = ending |

---
