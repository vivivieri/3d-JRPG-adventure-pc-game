---
id: workflow-report
type: how-to
phase: [1, 6]
audience: [flow, qa, builder]
status: active
authority: qa
tokens_est: 831
summary: "Agent workflow, iteration, smoke, report, tools"
---
# Flow QA — Agent workflow, iteration, smoke, report, tools

**Hub:** [`FLOW_QA.md`](../FLOW_QA.md)

## 5. Agent workflow (flow task)

```
1. READ  TECHNICAL_DESIGN.md + scene row in scenes.json
2. GodotPrompter — plan flags, triggers, encounter hooks
3. GDAI MCP — wire scene (triggers, dialogue, transitions)
4. python3 tools/validate_story_data.py
5. bash tools/run_unit_tests.sh
6. bash tools/run_integration_tests.sh  (when scenario exists)
7. On FAIL → python3 tools/qa_remediation_brief.py --flow-scenario <ID> --log-attempt
8. Change ONE flow lever; commit with scenario ID in message
9. Re-run F0 → F4 for that scenario only, then full suite
```

---


## 6. Unified iterative improvement (all domains)

```
         ┌─────────────────────────────────────────────┐
         │  BUILD (GodotPrompter plan → GDAI execute)  │
         └─────────────────────┬───────────────────────┘
                               ▼
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    │ L0 data  │ L2 art   │ L2 audio │ L2 model │ L4 flow  │
    │ validate │ visual   │ audio    │ model    │ INT-*    │
    └────┬─────┴────┬─────┴────┬─────┴────┬─────┴────┬─────┘
         │ FAIL     │ FAIL     │ FAIL     │ FAIL     │ FAIL
         ▼          ▼          ▼          ▼          ▼
    qa_remediation_brief.py  (one lever, revision_log, max 3 attempts)
         │          │          │          │          │
         └──────────┴──────────┴──────────┴──────────┘
                               ▼
                         REBUILD vN+1
```

| Domain | QA doc | Brief trigger |
|--------|--------|---------------|
| Data / story | This doc §2 F0 | `--validate-story` |
| Game flow | This doc | `--flow-scenario INT-*` |
| 3D model | `MODEL_QA.md` | `--technical-model` / `--jury` |
| Visual | `VISUAL_QA.md` | palette / jury |
| Audio (BGM) | `AUDIO_QA.md` | `--technical-audio` / `--jury` |
| Audio (P0 VO) | `AUDIO_QA.md` §A4–A5 | `--technical-vo` / `--jury` (vo_reviews) |

Master policy: `docs/ops/qa/QA_REMEDIATION_LOOP.md` §10.

---


## 7. L2 smoke auto-brief

When `run_playtest_smoke.sh` or domain smoke scripts fail technical lint or jury, they call:

```bash
bash tools/qa_emit_remediation.sh <kind> [args]
```

Agents must read the emitted brief before the next build attempt.

---


## 8. Agent report template (flow FAIL)

```markdown
[FLOW QA] scenario=INT-QUEST-01 attempt=2
  validate_story_data: PASS
  integration: FAIL at step "inspect well" — flag well_inspected not set
  lever_changed: trigger_wiring (well Area3D on_interact → set_flags)
  do_not_repeat: editing quest JSON only (attempt 1)
  godotiq: traced StoryManager.inspectable_well → no connection
  next: GDAI wire signal → re-run INT-QUEST-01
```

---


## 9. Tools

| Tool | Role |
|------|------|
| `tools/validate_story_data.py` | F0 data gate |
| `tools/run_integration_tests.sh` | F4 scenario runner |
| `tools/run_e2e_playthrough.sh` | F5 full spine |
| `tools/qa_remediation_brief.py` | Brief for any domain |
| `tools/qa_emit_remediation.sh` | Smoke/integration FAIL → brief |
| `game/data/qa/remediation_playbook.json` | §`data`, §`flow` entries |
