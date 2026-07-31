---
id: escalation-policy
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 193
summary: "Bounded escalation ladder — load problem, ladder, or usage"
---
# Escalation Policy

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`problem_ladder.md`](escalation/problem_ladder.md) | Problem + ladder |
| [`usage_bounds.md`](escalation/usage_bounds.md) | Usage + anti-loop |
**Version:** 1.0
**Purpose:** Guarantee every dev↔QA dispute converges to a decision. When fix→reopen can't resolve it (ambiguous/conflicting/infeasible requirement, or QA too strict), it escalates up a bounded ladder — ultimately to the Product Owner.
**Authority:** `game/data/qa/escalation_policy.json` · tool: `tools/pm_escalate.py`

