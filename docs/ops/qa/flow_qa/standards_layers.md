---
id: standards-layers
type: how-to
audience: [flow, qa, builder]
status: active
authority: qa
tokens_est: 516
summary: "Industry standards + defense layers"
---
# Flow QA — Industry standards + defense layers

**Hub:** [`FLOW_QA.md`](../FLOW_QA.md)

## 1. Industry standards we map to

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Critical path testing** | Main story completable without optional content | `story/scenes.json` spine + L5 E2E three endings |
| **Scenario / acceptance testing** | Given-when-then flows with pass/fail asserts | L4 `INT-*` scenarios in `AI_TESTING_SPEC.md` §6 |
| **Milestone acceptance criteria** | Phase gate checklist before advance | `AI_DEV_WORKFLOW.md` per-phase acceptance |
| **Vertical slice playtest** | One playable hub loop before full game | Phase 1 SC-02 ruined_village + INT-ZONE/Save |
| **Functional requirements (TRC-style)** | Save works, no progression blockers, no boot crash | L2 smoke boot + INT-SAVE-01 |
| **Exploratory testing with charter** | Time-boxed “try to break progression” | Human L6 `PLAYTEST_SCRIPT.md` — **after** L5 |
| **Root-cause debugging** | Trace signals/state, not random edits | Godotiq `trace_flow` / `signal_map` before re-patch |

**References:** ISTQB scenario testing; platform manufacturer functional test categories (save data, progression); Valve playtesting (observe blockers, categorize severity).

---


## 2. Defense layers (game flow)

```
F0  validate_story_data.py     → JSON cross-refs (flags, items, dialogue)
F1  run_unit_tests.sh           → parsers, calculators, flag math
F2  run_playtest_smoke.sh       → boot + art/audio/model smoke
F4  run_integration_tests.sh    → INT-* (`game/data/qa/integration_scenarios.json`)
F5  REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh  → full spine + 3 endings (Phase 6+)
F6  PLAYTEST_SCRIPT.md          → human 2–3h + feel checklist §7b (ship only)
```

**Flow QA focuses on F0, F4, F5.** Art/audio/model gates run in F2 but are documented separately.

---
