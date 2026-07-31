---
id: scope-severity
type: how-to
phase: [1, 6]
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 935
summary: "QA and Bug Process — QA scope + severity"
---
# QA and Bug Process — QA scope + severity

**Hub:** [`QA_AND_BUG_PROCESS.md`](../QA_AND_BUG_PROCESS.md)

## When to read

Use **QA and Bug Process — QA scope + severity** (roles: qa, pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. QA scope](#1-qa-scope)
- [2. Severity definitions](#2-severity-definitions)
- [Severity examples (this project)](#severity-examples-this-project)
- [Priority vs severity](#priority-vs-severity)


## 1. QA scope

| Layer | What to verify | Primary doc / tool |
|-------|----------------|-------------------|
| **AI build & test policy** | GDAI-only build; layered AI tests L0–L5; human after | `docs/ops/workflow/AI_DEV_WORKFLOW.md`, `docs/ops/qa/AI_TESTING_SPEC.md` |
| **Story data** | Scene IDs, flags, items, encounters align | `python3 tools/validate_story_data.py` |
| **Unit tests (L1)** | Logic, parsers, calculators, flags | `bash tools/run_unit_tests.sh` |
| **Smoke (L2)** | Boot, lint, art/flow smokes | `bash tools/run_playtest_smoke.sh` |
| **Acceptance gates** | Measurable pass/fail; WARN/SKIP ≠ PASS | `docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `validate_acceptance_criteria.py` |
| **3D / visual / audio QA** | Asset quality before/at ship | `MODEL_QA.md`, `VISUAL_QA.md`, `AUDIO_QA.md` |
| **Flow QA** | Progression, soft-locks, INT-* | `docs/ops/qa/FLOW_QA.md`, `run_integration_tests.sh` |
| **QA remediation** | Structured fix on FAIL | `docs/ops/qa/QA_REMEDIATION_LOOP.md`, `qa_emit_remediation.sh` |
| **Integration (L4)** | Multi-scene flows, combat, save | `bash tools/run_integration_tests.sh` |
| **E2E (L5)** | Full story + 3 endings | `bash tools/run_e2e_playthrough.sh` (Phase 6+) |
| **Asset compliance** | Copyright-safe shipped assets | `bash tools/check_asset_compliance.sh` |
| **Gameplay systems** | Combat, save, quests, endings | Per-doc QA checklists (see §7) + phase acceptance criteria |
| **Playthrough** | Full 2–3 h path, soft-locks | `PLAYTEST_SCRIPT.md` (human, **after L5**) |
| **Localization** | en / ja / zh keys present | `game/locale/translations.csv` (Phase 2+) |
| **Audio** | Scene BGM map, loops, boss phases, P0 VO gates | `scene_audio_map.json`, `AUDIO_PRODUCTION_GUIDE.md` §11, `AUDIO_QA.md` |
| **3D / art** | No primitives, hero meshes | `CHARACTER_BIBLE.md`, `ENVIRONMENT_KITS.md`, `docs/design/art/MODEL_QA.md` |

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
