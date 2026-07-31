---
id: index-playtest-gates
type: how-to
phase: [1, 6]
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 826
summary: "System index, playtest loop, gates, won't-fix, RC checklist"
---
# QA and Bug Process — System index, playtest loop, gates, won't-fix, RC checklist

**Hub:** [`QA_AND_BUG_PROCESS.md`](../QA_AND_BUG_PROCESS.md)

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
| **M2** — Combat vertical slice | Zero S0; S1 only with documented workaround |
| **M4** — Full story | Zero S0–S1 on main path |
| **M5** — Art rebuild | Zero S0–S1 on main path; no Kenney/primitive placeholders visible in player builds |
| **M6** — Steam & ship | Zero S0–S1; S2 triaged; S3 timeboxed; compliance script pass |
| **Ship** | Full playtest once per ending; GodotSteam 4.20+ on Godot 4.7 |

See `docs/ops/workflow/MILESTONES.md` for feature checklist. Build order: `docs/ops/workflow/IMPLEMENTATION_PLAN.md`.

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
