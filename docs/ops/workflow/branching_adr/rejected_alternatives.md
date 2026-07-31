---
id: rejected-alternatives
type: explanation
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 757
summary: "Rejected alternatives"
---
# Branching Decision Record — Rejected alternatives

**Hub:** [`BRANCHING_DECISION_RECORD.md`](../BRANCHING_DECISION_RECORD.md)

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
