---
id: why-rules
type: reference
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 423
summary: "Why QA fails without this + global pass rules"
---
# Acceptance Criteria — Why QA fails without this + global pass rules

**Hub:** [`ACCEPTANCE_CRITERIA.md`](../ACCEPTANCE_CRITERIA.md)

## 1. Why QA fails without this

| Useless QA | Valid QA |
|------------|----------|
| “F5 passed, 0 errors” for visuals | Screenshot + palette metrics + 2/3 jury with confidence ≥ 0.65 |
| Agent says “done” with no artifact | Evidence path listed in gate result |
| WARN treated as PASS for M5 | WARN = not ship-ready (`global_rules.warn_is_not_pass`) |
| Jury skipped (no API keys) = pass | SKIP = not PASS |
| Model says `overall_pass: true` alone | Tool recomputes pass from criterion booleans + confidence |
| Re-run same build hoping for different jury | Remediation brief + one lever change |

---


## 2. Global pass rules

From `acceptance_criteria.json` → `global_rules`:

| Rule | Meaning |
|------|---------|
| `warn_is_not_pass` | WARN may exit 0 in dev smoke but **not** M5 ship |
| `skip_is_not_pass` | Missing assets / no API keys = incomplete, not approved — **except** `issue_bootstrap.P1-00` deferred gates during Phase 1 bootstrap |
| `jury_min_pass_models` | **2** models must pass |
| `jury_min_confidence` | **0.65** minimum per model (enforced in `qa_acceptance_lib.py`) |
| `evidence_required_for_pass` | Agent report must cite artifact paths |
| `agent_must_cite_criterion_id` | Reports use gate ids e.g. `L2_visual_palette` |

### Invalid pass patterns (forbidden)

Listed in `acceptance_criteria.json` → `invalid_pass_patterns`. Agents must not use these.

---
