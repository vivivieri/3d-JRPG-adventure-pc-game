---
id: commands
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 400
summary: "[`AI_DEV_WORKFLOW.md`](../AI_DEV_WORKFLOW.md)"
---
# AI Dev Workflow — commands

**Hub:** [`AI_DEV_WORKFLOW.md`](../AI_DEV_WORKFLOW.md)

## 5. Command cheat sheet

```bash
# Every agent session
bash tools/ensure_gdai_mcp.sh

# Every commit (L0–L2)
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh

# Phase gates (L4 — add scripts as phases land)
bash tools/run_integration_tests.sh

# Phase 6+ (L5 — required before human QA)
bash tools/run_e2e_playthrough.sh

# Ship — AI tests first, then human (L6)
bash tools/check_asset_compliance.sh
# Human QA only after L0–L5 pass: docs/ops/qa/PLAYTEST_SCRIPT.md
```

---

## 6. Related docs

| Doc | Focus |
|-----|-------|
| `docs/ops/qa/AI_TESTING_SPEC.md` | **Detailed L0–L6 spec**, L3 procedures, E2E matrix, human QA gate |
| `docs/ops/agents/GDAI_CLOUD_SETUP.md` | MCP install, cloud snapshot, editor bridge |
| `docs/ops/workflow/IMPLEMENTATION_PLAN.md` | What to build each phase |
| `docs/ops/qa/QA_AND_BUG_PROCESS.md` | Bug severity, triage, human QA process |
| `docs/ops/qa/PLAYTEST_SCRIPT.md` | Manual 2–3 h playthrough (**after L5**) |
| `AGENTS.md` | Cloud agent quick reference |
