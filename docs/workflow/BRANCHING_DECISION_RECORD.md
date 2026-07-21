# ADR: Branching Strategy for Multi-Agent JRPG Development

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** Project architecture (documented for agents and stakeholders)
**Hub doc:** `docs/workflow/DEVELOPMENT_LIFECYCLE.md`

---

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

## Why environment branches were rejected

### 1. Stages are not separate deployables

| Stage | What it actually is in this project |
|-------|-------------------------------------|
| **Dev** | Work on trunk + feature branches |
| **QA** | `game-ci.yml` on every push to `game/development` |
| **UAT** | Tagged commit + RC zip (`cd-artifact.yml`) |
| **Preprod** | Tagged commit + Steam beta (`cd-steam.yml`) |
| **Prod** | Tagged commit + Steam prod + approval |

Each stage is a **gate + artifact on the same lineage**, not a diverging branch that needs periodic merges.

### 2. `main` is not the game trunk

GitLab Flow assumes `main` flows to `qa`. Here:

- `main` has **no** `project.godot`, no `.gd`, no ship `.tscn`
- `game/development` is the implementation trunk until M6
- Merging `main` → `qa` → `uat` would either be empty or wrong

### 3. Binary asset merge pain

Long-lived environment branches multiply merge conflicts on GLB, textures, and `.import` files. Tag promotion keeps **one lineage**; conflicts resolve at PR time on feature branches.

### 4. Environment drift risk

With `qa` behind `dev` and `uat` behind `qa`, teams must constantly merge forward. Tag promotion guarantees UAT/preprod/prod test **exact commits** that passed CI.

---

## Why per-agent forks were rejected

### Arguments for forks (acknowledged)

- AI agents can produce broken code or bad git history
- Isolated sandboxes prevent cross-agent interference
- Local heavy asset work stays off central `.git` until ready

### Why issue branches + orchestrator suffice here

| Control | Mechanism |
|---------|-----------|
| Blast radius | `cursor/p1-02-a091` — bad work never touches trunk until PR |
| Role separation | `run_agent_session_gate.sh` — one role per session |
| WIP limits | `sprint_board.json` → `max_in_progress` |
| Merge gate | PR + `game-ci.yml` required |
| Done proof | `pm_check_done_criteria.py`, evidence bundles |
| Remediation | Same issue re-dispatched; `qa_emit_remediation.sh` |

Forks would duplicate:

- Sprint board ↔ GitHub issue linkage
- `pm_sync_github_issues.py` / `pm_sync_linear.py` traceability
- Single-repo CI and branch protection

**Reserved for future reconsideration** if untrusted third-party agents contribute outside the PM orchestrator.

---

## Why trunk-based was not rejected

Common objection: *3D builds are too slow for trunk-based development.*

**Response:** We use **trunk-based with short-lived branches**, not continuous direct-to-trunk commits:

- Agents work on `cursor/*` until gates pass
- L0–L2 run every PR
- L4/L5 run at phase milestones only
- L6 is human on tagged RC only

Slow tests are **gated by layer**, not by maintaining five environment branches.

---

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

- `docs/workflow/BRANCHING.md`
- `docs/ci-cd/ENVIRONMENTS.md`
- `game/data/qa/environments.json`
- `tools/check_main_no_ship_code.sh` (main purity)

---

## References

- [Git branching strategies (DEV community overview)](https://dev.to/karmpatel/git-branching-strategies-a-comprehensive-guide-24kh) — evaluated; hybrid env-branch + fork model **not adopted**
- `docs/workflow/BRANCHING.md`
- `docs/workflow/DEVELOPMENT_LIFECYCLE.md`
- `docs/agents/MULTI_AGENT_BRANCH_STRATEGY.md`
