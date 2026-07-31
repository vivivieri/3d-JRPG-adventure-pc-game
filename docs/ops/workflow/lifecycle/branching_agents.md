---
id: branching-agents
type: explanation
audience: [pm, architect, release]
status: active
authority: workflow
tokens_est: 894
summary: "Branching, agent envs, issue lifecycle"
---
# Development Lifecycle — Branching, agent envs, issue lifecycle

**Hub:** [`DEVELOPMENT_LIFECYCLE.md`](../DEVELOPMENT_LIFECYCLE.md)

## 4. Branching mechanism (summary)

Full policy: `BRANCHING.md` · per-agent rules: `MULTI_AGENT_BRANCH_STRATEGY.md`

```
main                          ← design + game/data only (never ship .gd/.tscn)
  │
game/development              ← implementation trunk (all phases 1–8)
  │
cursor/<issue-id>-<suffix>     ← one issue, one branch, one PR → trunk
```

| Branch type | Lifetime | Who creates | Merges into |
|-------------|----------|-------------|-------------|
| `main` | Permanent | Humans / PM (docs) | — |
| `game/development` | Permanent | Bootstrap once | `main` **once at M6 ship** |
| `cursor/p1-02-a091` | Days (1 issue) | Worker agent | `game/development` |

**Release promotion uses tags on `game/development`, not branch merges:**

```bash
git tag v0.8.0-rc1 && git push origin v0.8.0-rc1    # UAT artifact
git tag v0.9.0-beta1 && git push origin v0.9.0-beta1  # Steam beta
git tag v1.0.0 && git push origin v1.0.0              # Production
```

---


## 5. Agent environments (isolation model)

Agents do **not** each get a permanent fork or environment branch. Isolation is **per session / per issue**.

| Role | Works on | Runtime environment | Isolation mechanism |
|------|----------|---------------------|---------------------|
| **PM** | `main` or `game/development` | Cloud agent (light on `main`) | Orchestrator + sprint board |
| **Architect** | `cursor/*` or trunk | Cloud snapshot on `game/development` | Feature branch + typed GDScript only |
| **Builder** | `cursor/*` | Cloud snapshot + **full MCP stack** | Feature branch; GDAI-only `.tscn` |
| **QA** | Trunk @ PR commit | CI runner or local `run_ci_checks.sh` | Read-only verification |
| **Flow** | Trunk @ milestone | MCP Pro test mode | Scenario scripts only |
| **Release** | Tagged commit | CD workflows | Tag + GitHub Environment approval |
| **Human** | UAT RC zip | Local install | L6 after L0–L5 |

### Cloud Agent branch rule

| Checkout branch | Godot / MCP | Use for |
|-----------------|-------------|---------|
| `main` | **Not booted** | Docs, `game/data/`, validators |
| `game/development` | **Required** | All implementation |

Launch cloud agents from the `game/development` environment snapshot for Builder work (`docs/ops/agents/CLOUD_SNAPSHOT_LAUNCH.md`).

### Session gate (every worker agent)

```bash
bash tools/run_agent_session_gate.sh <role> <issue_id>
```

Enforces: correct role, issue in `next_dispatch`, WIP caps, MCP preflight.

---


## 6. Issue lifecycle (one sprint task)

```mermaid
sequenceDiagram
  participant PM as PM Agent
  participant GH as GitHub Issue
  participant W as Worker Agent
  participant CI as Game CI
  participant Rel as Release

  PM->>PM: run_pm_orchestrator.sh
  PM->>GH: Issue from sprint pack (gate IDs, agent/*)
  PM->>W: pm_dispatch_packet.json + pm_dispatch_workers.py → dispatch/ready label
  W->>W: branch cursor/p1-02-a091
  W->>W: Architect plan OR Builder GDAI build
  W->>CI: PR → game/development
  CI-->>W: L0–L2 (L4/L5 if required)
  opt W->>W: run_candidate_tournament.sh (L2.5 — when M5 tournament policy)
  W->>PM: run_post_agent_cycle.sh --issue … --agent …
  Note over PM,Rel: At milestone
  PM->>Rel: tag v*-rc*
  Rel->>Rel: cd-artifact.yml → UAT zip
```

### Definition of done (issue)

- [ ] Acceptance gate IDs listed and **PASS**
- [ ] Evidence paths in issue or PR
- [ ] PR merged to correct branch (`game/development` for code)
- [ ] `pm_check_done_criteria.py` PASS
- [ ] Linear issue closed (if mirrored)

Templates: `.github/ISSUE_TEMPLATE/` · sprint pack: `docs/ops/sprints/Phase1-Sprint1-issues.md`

---
