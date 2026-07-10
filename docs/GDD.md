# Tides of Urashima — Game Design Document

**Version:** 0.2 (Pre-build)  
**Engine:** Godot 4  
**Platform:** PC (Steam)  
**Target audience:** Men 20–30  
**Playtime target:** 2–3 hours (main story)  
**Genre:** 3D adventure JRPG, turn-based combat  

**Related docs:** `docs/CHARACTER_BIBLE.md`, `docs/ENVIRONMENT_KITS.md`, `docs/BOSS_DESIGNS.md`, `docs/ENCOUNTER_TABLE.md`, `docs/CINEMATICS.md`, `docs/QUEST_AND_FLAGS.md`, `docs/TUTORIAL_DESIGN.md`, `docs/ENDING_DESIGN.md`, `docs/ITEMS_AND_ECONOMY.md`, `docs/COMBAT_SYSTEMS.md`, `docs/SKILLS_BIBLE.md`, `docs/UI_UX_FLOW.md`, `docs/SAVE_AND_FAIL_STATES.md`  

---

## 1. Elevator pitch

*Urashima Tarō returns from the Dragon Palace to find his village erased by time. A short, melancholy JRPG about consequence, memory, and the price of paradise.*

You explore a stylized coastal world, reunite with echoes of the past, and fight manifestations of regret in turn-based combat. The ending depends on whether you try to rewind history or anchor the future.

---

## 2. Source material & adaptation

**Public domain basis:** *Urashima Tarō* (Japanese folklore, centuries old — no licensing fee).

### Original tale (abridged)
A fisherman saves a turtle, visits the Dragon Palace beneath the sea, spends what feels like days with Princess Otohime, then returns home with a forbidden box. His village is gone; centuries have passed. He opens the box and ages instantly.

### Our dark adaptation
- **Opening:** Urashima saves a wounded sea spirit (not a cartoon turtle — a sacred kappa-turtle hybrid).
- **Dragon Palace:** Beauty with unease — perfect, sterile, no children, no seasons.
- **Return:** Not just aged — the village is a **ruin overtaken by the sea**. Survivors are spirits bound to objects.
- **The box:** Contains not age, but **the village's stolen years** — fuel for a final choice.
- **Antagonist:** Not evil princess — **Time itself**, personified as the Tide Keeper, who offers paradise at the cost of the living world.

### Themes (for 20–30 male audience)
- Consequence over nostalgia
- Masculine duty vs. escape (Urashima left everyone behind)
- Bittersweet endings over power fantasy
- Optional hard-mode boss patterns for mastery

---

## 3. Core gameplay loop

```
Explore hub/wilderness → Talk / investigate → Trigger encounter or story beat
    → Turn-based combat (optional grind) → Rewards (XP, items, lore)
    → Progress quest flag → Unlock new area → Repeat → Final choice → Ending
```

**Player fantasy:** "I can fix what I broke — but should I?"

---

## 4. Scope (v1 — shippable short game)

| Content | Count |
|---------|-------|
| Hub areas | 1 (Ruined Fishing Village) |
| Dungeons | 2 (Tidal Caves, Dragon Palace Gate) |
| Bosses | 3 (Shore Wraith, Palace Sentinel, Tide Keeper) |
| Party members | 3 (Urashima, Yuzu the shrine maiden spirit, Roku the diver) |
| Main quests | 5 — see `docs/QUEST_AND_FLAGS.md` |
| Side lore collectibles | 8 |
| Skills (total) | 15 player + 6 enemy — see `docs/SKILLS_BIBLE.md` |
| Playtime | 2–3 hours |

---

## 5. Characters

### Urashima Tarō (Protagonist)
- **Role:** Balanced fighter / party leader
- **Arc:** From escapist to accountable
- **Combat:** Sword + tidal skills (water element)
- **Key stat spread:** ATK 8, DEF 6, SPD 7, MP 5

### Yuzu (Companion — Shrine Maiden Spirit)
- **Role:** Healer / buffer
- **Backstory:** Died waiting for Urashima's return; bound to the broken torii gate
- **Combat:** Purify, heal, holy light
- **Unlock:** After clearing Tidal Caves

### Roku (Companion — Old Diver)
- **Role:** Tank / debuffer
- **Backstory:** Only living elder; remembers the truth about the box
- **Combat:** Taunt, shell guard, harpoon strike
- **Unlock:** After finding him in the village ruins

### Otohime (NPC / moral mirror)
- Not a party member. Appears in palace flashbacks and final confrontation dialogue.

### Tide Keeper (Final boss)
- Embodiment of stolen time. Phases: Calm → Surge → Ebb (choice gate).

---

## 6. World & locations

