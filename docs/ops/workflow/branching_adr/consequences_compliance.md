---
id: consequences-compliance
type: explanation
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 719
summary: "- Single implementation lineage — easy to bisect"
---
# Branching Decision Record — Consequences, mapping, compliance, refs

**Hub:** [`BRANCHING_DECISION_RECORD.md`](../BRANCHING_DECISION_RECORD.md)

## When to read

Use **Branching Decision Record — Consequences, mapping, compliance, refs** (roles: pm, architect) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [Consequences](#consequences)
- [Positive](#positive)
- [Negative / trade-offs](#negative-trade-offs)
- [Mitigations (see `DEVELOPMENT_LIFECYCLE.md` §10)](#mitigations-see-development_lifecyclemd-10)
- [Mapping: external advice → this project](#mapping-external-advice-this-project)
- [Compliance](#compliance)
- [References](#references)


## Consequences

### Positive

- Single implementation lineage — easy to bisect
- Spec/data PRs to `main` stay clean and fast
- Promotion is explicit: tag + `run_cd_gates.sh --channel <rc|beta|prod>`
- Agents share one orchestration model documented in `MULTI_AGENT_BRANCH_STRATEGY.md`

### Negative / trade-offs

- All agents share `game/development` history — requires PR discipline
- No automatic “deploy qa branch” — QA is CI on trunk (by design)
- Fork isolation must be replaced by session gates and branch protection

### Mitigations (see `DEVELOPMENT_LIFECYCLE.md` §10)

1. Require PR + CI for `game/development`
2. Enforce GitHub Environments on Steam CD
3. Optional per-sprint cloud snapshots (not per-agent forks)
4. Git LFS when asset volume warrants it

---


## Mapping: external advice → this project

| External pattern | Our equivalent |
|------------------|----------------|
| `main` integration branch | `game/development` |
| `qa` branch | CI on trunk (`env/qa` label) |
| `uat` branch | Tag `v*-rc*` + RC artifact |
| `preprod` branch | Tag `v*-beta*` + Steam beta |
| `prod` branch | Tag `v*.*.*` + Steam prod |
| Agent fork | `cursor/<issue-id>-<suffix>` |
| Supervisor merge approval | PR review + CI + PM orchestrator |
| Design / spec repo | `main` branch in same monorepo |

---


## Compliance

Agents and contributors **must not**:

- Create long-lived `qa`, `uat`, `preprod`, or `prod` git branches
- Use per-agent forks without explicit ADR amendment
- Merge ship code to `main` before M6 ship gate
- Skip CI and promote via branch merge instead of tags

Validators and docs referencing this decision:

- `docs/ops/workflow/BRANCHING.md`
- `docs/ops/ci-cd/ENVIRONMENTS.md`
- `game/data/qa/environments.json`
- `tools/check_main_no_ship_code.sh` (main purity)

---


## References

- [Git branching strategies (DEV community overview)](https://dev.to/karmpatel/git-branching-strategies-a-comprehensive-guide-24kh) — evaluated; hybrid env-branch + fork model **not adopted**
- `docs/ops/workflow/BRANCHING.md`
- `docs/ops/workflow/DEVELOPMENT_LIFECYCLE.md`
- `docs/ops/agents/MULTI_AGENT_BRANCH_STRATEGY.md`
