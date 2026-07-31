---
id: ci
type: reference
audience: [release, qa, pm]
status: active
authority: ci-cd
tokens_est: 900
summary: "Required CI gates, local reproduction, remediation"
---
# Continuous Integration

**Hub** — load one pack below.

| Pack | Topic |
|------|-------|
| [`branch_purpose.md`](ci/branch_purpose.md) | Branch split & purpose |
| [`required_gates.md`](ci/required_gates.md) | What CI runs / does not run |
| [`local_rr_remediation.md`](ci/local_rr_remediation.md) | Local repro, R&R, remediation |
| [`branch_protection_refs.md`](ci/branch_protection_refs.md) | Branch protection & cross-refs |
# Continuous Integration — GitHub Actions

**Version:** 1.3
**Workflow:** `.github/workflows/ci.yml` (main) · `.github/workflows/game-ci.yml` (`game/development`)
**Runner scripts:** `bash tools/run_docs_ci_checks.sh` (main) · `bash tools/run_ci_checks.sh` (game)
**Authority:** `game/data/qa/acceptance_criteria.json` → `ci_gates` / `docs_ci_gates`
**Branch policy:** `docs/ops/workflow/BRANCHING.md`

---
