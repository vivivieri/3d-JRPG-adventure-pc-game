---
id: templates-trace-logs
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 481
summary: "Templates, traceability, log sources"
---
# Project Management — Templates, traceability, log sources

**Hub:** [`PROJECT_MANAGEMENT.md`](../PROJECT_MANAGEMENT.md)

## 3. Issue templates

Use `.github/ISSUE_TEMPLATE/`:

| Template | When |
|----------|------|
| **Bug report** | Human or agent-found defect |
| **Gate failure** | CI/CD or `run_*_checks.sh` fail |
| **Feature / task** | Phase work from implementation plan |

**Pull request templates:** `.github/PULL_REQUEST_TEMPLATE/` — role handoff checklists + gate report (`docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`).

Title convention: `[ENV][Severity?][Gate?] Summary`

---


## 4. Traceability flow

```
GitHub Issue (#123)
    ├── linked PR (game/development)
    │     └── CI run → logs + gate ID in check name
    ├── commit SHA in issue body
    ├── artifacts/screenshots/*.png
    ├── artifacts/test-reports/ (optional)
    └── remediation: tools/qa_emit_remediation.sh output pasted in comment
```

### Agent obligation on FAIL

1. Run failing gate locally or read Actions log
2. `bash tools/qa_emit_remediation.sh <brief-id>` when available
3. Open or update issue with: gate ID, SHA, log excerpt, remediation lever
4. Label `env/qa` or `env/development`
5. **Do not close** until gate re-run PASS on same issue thread

---


## 5. Log sources by environment

| Source | Dev | QA | UAT | Preprod |
|--------|-----|----|----|---------|
| Godot Output (GDAI F5) | ✅ | — | — | — |
| Godotiq debug console | ✅ | ✅ | — | — |
| `run_ci_checks.sh` stdout | ✅ | ✅ | — | — |
| GitHub Actions log | — | ✅ | ✅ | ✅ |
| GitHub Release assets | — | — | ✅ | ✅ |
| Human playtest notes | — | — | ✅ | ✅ |
| Steam beta feedback | — | — | — | ✅ |

**Retention:** GitHub Actions logs ~90 days; attach critical logs to issues for long-term trace.

---
