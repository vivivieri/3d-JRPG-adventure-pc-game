---
id: remediation-loop
type: how-to
phase: [1, 6]
audience: [qa, pm]
status: active
authority: qa
tokens_est: 535
summary: "┌─────────┐ ┌──────────────┐ ┌─────────────────┐ ┌────────────┐"
---
# Remediation — Standards & Loop — Remediation loop

**Hub:** [`standards_loop.md`](../standards_loop.md)

## 2. The remediation loop (required on every FAIL)

```
┌─────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────┐
│ QA FAIL │───▶│ Brief script │───▶│ Pick ONE lever  │───▶│ Rebuild vN │
└─────────┘    │ + playbook   │    │ log revision    │    └─────┬──────┘
               └──────────────┘    └─────────────────┘          │
                                                                 ▼
                                                          ┌────────────┐
                                                          │ Re-run QA  │
                                                          └─────┬──────┘
                                                                │
                    ┌───────────────────────────────────────────┘
                    ▼
         PASS ──▶ ship asset
         FAIL ──▶ attempt < max? ──yes──▶ loop (must change different lever)
                    │
                    no ──▶ ESCALATE (tool tier ↑ or human L6)
```

### Step-by-step (agent mandatory)

1. **Capture** — jury JSON (`*.jury.json`), technical stderr, or lint output. Do not delete on FAIL.
2. **Brief** — `python3 tools/qa_remediation_brief.py --jury <path>` (or `--technical-model`, `--technical-audio`).
3. **Log** — append attempt to `artifacts/<domain>_reviews/<asset>/revision_log.json` via `--log-attempt`.
4. **Change ONE lever** from the brief (see §3). Document in commit message: `fix(urashima): attempt 2 — Tripo prompt + added coat folds (m5 fail)`.
5. **Do NOT repeat** anything listed under `do_not_repeat` in the playbook for that failure code.
6. **Re-QA** full layer (not just the step that failed — downstream may have masked issues).
7. **Escalate** after **2 failed attempts with the same lever class** (e.g. two `meshy_prompt` tweaks) → switch tool tier per `ART_AUTOMATION_PIPELINE.md` §1.

---
