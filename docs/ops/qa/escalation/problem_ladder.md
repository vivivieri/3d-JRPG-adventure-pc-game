---
id: problem-ladder
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 613
summary: "`dev → QA check → dev fix → QA reopen → …` can loop forever if the root cause isn't a code bug — because **neither dev nor QA can change the requirement.** Comm"
---
# Escalation Policy — Problem + ladder

**Hub:** [`ESCALATION_POLICY.md`](../ESCALATION_POLICY.md)

## The problem

`dev → QA check → dev fix → QA reopen → …` can loop forever if the root cause isn't a code bug — because **neither dev nor QA can change the requirement.** Common causes: ambiguous/conflicting requirements, an infeasible spec, a moving target, symptom-only fixes, flaky tests, or a non-measurable QA bar.


## The ladder (bounded — always converges)

```
Tier 1  dev ↔ QA loop        cap: max_reopens = 3   ── exceeded ─▶ Tier 2
Tier 2  Arbitration          owner: Architect (Design Authority / SA)
        classify root cause: code_bug | qa_too_strict | requirement_ambiguous
                             | requirement_conflict | infeasible
        resolve, OR (cap 2 / needs business decision) ── ▶ Tier 3
Tier 3  Product Owner (human, Telegram)   final authority — can change scope/requirements
```

- **Tier 1 — dev ↔ QA:** normal fix/reopen. QA must cite the **failing `acceptance_gate_id` + evidence** on every reopen; flaky tests are quarantined, not reopened. After **3 reopens** it must escalate — it cannot loop again.
- **Tier 2 — Arbitration (Architect = Design Authority / SA):** the arbiter reproduces, **classifies the root cause**, and acts:
  - `code_bug` → return to dev
  - `qa_too_strict` → adjust the gate threshold/criteria (QA + Architect), re-verify
  - `requirement_ambiguous` → amend the design doc / `game/data/` to disambiguate, reset acceptance, re-dispatch
  - `requirement_conflict` → amend design/data to remove the conflict; if it's a business trade-off → **escalate to Product Owner**
  - `infeasible` → descope, or **escalate to Product Owner** for a scope/priority call

  The arbiter can change the **requirement** (the thing dev/QA cannot) — that is what actually breaks the loop.
- **Tier 3 — Product Owner:** if arbitration can't resolve it or a **business/scope decision** is required, it goes to the Product Owner over **Telegram**. Only the PO can `amend_requirement | descope | wont_fix | approve_as_is | reprioritize`. The decision is recorded and the issue re-dispatched against the corrected spec (or closed).
