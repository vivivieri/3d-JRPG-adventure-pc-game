# Tides of Urashima — Playtest Script

**Version:** 1.2  
**Target duration:** 2–3 hours  
**Build:** Release candidate on `game/development`  
**Prerequisite:** **All AI tests L0–L5 must pass** on the same commit before any human runs this script. See `docs/AI_TESTING_SPEC.md` §8.  
**Minimum cohort:** 5 testers (diverse language rotation) — recorded in `artifacts/qa_reports/L6_human_playtest.json`  
**Cross-refs:** `docs/AI_TESTING_SPEC.md`, `docs/QA_AND_BUG_PROCESS.md` (severity, triage, bug template)

> **Human QA is last.** AI agents run data validation, unit tests, smoke, GDAI editor verify, integration tests, and full E2E (3 endings) first. Humans start only when `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` exits 0.

---

## 1. Playtest goals

| Goal | Metric |
|------|--------|
| Complete without guide | ≥80% testers |
| Understand 3 endings | Post-survey |
| Combat too easy/hard | Boss attempts ≤3 Normal |
| Movement / camera feel | Feel checklist §7b (1–5 scale) |
| Soft-lock | Zero |
| Localization | No missing keys en/ja/zh/zh-Hant |

---

## 2. Session setup

**Before starting — verify AI suite (or ask agent for report):**

- [ ] `bash tools/run_playtest_smoke.sh` → PASS  
- [ ] `bash tools/run_integration_tests.sh` → PASS  
- [ ] `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` → PASS  
- [ ] Record commit SHA: `git rev-parse HEAD`

**Human session:**

- [ ] Fresh `user://` delete
- [ ] Record playtime, deaths, ending chosen
- [ ] Note build commit + branch
- [ ] Language rotation across testers: en / ja / zh / zh-Hant (incl. one zh-Hant + Cantonese VO session)

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

## 7b. Feel checklist (required — rate 1–5)

Per `docs/GAME_FEEL.md`. Record per tester; average ≥3.5 required for ship.

| # | Question | 1 (bad) → 5 (great) |
|---|----------|---------------------|
| F1 | Movement feels responsive (no mushy input) | |
| F2 | Camera follows smoothly in field | |
| F3 | Combat hits feel readable (flash/SFX timing) | |
| F4 | Dialogue pacing comfortable (not too fast/slow) | |
| F5 | UI confirms/cancels feel snappy | |

---

## 8. Post-play survey (5 questions)

1. Which ending did you choose and why? (free text)
2. Was combat difficulty appropriate? (1–5)
3. Did you understand the box's meaning before SC-16? (Y/N)
4. Any moment you felt stuck? (scene ID)
5. Would you play again for another ending? (Y/N)

---

## 9. Bug reporting

Use the full template and severity definitions in **`docs/QA_AND_BUG_PROCESS.md`** §2–§3.

Quick reference:

| Severity | Example |
|----------|---------|
| S0 Blocker | Cannot progress past puzzle |
| S1 Major | Crash, lost save |
| S2 Minor | UI overlap, typo |
| S3 Polish | Visual clip |
