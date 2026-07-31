---
id: usage-bounds
type: reference
phase: [1, 6]
audience: [pm, qa]
status: active
authority: qa
tokens_est: 417
summary: "python3 tools/pm_escalate.py --issue P1-02 --to arbitration --reopens 3 --reason 'QA keeps failing L2_feel_smoke'"
---
# Escalation Policy — Usage + anti-loop

**Hub:** [`ESCALATION_POLICY.md`](../ESCALATION_POLICY.md)

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
