---
id: pitch-scope
type: explanation
audience: [narrative, pm, architect]
status: active
authority: vision
tokens_est: 683
summary: "Pitch, source, loop, scope"
---
# Game Design Document — Pitch, source, loop, scope

**Hub:** [`GDD.md`](../GDD.md)

## 1. Elevator pitch

*Urashima Tarō returns from the Dragon Palace to find his village erased by time. A short, melancholy JRPG about consequence, memory, and the price of paradise.*

You explore a stylized coastal world, reunite with echoes of the past, and fight manifestations of regret in turn-based combat. The ending depends on whether you try to rewind history or anchor the future.

---


## 2. Source material & adaptation

**Public domain basis:** *Urashima Tarō* (Japanese folklore, centuries old — no licensing fee).

### Original tale (abridged)
A fisherman saves a turtle, visits the Dragon Palace beneath the sea, spends what feels like days with Princess Otohime, then returns home with a forbidden box. His village is gone; centuries have passed. He opens the box and ages instantly.

### Our dark adaptation
- **Opening:** Urashima saves a wounded sea spirit (not a cartoon turtle — a sacred spirit-turtle of the coast).
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
| Main quests | 5 — see `docs/design/world/QUEST_AND_FLAGS.md` |
| Side lore collectibles | 8 |
| Skills (total) | 14 player (unique IDs; `strike` shared) + 6 enemy — see `docs/design/gameplay/SKILLS_BIBLE.md` |
| Playtime | 2–3 hours |

---
