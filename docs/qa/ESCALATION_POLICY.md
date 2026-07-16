# Escalation Policy — no infinite dev ↔ QA loops

**Version:** 1.0
**Purpose:** Guarantee every dev↔QA dispute converges to a decision. When fix→reopen can't resolve it (ambiguous/conflicting/infeasible requirement, or QA too strict), it escalates up a bounded ladder — ultimately to the Product Owner.
**Authority:** `game/data/qa/escalation_policy.json` · tool: `tools/pm_escalate.py`
**Cross-refs:** `docs/qa/QA_REMEDIATION_LOOP.md`, `docs/qa/QA_AND_BUG_PROCESS.md`, `docs/cheat-sheets/RR_CHEATSHEET.md`, `docs/agents/PM_STAKEHOLDER_REPORTING.md`

---

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

## Using it (`tools/pm_escalate.py`)

```bash
# Tier 1 cap reached -> hand to the Architect / SA:
python3 tools/pm_escalate.py --issue P1-02 --to arbitration --reopens 3 --reason "QA keeps failing L2_feel_smoke"

# Arbitration can't resolve / needs a business decision -> Product Owner (Telegram):
python3 tools/pm_escalate.py --issue P1-02 --to product_owner \
    --root-cause requirement_conflict --reason "PACING vs COMBAT specs conflict at SC-12"

# Record the Product Owner's decision when it returns:
python3 tools/pm_escalate.py --issue P1-02 --record-decision descope --by product_owner --rationale "cut SC-12 second wraith"
```

Escalation + decision records are written to `artifacts/escalations/` (git-ignored). The Product Owner channel reuses the stakeholder pipeline (`stakeholder_report_config.json` trigger `product_owner_decision`, `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`). Escalations are **alerts** and bypass the pre-delivery review gate (they must be immediate).

## Why it can't loop forever

Every tier has a **cap**, and exceeding it escalates **up**, never sideways. The chain terminates at the Product Owner, who has the authority to change or cut the requirement — so there is always a decision that ends the loop. Validated by `tools/validate_escalation_policy.py` (gate `L0_escalation_policy`).
