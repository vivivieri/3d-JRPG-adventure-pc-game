---
id: achievements
type: reference
phase: [2, 3]
audience: [builder, architect]
status: active
authority: gameplay
tokens_est: 527
summary: "`docs/design/vision/ENDING_DESIGN.md`, `docs/design/world/QUEST_AND_FLAGS.md`, `steam/STORE_PAGE.md`"
---
# Tides of Urashima — Steam Achievements

## When to read

Use **Tides of Urashima — Steam Achievements** (roles: builder, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [1. Story & endings](#1-story-endings)
- [2. Combat](#2-combat)
- [3. Exploration](#3-exploration)
- [4. Implementation notes](#4-implementation-notes)
- [5. QA checklist](#5-qa-checklist)


## 1. Story & endings

| ID | Name (EN) | Trigger (data: `achievements.json`) | Hidden |
|----|-----------|--------------------------------------|--------|
| `ACH_FIRST_STEP` | Washed Ashore | Flag `game_started` (set during SC-01) | No |
| `ACH_EMPTY_HOME` | Empty Home | All 3 `inspected_*` flags (SC-02) | No |
| `ACH_ENDING_REWIND` | The Rewind | Choose Rewind ending | No |
| `ACH_ENDING_ANCHOR` | The Anchor | Choose Anchor ending | No |
| `ACH_ENDING_DRIFT` | The Drift | Choose Drift ending | No |
| `ACH_ALL_ENDINGS` | Three Tides | See all 3 endings (meta) | No |

---

## 2. Combat

| ID | Name (EN) | Trigger | Hidden |
|----|-----------|---------|--------|
| `ACH_FIRST_BLOOD` | First Blood | Win SC-05 tutorial | No |
| `ACH_WRAITH_FALLEN` | Guilt Subsides | Defeat Shore Wraith | No |
| `ACH_SENTINEL_FALLEN` | Lacquer Broken | Defeat Palace Sentinel | No |
| `ACH_KEEPER_FALLEN` | Tide Answered | Defeat Tide Keeper | No |
| `ACH_HARD_TIDE` | Hard Tide | Beat Tide Keeper on Hard mode | **Yes** |

---

## 3. Exploration

| ID | Name (EN) | Trigger | Hidden |
|----|-----------|---------|--------|
| `ACH_LORE_COMPLETE` | Voices of the Coast | Read all 8 lore entries | No |
| `ACH_BOX_TRUTH` | Stolen Years | Complete SC-13 mirror scene | No |

---

## 4. Implementation notes

- Unlock via `SteamManager.unlock_achievement(id)` on flag set
- Sync on game completion
- `ACH_ALL_ENDINGS` checks meta `ending_unlocked` size ≥ 3
- Hidden achievement revealed on unlock

---

## 5. QA checklist

- [ ] No achievement fires twice
- [ ] Offline: queue unlock when Steam connects
- [ ] Names localized in Steam backend (en/ja/zh/zh-Hant)
