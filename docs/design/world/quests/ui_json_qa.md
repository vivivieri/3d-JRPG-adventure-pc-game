---
id: ui-json-qa
type: reference
phase: [1, 5]
audience: [narrative, builder, flow]
status: active
authority: world
tokens_est: 332
summary: "- **New quest:** Banner top-right, 3s fade; log sound"
---
# Quests & Flags — Quest UI, JSON, QA

**Hub:** [`QUEST_AND_FLAGS.md`](../QUEST_AND_FLAGS.md)

## When to read

Use **Quests & Flags — Quest UI, JSON, QA** (roles: narrative, builder, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [6. Quest UI behavior](#6-quest-ui-behavior)
- [7. Implementation JSON](#7-implementation-json)
- [8. QA checklist](#8-qa-checklist)

## 6. Quest UI behavior

- **New quest:** Banner top-right, 3s fade; log sound
- **Stage complete:** Checkmark on quest tracker; brief pulse
- **Quest complete:** Fanfare (short); XP/coins if scripted
- **Tracker:** Tab menu → Quests tab; shows active stage only (no spoilers)

---


## 7. Implementation JSON

`game/data/quests/main_quests.json` already contains all 5 quests with stages matching the
tables above (schema v2). When editing quests, change the JSON first, then this doc.

---


## 8. QA checklist

- [ ] Cannot enter caves before SC-04
- [ ] Cannot pass Shore Wraith arena without win or game over
- [ ] Cannot open palace interior without `wraith_pearl`
- [ ] Yuzu not in SC-09 combat roster
- [ ] Roku not in SC-05–SC-11 combat roster
- [ ] All 5 quests complete across one full playthrough
- [ ] Quest log never references unseen characters by name
