---
id: branching
type: reference
phase: [0, 1, 8]
audience: [pm, architect, builder, release]
status: active
authority: workflow
tokens_est: 211
summary: "main vs game/development — load roles, rules, or CI"
---
# Branching Policy

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`roles_rules.md`](branching/roles_rules.md) | Branch roles + rules |
| [`workflow_ci.md`](branching/workflow_ci.md) | Developer workflow + CI per branch |
| [`create_branch_refs.md`](branching/create_branch_refs.md) | Creating game branch + cross-refs |
**Version:** 1.2
**Authority:** Branch contents and merge policy. For the **full dev → ship lifecycle**, start at `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md`.
**Branching ADR:** `docs/ops/workflow/BRANCHING_DECISION_RECORD.md` — why we reject GitLab env branches and per-agent forks.

