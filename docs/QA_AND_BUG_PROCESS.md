# Tides of Urashima — QA & Bug Process

**Version:** 1.1 (Pre-build)  
**Cross-refs:** `docs/PLAYTEST_SCRIPT.md`, `docs/MILESTONES.md`, `docs/AI_DEV_WORKFLOW.md`, `tools/validate_story_data.py`, `tools/check_asset_compliance.sh`

This doc defines **how to find, report, triage, and verify bugs** for *Tides of Urashima*. Playtest scripts live in `PLAYTEST_SCRIPT.md`; this doc is the **process and templates**.

---

## 1. QA scope

| Layer | What to verify | Primary doc / tool |
|-------|----------------|-------------------|
| **AI build & test policy** | GDAI-only build; layered automated tests | `docs/AI_DEV_WORKFLOW.md` |
| **Story data** | Scene IDs, flags, items, encounters align | `python3 tools/validate_story_data.py` |
| **Unit tests (L1)** | Logic, parsers, calculators, flags | `bash tools/run_unit_tests.sh` |
| **Smoke (L2)** | Boot load, dev environment | `bash tools/run_playtest_smoke.sh` |
| **Integration (L4)** | Multi-scene flows, combat, save | `bash tools/run_integration_tests.sh` |
| **E2E (L5)** | Full story + 3 endings | `bash tools/run_e2e_playthrough.sh` (Phase 6+) |
| **Asset compliance** | Copyright-safe shipped assets | `bash tools/check_asset_compliance.sh` |
| **Gameplay systems** | Combat, save, quests, endings | Per-doc QA checklists (see §7) + phase acceptance criteria |
| **Playthrough** | Full 2–3 h path, soft-locks | `PLAYTEST_SCRIPT.md` (human, Phase 8) |
| **Localization** | en / ja / zh keys present | `game/locale/translations.csv` (Phase 2+) |
| **Audio** | Scene BGM map, loops, boss phases | `AUDIO_PRODUCTION_GUIDE.md` §11 |
| **3D / art** | No primitives, hero meshes | `CHARACTER_BIBLE.md`, `ENVIRONMENT_KITS.md` |

---

## 2. Severity definitions

| Severity | Label | Definition | Response target |
|----------|-------|------------|-----------------|
| **S0** | Blocker | Cannot progress main story; crash on boot; data corruption | Fix before any playtest ship |
| **S1** | Major | Crash in combat/cutscene; lost save; wrong ending; broken boss | Fix before milestone gate |
| **S2** | Minor | UI overlap, wrong stat, typo, missing SFX, workaround exists | Fix in polish pass |
| **S3** | Polish | Visual clip, audio pop, non-blocking aesthetic | Backlog; ship if timeboxed |

### Severity examples (this project)

| Severity | Example |
|----------|---------|
| S0 | SC-07 puzzle soft-lock; `wraith_pearl` not granted after Shore Wraith |
| S0 | `validate_story_data.py` fails on `main` |
| S1 | Game Over reload loses 30+ min progress (autosave broken) |
| S1 | Tide Keeper choice gate skippable → wrong ending |
| S1 | SC-16 attack input not blocked during choice |
| S2 | Shop price ≠ `ITEMS_AND_ECONOMY.md` |
| S2 | Missing `TUTORIAL_*` translation key in ja |
| S2 | BGM loop click at bar 33 |
| S3 | Coat clips through sandal at certain camera angle |
| S3 | Footstep variant repeats twice in a row |

### Priority vs severity

| | Fix now | Can wait |
|---|---------|----------|
| **Affects main path** | S0, S1 | S2 |
| **Optional / cosmetic** | — | S3 |

---

## 3. Bug report template

Copy into GitHub issue, Discord, or playtest spreadsheet.

