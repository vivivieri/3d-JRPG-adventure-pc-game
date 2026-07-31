---
id: context-decision
type: explanation
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 644
summary: "Context, decision, comparison"
---
# Branching Decision Record — Context, decision, comparison

**Hub:** [`BRANCHING_DECISION_RECORD.md`](../BRANCHING_DECISION_RECORD.md)

## Context

Multi-agent 3D JRPG development needs:

1. **Sprint iteration** inside fixed implementation phases
2. **Five promotion stages:** dev → qa → uat → preprod → prod
3. **Agent isolation** so one bad session cannot corrupt the trunk
4. **Heavy assets and slow gates** (L0–L6, GDAI scenes, GLB pipeline)
5. **Spec-first split:** `main` = design/data only; `game/development` = ship code

External guides often recommend **GitLab Flow with environment branches** (`main` → `qa` → `uat` → `preprod` → `prod`) plus **per-agent repository forks**.

We evaluated whether that hybrid fits *Tides of Urashima*.

---


## Decision

**Adopt:**

| Mechanism | Implementation |
|-----------|----------------|
| **Dual trunk** | `main` (specs) + `game/development` (implementation) |
| **Short-lived feature branches** | `cursor/<issue-id>-<suffix>` per sprint issue |
| **Trunk-based integration** | Merge to `game/development` via PR + CI |
| **Tag-based release promotion** | `v*-rc*`, `v*-beta*`, `v*.*.*` on trunk |
| **Layered quality gates** | L0–L6 instead of branch-per-stage |
| **PM orchestration** | `run_pm_orchestrator.sh`, session gates, evidence bundles |

**Reject:**

| Mechanism | Reason |
|-----------|--------|
| Long-lived `qa` / `uat` / `preprod` / `prod` **branches** | Stages are **quality states**, not parallel code lines |
| **Per-agent repository forks** | Orchestrator + issue branches already bound blast radius |
| **GitFlow** (`develop`, `release/*`, `hotfix/*`) | Too many long-lived branches for AI merge logic |
| **`main` as implementation integration branch** | Conflicts with spec-first policy |

---


## Comparison with common strategies

| Strategy | Fit | Notes |
|----------|-----|-------|
| **GitFlow** | ❌ Poor | Multiple persistent branches; merge-back confusion for agents |
| **GitLab Flow (env branches)** | ❌ Poor | Assumes `main` is deployable app trunk; we use `game/development` + tags |
| **Forking workflow** | ⚠️ Mediocre | Valid isolation idea; forks add sync overhead vs in-repo `cursor/*` branches |
| **Trunk-based + short branches** | ✅ Good | Matches `game/development` + `cursor/*` + CI |
| **Our hybrid: spec trunk + game trunk + tags** | ✅ Best | Unique to spec-first + single-repo indie JRPG |

---
