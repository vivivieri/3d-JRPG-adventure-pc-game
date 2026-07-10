# Tides of Urashima — Playtest Script

**Version:** 1.1 (Pre-build)  
**Target duration:** 2–3 hours  
**Build:** Implementation branch with full story  
**Cross-refs:** `docs/QA_AND_BUG_PROCESS.md` (severity, triage, bug template)

---

## 1. Playtest goals

| Goal | Metric |
|------|--------|
| Complete without guide | ≥80% testers |
| Understand 3 endings | Post-survey |
| Combat too easy/hard | Boss attempts ≤3 Normal |
| Soft-lock | Zero |
| Localization | No missing keys en/ja/zh |

---

## 2. Session setup

- [ ] Fresh `user://` delete
- [ ] Record playtime, deaths, ending chosen
- [ ] Note build commit + branch
- [ ] Language rotation: 1/3 each en/ja/zh across testers

---

## 3. Act I script (~30 min)

| Step | Action | Verify |
|------|--------|--------|
| 1 | New Game | SC-00 prologue plays |
| 2 | Skip / watch prologue | SC-01 spawn |
| 3 | WASD to village | Movement tutorial |
| 4 | Inspect banner, sandal, well | Q1 stage 1 |
| 5 | Save at well | Autosave + manual |
| 6 | Torii scene SC-03 | `met_yuzu_spirit` |
| 7 | Roku shack SC-04 | Shop opens; cave unlocked |
| 8 | Buy 1 salve | Economy works |
| 9 | SC-05 crab fight | Tutorial 3 turns |
| 10 | Enter caves SC-06 | Zone transition |

**Pass:** Reach caves in ≤35 min without stuck.

---

## 4. Act II script (~60 min)

| Step | Action | Verify |
|------|--------|--------|
| 11 | Water puzzle SC-07 | Solved ≤8 min |
| 12 | Optional chest | Loot works |
| 13 | SC-08 wraith fight | 2× Tide Wraith |
| 14 | SC-09 Shore Wraith | Solo; intent UI |
| 15 | SC-10 Yuzu join | Heal in party |
| 16 | SC-11 flashback | Skippable |
| 17 | SC-12 palace gate | Full party combat |
| 18 | Read 4+ lore entries | Journal OK |

**Pass:** Yuzu heals; pearl in inventory.

---

## 5. Act III script (~45 min)

| Step | Action | Verify |
|------|--------|--------|
| 19 | SC-13 mirror | Choice recorded |
| 20 | SC-14 Sentinel | Spirit weakness felt |
| 21 | SC-15 Tide Keeper | 3 phases; choice at 10% |
| 22 | SC-16 choice | Two-step confirm |
| 23 | Ending + credits | Achievement unlock |
| 24 | Title gallery | Ending logged |

**Pass:** One full ending in ≤3h total.

---

## 6. Regression checks

- [ ] Load save mid-Act II — flags intact
- [ ] Game Over → reload — pre-boss autosave
- [ ] Tab menu all tabs
- [ ] Hard mode Sentinel noticeably harder
- [ ] `bash tools/check_asset_compliance.sh` pass on build

---

## 7. Post-play survey (5 questions)

1. Which ending did you choose and why? (free text)
2. Was combat difficulty appropriate? (1–5)
3. Did you understand the box's meaning before SC-16? (Y/N)
4. Any moment you felt stuck? (scene ID)
5. Would you play again for another ending? (Y/N)

---

## 8. Bug reporting

Use the full template and severity definitions in **`docs/QA_AND_BUG_PROCESS.md`** §2–§3.

Quick reference:

| Severity | Example |
|----------|---------|
| S0 Blocker | Cannot progress past puzzle |
| S1 Major | Crash, lost save |
| S2 Minor | UI overlap, typo |
| S3 Polish | Visual clip |
