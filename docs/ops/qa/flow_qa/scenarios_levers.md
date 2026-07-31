---
id: scenarios-levers
type: how-to
audience: [flow, qa, builder]
status: active
authority: qa
tokens_est: 563
summary: "L4 scenarios + lever taxonomy"
---
# Flow QA — L4 scenarios + lever taxonomy

**Hub:** [`FLOW_QA.md`](../FLOW_QA.md)

## 3. Integration scenarios (L4)

Implement in `game/tests/integration/` as phases land. **Catalog:** `game/data/qa/integration_scenarios.json`. IDs from `AI_TESTING_SPEC.md` §6:

| Phase | ID | Asserts |
|-------|-----|---------|
| 2 | `INT-MENU-01` | New game → beach; `game_started` |
| 2 | `INT-ZONE-01` | Beach → ruined_village transition |
| 2 | `INT-SAVE-01` | Well save round-trip |
| 3 | `INT-DLG-01` | SC-03 torii dialogue fires |
| 3 | `INT-QUEST-01` | Q1 stage advances after inspectables |
| 3 | `INT-FIELD-01` | SC-01–05 no soft-lock |
| 4 | `INT-CMB-01` | Salt Crab tutorial win |
| 4 | `INT-CMB-02` | Full combat turn resolves |
| 5 | `INT-PUZ-01` | SC-07 water puzzle + saber |
| 5 | `INT-BOSS-01` | Shore Wraith → `wraith_pearl` |
| 5 | `INT-PARTY-01` | Yuzu joins |
| 6 | `INT-GATE-01` | Palace gate with pearl |
| 6 | `INT-BOSS-02` | Sentinel + Tide Keeper → SC-16 |

**On scenario FAIL:**

```bash
python3 tools/qa_remediation_brief.py --flow-scenario INT-QUEST-01 --log-attempt
```

---


## 4. Flow lever taxonomy (change one per attempt)

| Lever | Fix when | Tools |
|-------|----------|-------|
| `data_fix` | L0 validation: unknown flag/item/dialogue | Edit `game/data/` JSON; re-run `validate_story_data.py` |
| `trigger_wiring` | Interactable never fires | GDAI: Area3D, signals, `interactable.gd` |
| `flag_logic` | Quest stuck, wrong branch | `QUEST_AND_FLAGS.md`; quest stage conditions |
| `combat_logic` | Combat hang, no win | Combat autoload, encounter `on_win` grants |
| `save_system` | Save/load regression | `SAVE_AND_FAIL_STATES.md`; well trigger |
| `zone_transition` | Zone load fail, wrong spawn | `LEVEL_DESIGN.md`; transition volumes |
| `ui_navigation` | Menu/dialogue soft-lock | Godotiq `ui_map`; dialogue block `on_complete` |
| `godotiq_trace` | Unknown hang after 2 blind patches | `godotiq_trace_flow`, `godotiq_signal_map` |

**Forbidden:** Re-run same integration test without changing lever. Patch random `.gd` without tracing failing scenario step.

---
