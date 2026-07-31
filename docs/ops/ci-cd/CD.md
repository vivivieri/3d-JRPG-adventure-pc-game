---
id: cd
type: how-to
phase: [6, 8]
audience: [release, pm]
status: active
authority: ci-cd
tokens_est: 207
summary: "CD workflows — load purpose, Steam secrets, or remediation"
---
# Continuous Delivery

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`purpose_prereqs_workflows.md`](cd/purpose_prereqs_workflows.md) | Purpose, prerequisites, workflows |
| [`local_secrets.md`](cd/local_secrets.md) | Local CD + Steam secrets |
| [`vs_ci_remediation.md`](cd/vs_ci_remediation.md) | CD vs CI, remediation, refs |
**Version:** 1.1
**Workflows:** `.github/workflows/cd-artifact.yml` · `.github/workflows/cd-steam.yml`
**Gate script:** `bash tools/run_cd_gates.sh`
**Steam checklist:** `docs/ops/ci-cd/STEAM_RELEASE_CHECKLIST.md`
**Branch policy:** `docs/ops/workflow/BRANCHING.md`

---

