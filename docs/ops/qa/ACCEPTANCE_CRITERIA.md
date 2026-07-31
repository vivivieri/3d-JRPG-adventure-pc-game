---
id: acceptance-criteria
type: reference
audience: [qa, pm, builder]
status: active
authority: qa
tokens_est: 259
summary: "Measurable pass/fail gates — load catalog or jury section"
---
# Acceptance Criteria

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`why_rules.md`](acceptance/why_rules.md) | Why QA fails without this + global pass rules |
| [`gate_catalog.md`](acceptance/gate_catalog.md) | Gate catalog summary |
| [`jury_report.md`](acceptance/jury_report.md) | Jury enforcement + agent report template |
| [`phase_tools.md`](acceptance/phase_tools.md) | Phase gates, tools, remediation relationship |
**Version:** 1.3
**Authority:** If a gate is not defined here with a **metric or boolean threshold**, it **cannot block ship**. Vague “looks good” is not QA.

**Machine-readable catalog:** `game/data/qa/acceptance_criteria.json`

## Candidate tournament (non-ship)

Optional pre-merge champion/challenger — gate id `L2_candidate_select` (`docs/ops/qa/CANDIDATE_TOURNAMENT.md`).
