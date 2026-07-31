---
id: pr-session-ship
type: reference
phase: [0, 1]
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 456
summary: "PR, session, ship/CD"
---
# Controls Cheat Sheet — PR, session, ship/CD

**Hub:** [`CONTROLS_CHEATSHEET.md`](../CONTROLS_CHEATSHEET.md)

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
