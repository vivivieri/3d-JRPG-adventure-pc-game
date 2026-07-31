---
id: jury-report
type: reference
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 373
summary: "Jury enforcement + agent report template"
---
# Acceptance Criteria — Jury enforcement + agent report template

**Hub:** [`ACCEPTANCE_CRITERIA.md`](../ACCEPTANCE_CRITERIA.md)

## 4. Jury acceptance enforcement

Jury scripts (`review_*_vision.py`) **recompute** pass after each model response:

1. Every criterion boolean must match `expect` in catalog
2. `confidence ≥ 0.65`
3. On fail: `issues[]` must be non-empty
4. Consensus: ≥2 active models with `acceptance.valid_pass`

Jury JSON includes:

```json
"acceptance": {
  "gate_id": "L2_visual_jury",
  "criteria_results": { "v1_primitives_visible": true, ... },
  "confidence_ok": true,
  "valid_pass": true
}
```

**Do not** trust raw `overall_pass` from the LLM without the `acceptance` block.

---


## 5. Agent report template (required fields)

Every QA task ends with this block. **Missing fields = report invalid.**

```markdown
[QA ACCEPTANCE] task=<id> gate=<GATE_ID>
  criterion: L2_model_technical
  measured:
    tris: 14234 (expected 8000–22000)
    textures: 2 (expected >= 1)
  evidence:
    - game/assets/models/characters/urashima/urashima.glb
    - artifacts/model_reviews/urashima.model_jury.json
  jury: L2_model_jury PASS (2/3, conf>=0.65)
  invalid_pass_avoided: no WARN-as-PASS, no SKIP-as-PASS
  remediation: none | attempt N — <lever changed>
  result: VALID PASS | FAIL | WARN (dev only)
```

---
