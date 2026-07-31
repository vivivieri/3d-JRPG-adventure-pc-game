---
id: environments
type: reference
phase: [6, 8]
audience: [pm, release]
status: active
authority: ci-cd
tokens_est: 223
summary: "dev→qa→uat→prod — load map, requirements, or promotion"
---
# Environments

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`map_preprod.md`](environments/map_preprod.md) | Environment map + preprod necessity |
| [`requirements_github.md`](environments/requirements_github.md) | Per-env requirements + GitHub Environments |
| [`promotion_logs.md`](environments/promotion_logs.md) | Promotion, log correlation, refs |
**Version:** 1.1
**Machine-readable:** `game/data/qa/environments.json`
**Lifecycle hub:** `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md` — full dev → ship flow (this doc = per-stage detail)
**Branching ADR:** `docs/ops/workflow/BRANCHING_DECISION_RECORD.md` — stages are **not** long-lived git branches

