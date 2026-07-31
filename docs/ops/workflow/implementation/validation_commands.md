---
id: validation-commands
type: how-to
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 351
summary: "Implementation Plan — Validation commands — python3 tools/validate_story_data.py"
---
# Implementation Plan — Validation commands

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## When to read

Use **Implementation Plan — Validation commands** (roles: pm, architect) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



## Validation commands

```bash
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
python3 tools/validate_audio_qa_catalog.py
python3 tools/validate_scene_audio_map.py
python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
python3 tools/review_vo_vision.py --clip sc00_urashima_01 --locale en
bash tools/ensure_gdai_mcp.sh
bash tools/run_unit_tests.sh
bash tools/check_dev_environment.sh
bash tools/run_playtest_smoke.sh
bash tools/run_model_smoke_checks.sh      # when gate GLBs exist
bash tools/run_visual_smoke_checks.sh     # when zone screenshots exist
bash tools/run_audio_smoke_checks.sh      # when gate BGM + VO clips exist
bash tools/generate_ai_vo.sh --list       # VO plan (dry-run: add --dry-run via python3)
bash tools/run_integration_tests.sh       # Phase 2+ gates
bash tools/run_e2e_playthrough.sh         # Phase 6 gate (not SKIP)
bash tools/check_asset_compliance.sh      # when assets exist
```

**QA policy:** `docs/ops/qa/ACCEPTANCE_CRITERIA.md` · **On FAIL:** `tools/qa_emit_remediation.sh` per `docs/ops/qa/QA_REMEDIATION_LOOP.md`

---

