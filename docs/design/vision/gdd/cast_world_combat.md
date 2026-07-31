---
id: cast-world-combat
type: explanation
phase: [1, 6]
audience: [narrative, pm, architect]
status: active
authority: vision
tokens_est: 844
summary: "Characters, world, combat, progression"
---
# Game Design Document — Characters, world, combat, progression

**Hub:** [`GDD.md`](../GDD.md)

## 5. Characters

### Urashima Tarō (Protagonist)
- **Role:** Balanced fighter / party leader
- **Arc:** From escapist to accountable
- **Combat:** Sword + tidal skills (water element)
- **Base stats (L1, `party.json`):** HP 120, MP 30, ATK 14, DEF 10, MAG 8, RES 9, SPD 11

### Yuzu (Companion — Shrine Maiden Spirit)
- **Role:** Healer / buffer
- **Backstory:** Died waiting for Urashima's return; bound to the broken torii gate
- **Combat:** Purify, heals, spirit light (`SKILLS_BIBLE.md` §2)
- **Unlock:** SC-10 — after defeating the Shore Wraith in Tidal Caves (`yuzu_joined`)

### Roku (Companion — Old Diver)
- **Role:** Tank / debuffer
- **Backstory:** Only living elder; remembers the truth about the box
- **Combat:** Taunt, shell guard, harpoon strike
- **Unlock:** SC-12 — Roku joins combat at the Dragon Palace Gate (`roku_combat_active`); narrative meet at SC-04 (`met_roku`)

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
- **Scope note:** Reverse-gravity rooms cut from v1; see `docs/design/world/ENVIRONMENT_KITS.md`

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
- Bosses require reading patterns (telegraphed "intent" UI) — see `docs/design/gameplay/BOSS_DESIGNS.md`
- No grinding required for story completion on Normal — see `docs/design/gameplay/ENCOUNTER_TABLE.md`

See `game/data/README.md` for full JSON schema.

---


## 8. Progression

| System | Implementation |
|--------|----------------|
| Level cap | 15 (short game) |
| XP curve | Linear-ish; tuned for ~2 fights per area before boss |
| Equipment | Weapon + armor + charm (3 slots) |
| Currency | Shell coins (環貝) |
| Shops | Roku's cache — potions, antidote, skill scroll (one-time); see `docs/design/gameplay/ENCOUNTER_TABLE.md` §7 |

---
