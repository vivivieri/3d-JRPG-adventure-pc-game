---
id: m0-data-ai
type: reference
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 359
summary: "- [x] Data architecture (`docs/engineering/technical/DATA_ARCHITECTURE.md`)"
---
# Milestones — Pre-build — M0e / M0h

**Hub:** [`pre_build.md`](../pre_build.md)

## M0e — Story data layer (main branch)
- [x] Data architecture (`docs/engineering/technical/DATA_ARCHITECTURE.md`)
- [x] Story spine + flags (`game/data/story/`)
- [x] 5 quests, 9 encounters, 20 items, 22 dialogue scenes
- [x] Shop, achievements, new game defaults
- [x] `tools/validate_story_data.py`



## M0h — AI dev workflow & testing (main baseline)
- [x] AI build policy — GodotPrompter + MCP stack (`.cursorrules` §0, `docs/ops/agents/MCP_STACK.md`)
- [x] Unit test scaffold on **`game/development`** (`game/tests/unit/`, `tools/run_unit_tests.sh`) — restored with P1-00
- [x] Smoke tests (`tools/run_playtest_smoke.sh`)
- [x] Acceptance criteria catalog (`docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `game/data/qa/acceptance_criteria.json`)
- [x] Domain QA gates (MODEL/VISUAL/AUDIO/FLOW QA + `QA_REMEDIATION_LOOP.md`)
- [x] Phase acceptance criteria documented (`docs/ops/workflow/AI_DEV_WORKFLOW.md` §4)
- [x] AI testing spec L0–L6 (`docs/ops/qa/AI_TESTING_SPEC.md`) — human QA after L5
- [ ] Integration tests (`tools/run_integration_tests.sh`) — expand Phase 2+
- [ ] E2E three endings (`tools/run_e2e_playthrough.sh`) — Phase 6
