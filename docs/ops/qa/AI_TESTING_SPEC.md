---
id: ai-testing-spec
type: reference
audience: [qa, flow]
status: active
authority: qa
tokens_est: 899
summary: "All implementation on `main` (Phases 1–8)"
---
# AI Testing Specification

**Version:** 1.4
**Applies to:** All implementation on `main` (Phases 1–8)
**Parent doc:** `docs/ops/workflow/AI_DEV_WORKFLOW.md` (build policy + acceptance criteria)
**Cross-refs:** `AGENTS.md`, `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`, `docs/ops/qa/PLAYTEST_SCRIPT.md`, `docs/ops/qa/QA_AND_BUG_PROCESS.md`, `docs/ops/qa/FLOW_QA.md`, `docs/ops/qa/QA_REMEDIATION_LOOP.md`

This document is the **detailed spec** for AI agent testing. It defines **how** to run each layer (L0–L5) and when humans may begin QA.

---
## 0. Golden rule — human QA comes last

```
L2.5 (optional) → L0 → L1 → L2 → L3 → L4 → L5  (all AI — must pass for ship)
         ↓
L6 Human QA  (only after L0–L5 green on release candidate)
```

**L2.5 candidate tournament** (`docs/ops/qa/CANDIDATE_TOURNAMENT.md`) is **pre-merge only** — champion/challenger picker above L0–L6. It does **not** replace or block ship gates.

| Rule | Detail |
|------|--------|
| **No human playtest for ship** until `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` exits 0 | L5 is the final AI gate |
| **No human sign-off** until L0–L5 all pass on the same commit | Same `game/development` RC SHA for AI + human |
| **Agents must not** ask humans to playtest to debug incomplete AI coverage | Fix via L0–L5 first |
| **Phase 1–7 work** uses L0–L4 (and L5 at Phase 6); humans do not run `PLAYTEST_SCRIPT.md` mid-rebuild |

Human QA (`docs/ops/qa/PLAYTEST_SCRIPT.md`) is **Phase 8 / ship gate only**, and **always after** the full AI automated suite.

---

## 1. Test layer summary

| Layer | Command / tool | Frequency | Blocks |
|-------|----------------|-----------|--------|
| **L0** | `validate_story_data.py`, `validate_base_classes.py`, `validate_audio_qa_catalog.py`, `validate_scene_audio_map.py`, `check_base_class_compliance.sh`, `check_rr_compliance.sh` | Every commit | — |
| **L1** | `run_unit_tests.sh`, `check_gdscript_changed.sh` | Every commit | — |
| **L2** | `run_playtest_smoke.sh`, `check_animation_whitelist.py`, `run_feel_smoke_checks.sh`, `check_glb_import_scripts.py` | Every commit | — |
| **L2.5** | `run_candidate_tournament.sh` (optional pre-merge) | Zone/asset tournaments when policy requires | — |
| **L3** | GDAI MCP (see §3) | Every scene/visual task | — |
| **L4** | `bash tools/run_integration_tests.sh` | Phase gates 2–6 | Phase advance |
| **L5** | `bash tools/run_e2e_playthrough.sh` | Phase 6 complete + release candidate | **Human QA** |
| **L6** | `docs/ops/qa/PLAYTEST_SCRIPT.md` | After L5 on RC | **Ship** |

---

## Layer packs (progressive disclosure)

Load only the layer you are running — do not preload this whole bible.

| Layer | Pack |
|-------|------|
| L0 | [testing/l0.md](testing/l0.md) |
| L1 | [testing/l1.md](testing/l1.md) |
| L2 | [testing/l2.md](testing/l2.md) |
| L3 | [testing/l3.md](testing/l3.md) |
| L4 | [testing/l4.md](testing/l4.md) |
| L5 | [testing/l5.md](testing/l5.md) |
| L6 | [testing/l6.md](testing/l6.md) |
| Toolkit | [testing/toolkit.md](testing/toolkit.md) |
| Phases / report | [testing/phases_and_report.md](testing/phases_and_report.md) |

## 9. Phase → required test layers

| Phase | Layers required before phase sign-off |
|-------|--------------------------------------|
| 0 | L0, L1, L2, L3 (boot) |
| 1 | L0–L3 |
| 2 | L0–L4 |
| 3 | L0–L4 |
| 4 | L0–L4 |
| 5 | L0–L4 |
| 6 | L0–L5 |
| 7 | L0–L5 (+ asset compliance) |
| 8 | L0–L5 on RC → **then L6 human** → export |

**Human QA never runs before Phase 6 L5 is implemented and passing.**

---

