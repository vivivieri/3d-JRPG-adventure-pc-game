# Tides of Urashima — Boss Design Sheets

**Version:** 1.1 (Pre-build — reconciled with data)  
**Combat type:** Turn-based, speed-initiative, telegraphed intent UI  
**Cross-refs:** `docs/GDD.md` §7, `docs/ENCOUNTER_TABLE.md`, `game/data/enemies/enemies.json`, `docs/CHARACTER_BIBLE.md` §6 (3D specs)

> **Canonical numbers:** All stats, skill IDs, phase thresholds, and drops below mirror
> `game/data/enemies/enemies.json` + `game/data/skills/skills.json` (see `docs/README.md`
> numeric values rule). Flavor action names are listed next to their data skill IDs.

---

## 1. Global boss rules

| Rule | Detail |
|------|--------|
| Intent UI | Every non-basic action telegraphed 1 turn ahead (icon + label) |
| Phases | HP threshold triggers; banner + short animation |
| Adds | Max 1 add on field for v1 (performance + readability) |
| Escape | Disabled for all bosses |
| Normal mode | Story completable without grinding |
| Hard mode | Optional; faster patterns, less intent delay (post-normal unlock or menu toggle) |
| Limit gauge | Fills on damage dealt/taken; boss fights teach by SC-09 |

### Intent icon mapping

| Icon | Meaning |
|------|---------|
| Sword | Physical attack |
| Skull | High damage / debuff |
| Shield | Defensive buff |
| Sparkles | Spirit / magic |
| Waves | Water AoE |
| Clock | Time manipulation (Tide Keeper only) |

---

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

**3D production:** Full mesh breakdown, poly budgets, GLB paths — `docs/CHARACTER_BIBLE.md` §6 (`shore_wraith`).

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

**3D production:** Full mesh breakdown, poly budgets, GLB paths, arena scale — `docs/CHARACTER_BIBLE.md` §6 (`palace_sentinel`).

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

**3D production:** Phase mesh swaps, materials, animations — `docs/CHARACTER_BIBLE.md` §6 (`tide_keeper`).

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

## 5. Tutorial enemy — Salt Crab (`salt_crab`)

**Storyboard:** SC-05  
**Not a boss** but combat template.

| Stat | HP 40 | ATK 7 | DEF 5 | SPD 6 |
|------|-------|-------|-------|-------|
| Skills | `claw_snap` (ATK ×1.0) 80% / `shell_harden` (Def Up) 20% below 50% HP |
| AI | Weighted (see `enemies.json`) |
| Tutorial | Force Attack → Skill → Defend prompts |

Guaranteed win; no escape needed.

---

## 6. Standard enemies (non-boss patterns)

### Tide Wraith (`tide_wraith`)

| HP 50 | ATK 6 | MAG 10 | DEF 4 | RES 6 | SPD 9 |
|-------|-------|--------|-------|-------|-------|
| Skill | `drown_touch` — MAG ×1.1 water + 40% Poison 3 turns |
| AI | Weighted 100% `drown_touch` |
| Drops | `spirit_shard` 30% |

### Salt Crab (`salt_crab`) — field

See tutorial above; field versions identical, lower XP.

---

## 7. Boss intro / outro timing

| Boss | Intro | Phase banner | Death to next scene |
|------|-------|--------------|---------------------|
| Shore Wraith | 5s emerge | 2s | 3s → SC-10 |
| Palace Sentinel | 3s march | — | 2s → SC-15 setup |
| Tide Keeper | 6s rise | 2s each phase | Choice → ending (no return) |

---

## 8. Data implementation notes

Boss phases are already encoded in `game/data/enemies/enemies.json` — the combat runtime consumes:

```json
{
  "ai": { "type": "phase", "phases": [{ "hp_above": 0.5, "weights": [...] }] },
  "phases": [
    { "hp_threshold": 0.5, "announcement": "The drowned rise with me!" },
    { "hp_threshold": 0.1, "announcement": "Choose.", "triggers_choice": true }
  ]
}
```

- `ai.phases[].hp_above` — skill-weight bands (behavior per phase)
- `phases[].hp_threshold` — banner announcements; `triggers_choice: true` freezes combat and sets `tide_keeper_phase3`
- Hard mode multipliers (HP ×1.15, ATK ×1.10, intent delay 0 in phase 2+) are applied at runtime from `user://settings.json` → `hard_mode: bool` — not stored per enemy.

---

## 9. Playtest acceptance

- [ ] First-time player beats Shore Wraith without grinding (≤ 2 attempts)
- [ ] Sentinel teaches Yuzu Spirit skill without explicit text wall
- [ ] Tide Keeper fight 8–12 minutes Normal
- [ ] Choice gate cannot be skipped accidentally; confirm button required
- [ ] All intent icons match action outcome 100%
