---
id: pr-session-ship
type: reference
phase: [0, 1]
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 572
summary: "Controls Cheat Sheet — PR, session, ship/CD — export GH_TOKEN=github_pat_...   # Cursor Secrets"
---
# Controls Cheat Sheet — PR, session, ship/CD

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

## When to read

Use **Controls Cheat Sheet — PR, session, ship/CD** (roles: pm, builder, qa, release) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [PR + GitHub controls](#pr-github-controls)
- [PR templates (`.github/PULL_REQUEST_TEMPLATE/`)](#pr-templates-githubpull_request_template)
- [Branch protection (`tools/setup_github_project.sh`)](#branch-protection-toolssetup_github_projectsh)
- [Issue templates](#issue-templates)
- [Session startup (before scene work)](#session-startup-before-scene-work)
- [Ship / CD controls](#ship-cd-controls)


## PR + GitHub controls

### PR templates (`.github/PULL_REQUEST_TEMPLATE/`)

| Template | Branch | Requires |
|----------|--------|----------|
| **game_development.md** | `game/development` | PM / Architect / Builder / QA checkboxes + gate report |
| **docs_main.md** | `main` | Docs-only checklist + `run_docs_ci_checks.sh` |

### Branch protection (`tools/setup_github_project.sh`)

| Branch | Status check | PR review |
|--------|--------------|-----------|
| `main` | Docs + design data gates | **None** (CI-only) |
| `game/development` | L0–L2 headless gates | **None** (CI-only) |

```bash
export GH_TOKEN=github_pat_...   # Cursor Secrets
bash tools/setup_github_project.sh
```

Manual fallback: `docs/ops/ci-cd/GITHUB_SETUP.md` §2.

### Issue templates

| Template | Enforces |
|----------|----------|
| `feature_task.yml` | Phase, gate IDs, `agent_owner` |
| `gate_failure.yml` | Gate ID, SHA, remediation |
| `bug_report.yml` | Severity, env, repro |

Labels: `agent/*`, `gate/*`, `env/*` — see `docs/ops/agents/PROJECT_MANAGEMENT.md` §2.

---


## Session startup (before scene work)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh       # blocks Builder without P0 MCP
bash tools/check_rr_compliance.sh
```

---


## Ship / CD controls

```bash
bash tools/run_cd_gates.sh --channel rc      # CI + assets
bash tools/run_cd_gates.sh --channel beta    # + L5 E2E required
bash tools/run_cd_gates.sh --channel prod    # + L6 policy
```

Tags on `game/development` only until M6 (`docs/ops/ci-cd/CD.md`).

---