### 6.1 Ruined Fishing Village (Hub)
- Broken pier, submerged homes, faded festival banners
- Shrine with cracked torii (Yuzu's anchor)
- Roku's shack (lore, shop restock)
- Save point at the old well

### 6.2 Tidal Caves (Dungeon 1)
- Crab and wraith enemies, tidal puzzle (raise/lower water via switches)
- Boss: **Shore Wraith** (manifestation of drowned villagers)

### 6.3 Dragon Palace Gate (Dungeon 2)
- Ethereal **ryūgū-jō** architecture (lacquer pillars, curved eaves) — floating walkways over void sea
- Palace Sentinel miniboss → Tide Keeper final boss
- Visual contrast: gold/coral vs. grey ruin hub
- **Scope note:** Reverse-gravity rooms cut from v1; see `docs/ENVIRONMENT_KITS.md`

---

## 7. Combat system (summary)

**Type:** Turn-based with **Speed-initiative** (classic JRPG, not action).

| Component | Detail |
|-----------|--------|
| Turn order | Sorted by SPD each round; ties broken randomly |
| Actions | Attack, Skill, Item, Defend, Escape (non-boss) |
| Resources | HP, MP, Limit gauge (fills on damage dealt/taken) |
| Elements | Water, Spirit, Physical |
| Status | Poison, Regen, Stun, Def Up, Def Down |
| Party size | 3 active |
| Enemy AI | Data-driven priority trees in JSON |

**Design goals:**
- First battle teaches mechanics in &lt; 3 minutes
- Bosses require reading patterns (telegraphed "intent" UI) — see `docs/BOSS_DESIGNS.md`
- No grinding required for story completion on Normal — see `docs/ENCOUNTER_TABLE.md`

See `game/data/README.md` for full JSON schema.

---

## 8. Progression

| System | Implementation |
|--------|----------------|
| Level cap | 15 (short game) |
| XP curve | Linear-ish; tuned for ~2 fights per area before boss |
| Equipment | Weapon + armor + charm (3 slots) |
| Currency | Shell coins (環貝) |
| Shops | Roku's cache — potions, antidote, skill scroll (one-time); see `docs/ENCOUNTER_TABLE.md` §7 |

---

## 9. Narrative structure (3 acts)

### Act I — The Return (30 min)
Arrive at ruins. Learn time has stolen everything. Enter Tidal Caves.

### Act II — The Depths (60 min)
Meet Yuzu. Reach Dragon Palace Gate. Flashbacks reveal Otohime's bargain.

### Act III — The Tide (30–45 min)
Roku reveals box truth. Assault palace gate. Final choice + boss.

---

## 10. Endings (3)

| Ending | Trigger | Tone |
|--------|---------|------|
| **Rewind** | Open box to restore village | Bittersweet — village returns but Urashima fades |
| **Anchor** | Destroy box, bind spirits to land | Hopeful — small community rebuilds |
| **Drift** | Refuse both; walk into sea | Tragic — cycle continues |

---

## 11. Controls (PC)

| Action | Default |
|--------|---------|
| Move | WASD |
| Interact | E |
| Menu | Tab |
| Confirm | Enter / Space |
| Cancel | Esc |

Full controller support planned for polish milestone.

---

## 12. Technical architecture

```
game/
  scripts/core/       GameManager, SaveSystem, EventBus
  scripts/combat/     TurnManager, Combatant, SkillResolver
  scripts/narrative/  DialogueRunner, QuestTracker
  scripts/player/     PlayerController (exploration)
  data/               JSON — skills, enemies, dialogue, quests
  scenes/             Godot scenes (world, combat, UI)
```

**Data-driven design:** All combat and dialogue content in JSON/YAML for fast AI-assisted iteration.

---

## 13. Milestones

| ID | Deliverable | Done when |
|----|-------------|-----------|
| M0 | GDD + storyboard + repo | ✓ This doc |
| M0b | i18n (en / ja / zh) | ✓ LocalizationManager + CSV |
| M0c | Pre-build art specs | ✓ CHARACTER_BIBLE, ENVIRONMENT_KITS, BOSS_DESIGNS, ENCOUNTER_TABLE, CINEMATICS |
| M0d | Pre-build game design specs | ✓ QUEST_AND_FLAGS, TUTORIAL, ENDING, COMBAT, UI, etc. |
| M0e | Story data layer (`game/data/`) | ✓ DATA_ARCHITECTURE, validate_story_data.py |
| M1 | Greybox movement + dialogue | Walk village, talk to NPC |
| M2 | Combat vertical slice | 1 fight feels good |
| M3 | Chapter 1 playable | Tidal Caves complete |
| M4 | Full story | All 3 endings |
| M5 | Polish + Steam page | Trailer, store live |
| M6 | Art rebuild (high-detail Japanese) | Vertical slice SC-02 → full production per ART_DIRECTION v1.1 |

---

## 14. Steam positioning

- **Tags:** JRPG, Story Rich, Short, Atmospheric, Turn-Based Combat
- **Price band:** $4.99–$9.99 (short narrative game)
- **USP:** "A 2-hour emotional folktale — Dark Urashima Tarō"

---

## 15. Localization

Supported languages at launch: **English**, **Japanese**, **Simplified Chinese**.

- UI and game data: `game/locale/translations.csv`
- Story dialogue: inline `{ en, ja, zh }` per line
- Language selector on main menu; preference saved to `user://settings.json`
- See `docs/LOCALIZATION.md` for translator workflow

---

## 16. Risk register

| Risk | Mitigation |
|------|------------|
| Scope creep | Lock 3 locations until post-launch |
| Asset inconsistency | Single style bible + vertical slice gate (`docs/ART_DIRECTION.md` §10) |
| License violations | `docs/ASSET_COMPLIANCE.md` + `tools/check_asset_compliance.sh` before ship |
| Combat feel | Vertical slice before content production |
