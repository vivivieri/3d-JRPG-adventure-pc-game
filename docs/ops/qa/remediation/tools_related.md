---
id: tools-related
type: how-to
phase: [1, 6]
audience: [qa, builder, visual]
status: active
authority: qa
tokens_est: 562
summary: "Tools, related docs, unified improvement"
---
# QA Remediation Loop — Tools, related docs, unified improvement

**Hub:** [`QA_REMEDIATION_LOOP.md`](../QA_REMEDIATION_LOOP.md)

## 8. Tools

| Tool | Role |
|------|------|
| `game/data/qa/remediation_playbook.json` | Failure code → actions, do-not-repeat, lever class |
| `tools/qa_remediation_brief.py` | Generate brief from jury JSON or technical check |
| `artifacts/*/revision_log.json` | Per-asset attempt history (gitignored outputs; log structure committed as example) |

---


## 9. Related docs

| Doc | Role |
|-----|------|
| `docs/ops/qa/FLOW_QA.md` | **Game flow** — L0/L4/L5 progression + flow levers |
| `docs/ops/qa/QA_AND_BUG_PROCESS.md` | Gameplay bugs (S0–S3) — separate from art QA loop |
| `docs/ops/qa/AI_TESTING_SPEC.md` | L0–L6 test layers |
| `docs/ops/qa/PLAYTEST_SCRIPT.md` | Human L6 after automated pass |

---


## 10. Unified iterative improvement (all domains)

Everything in the project improves the same way:

```
BUILD → MEASURE (automated QA) → BRIEF on FAIL → change ONE lever → REBUILD
```

| Domain | Measure | Brief command |
|--------|---------|---------------|
| Story data | `validate_story_data.py` | `qa_emit_remediation.sh data-story` |
| Game flow | `run_integration_tests.sh` / E2E | `qa_emit_remediation.sh flow-scenario INT-*` |
| 3D model | model smoke / MODEL_QA | `qa_emit_remediation.sh model-tech\|model-jury` |
| Visual | visual smoke / VISUAL_QA | `qa_emit_remediation.sh visual-palette\|visual-jury` |
| Audio (BGM) | audio smoke / AUDIO_QA | `qa_emit_remediation.sh audio-tech\|audio-jury` |
| Audio (P0 VO) | audio smoke / AUDIO_QA §A4–A5 | `qa_emit_remediation.sh vo-tech\|vo-jury` |

Smoke and integration scripts **auto-emit** briefs on FAIL via `tools/qa_emit_remediation.sh`.

**Game flow detail:** `docs/ops/qa/FLOW_QA.md` — critical path testing, INT-* scenarios, flow lever taxonomy (`data_fix`, `trigger_wiring`, `flag_logic`, `godotiq_trace`, …).

**Stop rules apply to all domains:** max 3 attempts per asset/scenario; same lever class twice → blocked; then escalate (tool tier ↑ or human L6).
