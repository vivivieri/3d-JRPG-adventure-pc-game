---
id: enhancements-commands
type: explanation
phase: [0, 1, 8]
audience: [pm, architect, release]
status: active
authority: workflow
tokens_est: 978
summary: "Enhancements, commands, cross-refs"
---
# Development Lifecycle — Enhancements, commands, cross-refs

**Hub:** [`DEVELOPMENT_LIFECYCLE.md`](../DEVELOPMENT_LIFECYCLE.md)

## 10. Lifecycle enhancements

| # | Enhancement | Status | How |
|---|-------------|--------|-----|
| 1 | PR-only trunk protection | **Shipped** | `bash tools/setup_github_project.sh` — requires admin `GH_TOKEN` |
| 2 | GitHub Environments on CD | **Shipped** | `cd-artifact.yml`, `cd-steam.yml`, `qa-nightly.yml` |
| 3 | Environment reviewers | **Shipped** | Same setup script; optional `GITHUB_ENV_REVIEWER_LOGIN_2` for prod |
| 4 | Git LFS for large assets | **Shipped** | `.gitattributes`, `tools/install_git_lfs.sh`, `docs/ops/ci-cd/GIT_LFS.md` |
| 5 | Per-sprint cloud snapshots | **Pending** | Manual snapshot rebuild per sprint — see `CLOUD_SNAPSHOT_LAUNCH.md` |

### 10.1 Trunk protection (enhancement 1)

```bash
export GH_TOKEN=github_pat_...   # Administration: read/write
bash tools/setup_github_project.sh
```

| Control | Value |
|---------|-------|
| Branches | `main`, `game/development` |
| Required check | `Docs + design data gates` / `L0–L2 headless gates` |
| PR reviews | 1 required |

### 10.2 GitHub Environments on CD (enhancement 2–3)

| Workflow | Environment | Trigger |
|----------|-------------|---------|
| `qa-nightly.yml` | `qa` | Schedule / manual |
| `cd-artifact.yml` | `uat` | Tag `v*-rc*` |
| `cd-artifact.yml` | `steam-beta` | Tag `v*-beta*` |
| `cd-artifact.yml` | `steam-production` | Tag `v*.*.*` (semver ship) |
| `cd-steam.yml` | `steam-beta` / `steam-production` | `workflow_dispatch` |

Reviewer setup (enhancement 3):

```bash
export GH_TOKEN=...
export GITHUB_ENV_REVIEWER_LOGIN=your-github-login        # default: repo owner
export GITHUB_ENV_REVIEWER_LOGIN_2=second-reviewer-login  # optional; steam-production
bash tools/setup_github_project.sh
```

### 10.3 Per-sprint cloud snapshots (enhancement 5 — pending)

One snapshot per active sprint batch on `game/development` — cheaper than per-agent forks, gives reproducible MCP stack state. **Not automated yet** — rebuild manually at sprint boundaries (`docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md`).

### 10.4 Git LFS (enhancement 4)

| Item | Location |
|------|----------|
| Patterns | `.gitattributes` |
| Install | `bash tools/install_git_lfs.sh` (also in CI + cloud dev) |
| Policy | `docs/ops/ci-cd/GIT_LFS.md` |

### 10.5 Explicit carry-over protocol

When a cycle ends with open issues:

```bash
python3 tools/pm_close_sprint.py --carry-over P1-06
```

Next cycle picks up carry-over before new scope (`AGILE_WITHIN_PHASES.md` §12.1).

---


## 11. Quick commands by lifecycle stage

```bash
# Design (main)
bash tools/run_docs_ci_checks.sh

# Dev session start (game/development)
bash tools/ensure_mcp_stack.sh
bash tools/run_agent_session_gate.sh builder P1-02

# QA verification
bash tools/run_ci_checks.sh

# UAT release candidate
bash tools/run_cd_gates.sh --channel rc
git tag v0.8.0-rc1 && git push origin v0.8.0-rc1

# Preprod / prod
bash tools/run_cd_gates.sh --channel beta   # or --channel prod
```

---


## 12. Cross-refs

| Doc | Topic |
|-----|-------|
| `BRANCHING.md` | Branch contents and merge policy |
| `BRANCHING_DECISION_RECORD.md` | Why not GitLab env branches / forks |
| `ENVIRONMENTS.md` | Per-stage requirements and labels |
| `IMPLEMENTATION_PLAN.md` | Phase 0–8 task tables |
| `AGILE_WITHIN_PHASES.md` | Sprint cadence inside phases |
| `MULTI_AGENT_BRANCH_STRATEGY.md` | Issue branch workflow |
| `MULTI_AGENT_TEAM.md` | Role handoffs |
| `AI_DEV_WORKFLOW.md` | Build + test policy |
| `PROJECT_MANAGEMENT.md` | Issue labels and templates |
| `CI.md` / `CD.md` | Automation detail |
| `GIT_LFS.md` | Large asset tracking (`.gitattributes`) |
