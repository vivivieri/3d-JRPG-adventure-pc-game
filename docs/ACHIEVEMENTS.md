# Tides of Urashima — Steam Achievements

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/ENDING_DESIGN.md`, `docs/QUEST_AND_FLAGS.md`, `steam/STORE_PAGE.md`

**Total:** 13 achievements (easy distribution for short game)

---

## 1. Story & endings

| ID | Name (EN) | Trigger | Hidden |
|----|-----------|---------|--------|
| `ACH_FIRST_STEP` | Washed Ashore | Complete SC-01 | No |
| `ACH_EMPTY_HOME` | Empty Home | Complete SC-02 all inspects | No |
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
