---
id: remediation-done
type: reference
phase: [0, 1]
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 486
summary: "Controls Cheat Sheet — Remediation, DoD, verify, related — 1. `bash tools/qa_emit_remediation.sh <brief-id>"
---
# Controls Cheat Sheet — Remediation, DoD, verify, related

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

## When to read

Use **Controls Cheat Sheet — Remediation, DoD, verify, related** (roles: pm, builder, qa, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [Remediation (QA FAIL loop)](#remediation-qa-fail-loop)
- [Definition of done (merge)](#definition-of-done-merge)
- [Quick verify commands](#quick-verify-commands)
- [Related docs](#related-docs)


## Remediation (QA FAIL loop)

1. `bash tools/qa_emit_remediation.sh <brief-id>`
2. Change **one lever** (mesh / albedo / lighting / prompt — not all at once)
3. Re-run failing gate; paste evidence in issue
4. Same prompt twice → **blocked** after 2 attempts (`docs/ops/qa/QA_REMEDIATION_LOOP.md`)

---


## Definition of done (merge)

- [ ] PR template checkboxes satisfied for touched roles
- [ ] All listed **gate IDs PASS** on PR commit (CI green)
- [ ] QA gate report in PR body with evidence paths
- [ ] Builder: `.gdai_built` updated if scenes changed
- [ ] Correct branch (`main` = docs/data; `game/development` = code)

---


## Quick verify commands

```bash
# game/development
bash tools/run_ci_checks.sh
bash tools/check_rr_compliance.sh
bash tools/check_l3_gdai_built.sh

# main
bash tools/run_docs_ci_checks.sh

# pre-tag
bash tools/run_cd_gates.sh --channel rc
```

---


## Related docs

| Doc | Contents |
|-----|----------|
| `docs/ops/cheat-sheets/RR_CHEATSHEET.md` | Role ownership |
| `docs/ops/ci-cd/CI.md` | Full CI matrix |
| `docs/ops/qa/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| `docs/ops/agents/PROJECT_MANAGEMENT.md` | Issues, labels, traceability |
| `docs/ops/ci-cd/GITHUB_SETUP.md` | PAT + branch protection |
| `docs/ops/qa/QA_REMEDIATION_LOOP.md` | FAIL iteration |
| `game/data/qa/acceptance_criteria.json` | Machine-readable gates |