```markdown
## Summary
One-line description of the bug.

## Severity
S0 / S1 / S2 / S3

## Build
- Branch: cursor/...
- Commit: abc1234
- Platform: Linux / Windows
- Language: en / ja / zh

## Steps to reproduce
1. New game (or load save: slot 1, Act II)
2. Go to SC-07 tidal caves puzzle
3. Flip switch A twice without switch B
4. ...

## Expected
Water lowers; player can reach latch.

## Actual
Water state stuck; latch unreachable.

## Scene / zone
- Scene ID: SC-07
- Zone: tidal_caves
- Flags (if known): water_puzzle_solved=false

## Evidence
- Screenshot / video / save file path
- Console log excerpt (if crash)

## Regression
- [ ] Worked in previous build
- [ ] Never worked
- [ ] Unknown
```

### Required fields by severity

| Field | S0–S1 | S2–S3 |
|-------|-------|-------|
| Steps to reproduce | Required | Required |
| Scene ID | Required | Recommended |
| Build commit | Required | Required |
| Save file | If save-related | Optional |
| Screenshot/video | Strongly recommended | Optional |

---

## 4. Triage workflow

```
Report filed
    ↓
Triage (within 1 session)
    ├─ Reproduce? → No → Need info → back to reporter
    ├─ Duplicate? → Link primary issue; close duplicate
    ├─ Assign severity (§2)
    └─ Assign owner + milestone (M4/M5/M6)
    ↓
Fix on feature branch
    ↓
Verify (§5)
    ↓
Close issue + note commit/PR
```

### Triage checklist (maintainer)

- [ ] Reproduced on clean `user://` save (or provided save)
- [ ] Severity matches §2 (escalate if main-path blocked)
- [ ] Scene ID and flags documented
- [ ] Not a duplicate of open issue
- [ ] Linked to milestone if S0–S1

### GitHub labels (recommended)

| Label | Use |
|-------|-----|
| `bug` | All defects |
| `severity/s0-blocker` | Ship stop |
| `severity/s1-major` | Milestone gate |
| `severity/s2-minor` | Polish queue |
| `severity/s3-polish` | Backlog |
| `area/combat` | Combat, bosses, skills |
| `area/story` | Scenes, dialogue, flags |
| `area/ui` | Menus, HUD |
| `area/audio` | BGM, SFX |
| `area/l10n` | Translations |
| `area/save` | Save/load, game over |

---

## 5. Verification (definition of done)

A bug is **closed** only when:

1. **Fix merged** to target branch with clear commit message (`fix: SC-07 puzzle soft-lock when...`).
2. **Original steps** no longer reproduce on fixed build.
3. **Regression spot-check** from §6 (at minimum the act containing the fix).
4. **Automated checks** pass if data/assets touched:
   ```bash
   python3 tools/validate_story_data.py
   bash tools/check_asset_compliance.sh
   ```
5. **Related doc updated** if behavior was spec-defined (e.g. economy price, flag name).

### Verify matrix by area

| Area | Minimum verify |
|------|----------------|
| Story / quest | Load save before scene; replay scene; flag set in `user://` |
| Combat | Win and lose fight; check intent UI; boss phases |
| Save | Manual + autosave; load mid-act; game over reload |
| Ending | Reach SC-16; each choice once per full playtest cycle |
| Audio | Scene from `AUDIO_PRODUCTION_GUIDE.md` §4 map |
| L10n | Switch language; revisit same scene |

---

## 6. Regression suite

Run before each milestone demo or playtest build.

### Automated (required)

```bash
python3 tools/validate_story_data.py
bash tools/check_asset_compliance.sh
```

### Smoke (15 min)

| # | Action | Pass |
|---|--------|------|
| 1 | Launch → title → new game | No crash |
| 2 | SC-00 skip or watch → SC-01 | Spawn OK |
| 3 | Walk village → SC-05 crab | Combat starts |
| 4 | Win combat → Tab menu | All tabs open |
| 5 | Save at well → quit → load | Position + flags OK |

### Full regression

Follow `PLAYTEST_SCRIPT.md` Acts I–III once per milestone (M4 combat, M5 story complete, M6 polish).

