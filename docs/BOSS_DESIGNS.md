# Tides of Urashima — Boss Design Sheets

**Version:** 1.0 (Pre-build)  
**Combat type:** Turn-based, speed-initiative, telegraphed intent UI  
**Cross-refs:** `docs/GDD.md` §7, `docs/ENCOUNTER_TABLE.md`, `game/data/enemies/enemies.json`

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

### Stats (Normal)

| Stat | Value |
|------|-------|
| HP | 420 |
| ATK | 14 |
| DEF | 8 |
| SPD | 6 |
| MP | 0 |

### Phase 1 — Accusation (100% → 50% HP)

**Behavior:** Slow, heavy hits; punishes idle healing.

| Turn priority | Action | Intent | Effect |
|---------------|--------|--------|--------|
| 1 | Drowned Grasp | Skull | Single target 120% ATK |
| 2 | Regret Aura | Waves | All party: Def Down 2 turns |
| 3 | Heavy Slam | Sword | Single 150% ATK; skip if stunned |
| Repeat | Cycle with 20% chance Grasp → Slam swap |

**Player teach moment:** Use Defend on Slam turn; Yuzu heal on Grasp turn if available (joined after fight — solo Urashima for this fight in v1 data; if Yuzu pre-join, adjust HP up 15%).

**Note:** Current story order has Yuzu join **after** SC-09. Boss is **Urashima solo** — tune HP to ~320 for solo.

### Phase 2 — Collective (50% → 0% HP)

**Trigger:** Banner "The drowned rise with me!"

| Change | Detail |
|--------|--------|
| SPD | +2 |
| New skill | Summon Tide Wraith (once, at 40% HP) |
| Pattern | Grasp → Aura → Slam → Grasp (faster) |

**Add — Tide Wraith:** 80 HP, ATK 8; dies in 2–3 hits; no intent on add (standard enemy rules).

### Hard mode deltas

- Intent icons appear **same turn** (no preview) in phase 2
- Regret Aura also applies Poison 2 turns
- Add spawns at 50% instead of 40%

### Rewards

| Drop | Rate |
|------|------|
| XP | 120 (solo) / 150 (if party) |
| Shell coins | 45 |
| Item | Antidote ×1 (100% first kill) |

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

### Stats (Normal)

| Stat | Value |
|------|-------|
| HP | 380 |
| ATK | 16 |
| DEF | 14 |
| SPD | 8 |
| MP | 20 |

### Phase 1 — Guardian (100% → 0% HP, single phase)

**Behavior:** Defensive rotation; spike damage if ignored.

| Turn priority | Action | Intent | Effect |
|---------------|--------|--------|--------|
| Opening | Oath of Stillness | Shield | Def Up 3 turns |
| Cycle A | Spear Thrust | Sword | Single 130% ATK |
| Cycle B | Palace Reprisal | Skull | Single 160% ATK if target healed last turn |
| Every 3rd | Barrier Pulse | Shield | Self Regen 5% HP |

**Spirit weakness:** Yuzu Purify / Holy Light deals **150%** damage. UI hint after first Barrier Pulse: *"Spirit arts pierce the lacquer."*

### Hard mode deltas

- DEF +4
- Reprisal triggers on **any** buff, not just heal
- Barrier Pulse every 2nd turn

### Rewards

| Drop | Rate |
|------|------|
| XP | 100 |
| Shell coins | 60 |
| Item | Skill scroll `spirit_veil` (one-time 100%) |

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

### Stats (Normal)

| Stat | Value |
|------|-------|
| HP | 900 |
| ATK | 18 |
| DEF | 10 |
| SPD | 9 |
| MP | 50 |

### Phase 1 — Calm (100% → 66% HP)

**Tone:** "Paradise is mercy."

| Action | Intent | Effect |
|--------|--------|--------|
| Tidal Fingers | Waves | All party 80% ATK water |
| Borrowed Moment | Clock | Urashima SPD Down 2 turns |
| Gentle Pull | Sword | Single 110% ATK + MP drain 5 |

**Pattern:** Fingers → Pull → Fingers → Borrowed (loop)

### Phase 2 — Surge (66% → 25% HP)

**Trigger:** Banner "Then let the sea decide!"  
**Camera:** Slow orbit during phase (see `CINEMATICS.md`)

| Change | Detail |
|--------|--------|
| ATK | +3 |
| New | Maelstrom | Waves | All 120% ATK; Def Down 1 turn |
| Pattern | Maelstrom every 3rd turn; Borrowed Moment → Pull between |

### Phase 3 — Ebb (25% → 10% HP)

**Trigger:** Banner "Even mercy... tires."

| Change | Detail |
|--------|--------|
| SPD | -2 |
| Tone | Dialogue barks shorter; more pauses |
| New | Ebb Remembrance | Sparkles | Single 100% Spirit; heals self 3% (ironic) |

### Choice gate (10% HP)

**Combat pauses.** No timer.

| UI | Options |
|----|---------|
| Choice overlay | **Rewind** / **Anchor** / **Drift** |
| Dialogue | Tide Keeper: "Return what was taken — or become the tide." |

**After choice:** Boss uses final skill `Last Mercy` (cosmetic 1 turn) → scripted defeat → ending scene.

**Technical:** Set flag `final_choice_made`; do not allow attack input during prompt.

### Hard mode deltas

- HP 1100
- Maelstrom in phase 2 has **no** intent preview
- Borrowed Moment also applies Stun 1 turn (25% chance)
- Choice gate at 15% HP (less room for error)

### Rewards

| Drop | Rate |
|------|------|
| XP | 250 |
| Shell coins | 100 |
| Item | None (story reward = ending) |

---

## 5. Tutorial enemy — Salt Crab (`salt_crab`)

**Storyboard:** SC-05  
**Not a boss** but combat template.

| Stat | HP 40 | ATK 6 | DEF 4 | SPD 4 |
|------|-------|-------|-------|-------|
| Skills | Pinch (100% ATK) only |
| AI | Attack lowest HP |
| Tutorial | Force Attack → Skill → Defend prompts |

Guaranteed win; no escape needed.

---

## 6. Standard enemies (non-boss patterns)

### Tide Wraith (`tide_wraith`)

| HP 70 | ATK 10 | DEF 3 | SPD 9 |
|-------|--------|-------|-------|
| Skill | Drown Touch — 90% ATK + Poison 2 turns |
| AI | Target lowest HP; 30% double attack if alone |

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

Add to `game/data/enemies/enemies.json`:

```json
{
  "intent_delay": 1,
  "phases": [
    { "hp_threshold": 0.5, "skill_unlock": ["summon_wraith"], "stat_mod": { "spd": 2 } }
  ],
  "hard_mode": {
    "intent_delay": 0,
    "stat_mod": { "hp": 1.15 }
  }
}
```

**Hard mode toggle:** `user://settings.json` → `hard_mode: bool`; menu option in M5 polish.

---

## 9. Playtest acceptance

- [ ] First-time player beats Shore Wraith without grinding (≤ 2 attempts)
- [ ] Sentinel teaches Yuzu Spirit skill without explicit text wall
- [ ] Tide Keeper fight 8–12 minutes Normal
- [ ] Choice gate cannot be skipped accidentally; confirm button required
- [ ] All intent icons match action outcome 100%
