---
id: act2-act3-regression
type: how-to
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 347
summary: "Act II, Act III, regression"
---
# Playtest Script — Act II, Act III, regression

**Hub:** [`PLAYTEST_SCRIPT.md`](../PLAYTEST_SCRIPT.md)

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