### Post-fix regression

When fixing a bug, always re-run:

- The **exact steps** from the report
- **One scene before and after** the affected scene
- **Automated checks** if any `game/data/` or `game/assets/` changed

---

## 7. Per-system QA index

Each design doc has a checklist — use during focused passes:

| Doc | Section |
|-----|---------|
| `QUEST_AND_FLAGS.md` | §8 QA checklist |
| `COMBAT_SYSTEMS.md` | §11 |
| `SAVE_AND_FAIL_STATES.md` | §8 |
| `ENDING_DESIGN.md` | §10 |
| `TUTORIAL_DESIGN.md` | §8 |
| `UI_UX_FLOW.md` | §12 |
| `ITEMS_AND_ECONOMY.md` | §11 |
| `PUZZLE_DESIGN.md` | §9 |
| `SKILLS_BIBLE.md` | §8 |
| `SETTINGS_ACCESSIBILITY.md` | §7 |
| `ACHIEVEMENTS.md` | §5 |
| `ENCOUNTER_TABLE.md` | §12 |
| `AUDIO_PRODUCTION_GUIDE.md` | §11 |
| `REPLAY_DESIGN.md` | §11 |
| `NARRATIVE_WRITING_GUIDE.md` | §9 |
| `PROGRESSION_TUNING.md` | §10 |
| `GAME_FEEL.md` | §9 |
| `LORE_AND_ENVIRONMENTAL_STORY.md` | §10 |
| `WORLD_MAP_AND_FLOW.md` | §10 |
| `CHARACTER_BIBLE.md` | Production order + global rules |

---

## 8. Playtest → bug loop

```
Schedule playtest (PLAYTEST_SCRIPT.md §2)
    ↓
Tester runs script + exploratory 30 min
    ↓
Post-survey (§9 of PLAYTEST_SCRIPT)
    ↓
File bugs with template (§3)
    ↓
Triage (§4) → fix → verify (§5)
    ↓
Next playtest on newer build
```

### Playtest metrics to track

| Metric | Target | Action if missed |
|--------|--------|------------------|
| Complete without guide | ≥80% | S1 tutorial/quest bugs |
| Boss attempts (Normal) | ≤3 | Tune encounter or fix combat bug |
| Soft-lock count | 0 | S0 immediately |
| Missing l10n keys | 0 | S2 per language |
| Time to complete | 2–3 h | Pacing doc review, not always bug |

---

## 9. Milestone gates (bug bar)

| Milestone | Bug bar |
|-----------|---------|
| **M4** — Combat vertical slice | Zero S0; S1 only with documented workaround |
| **M5** — Full story | Zero S0–S1 on main path |
| **M6** — Polish / ship | Zero S0–S1; S2 triaged; S3 timeboxed |
| **Ship** | Compliance script pass; full playtest once per ending |

See `docs/MILESTONES.md` for feature checklist.

---

## 10. Won't fix / by design

Document these to avoid duplicate reports:

| Behavior | Reason |
|----------|--------|
| Yuzu not playable before SC-10 | `QUEST_AND_FLAGS.md` |
| Urashima solo at Shore Wraith | Story order |
| SC-13 mirror choice is flavor only | `ENDING_DESIGN.md` |
| No control remapping v1 | `SETTINGS_ACCESSIBILITY.md` |
| Procedural placeholder audio | Replaced per `AUDIO_PRODUCTION_GUIDE.md` before ship |

Add new entries here when closing issues as **won't fix**.

---

## 11. QA checklist (release candidate)

- [ ] `validate_story_data.py` — pass
- [ ] `check_asset_compliance.sh` — pass
- [ ] Smoke suite §6 — pass
- [ ] Full `PLAYTEST_SCRIPT.md` — one run per ending (3 total)
- [ ] Zero open S0–S1
- [ ] Hard mode spot-check (Sentinel)
- [ ] en / ja / zh — no missing keys on main path
- [ ] README build instructions reproduce clean run
